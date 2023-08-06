dbus-deviation
==============

dbus-deviation is a project for parsing D-Bus introspection XML and processing
it in various ways. Its main tool is dbus-interface-diff, which calculates the
difference between two D-Bus APIs for the purpose of checking for API breaks.
This functionality is also available as a Python module, dbusdeviation.

A second Python module, dbusapi, is provided for parsing D-Bus introspection
XML to produce an AST representing a D-Bus interface.

dbus-deviation’s API is currently unstable and is likely to change wildly.

Using dbus-deviation
====================

dbus-deviation can be used as a utility program or as a Python library.

The utility programs:
 - dbus-interface-diff:
     Check for differences between two versions of the same D-Bus API and
     print details of each difference. It can check for problems with forwards
     and backwards compatibility, as well as general informational
     differences.

     Example:
       dbus-interface-diff \
           com.example.Interface1.xml \  # old version of the interface
           com.example.Interface2.xml    # new version of the interface

 - dbus-interface-vcs-helper:
     This is a helper program designed to be used by dbus-deviation.mk.

As a library, the core object is an InterfaceParser, allowing a D-Bus API to
be parsed and represented as an AST. See the API documentation for more
explanation and examples.

dbus-deviation.mk
-----------------

This is a Makefile snippet which should be copied into your project, added to
git, and the following two lines included in your top-level Makefile.am:
```
dbus_api_xml_files = list of D-Bus interface XML files
-include $(top_srcdir)/dbus-deviation.mk
```

Do not add it to EXTRA_DIST. It is designed to work from git checkouts only.

Then run:
```
make dbus-deviation-mk-install
```
to set up the API signature database. This assumes that your project defines
D-Bus interfaces in XML files, and does not generate them at runtime.

Finally, copy pre-push.hook to .git/hooks/pre-push and ensure it’s executable.
This script will automatically update the API signature database when a new
release tag is pushed to the git remote.

There is currently no streamlined support for projects which generate D-Bus
interfaces at runtime.

dbus-deviation.mk defines the following rules:
 - dist-dbus-api-compatibility (a dependency of dist-hook)
 - check-dbus-api-compatibility (a dependency of check-local)
 - dbus-deviation-mk-install (never triggered automatically)

Dependencies
============

 - argparse
 - lxml

Development
===========

For fun, dbus-deviation uses the following services to do continuous
integration and gather build statistics:
 - https://travis-ci.org/pwithnall/dbus-deviation
 - https://landscape.io/github/pwithnall/dbus-deviation
 - https://coveralls.io/r/pwithnall/dbus-deviation
 - https://codecov.io/github/pwithnall/dbus-deviation

Licensing
=========

dbus-deviation is licensed under the LGPL version 2.1 (or, at your option, any
later version). See COPYING for more details.

dbus-deviation versions 0.4.0 and earlier were licensed under the choice of the
Academic Free License version 2.1, or the GNU General Public License version 2
(or, at your option, any later version). This is the same license as D-Bus
itself. Version 0.5.0 was relicensed to LGPLv2.1+ as it’s a more standard license
with less ambiguity about its implications.

Bugs
====

Bug reports and patches should be sent via GitHub or Gitlab:
 - https://github.com/pwithnall/dbus-deviation
 - https://gitlab.com/dbus-deviation/dbus-deviation

Contact
=======

Philip Withnall <philip@tecnocode.co.uk>
https://tecnocode.co.uk/dbus-deviation/
