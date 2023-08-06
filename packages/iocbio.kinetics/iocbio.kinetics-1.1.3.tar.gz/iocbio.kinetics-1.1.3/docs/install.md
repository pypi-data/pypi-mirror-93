# Installation and Upgrade

There are several ways to install the software.

For Linux and Mac, installation using `pip` is recommended. See
the section below.

For Windows, you can choose whether to fetch the software as an
executable inside ZIP file (see below), use Anaconda python
environment together with its package management (see
[conda](#conda-anaconda-or-miniconda3)), or use the standard Python
installation with `pip`.


## pip

To be able to install PyQt5 using pip, you have to use python3.5 or
higher. If not available in the system, you can replace `pip3` command
below with `python3 -m pip`.

To install published version, run

```
pip3 install --user iocbio.kinetics
```
This will install all dependencies and it is expected to add a command `iocbio-kinetics` into your `PATH`. 
If the command is missing after installation, check whether the default location
of `pip3` installation is in your path. For Linux, it should be `~/.local/bin`.

To install, use the Git repository directly, for HTTPS users:
```
pip3 install --user git+https://gitlab.com/iocbio/kinetics
```
and for SSH users:
```
python3 -m pip install --user git+ssh://git@gitlab.com/iocbio/kinetics.git
```


For development, use

```
pip3 install --user -e .
```

in the source directory. To install the current version from the source, use

```
pip3 install --user .
```

Note that `--user` is recommended to avoid messing up the system
packages.

For upgrade, add `--upgrade` after install keyword. For example,
```
pip3 install --upgrade --user git+https://gitlab.com/iocbio/kinetics
```
or
```
python3 -m pip install --upgrade --user git+ssh://git@gitlab.com/iocbio/kinetics.git
```

## Windows ZIP binary

Starting from 1.1.1 release, MS Windows executable is provided in the
form of ZIP file. This allows to install and use the program quickly
as all the required packages are included in the provided ZIP.

To install, download the ZIP package from the link provided in the
corresponding [release
notes](https://gitlab.com/iocbio/kinetics/-/releases). Unpack the ZIP
file which would result in folder `Kinetics`. You could place this
folder as you see fit on your PC. To start IOCBIO Kinetics, enter the
folder and start `kinetics.bat` by double clicking on it.

On the first start, after connecting to the database, you would need
to enter "Settings". If you use your own modules, the path to them
will have to be specified as well.

## conda (Anaconda or Miniconda3)

Here, concise installation instructions are given. For illustrated
instructions with screenshots, see [Detailed Anaconda
instructions](https://gitlab.com/iocbio/sparks/blob/master/docs/INSTALL.Anaconda.md). Those
instructions are for `iocbio.sparks` package. For Kinetics software,
just replace `iocbio.sparks` with `iocbio.kinetics` in the linked
instructions.

### Installation Anaconda

Install Anaconda Python environment by downloading it from
https://www.anaconda.com/ . The package uses Python 3 language, so,
the version supporting it should be installed. At the moment of
writing, its Python 3.6.

#### Installation of channels

For installation from GUI:
* Start Anaconda Navigator
* Add channels by clicking "Channels" on the main screen and adding:
    * conda-forge
    * iocbio
* icon for `iocbio.kinetics` application should appear on the main
  Anaconda Navigator. Click on its install for installation.
  
Please note, it may take several minutes to install the application due 
to its dependencies.

For installation from CLI, start Anaconda Prompt. In the prompt, add channels:
```
conda config --append channels conda-forge
conda config --append channels iocbio
```
and install software
```
conda install -c iocbio iocbio-kinetics
```
and you are all set.


For running iocbio.kinetics in Windows, its possible to start it as an
application from Anaconda Navigator or, directly, from starting
`iocbio-kinetics` in `Anaconda/Scripts` directory. For convenience, a
shortcut can be created on desktop or Start Menu by the user.


## Use with R

If `iocbio-banova` is used, some additional packges are needed. Install R and the following packages in R:

```
install.packages(c("tidyverse", "BayesFactor", "formula.tools", "ggplot2"))
```

In addition, you will need to install `rpy2` Python package. Use `pip`
or Anaconda, depending on your environment.