History
=======

1.0.0 (2020-05-16)
------------------

* Updates dependencies.
* Refactors.
* Supports Python 3.8 only.

0.5.5 (2015-08-19)
------------------

* Adds TimeoutError, ConnectionRefusedError / socket.error exceptions.
* Adds error handling the PyPI service down.
* Changes Sphinx theme to sphinx_rtd_theme.
* Adds counter of the each depth.

0.5.4 (2015-07-22)
------------------

* Adds latest_version function.
* Adds link_prefix for overriding node link.

0.5.3 (2015-07-19)
------------------

* Adds exception InvalidMetadata type.

0.5.2 (2015-07-15)
------------------

* Fixes duplicated line of linkdraw.
* Changes linkdraw colors by dependencies depth.
* Adds depth property to graph nodes.
* Adds parsing the package dependency depth.

0.5.1 (2015-07-12)
------------------

* Changes Package.search method to a function.
* Fixes infinity loop trace_chain.
* Fixes `None` redundant second argument of `dict.get()`.
* Fixes `len()` used to check if collection has items.
* Fixes old-style string formatting.

0.5.0 (2015-06-22)
------------------

* Supports memcached as the backend of cache.

0.4.6 (2015-06-11)
------------------

* Fixes not control the version of package correctly.

0.4.5 (2015-06-07)
------------------

* Adds disable time, descr for Linkdraw.

0.4.4 (2015-06-03)
------------------

* Removes debug print.

0.4.3 (2015-06-02)
------------------

* Adds JSON decoder for Linkdraw.

0.4.2 (2015-05-31)
------------------

* Fixes #7 not handling the failure of python setup egg_info.
* Adds py_deps.exceptions module.
* Adds py_deps.logger module.
* Fixes issues of DistributionNotFound, InstallationErrror.

0.4.1 (2015-05-28)
------------------

* Adds Container.list_data method.
* Unsupports wheel format for distribution.

0.4.0 (2015-05-20)
------------------

* Searching packages from PyPI.

0.3.0 (2015-05-12)
------------------

* Supports NetworkX DiGraph objects.
* Changes to use mock instead of pip.req.RequirementSet.prepare_files.
* Coverage 98% over.

0.2.0 (2015-05-10)
------------------

* Cache the parsed dependencies.
* Fixes setting the url of node and targets.

0.1.1 (2015-05-08)
------------------

* Fixes test data of pretty_print, linkdraw.

0.1.0 (2015-05-07)
------------------

* Supports generating linkdraw data.
* Supports pip 6.1.1 over.
* Supports wheel format for distribution.
* Adds unit tests.

0.0.1 (2015-04-29)
------------------

* First release
