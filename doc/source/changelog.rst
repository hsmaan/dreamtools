ChangeLog
==============


1.2.6
-------

:2 March 2016:

* CHANGES: 
    - since dreamtools is now in bioconda, we removed the installation
      scripts conda_install.bat and conda_install.sh. 
    - Doc updates.


1.2.5
--------

* More cleanup for conda (removing tests from the distribution)

1.2.4
---------

* cleanup for bioconda

1.2.3
---------

* CHANGES: improved documentation
* NEWS: 2 installer for linux/mac and for windows


1.2.2
------

* NEWS: add --version in dreamtools standalone
* NEWS: add install.sh

1.2.1
------

* Some synapse data requires the synapse's user to accept the conditions of use on the synapse web page (by clicking on some widgets. In dreamtools, if the terms have not been accepted, there was just an error message from synapse. We now catch the error, print a more friendly message and open the synapse project so that the user can browse through the project directly to accept the conditions. 

1.2.0
------

* Better handling of errors and more friendly messages in the dreamtools standalone app.


1.1.1
--------

* Fixes a couple of Python3 issues
* Finalise travis integration. Coverage and testing simplified but 
  allows Travis to finish on time. May add back tests little by little in the
  future.
* Update README and doc.


1.1.0
----------

* Portage to Python3
* Add missing data files in D7C1
* Discard tests related to D9C3, which is not yet included.

1.0.0
--------
first official release synchronized with submission to F1000
`F1000 link <http://f1000research.com/articles/4-1030/v1>`_


0.11
------

* adding license
* adding onweb option in the executable.
* settings now uses CustomConfig class from easydev rather than a local
  implementation.
* fixing the distribution (MANIFEST)
* adding a docker example
* fixing Login to be interactive not jsut an error
* Fix MANIFEST to add missing cython file and README.rst
* All challenges from DREAM2 to DREAM8 are included except for D6C2, D7C2 and
D8C3. D6C2 and D7C2 may be included soon and D8C3 is available on an external
site. D8.5 and D9.5 and D9C1 also available.


0.9.2
-------

* CHANGES: some changes in dream2/dream3 to finalise all those challenges.

0.9.1
---------

* NEWS: add :class:`dreamtools.dream9.scoring.D9C1` challenge
* NEWS: add :class:`dreamtools.dream6.scoring.D6C3` challenge

0.9.0
---------

* Upgrade version to higher number to reflect the fact that the package is now more robust

0.1.6
--------

* Add a bunch of other challenges mostly D2/D3/D4/D5 and fixes + tests

0.1.5
----------


 * NEWS: some new classes :class:`dreamtools.dream2` related to DREAM2
 * NEWS: add :class:`dreamtools.dream5.scoring.D5C1` challenge in Dreamtools
 * NEWS: add :class:`dreamtools.dream3.scoring.D3C2` challenge in Dreamtools
 * NEWS: add :class:`dreamtools.dream3.scoring.D3C3` challenge in Dreamtools
 * NEWS: add :class:`dreamtools.dream3.scoring.D3C4` challenge in Dreamtools
 * Changes: fix :class:`dreamtools.dream4.scoring.D4C2` challenge in Dreamtools

0.1.4
-------

 * NEWS: add :class:`dreamtools.dream4.scoring.D4C2` challenge in Dreamtools
 * NEWS: add :class:`dreamtools.dream4.scoring.D4C1` challenge in Dreamtools
 * CHANGES: move a download_data method from D5C2 into the :class:`Challenge` main class
   to factorise some code.

0.1.3
------

 * NEWS: add D4C3 challenge in Dreamtools

0.1.2
---------

* NEWS: added dreamtools-layout for the developer to automatically create a challenge layout 
* CHANGES: dreamtools-scoring now handles automatically new challenges providing the Challenge
  class has the mehod score() and download_template() available.


0.1.1
------

* NEWS: add D9dot5C1 challenge


0.1.0
-------

* NEWS: Challenge D8C1, D8C2, D5C2, D7C1 (D6C1) available
* NEWS: dreamtools-scoring standalone provided
