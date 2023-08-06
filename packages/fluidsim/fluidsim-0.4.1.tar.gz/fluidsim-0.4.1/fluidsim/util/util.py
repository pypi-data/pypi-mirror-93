"""Utilities for the numerical simulations (:mod:`fluidsim.util.util`)
======================================================================

Public API
----------

.. autofunction:: load_sim_for_plot

.. autofunction:: load_state_phys_file

.. autofunction:: load_for_restart

.. autofunction:: modif_resolution_from_dir

.. autofunction:: modif_resolution_from_dir_memory_efficient

Internal API
------------

.. autofunction:: open_patient

"""

import inspect
import os
import time
from copy import deepcopy as _deepcopy
from datetime import timedelta
from functools import partial
from importlib import import_module
from pathlib import Path
from time import perf_counter
from typing import Union

import fluiddyn as fld
import h5netcdf
import h5py
import numpy as _np
from fluiddyn.io.redirect_stdout import stdout_redirected
from fluiddyn.util import mpi
from fluiddyn.util.util import get_memory_usage
from fluidsim_core import loader

from fluidsim import path_dir_results

from fluidsim.base.params import (
    Parameters,
    fix_old_params,
    load_info_solver,
    load_params_simul,
    merge_params,
)
from fluidsim.base.solvers.info_base import create_info_simul

from .output import save_file

available_solvers = partial(
    loader.available_solvers, entrypoint_grp="fluidsim.solvers"
)

import_module_solver_from_key = partial(
    loader.import_module_solver, entrypoint_grp="fluidsim.solvers"
)

import_simul_class_from_key = partial(
    loader.import_cls_simul, entrypoint_grp="fluidsim.solvers"
)


def print_memory_usage_seq(message, flush=None):
    mem = get_memory_usage()
    print(message, f"{mem/1024: 7.3f} Go", flush=flush)


def available_solver_keys():
    """List all available solvers.

    Returns
    -------
    list

    """
    return sorted(available_solvers())


def get_dim_from_solver_key(key):
    """Try to guess the dimension from the solver key (via the operator name)."""
    cls = import_simul_class_from_key(key)
    info = cls.InfoSolver()
    class_name = info.classes.Operators.class_name

    # special cases:
    if class_name == "OperatorsPseudoSpectralSW1L":
        return "2"

    for dim in range(4):
        if str(dim) in class_name:
            return str(dim)

    raise NotImplementedError(
        "Cannot deduce dimension of the solver from the name " + class_name
    )


def pathdir_from_namedir(name_dir: Union[str, Path, None] = None):
    """Return the path of a result directory.

    name_dir: str, optional

      Can be an absolute path, a relative path, or even simply just
      the name of the directory under $FLUIDSIM_PATH.

    """
    if name_dir is None:
        return os.getcwd()

    if not isinstance(name_dir, Path):
        name_dir = Path(name_dir)

    name_dir = name_dir.expanduser()

    if name_dir.is_dir():
        return name_dir.absolute()

    if not name_dir.is_absolute():
        name_dir = path_dir_results / name_dir

    if not name_dir.is_dir():
        raise ValueError(str(name_dir) + " is not a directory")

    return name_dir


class ModulesSolvers(dict):
    """Dictionary to gather imported solvers."""

    def __init__(self, names_solvers):
        for key in names_solvers:
            self[key] = import_module_solver_from_key(key)


def name_file_from_time_approx(path_dir, t_approx=None):
    """Return the file name whose time is the closest to the given time.

    .. todo::

        Can be elegantly implemented using regex as done in
        ``fluidsim.base.output.phys_fields.time_from_path``

    """
    if not isinstance(path_dir, Path):
        path_dir = Path(path_dir)

    path_files = sorted(tuple(path_dir.glob("state_phys_t*")))
    nb_files = len(path_files)
    if nb_files == 0 and mpi.rank == 0:
        raise ValueError("No state file in the dir\n" + str(path_dir))

    name_files = [path.name for path in path_files]
    if "state_phys_t=" in name_files[0]:
        ind_start_time = len("state_phys_t=")
    else:
        ind_start_time = len("state_phys_t")

    times = _np.empty([nb_files])
    for ii, name in enumerate(name_files):
        tmp = ".".join(name[ind_start_time:].split(".")[:2])
        if "_" in tmp:
            tmp = tmp[: tmp.index("_")]
        times[ii] = float(tmp)
    if t_approx is None:
        t_approx = times.max()
    i_file = abs(times - t_approx).argmin()
    name_file = path_files[i_file].name
    return name_file


def load_sim_for_plot(
    name_dir=None, merge_missing_params=False, hide_stdout=False
):
    """Create a object Simul from a dir result.

    Creating simulation objects with this function should be fast because the
    state is not initialized with the output file and only a coarse operator is
    created.

    Parameters
    ----------

    name_dir : str (optional)

      Name of the directory of the simulation. If nothing is given, we load the
      data in the current directory.
      Can be an absolute path, a relative path, or even simply just
      the name of the directory under $FLUIDSIM_PATH.

    merge_missing_params : bool (optional, default == False)

      Can be used to load old simulations carried out with an old fluidsim
      version.

    hide_stdout : bool (optional, default == False)

      If True, without stdout.

    """
    path_dir = pathdir_from_namedir(name_dir)
    solver = _import_solver_from_path(path_dir)
    params = load_params_simul(path_dir)

    if merge_missing_params:
        merge_params(params, solver.Simul.create_default_params())

    params.path_run = path_dir
    params.init_fields.type = "constant"
    params.init_fields.modif_after_init = False
    params.ONLY_COARSE_OPER = True
    params.NEW_DIR_RESULTS = False
    params.output.HAS_TO_SAVE = False
    params.output.ONLINE_PLOT_OK = False

    try:
        params.preprocess.enable = False
    except AttributeError:
        pass

    try:
        params.oper.type_fft = "default"
        params.oper.type_fft2d = "sequential"
    except AttributeError:
        pass

    fix_old_params(params)

    with stdout_redirected(hide_stdout):
        sim = solver.Simul(params)
    return sim


def _import_solver_from_path(path_dir):
    info_solver = load_info_solver(path_dir)
    solver = import_module(info_solver.module_name)
    return solver


def load_state_phys_file(
    name_dir=None,
    t_approx=None,
    modif_save_params=True,
    merge_missing_params=False,
    init_with_initialized_state=True,
    hide_stdout=False,
):
    """Create a simulation from a file.

    For large resolution, creating a simulation object with this function can
    be slow because the state is initialized with the output file.

    Parameters
    ----------

    name_dir : str (optional)

      Name of the directory of the simulation. If nothing is given, we load the
      data in the current directory.
      Can be an absolute path, a relative path, or even simply just
      the name of the directory under $FLUIDSIM_PATH.

    t_approx : number (optional)

      Approximate time of the file to be loaded.

    modif_save_params :  bool (optional, default == True)

      If True, the parameters of the simulation are modified before loading::

        params.output.HAS_TO_SAVE = False
        params.output.ONLINE_PLOT_OK = False

    merge_missing_params : bool (optional, default == False)

      Can be used to load old simulations carried out with an old fluidsim
      version.

    init_with_initialized_state : bool (optional, default == True)

      If True, call sim.output.init_with_initialized_state.

    hide_stdout : bool (optional, default == False)

      If True, without stdout.

    """

    params, Simul = load_for_restart(name_dir, t_approx, merge_missing_params)

    if modif_save_params:
        params.output.HAS_TO_SAVE = False
        params.output.ONLINE_PLOT_OK = False

    params.ONLY_COARSE_OPER = False
    try:
        params.oper.type_fft = "default"
        params.oper.type_fft2d = "sequential"
    except AttributeError:
        pass

    with stdout_redirected(hide_stdout):
        sim = Simul(params)

    if init_with_initialized_state:
        sim.output.init_with_initialized_state()

    return sim


def load_for_restart(name_dir=None, t_approx=None, merge_missing_params=False):
    """Load params and Simul for a restart.

    >>> params, Simul = load_for_restart(name_dir)

    Parameters
    ----------

    name_dir : str (optional)

      Name of the directory of the simulation. If nothing is given, we load the
      data in the current directory.
      Can be an absolute path, a relative path, or even simply just
      the name of the directory under $FLUIDSIM_PATH.

    t_approx : number (optional)

      Approximate time of the file to be loaded.

    merge_missing_params : bool (optional, default == False)

      Can be used to load old simulations carried out with an old fluidsim
      version.

    """

    path_dir = pathdir_from_namedir(name_dir)
    solver = _import_solver_from_path(path_dir)

    # choose the file with the time closer to t_approx
    name_file = name_file_from_time_approx(path_dir, t_approx)
    path_file = os.path.join(path_dir, name_file)

    if merge_missing_params:
        # this has to be done by all processes otherwise there is a problem
        # with Transonic (see https://foss.heptapod.net/fluiddyn/fluidsim/issues/26)
        default_params = solver.Simul.create_default_params()

    if mpi.rank > 0:
        params = None
    else:
        with h5py.File(path_file, "r") as file:
            params = Parameters(hdf5_object=file["info_simul"]["params"])

        if merge_missing_params:
            merge_params(params, default_params)

        params.path_run = path_dir
        params.NEW_DIR_RESULTS = False
        params.init_fields.type = "from_file"
        params.init_fields.from_file.path = path_file
        params.init_fields.modif_after_init = False
        try:
            params.preprocess.enable = False
        except AttributeError:
            pass

        fix_old_params(params)

    if mpi.nb_proc > 1:
        params = mpi.comm.bcast(params, root=0)

    return params, solver.Simul


def modif_resolution_all_dir(t_approx=None, coef_modif_resol=2, dir_base=None):
    """Save files with a modified resolution."""
    raise DeprecationWarning("Sorry, use modif_resolution_from_dir instead")


def modif_resolution_from_dir(
    name_dir=None, t_approx=None, coef_modif_resol=2, PLOT=True
):
    """Save a file with a modified resolution."""

    path_dir = pathdir_from_namedir(name_dir)

    solver = _import_solver_from_path(path_dir)

    sim = load_state_phys_file(name_dir, t_approx)

    params2 = _deepcopy(sim.params)
    params2.output.HAS_TO_SAVE = True
    params2.oper.nx = int(sim.params.oper.nx * coef_modif_resol)
    params2.oper.ny = int(sim.params.oper.ny * coef_modif_resol)

    try:
        params2.oper.nz = int(sim.params.oper.nz * coef_modif_resol)
    except AttributeError:
        dimension = 2
    else:
        dimension = 3

    params2.init_fields.type = "from_simul"

    sim2 = solver.Simul(params2)
    sim2.init_fields.get_state_from_simul(sim)

    print(sim2.params.path_run)

    oper_new = sim2.params.oper
    if dimension == 3:
        dir_new_file = f"/State_phys_{oper_new.nx}x{oper_new.ny}x{oper_new.nz}"
    else:
        dir_new_file = f"/State_phys_{oper_new.nx}x{oper_new.ny}"

    sim2.output.path_run = str(path_dir) + dir_new_file
    print("Save file in directory\n" + sim2.output.path_run)
    sim2.output.phys_fields.save(particular_attr="modif_resolution")

    print("The new file is saved.")

    if PLOT:
        sim.output.phys_fields.plot(numfig=0)
        sim2.output.phys_fields.plot(numfig=1)
        fld.show()


class StatePhysLike:
    def __init__(self, path_file, oper, oper2):
        self.path_file = path_file
        self.oper = oper
        self.oper2 = oper2
        self.info = "state_phys"

        self.field = oper.create_arrayX()
        self.field_spect = oper.create_arrayK()
        print_memory_usage_seq("Memory usage after init fields:           ")

        self.field2 = oper2.create_arrayX()
        print(
            "size field2:                               "
            f"{self.field2.nbytes / 1024**3:7.3f} Go"
        )
        print_memory_usage_seq("Memory usage after init field2:           ")
        self.field2_spect = oper2.create_arrayK(0)
        print(
            "size field2_spect:                         "
            f"{self.field2_spect.nbytes / 1024**3:7.3f} Go"
        )
        print_memory_usage_seq("Memory usage after init field2_spect:     ")

        if path_file.suffix == ".nc":
            self.h5pack = h5netcdf
        else:
            self.h5pack = h5py

        with self.h5pack.File(self.path_file, "r") as h5file:
            group_state_phys = h5file["/state_phys"]
            self.keys = list(group_state_phys.keys())
            self.time = float(group_state_phys.attrs["time"])
            self.it = int(group_state_phys.attrs["it"])
            self.name_run = h5file.attrs["name_run"]

    def get_var(self, key):
        print(f'get_var("{key}")')

        def start_counter(message):
            print(f"- {message + '...':30s}", end="", flush=True)
            return perf_counter()

        def end_counter(t_start):
            print(f"done in {timedelta(seconds=perf_counter() - t_start)}")

        t_start = start_counter("reading field from disk")
        with self.h5pack.File(self.path_file, "r") as h5file:
            group_state_phys = h5file["/state_phys"]
            self.field[:] = group_state_phys[key][...]
        end_counter(t_start)

        t_start = start_counter("forward fft smaller field")
        self.oper.fft_as_arg(self.field, self.field_spect)
        end_counter(t_start)

        dimension = len(self.field_spect.shape)
        if dimension not in [2, 3]:
            raise NotImplementedError

        t_start = start_counter("filling field2_fft")
        self.oper2.fill_field_fft(self.field_spect, self.field2_spect, self.oper)
        end_counter(t_start)

        t_start = start_counter("backward fft field2")
        self.oper2.ifft_as_arg(self.field2_spect, self.field2)
        end_counter(t_start)

        return self.field2


def modif_resolution_from_dir_memory_efficient(
    name_dir=None, t_approx=None, coef_modif_resol=2
):
    """Save a file with a modified resolution.

    Faster and more memory efficient than ``modif_resolution_from_dir`` (but
    not plot).

    """
    t_start = perf_counter()

    if mpi.nb_proc > 1:
        raise NotImplementedError

    path_dir = pathdir_from_namedir(name_dir)
    solver = _import_solver_from_path(path_dir)

    name_file = name_file_from_time_approx(path_dir, t_approx)
    path_file = path_dir / name_file
    print(f"Changing resolution of the state contained in\n{path_file}")

    Simul = solver.Simul
    try:
        info_solver = Simul.info_solver
    except AttributeError:
        info_solver = Simul.InfoSolver()
        info_solver.complete_with_classes()

    with h5py.File(path_file, "r") as h5file:
        params = Parameters(hdf5_object=h5file["/info_simul/params"])

    try:
        params.oper.type_fft = "default"
        params.oper.type_fft2d = "sequential"
    except AttributeError:
        pass

    params2 = _deepcopy(params)
    params2.output.HAS_TO_SAVE = True
    nx2 = params2.oper.nx = int(params.oper.nx * coef_modif_resol)
    ny2 = params2.oper.ny = int(params.oper.ny * coef_modif_resol)

    try:
        nz2 = params2.oper.nz = int(params.oper.nz * coef_modif_resol)
    except AttributeError:
        dimension = 2
        shape = (params.oper.ny, params.oper.nx)
        shape2 = (ny2, nx2)
    else:
        dimension = 3
        shape = (params.oper.nz, params.oper.ny, params.oper.nx)
        shape2 = (nz2, ny2, nx2)

    from .mini_oper_modif_resol import MiniOperModifResol

    oper = MiniOperModifResol(shape)
    print_memory_usage_seq(
        'Memory usage after init operator "input": ', flush=True
    )
    oper2 = MiniOperModifResol(shape2)

    print_memory_usage_seq('Memory usage after init operator "output":')
    info2 = create_info_simul(info_solver, params2)

    state_phys = StatePhysLike(path_file, oper, oper2)

    if dimension == 3:
        dir_new_new = f"State_phys_{nx2}x{ny2}x{nz2}"
    else:
        dir_new_new = f"State_phys_{nx2}x{ny2}"

    path_file_out = path_file.parent / dir_new_new / path_file.name
    path_file_out.parent.mkdir(exist_ok=True)
    print(f"Saving file {path_file_out.name}...", flush=True)
    save_file(
        path_file_out,
        state_phys,
        info2,
        state_phys.name_run,
        oper2,
        state_phys.time,
        state_phys.it,
        particular_attr="modif_resolution",
    )
    print(
        f"File {path_file_out.name} saved in:\n{path_file_out.parent}\n"
        f"total duration: {timedelta(seconds=perf_counter() - t_start)}"
    )


def times_start_end_from_path(path):
    """Return the start and end times from a result directory path."""

    path_file = path + "/stdout.txt"
    if not os.path.exists(path_file):
        print("Given path does not exist:\n " + path)
        return 666, 666

    with open(path_file, "r") as file_stdout:

        line = ""
        while not line.startswith("it ="):
            line = file_stdout.readline()

        words = line.split()
        t_s = float(words[6])

        # in order to get the information at the end of the file,
        # we do not want to read the full file...
        file_stdout.seek(0, os.SEEK_END)  # go to the end
        nb_caract = file_stdout.tell()
        nb_caract_to_read = min(nb_caract, 1000)
        file_stdout.seek(file_stdout.tell() - nb_caract_to_read, os.SEEK_SET)
        while line != "":
            if line.startswith("it ="):
                line_it = line
            last_line = line
            line = file_stdout.readline()

        if last_line.startswith("save state_phys"):
            name_file = last_line.split()[-1]
            name_file, ext = os.path.splitext(name_file)
            word = name_file.split("_it=")[0].split("state_phys_t")[-1]
            t_e = float(word.replace(ext, ""))
        else:
            words = line_it.split()
            t_e = float(words[6])

    # print('t_s = {0:.3f}, t_e = {1:.3f}'.format(t_s, t_e))

    return t_s, t_e


def open_patient(
    path,
    *args,
    time_wait_total=200,
    time_wait_once=2,
    class_file=h5py.File,
    **kwargs,
):
    """Open a hdf5 type file in a "patient" way.

    If the file is already opened by another process (``errno==11`` for hdf5),
    the error is caught and we retry later.

    Parameters
    ----------

    time_wait_total : number (optional)

      Time to wait before raising the error.

    time_wait_once : number (optional)

      Time between attempts.

    class_file : type (optional)

      Class of the file (default ``h5py.File``, but could be ``h5netcdf.File``).

    """
    time_first_try = time.time()
    while True:
        try:
            file = class_file(path, *args, **kwargs)
            break
        except OSError as error:
            errno = int(repr(error).split("errno = ")[1].split(",")[0])
            if errno != 11 or time.time() - time_first_try > time_wait_total:
                raise
            time.sleep(time_wait_once)
    return file
