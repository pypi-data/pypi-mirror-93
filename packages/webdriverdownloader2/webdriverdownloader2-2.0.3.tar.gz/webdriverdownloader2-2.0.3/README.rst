``webdriverdownloader``
=======================

Python module to facilitate downloading and deploying `WebDriver <https://www.w3.org/TR/webdriver/>`_
binaries.  The classes in this module can be used to automatically search for
and download the latest version (or a specific version) of a WebDriver binary
(will download to ``$HOME/webdriver`` or ``/usr/local/webdriver`` if run with
``sudo``), extract the binary from the downloaded archive and create a symlink
in either ``/usr/local/bin`` (if run with ``sudo``) or ``$HOME/bin``.

Note: For non-root users, the ``$HOME/bin`` directory may not be in the search
PATH.  If you are unable to add this directory your search path, a workaround
is to capture the return value from the ``download()`` or ``download_and_install()``
method (see the docstrings for those methods for more information on the return
values) and pass the path to the downloaded webdriver binary as a parameter to
the constructor for the Selenium WebDriver instance.  See the documentation for
the ``executable_path`` parameter for the relevant WebDriver class for more
information.


Installation
------------

This module is available on the Python Package Index (PyPI) and can be
installed as follows:

``pip install webdriverdownloader``


Dependencies
------------

This module is dependent on the following additional packages:

- `beautifulsoup4 <https://pypi.org/project/beautifulsoup4/>`_
- `requests <https://pypi.org/project/requests/>`_
- `tqdm <https://pypi.org/project/tqdm/>`_
- `py-cpuinfo <https://pypi.org/project/py-cpuinfo/>`_
- `loguru <https://pypi.org/project/loguru/>`_


Classes
-------

The following classes are available:

- ``ChromeDriverDownloader`` for downloading and installing `chromedriver <https://sites.google.com/a/chromium.org/chromedriver/downloads>`_ (for Google Chrome).
- ``GeckoDriverDownloader`` for downloading and installing `geckodriver <https://github.com/mozilla/geckodriver>`_ (for Mozilla Firefox).


Status
------

![Python package cross version testing](https://github.com/bodharma/webdriverdownloader/workflows/Python%20package%20cross%20version%20testing/badge.svg)



Example module usage
--------------------

Example::

   >>> from webdriverdownloader import GeckoDriverDownloader
   >>> gdd = GeckoDriverDownloader()
   >>> gdd.download_and_install()
   1524kb [00:00, 1631.24kb/s]
   ('/Users/lsaguisag/webdriver/geckodriver-v0.20.1-macos/geckodriver', '/Users/lsaguisag/bin/geckodriver')
   >>> gdd.download_and_install("v0.20.0")
   1501kb [00:02, 678.92kb/s]
   Symlink /Users/lsaguisag/bin/geckodriver already exists and will be overwritten.
   ('/Users/lsaguisag/webdriver/geckodriver-v0.20.0-macos/geckodriver', '/Users/lsaguisag/bin/geckodriver')
   >>> gdd.download_and_install()
   Symlink /Users/lsaguisag/bin/geckodriver already exists and will be overwritten.
   ('/Users/lsaguisag/webdriver/geckodriver-v0.20.1-macos/geckodriver', '/Users/lsaguisag/bin/geckodriver')
   >>>


Command line tool
-----------------

There is a command-line tool that is also available.  After installing the
package, it can be used as follows (Windows example)::

   > webdriverdownloader chrome:2.38 firefox
   Downloading WebDriver for browser: 'chrome'
   3300kb [00:00, 11216.38kb/s]
   Driver binary downloaded to: C:\Users\lsaguisag\webdriver\chrome\2.38\chromedriver_win32\chromedriver.exe
   Driver copied to: C:\Users\lsaguisag\bin\chromedriver.exe

   Downloading WebDriver for browser: 'firefox'
   3031kb [00:01, 2253.64kb/s]
   Driver binary downloaded to: C:\Users\lsaguisag\webdriver\gecko\v0.20.1\geckodriver-v0.20.1-win64\geckodriver.exe
   Driver copied to: C:\Users\lsaguisag\bin\geckodriver.exe


License
-------

This is released under an MIT license.  See the ``LICENSE`` file in this
repository for more information.

Important: Consult the license terms of the providers of the WebDriver
downloads prior to downloading / using the WebDrivers.
