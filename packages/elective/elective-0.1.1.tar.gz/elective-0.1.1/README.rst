elective
--------

A CSS naming hierarchy enforcer.

.. image:: https://badge.fury.io/py/elective.svg
   :target: https://badge.fury.io/py/elective
   :alt: PyPI Version
.. image:: https://readthedocs.org/projects/elective/badge/?version=latest
   :target: https://elective.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

What is elective?
~~~~~~~~~~~~~~~~~

``elective`` is a Python program configuration option loader, capable
of loading options from configuration files (TOML, JSON, YAML), the
environment, or the command line, all with the same names and formats.
There are many other fine options available, but none offered this
combination of formats, configurable precedence, clear code and
documentation, or adequate testing.  Most also still use the ini
format, which ``elective`` will not.

Roadmap
~~~~~~~

* Implement basic TOML configuration loading from ``pyproject.toml`` (bring in from ``pccc``, target:  0.2.0).
* Consolidate TOML, JSON, and YAML loading (target:  0.2.0).
* Add ``argparser`` (target:  0.4.0).
* Implement and add environment variable processing (target:  0.5.0).
* Implement and add ``*.env`` file processing (target:  0.6.0).
* Implement testing, build, documentation, and CI (complete:  0.1.0).

Installation
~~~~~~~~~~~~

Install elective with::

  pip install elective
  pip freeze > requirements.txt

or with poetry::

  poetry add elective

Usage
~~~~~

In code::

  >>> import elective
  >>> conf = elective.Config()

See the source and `documentation
<https://elective.readthedocs.io/en/latest/>`_ for more information.

Copyright and License
~~~~~~~~~~~~~~~~~~~~~

SPDX-License-Identifier: `GPL-3.0-or-later
<https://spdx.org/licenses/GPL-3.0-or-later.html>`_

elective, a CSS naming hierarchy enforcer.
Copyright (C) 2021 `Jeremy A Gray <jeremy.a.gray@gmail.com>`_.

This program is free software: you can redistribute it and/or modify
it under the terms of the `GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.html>`_ as published by the Free
Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the `GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.html>`_ along with this program.
If not, see https://www.gnu.org/licenses/.

Author
~~~~~~

`Jeremy A Gray <jeremy.a.gray@gmail.com>`_
