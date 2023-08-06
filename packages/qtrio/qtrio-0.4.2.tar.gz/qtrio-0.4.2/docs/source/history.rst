Release history
===============

.. currentmodule:: qtrio

.. towncrier release notes start

Qtrio 0.4.2 (2021-02-04)
------------------------

No significant changes.  Released for documentation improvements.


Qtrio 0.4.1 (2021-01-06)
------------------------

Features
~~~~~~~~

- Constrained all dependencies for better long term compatibility and reduced pip resolution time. (`#211 <https://github.com/altendky/qtrio/issues/211>`__)


Qtrio 0.4.0 (2021-01-04)
------------------------

Features
~~~~~~~~

- Extract a subset of :func:`qtrio.dialogs.check_dialog_protocol` into a parent protocol
  :func:`qtrio.dialogs.check_basic_dialog_protocol` which can be used to describe a dialog
  without ``.shown`` or ``.wait()``. (`#197 <https://github.com/altendky/qtrio/issues/197>`__)
- Added file dialog creation helper :func:`qtrio.dialogs.create_file_open_dialog`. (`#198 <https://github.com/altendky/qtrio/issues/198>`__)
- Added :class:`qtrio.dialogs.ProgressDialog` and creation helper
  :func:`qtrio.dialogs.create_progress_dialog`. (`#199 <https://github.com/altendky/qtrio/issues/199>`__)
- Added :meth:`qtrio.dialogs.FileDialog.set_path`. (`#200 <https://github.com/altendky/qtrio/issues/200>`__)


Bugfixes
~~~~~~~~

- Include the missing ``py.typed`` file that is used to state there are type hints to process. (`#206 <https://github.com/altendky/qtrio/issues/206>`__)


Improved documentation
~~~~~~~~~~~~~~~~~~~~~~

- Added :ref:`download example <download_example>`. (`#23 <https://github.com/altendky/qtrio/issues/23>`__)


Qtrio 0.3.0 (2020-10-16)
------------------------

Headline features
~~~~~~~~~~~~~~~~~

- Integrate with pytest-trio for :ref:`testing <testing>`. (`#9 <https://github.com/altendky/qtrio/issues/9>`__)
- Python 3.9 supported. (`#113 <https://github.com/altendky/qtrio/issues/113>`__)


Breaking changes
~~~~~~~~~~~~~~~~

- Removed ``qtrio.host()`` in favor of pytest-trio for :ref:`testing <testing>`. (`#9 <https://github.com/altendky/qtrio/issues/9>`__)
- :func:`qtrio.run` returns the passed async function's result instead of a combined Trio and Qt outcome. (`#9 <https://github.com/altendky/qtrio/issues/9>`__)


QTrio 0.2.0 (2020-09-19)
------------------------

Headline features
~~~~~~~~~~~~~~~~~

- Introduce QTrio specific wrappers for some builtin :ref:`dialogs <dialogs>`. (`#2 <https://github.com/altendky/qtrio/issues/2>`__)
- Added :func:`qtrio.open_emissions_nursery()` for connecting signals to both async and sync slots. (`#57 <https://github.com/altendky/qtrio/issues/57>`__)


Features
~~~~~~~~

- Provide more control over the reentry event type via :func:`qtrio.register_event_type`,
  :func:`qtrio.register_requested_event_type`, and :func:`qtrio.registered_event_type`. (`#16 <https://github.com/altendky/qtrio/issues/16>`__)
- Enable running the CLI via ``python -m qtrio``. (`#99 <https://github.com/altendky/qtrio/issues/99>`__)
- Accept a ``clock`` parameter.  Supported by :func:`qtrio.run` and :class:`qtrio.Runner`. (`#121 <https://github.com/altendky/qtrio/issues/121>`__)
- Run and test timeouts report a :class:`trio.MultiError` to make context of the active tasks at the time of cancellation available. (`#135 <https://github.com/altendky/qtrio/issues/135>`__)


Bugfixes
~~~~~~~~

- Remove noisy output from :meth:`qtrio.Runner.trio_done`. (`#11 <https://github.com/altendky/qtrio/issues/11>`__)


Improved documentation
~~~~~~~~~~~~~~~~~~~~~~

- Badges now in new resources section of readme and main doc page. (`#103 <https://github.com/altendky/qtrio/issues/103>`__)
- Classifiers for 3.6, 3.7, and 3.8 are included. (`#104 <https://github.com/altendky/qtrio/issues/104>`__)
- Link to issues included in resources section. (`#106 <https://github.com/altendky/qtrio/issues/106>`__)
- List all resource URLs in PyPI project URLs. (`#107 <https://github.com/altendky/qtrio/issues/107>`__)
- Use ``stable`` for :mod:`outcome` intersphinx links. (`#109 <https://github.com/altendky/qtrio/issues/109>`__)
- Add section about :ref:`installation`, mostly to describe extras. (`#155 <https://github.com/altendky/qtrio/issues/155>`__)
- Show ``[sources]`` links in documentation linked to included code. (`#168 <https://github.com/altendky/qtrio/issues/168>`__)
- Update the :ref:`layer 2 example <getting_started_layer_2>` to use ``async for _ in emissions.channel:``. (`#173 <https://github.com/altendky/qtrio/issues/173>`__)


For contributors
~~~~~~~~~~~~~~~~

- Shift to a single ``qtrio._tests`` package rather than distributing with one ``_tests`` per code package. (`#139 <https://github.com/altendky/qtrio/issues/139>`__)
- pytest type hints are no longer ignored.  Version 6 or later required. (`#153 <https://github.com/altendky/qtrio/issues/153>`__)
- ``black`` config updated, use ``black .`` to format. (`#174 <https://github.com/altendky/qtrio/issues/174>`__)


QTrio 0.1.0 (2020-07-10)
------------------------

- Initial release
