========================
Shpaml-Jinja Integration
========================

Overview
========

Aml ("A markup language") is a pre/post-processor for shpaml.
It extends shpaml syntax with shortcuts useful when shpaml output is
a template engine.

Currently supported template engines are Jinja and ERb.

Aml provides three main feature points:

Indentation check
-----------------

Indentation is significant in shpaml but
shpaml itself will happily convert a file mixing tabs and spaces.
The result is usually not what template designer intended, so
aml requires that only spaces are used for indentation.

Template engine shortcuts
-------------------------

Shpaml automatically closes HTML tags but
template tags it just passes straight through. As a result
both opening and closing template tags are required, which is
clearly an inconvenience.

Aml applies shpaml-like rules to template tags and closes them
automatically. Aml is smart enough to handle more complex
template tags like if/else/endif correctly.

Useless whitespace removal
--------------------------

Shpaml converts each line in input file to one line in output file
and preserves whitespace used for indentation. This can result in
unwanted namespace emitted when tag text is placed on a separate
line.

Shpaml provides syntax to specify tag text without adding whitespace
to it, but this syntax is not compatible with template engine shortcuts
provided by aml. Aml therefore removes whitespace between block
tags and their children.

Usage
=====

Basic Usage
-----------

Aml provides modules that pre-configure aml for a particular template
engine, and that can be used with no configuration. These modules are
aml_jinja.py for Jinja templates and aml_erb.py for ERb templates.

Template-specific aml modules can be imported into a Python program
and used as follows:

::

  import aml_jinja
  jinja_template_text = aml_jinja.convert_text(aml_template_text)

Alternatively, these modules can be invoked from the command line
to perform the conversion, as follows:

::

  python aml_jinja.py [-o output] [input]

If input is not specified or is - (dash), standard input is read.
If output is not specified or is -, processed text is written to
standard output.

Single-File Packages
--------------------

Template-specific aml modules can be bundled together with all of their
dependencies into a single file. These single-file packages are
template-specific as well. Their usage is identical to basic usage
described in the previous section.

Advanced Usage
--------------

Aml can be dynamically configured at runtime. The primary benefit of
runtime configuration is that whitespace removal can be turned on or
off, as desired. For example, to configure aml for Jinja templates
and to disable whitespace removal:

::

  import aml
  import aml.jinja_shortcuts
  
  aml.configure(aml.jinja_shortcuts.JinjaShortcuts, False)
  
  aml.convert_text(jinja_text)

Aml-specific syntax
===================

Please see jinja.rst or erb.rst for syntax details specific to the
template engine in use.

Requirements
============

Shpaml requires Python 2.4 or better, and works under Python 3.1. [#shpaml-python-req]_

Other Python scripts have been tested with Python 2.4 and Python 2.6.

.. [#shpaml-python-req] http://mail.python.org/pipermail/python-announce-list/2009-December/008021.html

Running Tests
=============

::

  make
  python test/run_tests.py

License
=======

Shpaml is in public domain.

Other scripts are licensed under the 2 clause BSD license.

Please refer to LICENSE file in the source distribution for complete
license text.
