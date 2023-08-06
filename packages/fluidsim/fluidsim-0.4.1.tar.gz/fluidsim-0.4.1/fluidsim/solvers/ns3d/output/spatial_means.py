"""Spatial means output (:mod:`fluidsim.solvers.ns3d.output.spatial_means`)
===========================================================================

.. autoclass:: SpatialMeansNS3D
   :members:
   :private-members:

"""

import os
import numpy as np

from fluiddyn.util import mpi

from fluidsim.base.output.spatial_means import SpatialMeansBase


class SpatialMeansNS3D(SpatialMeansBase):
    """Spatial means output."""

    def _save_one_time(self):
        tsim = self.sim.time_stepping.t
        self.t_last_save = tsim
        nrj_vx_fft, nrj_vy_fft, nrj_vz_fft = self.output.compute_energies_fft()
        energy_fft = nrj_vx_fft + nrj_vy_fft + nrj_vz_fft
        nrj_vx = self.sum_wavenumbers(nrj_vx_fft)
        nrj_vy = self.sum_wavenumbers(nrj_vy_fft)
        nrj_vz = self.sum_wavenumbers(nrj_vz_fft)
        energy = nrj_vx + nrj_vy + nrj_vz

        f_d, f_d_hypo = self.sim.compute_freq_diss()
        epsK = self.sum_wavenumbers(f_d * 2 * energy_fft)
        epsK_hypo = self.sum_wavenumbers(f_d_hypo * 2 * energy_fft)

        if self.sim.params.nu_4 > 0.0:
            f_d4 = self.params.nu_4 * self.oper.K4
            epsK4 = self.sum_wavenumbers(f_d4 * 2 * energy_fft)
            del f_d4

        if self.sim.params.nu_8 > 0.0:
            f_d8 = self.params.nu_8 * self.oper.K8
            epsK8 = self.sum_wavenumbers(f_d8 * 2 * energy_fft)
            del f_d8

        if self.sim.params.forcing.enable:
            deltat = self.sim.time_stepping.deltat
            forcing_fft = self.sim.forcing.get_forcing()

            fx_fft = forcing_fft.get_var("vx_fft")
            fy_fft = forcing_fft.get_var("vy_fft")
            fz_fft = forcing_fft.get_var("vz_fft")

            vx_fft = self.sim.state.state_spect.get_var("vx_fft")
            vy_fft = self.sim.state.state_spect.get_var("vy_fft")
            vz_fft = self.sim.state.state_spect.get_var("vz_fft")

            PK1_fft = np.ascontiguousarray(
                np.real(
                    vx_fft.conj() * fx_fft
                    + vy_fft.conj() * fy_fft
                    + vz_fft.conj() * fz_fft
                )
            )
            PK2_fft = (
                (abs(fx_fft) ** 2 + abs(fy_fft) ** 2 + abs(fz_fft) ** 2)
                * deltat
                / 2
            )

            PK1 = self.sum_wavenumbers(PK1_fft)
            PK2 = self.sum_wavenumbers(PK2_fft)

        if mpi.rank == 0:

            self.file.write(
                f"####\ntime = {tsim:11.5e}\n"
                f"E    = {energy:11.5e}\n"
                f"Ex   = {nrj_vx:11.5e} ; Ey   = {nrj_vy:11.5e} ; Ez   = {nrj_vz:11.5e}\n"
                f"epsK = {epsK:11.5e} ; epsK_hypo = {epsK_hypo:11.5e} ; "
                f"epsK_tot = {epsK + epsK_hypo:11.5e} \n"
            )

            if self.sim.params.nu_4 > 0.0:
                self.file.write(f"epsK4 = {epsK4:11.5e}\n")

            if self.sim.params.nu_8 > 0.0:
                self.file.write(f"epsK8 = {epsK8:11.5e}\n")

            if self.sim.params.forcing.enable:
                self.file.write(
                    f"PK1  = {PK1:11.5e} ; PK2       = {PK2:11.5e} ; "
                    f"PK_tot   = {PK1 + PK2:11.5e} \n"
                )

            self.file.flush()
            os.fsync(self.file.fileno())

        if self.has_to_plot and mpi.rank == 0:

            self.axe_a.plot(tsim, energy, "k.")

            # self.axe_b.plot(tsim, epsK_tot, 'k.')
            # if self.sim.params.forcing.enable:
            #     self.axe_b.plot(tsim, PK_tot, 'm.')

            if tsim - self.t_last_show >= self.period_show:
                self.t_last_show = tsim
                fig = self.axe_a.get_figure()
                fig.canvas.draw()

    def load(self):
        dict_results = {"name_solver": self.output.name_solver}

        with open(self.path_file) as file_means:
            lines = file_means.readlines()

        lines_t = []
        lines_E = []
        lines_Ex = []
        lines_PK = []
        lines_epsK = []
        lines_epsK4 = []
        lines_epsK8 = []

        for il, line in enumerate(lines):
            if line.startswith("time ="):
                lines_t.append(line)
            if line.startswith("E    ="):
                lines_E.append(line)
            if line.startswith("Ex   ="):
                lines_Ex.append(line)
            if line.startswith("PK1  ="):
                lines_PK.append(line)
            if line.startswith("epsK ="):
                lines_epsK.append(line)
            elif line.startswith("epsK4 ="):
                lines_epsK4.append(line)
            elif line.startswith("epsK8 ="):
                lines_epsK8.append(line)

        nt = len(lines_t)
        if nt > 1:
            nt -= 1

        t = np.empty(nt)
        E = np.empty(nt)
        Ex = np.empty(nt)
        Ey = np.empty(nt)
        Ez = np.empty(nt)
        PK1 = np.zeros(nt)
        PK2 = np.zeros(nt)
        PK_tot = np.zeros(nt)
        epsK = np.empty(nt)
        epsK_hypo = np.zeros(nt)
        epsK_tot = np.zeros(nt)

        if lines_epsK4:
            epsK4 = np.empty(nt)

        if lines_epsK8:
            epsK8 = np.empty(nt)

        for il in range(nt):
            line = lines_t[il]
            words = line.split()
            t[il] = float(words[2])

            line = lines_E[il]
            words = line.split()
            E[il] = float(words[2])

            line = lines_Ex[il]
            words = line.split()
            Ex[il] = float(words[2])
            Ey[il] = float(words[6])
            Ez[il] = float(words[10])

            if self.sim.params.forcing.enable:
                line = lines_PK[il]
                words = line.split()
                PK1[il] = float(words[2])
                PK2[il] = float(words[6])
                PK_tot[il] = float(words[10])

            line = lines_epsK[il]
            words = line.split()
            epsK[il] = float(words[2])
            epsK_hypo[il] = float(words[6])
            epsK_tot[il] = float(words[10])

            if lines_epsK4:
                line = lines_epsK4[il]
                words = line.split()
                epsK4[il] = float(words[2])

            if lines_epsK8:
                line = lines_epsK8[il]
                words = line.split()
                epsK8[il] = float(words[2])

        dict_results["t"] = t
        dict_results["E"] = E
        dict_results["Ex"] = Ex
        dict_results["Ey"] = Ey
        dict_results["Ez"] = Ez

        dict_results["PK1"] = PK1
        dict_results["PK2"] = PK2
        dict_results["PK_tot"] = PK_tot

        dict_results["epsK"] = epsK
        dict_results["epsK_hypo"] = epsK_hypo
        dict_results["epsK_tot"] = epsK_tot

        if lines_epsK4:
            dict_results["epsK4"] = epsK4

        if lines_epsK8:
            dict_results["epsK8"] = epsK8

        return dict_results

    def plot(self, plot_injection=True, plot_hyper=False):
        dict_results = self.load()

        t = dict_results["t"]
        E = dict_results["E"]
        Ex = dict_results["Ex"]
        Ey = dict_results["Ey"]
        Ez = dict_results["Ez"]

        epsK = dict_results["epsK"]
        epsK_hypo = dict_results["epsK_hypo"]
        epsK_tot = dict_results["epsK_tot"]

        fig, ax = self.output.figure_axe()
        ax.set_title("Energy and enstrophy\n" + self.output.summary_simul)
        ax.set_ylabel("$E(t)$")
        ax.set_xlabel("$t$")
        ax.plot(t, E, "k", linewidth=2)
        ax.plot(t, Ex, "b")
        ax.plot(t, Ey, "r")
        ax.plot(t, Ez, "c")

        fig, ax = self.output.figure_axe()
        ax.set_title(
            "Dissipation of energy and enstrophy\n" + self.output.summary_simul
        )
        ax.set_ylabel(r"$\epsilon_K(t)$")
        ax.set_xlabel("$t$")

        def _plot(x, y, fmt, label=None, linewidth=1, zorder=10):
            ax.plot(
                x,
                y,
                fmt,
                label=label,
                linewidth=linewidth,
                zorder=zorder,
            )

        _plot(t, epsK, "r", r"$\epsilon$", linewidth=2)
        if self.sim.params.nu_m4 != 0:
            _plot(t, epsK_hypo, "g", r"$\epsilon_{-4}$", linewidth=2)
            _plot(t, epsK_tot, "k", r"$\epsilon_{tot}$", linewidth=2)

        if "epsK4" in dict_results and plot_hyper:
            epsK4 = dict_results["epsK4"]
            if not np.allclose(epsK, epsK4):
                _plot(
                    t,
                    epsK4,
                    "r:",
                    r"$\epsilon_4$",
                )

        if "epsK8" in dict_results and plot_hyper:
            epsK8 = dict_results["epsK8"]
            if not np.allclose(epsK, epsK8):
                _plot(
                    t,
                    epsK8,
                    "r:",
                    r"$\epsilon_8$",
                )

        if "PK_tot" in dict_results and plot_injection:
            PK_tot = dict_results["PK_tot"]
            ax.plot(t, PK_tot, "r--", label=r"$P$", zorder=0)

        ax.legend()
