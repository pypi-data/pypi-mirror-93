.. :changelog:

History
-------

0.7.0 (2021-02-04)
++++++++++++++++++

* Replaced existing migrations with new migration (borking existing
  databases) to fix error with non-proxy model that migrations would
  not handle.


0.6.0 (2021-02-01)
++++++++++++++++++

* Removed all attempts to reuse Django model instances sharing the
  same details (names, repositories, language declarations).
* The above change is handled in a single migration; this will break
  existing installations that contain data.


0.5.0 (2020-12-03)
++++++++++++++++++

* Added validation for some models.
* Added blank=True to some fields that must sometimes be empty.


0.4.0 (2020-11-23)
++++++++++++++++++

* Corrected bugs in validators.
* Updated models to properly mark some fields as optional.
* Added model validation to XML import script.


0.3.1 (2020-11-16)
++++++++++++++++++

* No changes; clean rebuild for PyPI.


0.3.0 (2020-11-16)
++++++++++++++++++

* Added django-reversion support.

* Corrected some model and import bugs. Unfortunately caused problems
  with Django migrations, and these have been reset.


0.2.0 (2020-10-20)
++++++++++++++++++

* Added test (and associated code fixes) of round-trip import and
  serialisation of EAD3 XML.


0.1.2 (2020-10-16)
++++++++++++++++++

* Added XSD files to MANIFEST.in, so that the EAD3 XSD is included in
  the package.


0.1.1 (2020-10-13)
++++++++++++++++++

* Added dependency on lxml.


0.1.0 (2020-10-09)
++++++++++++++++++

* First release on PyPI.
