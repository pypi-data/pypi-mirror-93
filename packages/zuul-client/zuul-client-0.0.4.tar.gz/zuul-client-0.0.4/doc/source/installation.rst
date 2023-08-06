:title: Installation

Installation
============

About using pip
---------------

Installing zuul-client from source or PyPI requires pip.

*Install pip on Linux*::

  [apt-get | yum] install python-pip

However using pip to install python packages directly on your operating system might
interfere with your OS's package management. It is recommended to use pip within
a virtual environment instead.

*Install python virtualenv*::

  [apt-get | yum | dnf] install python-virtualenv

*Create a virtualenv*::

  python -m venv zuul-client-venv

*Activate the virtual environment*::

  source zuul-client-venv/bin/activate

The pip executable will be pre-installed in the virtual environment.

More information on virtual environments here: https://docs.python.org/3/library/venv.html

Via the Python Package Index (PyPI)
-----------------------------------

The Python Package Index (PyPI) hosts the latest tagged version of zuul-client.

Within a virtual environment or after having installed pip on your system:

*Install zuul-client*::

  pip install zuul-client

Via the zuul-client container
-----------------------------

A container engine such as `podman <https://podman.io/getting-started/installation>`_
or `docker <https://docs.docker.com/get-docker/>`_ is required to use the
zuul-client container.

*Pull the container*::

  [docker | podman] pull docker.io/zuul/zuul-client

The above command will pull the *latest* version of zuul-client, ie at its current
state on the master branch. Alternatively, you can pull any tagged version of
zuul-client above 0.0.3::

  [docker | podman] pull docker.io/zuul/zuul-client:x.y.z

where **x.y.z** is the desired tagged version.

*Run zuul-client from the container*::

  [docker | podman] run docker.io/zuul/zuul-client --help

Please refer to the container engine's documentation for more runtime options.

From source
-----------

Within a virtual environment or after having installed pip on your system:

*Install zuul-client*::

  pip install .

