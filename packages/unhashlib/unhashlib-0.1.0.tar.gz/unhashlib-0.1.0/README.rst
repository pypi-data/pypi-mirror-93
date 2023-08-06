=========
unhashlib
=========

.. image:: https://img.shields.io/pypi/v/unhashlib.svg
   :alt: PyPI


``unhashlib`` is a Python string class enhancement (a mixin).

Installation
------------

The easiest way to install the package is via ``pip``::

    $ pip install unhashlib

Usage
-----

.. code:: python

    from unhashlib import unhashlib

    s1 =  unhashlib('the tragicall historye of romeus and juliet')

    len(s1)
    > 43

    s1.title()
    > 'The Tragicall Historye Of Romeus And Juliet'

    from hashlib import sha256
    print(s1.get_algorithm(sha256(s1.encode('utf-8')).hexdigest()))
    > 'sha256'

    print(s1.check(sha256(s1.encode('utf-8')).hexdigest()))
    > True

    from hashlib import md5
    s2 = unhashlib(md5('python'.encode('utf-8')).hexdigest())
    print(s2.crack())
    > 'python'
