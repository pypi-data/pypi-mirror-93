================
collective.pivot
================

Plone plugin which makes a connection to the CGT's DB PIVOT.
This one display listing and details of various tourist offers.
It's also possible to add filters.


Translations
------------

This product has been translated into

- French


Installation
------------

Install collective.pivot by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.pivot


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/imio/collective.pivot/issues
- Source Code: https://github.com/imio/collective.pivot


License
-------

The project is licensed under the GPLv2.


Contributors
============

- Christophe Boulanger, christophe.boulanger@imio.be


Changelog
=========


1.0a4 (2021-02-01)
------------------

- Fix offer codeCgt
  [boulch]


1.0a3 (2020-12-17)
------------------

- [WEB-3482] Add toggle map button
  [thomlamb]

- [WEB-3482] Adding styles for pivot view
  [thomlamb]

- [WEB-3482] Add less package for react and webpack
  [thomlamb]


1.0a2 (2020-12-17)
------------------
- [WEB-3482] Add toggle map button
  [thomlamb]

- [WEB-3482] Adding styles for pivot view
  [thomlamb]

- [WEB-3482] Add less package for react and webpack
  [thomlamb]

- [WEB-3482] Get new attributes from Pivot : email
  [boulch]

- [WEB-3482] Get new attributes from Pivot (CP, Locality, phone1)
  [boulch]

- [WEB-3482] Split to diffetent files js and css on react project
  [thomlamb]


1.0a1 (2020-12-04)
------------------
- added a react and webpack project for the pivot frontend
  [thomlamb]

- Initial release.
  [boulch]


