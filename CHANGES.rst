Changelog
=========

2.0.4 (unreleased)
------------------

Breaking changes:

- *add item here*

New features:

- *add item here*

Bug fixes:

- *add item here*


2.0.3 (2017-05-09)
------------------

Bug fixes:

- Remove unused import and added a missing import on example.
  [bruno]

- Update setup.py to point to github repository.
  [esteele]

2.0.2 (2015-11-28)
------------------

Fixes:

- Changed i18n_domain to "plone".
  [staeff]

- Removed unneeded i18n-attribute.
  [staeff]


2.0.1 (2015-05-04)
------------------

- pep8.
  [maurits]

- Whitespaces cleanup.
  [gforcada]


2.0 (2012-08-30)
----------------

* Update to work with grokcore.view >= 2.2. This generally means that this
  package is no longer compatible with Plone < 4.3.
  [davisagli]

* Change i18n domain to plone.dexterity to reuse the translations. plone.dexterity
  already has all the strings needed.
  [gaudenz]

* Fixes documentation mistake of documented ``form.wrapped()`` directive
  which is in fact ``form.wrap()``
  [romanofski]

* A number of schema directives were moved to other packages and reimplemented
  to not depend on grok.  The ``Schema`` class and the ``model``, ``fieldset``,
  and ``primary`` directives were moved to ``plone.supermodel.model``. The
  ``omitted``, ``no_omit``, ``mode``, ``widget``, ``order_before``,
  ``order_after``, ``read_permission``, and ``write_permission`` directives were
  moved to ``plone.autoform.directives``.

  For now the directives are still available under their old names in this
  package, but they are deprecated and may be removed at some point.

  Some minor related changes:

  * Tagged values are now stored on schemas as soon as they are defined, rather
    than when the schemas are grokked. Additional actions required by the
    directives, if any, are performed at the end of ZCML configuration.
  * Due to a bug in zope.interface, ``plone.supermodel.model.Schema`` must be
    the `first` base class of any schema to which the directives should apply.
    Also, unfortunately it is no longer possible to give an error if the schema
    directives are called on an interface that is not a ``Schema``.

  [davisagli]

1.0 - 2011-05-20
----------------

* No changes.

1.0b7 - 2010-04-20
------------------

* Allow arbitrary extra parameters for the fieldset directive. This is useful
  for extensions that want to tweak fieldset behaviour or rendering.
  [wichert]

* Add ``no_omit`` directive, so that fields that have been omitted can be
  re-included again on for a more specific form interface.
  [davisagli]

* Accept a form interface as an optional positional argument for the ``mode``
  and ``omitted`` directives, and store it in the tagged values using the new
  format expected by plone.autoform.
  [davisagli]

* Add ``@form.error_message()`` decorator for registering custom error
  messages for errors and/or fields.
  [optilude]

* Add ``@form.validator()`` decorator to register a simple field validator.
  See README.txt for details.
  [optilude]

* Support unwrapped forms (in Zope 2.12). The default is to wrap in Zope <
  2.12, and not to wrap in Zope >= 2.12. A new ``form.wrapped()`` directive
  can be used to force wrapping or non-wrapping (by passing ``False`` as an
  argument).
  [optilude]

* Warn more forcefully when using form directives on interfaces not deriving
  from ``Schema``, or using schema hints that refer to field names that cannot
  be found.
  [optilude]

1.0b6 - 2009-10-08
------------------

* Add support for the ``primary()`` directive, which is used to set the
  primary field for marshalling. See the ``plone.rfc822`` for details.
  [optilude]

1.0b5 - 2009-07-21
------------------

* Updated to new five.grok release.
  [optilude]

1.0b3 - 2009-07-12
------------------

* Made adjustments for changes in plone.supermodel's API.
  [optilude]

1.0b2 - 2009-06-15
------------------

* Make sure that we don't lose the function when using the
  @form.default_value() decorator and the other value decorators.
  [optilude]

1.0b1 - 2009-04-17
------------------

* Initial release
