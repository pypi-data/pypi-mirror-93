Changes
=======

All notable changes to this project will be documented in this file.

The format is based on `Keep a
Changelog <https://keepachangelog.com/en/1.0.0/>`__, and this project
adheres to `Semantic
Versioning <https://semver.org/spec/v2.0.0.html>`__.

.. Type of changes
.. ---------------
.. Added      Added for new features.
.. Changed    Changed for changes in existing functionality.
.. Deprecated Deprecated for soon-to-be removed features.
.. Removed    Removed for now removed features.
.. Fixed      Fixed for any bug fixes.
.. Security   Security in case of vulnerabilities.

Unreleased_
-----------

.. towncrier release notes start

.. _Unreleased: https://foss.heptapod.net/fluiddyn/fluidsim/-/compare/0.4.1...branch%2Fdefault

0.4.1_ (2021-02-02)
-------------------

Few bugfixes and `!192
<https://foss.heptapod.net/fluiddyn/fluidsim/-/merge_requests/192>` (temporal
spectra for ns3d solvers).

0.4.0_ (2021-01-11)
-------------------

* `!186 <https://foss.heptapod.net/fluiddyn/fluidsim/-/merge_requests/186>`__: Package split into ``fluidsim-core`` and ``fluidsim``

  - Base classes and abstract base classes defined for ``params``, ``info_solver``, ``sim``, ``output`` instances
  - Entry points as a *plugin framework* to register FluidSim solvers

* ``base/output/print_stdout.py``: better regularity saving + method ``plot_clock_times``

* Able to run bigger simulations (``2034x2034x384``) on the Occigen cluster (in
  particular new function ``fluidsim.modif_resolution_from_dir_memory_efficient``)

0.3.3_ (2020-10-15)
-------------------

- Bugfixes and optimizations (in particular for ns3d solvers)
- Forcing WATU Coriolis and Milestone for ns3d.strat
- pyproject.toml and isolated build
- Timestepping using phase-shifting for dealiasing
- Improve regularity of saving for some outputs

0.3.2_ (2019-11-14)
-------------------

- Bug fixes and Transonic 0.4 compatibility

0.3.1_ (2019-03-07)
-------------------

- Windows compatibility
- Only Python code (stop using Cython)
- Improvements ns2d.strat

0.3.0_ (2019-01-31)
-------------------

- Drop support for Python 2.7!
- Accelerated by Transonic & Pythran (also time stepping)
- Better setup.py (by Ashwin Vishnu)
- Improvement ns2d.strat (by Miguel Calpe Linares)
- Much better testing (internal, CI, compatibility pytest, coverage 87%)
- Fix several bugs :-)
- New function load_for_restart

0.2.2_ (2018-07-01)
-------------------

- Let fluidfft decides which FFT class to use (dependency fluidfft >= 0.2.4)

0.2.1_ (2018-05-24)
-------------------

- IPython magic commands (by Ashwin Vishnu).
- Bugfix divergence-free flow and time_stepping in ns3d solvers.

0.2.0_ (2018-05-04)
-------------------

- Many bugfixes and nicer code (using the Python code formatter Black).
- Faster ns3d solver.
- ns2d.strat + anisotropic forcing (by Miguel Calpe Linares).
- Nicer forcing parameters.

0.1.1
-----

- Better ``phys_fields.plot`` and ``phys_fields.animate`` (by Ashwin Vishnu and
  Miguel Calpe Linares).
- Faster installation (with configuration file).
- Installation without mpi4py.
- Faster time stepping with less memory allocation.
- Much faster ns3d solvers.

0.1.0
-----

- Uses fluidfft and Pythran

0.0.5
-----

- Compatible fluiddyn 0.1.2

0.0.4
-----

- 0D models (predaprey, lorenz)
- Continuous integration, unittests with bitbucket-pipelines

0.0.3a0
-------

Merge with geofluidsim (Ashwin Vishnu Mohanan repository)

- Movies.
- Preprocessing of parameters.
- Less bugs.

0.0.2a1
-------

- Use a cleaner parameter container class (fluiddyn 0.0.8a1).

0.0.2a0
-------

- SetOfVariables inherits from numpy.ndarray.

- The creation of default parameter has been simplified and is done
  by a class function Simul.create_default_params.

0.0.1a
------

- Split the package fluiddyn between one base package and specialized
  packages.

.. _0.4.1: https://foss.heptapod.net/fluiddyn/fluidsim/-/compare/0.4.0...0.4.1
.. _0.4.0: https://foss.heptapod.net/fluiddyn/fluidsim/-/compare/0.3.3...0.4.0
.. _0.3.3: https://foss.heptapod.net/fluiddyn/fluidsim/-/compare/0.3.2...0.3.3
.. _0.3.2: https://foss.heptapod.net/fluiddyn/fluidsim/-/compare/0.3.1...0.3.2
.. _0.3.1: https://foss.heptapod.net/fluiddyn/fluidsim/-/compare/0.3.0...0.3.1
.. _0.3.0: https://foss.heptapod.net/fluiddyn/fluidsim/-/compare/0.2.2...0.3.0
.. _0.2.2: https://foss.heptapod.net/fluiddyn/fluidsim/-/compare/0.2.1...0.2.2
.. _0.2.1: https://foss.heptapod.net/fluiddyn/fluidsim/-/compare/0.2.0...0.2.1
.. _0.2.0: https://foss.heptapod.net/fluiddyn/fluidsim/-/compare/0.1.1...0.2.0
