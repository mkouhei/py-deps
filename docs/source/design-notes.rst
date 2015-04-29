==============
 Design notes
==============

Memo
====

============== ================ ==================== ======================
purpose        setup.py         Egg                  wheel (metadata.json)
============== ================ ==================== ======================
requires       install_requires requires.txt         run_requires.requires
no PyPI        dependency_links dependency_links.txt
optional       extras_require                        extras
extra resource                                       run_requires.extra
test                                                 test_requires.requires
============== ================ ==================== ======================

