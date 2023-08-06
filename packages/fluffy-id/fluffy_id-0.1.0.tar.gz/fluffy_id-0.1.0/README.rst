==============
Fluffy-ID
==============


.. image:: https://img.shields.io/pypi/v/fluffy_id.svg
        :target: https://pypi.python.org/pypi/fluffy_id

.. image:: https://img.shields.io/travis/yoophi/fluffy_id.svg
        :target: https://travis-ci.com/yoophi/fluffy_id

.. image:: https://readthedocs.org/projects/fluffy-id/badge/?version=latest
        :target: https://fluffy-id.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Quickly and easily generate individual or bulk sets of globally unique identifiers (GUIDs).


* Free software: MIT license
* Documentation: https://fluffy-id.readthedocs.io.


Features
--------

* Generate GUIDs.

   .. code:: sh

      $ fluffy_id
      13522471585935524865

      $ fluffy_id --shard-id 4
      13522471789401214977

      $ fluffy_id 5 --shard-id 4
      13522471911983943681
      13522471911983943682
      13522471911983943683
      13522471911983943684
      13522471911983943685


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
