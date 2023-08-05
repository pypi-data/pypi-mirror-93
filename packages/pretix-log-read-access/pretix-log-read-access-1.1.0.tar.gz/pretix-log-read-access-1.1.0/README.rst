Log read-only order data access
===============================

This is a plugin for `pretix`_. 

This plugin logs any access to extended information (e.g. question answers) of a specific order, as well as all export jobs. No warranty for completeness given.
Access to list of orders / search is not logged.

How to use
----------

- Install the plugin on the server, e.g. from ``pip install git+https://github.com/pretix-unofficial/pretix-hide-sold-out.git@main#egg=pretix-hide-sold-out``

- Done. There is **no** need to enable this plugin on event level. For security reasons, it's always enabled system-wide
  so no-one can temporarily disable it to hide their actions.

Caveats:

- No guarantee is given that tis logs all possible paths to access data.

- Does not log potential data access through other plugins.

- For exports, only the export configuration (e.g. "full export of paid orders") is logged, not the included records
  individually. For exports performed through the API, not even the parameters are logged, just the name of the export
  provider that has been used.

- API access is only logged when performed through a web-based user session, API requests using API tokens, OAuth
  applications or devices are **not logged**.

- Searching for orders with a specific reply to a question are only allowed for super-users in admin mode since this
  could otherwise lead to data leaks.

Development setup
-----------------

1. Make sure that you have a working `pretix development setup`_.

2. Clone this repository.

3. Activate the virtual environment you use for pretix development.

4. Execute ``python setup.py develop`` within this directory to register this application with pretix's plugin registry.

5. Execute ``make`` within this directory to compile translations.

6. Restart your local pretix server. You can now use the plugin from this repository for your events by enabling it in
   the 'plugins' tab in the settings.

This plugin has CI set up to enforce a few code style rules. To check locally, you need these packages installed::

    pip install flake8 isort black docformatter

To check your plugin for rule violations, run::

    docformatter --check -r .
    black --check .
    isort -c .
    flake8 .

You can auto-fix some of these issues by running::

    docformatter -r .
    isort .
    black .

To automatically check for these issues before you commit, you can run ``.install-hooks``.


License
-------


Copyright 2021 pretix team

Released under the terms of the Apache License 2.0



.. _pretix: https://github.com/pretix/pretix
.. _pretix development setup: https://docs.pretix.eu/en/latest/development/setup.html
