chcss
-----

A CSS naming hierarchy enforcer.

.. image:: https://badge.fury.io/py/chcss.svg
   :target: https://badge.fury.io/py/chcss
   :alt: PyPI Version
.. image:: https://readthedocs.org/projects/chcss/badge/?version=latest
   :target: https://chcss.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

What is chcss?
~~~~~~~~~~~~~~

``chcss`` is a PyParsing based grammar for parsing and verifying that
CSS class names are used in the correct hierarchy in HTML files.
``chcss`` parses HTML files into a DOM model, and then walks the tree
checking class identifiers to ensure they are arranged hierarchically.

The basic grammar is::

  namespace-function((-component)+(-element(-modifier)*)?)?

So long as identifiers are correctly nested, the program returns with
exit status 0.  If errors are detected, the program returns with exit
status 1 and a hopefully helpful error message as to which identifier
on which element caused the first violation, with the goal being easy
integration into a git ``commit-msg`` hook or ``pre-commit``.

Roadmap
~~~~~~~

* Implement testing, build, documentation, and CI.
* Implement ``class`` identifier parser.
* Implement parser field definitions in configuration file.
* Implement ignorable ``class`` identifiers in configuration file
  (i.e. Bootstrap).
* Implement HTML DOM parser (from library).
* Produce ``class`` identifiers from HTML DOM.
* Verify ``class`` identifier hierarchy.
* Use information from HTML DOM and ``class`` identifier parser to raise
  exceptions and provide useful error messages.
* Implement hierarchical ``id`` identifier parsing (maybe; target: post 1.0.0).

Installation
~~~~~~~~~~~~

Install chcss with::

  pip install chcss
  pip freeze > requirements.txt

or add as a poetry dev-dependency.

If you desire a package locally built with poetry, download the
source, change the appropriate lines in ``pyproject.toml``, and
rebuild.

To use as a git ``commit-msg`` hook, copy the script ``chcss`` to
``.git/hooks/commit-msg`` and set the file as executable or integrate
the script or module into your existing ``commit-msg`` hook.  Running
``chcss`` as a hook relies on ``git`` setting the current working
directory of the script to the root of the repository (where
``pyproject.toml`` or ``package.json`` typically lives).  If this is
not the repository default, pass the configuration file path as an
argument or symlink from the current working directory to an
appropriate configuration file.  Optimally, run ``chcss`` from
``pre-commit`` to check HTML files as necessary.

Usage
~~~~~

Console::

  chcss file.html
  cat file.html | chcss

In Python::

  >>> import chcss

See the source and `documentation
<https://chcss.readthedocs.io/en/latest/>`_ for more information.

Configuration
~~~~~~~~~~~~~

See ``chcss.toml`` for an example ``[tool.chcss]`` section that may be
copied into a ``pyproject.toml`` file.  The same entries may be used
in a ``chcss`` entry in ``package.json`` for JavaScript/TypeScript
projects.

Parsing Grammar
~~~~~~~~~~~~~~~

Basic Specification::

  namespace-function((-component)+(-element(-modifier)*)?)?

Copyright and License
~~~~~~~~~~~~~~~~~~~~~

SPDX-License-Identifier: `GPL-3.0-or-later
<https://spdx.org/licenses/GPL-3.0-or-later.html>`_

chcss, a CSS naming hierarchy enforcer.
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
