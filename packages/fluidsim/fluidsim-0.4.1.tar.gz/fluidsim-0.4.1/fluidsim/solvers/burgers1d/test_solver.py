import unittest

from .solver import Simul

from fluiddyn.util import mpi

from fluidsim.util.testing import TestSimul, skip_if_no_fluidfft


@skip_if_no_fluidfft
class TestSolverSquare1D(TestSimul):
    Simul = Simul

    @classmethod
    def init_params(cls):

        params = cls.params = cls.Simul.create_default_params()

        params.short_name_type_run = "test"
        params.output.sub_directory = "unittests"

        params.oper.nx = 40
        params.oper.Lx = 1.0

        params.time_stepping.type_time_scheme = "RK2"

        params.nu_2 = 0.01

        params.time_stepping.t_end = 0.4
        params.time_stepping.USE_CFL = False

        params.init_fields.type = "gaussian"

        params.output.periods_print.print_stdout = 0.25
        params.output.periods_save.phys_fields = 0.5
        params.output.periods_plot.phys_fields = 0.0
        params.output.phys_fields.field_to_plot = "u"

    @unittest.skipIf(
        mpi.nb_proc > 1, "MPI not implemented, for eg. sim.oper.gather_Xspace"
    )
    def test_simul(self):
        sim = self.sim
        sim.time_stepping.start()
