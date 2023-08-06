v4.0.0
======

Moved ``dependency_context`` and ``run`` to
`jaraco.apt <https://pypi.org/project/jaraco.apt>`_.

v3.0.0
======

Refreshed package metadata.
Require Python 3.6 or later.

2.0
===

Switch to `pkgutil namespace technique
<https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages>`_
for the ``jaraco`` namespace.

1.8
===

* Dropped support for Python 3.3.
* Refreshed project metadata using declarative config.
* ``ExceptionTrap`` now presents ``type``, ``value``,
  and ``tb`` attributes.

1.7
===

* Added ``suppress`` context manager as `found in Python
  3.4
  <https://docs.python.org/3/library/contextlib.html#contextlib.suppress>`_
  but with decorator support.

1.6
===

* Refresh project skeleton. Moved hosting to Github.

1.5
===

* Also allow the ``dest_ctx`` to be overridden in ``repo_context``.

1.4
===

* Added ``remover`` parameter to ``context.temp_dir``.

1.2
===

* Adopted functionality from jaraco.util.context (10.8).
