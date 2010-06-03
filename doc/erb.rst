Aml-specific syntax
===================

Expressions
-----------

``= expression`` is translated to ``<%= expression %>``. = must be the
first non-whitespace charater on its line (expression takes over an
entire line). Example:

::

  a
    = target.name

translates to:

::

  <a>
    <%= target.name %>
  </a>

Ruby constructs
---------------

``% keyword`` is translated to ``<% keyword %>``. Blocks will be closed by aml
automatically. See the next section for an example.

Auto-closing blocks
-------------------

Aml automatically closes blocks generated via its shortcuts.
Aml knows that some blocks need special handling. For example,
the following input:

::

  % if foo
    bar
  % else
    baz

translates to:

::

  <% if foo %>
    bar
  <% else %>
    baz
  <% end %>

Self-closing blocks
-------------------

These are mostly useful as placeholders with helpers like ``content_for``.
Aml allows empty self-closed blocks to be specified similarly to how empty
self-closed html tags are specified.

::

  % >content_for :bar

translates to:

::

  <% content_for :bar %><% end %>

Whitespace after > in self-closing tags
---------------------------------------

In both blocks and HTML self-closing tags the whitespace between
``>`` and the tag name is optional. For example the following two lines
are equivalent in aml:

::

  > br
  >br

and these two lines are also equivalent:

::

  % >content_for :bar
  % > content_for :bar
