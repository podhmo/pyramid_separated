pyramid_separated
========================================

separated config files support.


how to use
----------------------------------------

if you want to share common settings, share with development.ini and production.ini.

.. code:: python

    config.include("pyramid_separated")
    config.add_config_file("common.ini", category="common", overwrite=False)


development.ini

.. code::

    common.ini = %(here)s/common.ini


common.ini

.. code::


    [common]
    sqlalchemy.url = sqlite://app.db
    sqlalchemy.echo = True

overwrite option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

overwrite option is True, then, overwrite settings via settings that separated ini files.


path settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

assetspec format is also ok.

.. code::

    common.ini = app.config:common.ini
