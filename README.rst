========================
Shpaml-Jinja Integration
========================

Overview
========

Aml ("A markup language") is a pre/post-processor for shpaml.
It extends shpaml syntax with shortcuts useful when shpaml output is
a jinja template.

Aml provides three main feature points:

Indentation check
-----------------

Indentation is significant in shpaml but
shpaml itself will happily convert a file mixing tabs and spaces.
The result is usually not what template designer intended, so
aml requires that only spaces are used for indentation.

Jinja shortcuts
---------------

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
to it, but this syntax is not compatible with Jinja shortcuts
provided by aml. Aml therefore removes whitespace between block
tags and their children.

Usage
=====

Aml module can be imported into a Python program and used as follows:

::

  import aml
  jinja_template_text = aml.convert_text(aml_template_text)

Alternatively, aml.py can be invoked from the command line to perform
the conversion, as follows:

::

  python aml.py [-o output] [input]

If input is not specified or is - (dash), standard input is read.
If output is not specified or is -, processed text is written to
standard output.

Aml-specific syntax
===================

Expressions
-----------

``= expression`` is translated to ``{{ expression }}``. = must be the
first non-whitespace charater on its line (expression takes over an
entire line). Example:

::

  a
    = target.name

translates to:

::

  <a>
    {{ target.name }}
  </a>

Text marked for translation
---------------------------

``~ text`` is translated to ``{% trans %}text{% endtrans %}``.
Like ``= expression`` ``~ text`` takes over an entire line, and
~ must be the first non-whitespace character. Example:

::

  a
    ~ Click here

translates to:

::

  <a>
    {% trans %}Click here{% endtrans %}
  </a>

Template tags
-------------

``% tag`` is translated to ``{% tag %}``. Tags will be closed by aml
automatically. See the next section for an example.

Auto-closing template tags
--------------------------

Aml automatically closes template tags generated via its shortcuts.
Aml knows that some tags need special handling. For example,
the following input:

::

  % if foo
    bar
  % else
    baz

translates to:

::

  {% if foo %}
    bar
  {% else %}
    baz
  {% endif %}

Self-closing template tags
--------------------------

These are mostly useful for empty blocks. Aml allows empty self-closed
template tags to be specified similarly to how empty self-closed html
tags are specified.

::

  % >block foo

translates to:

::

  {% block foo %}{% endblock %}

Whitespace after > in self-closing tags
---------------------------------------

In both template tags and HTML self-closing tags the whitespace between
``>`` and the tag name is optional. For example the following two lines
are equivalent in aml:

::

  > br
  >br

and these two lines are also equivalent:

::

  % >block
  % > block

Requirements
============

Shpaml requires Python 2.4 or better, and works under Python 3.1. [#shpaml-python-req]_

Other Python scripts have been tested with Python 2.4 and Python 2.6.

.. [#shpaml-python-req] http://mail.python.org/pipermail/python-announce-list/2009-December/008021.html

License
=======

Shpaml is in public domain.

Other scripts are licensed under the 2 clause BSD license.

Please refer to LICENSE file in the source distribution for complete
license text.
