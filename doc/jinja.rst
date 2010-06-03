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
