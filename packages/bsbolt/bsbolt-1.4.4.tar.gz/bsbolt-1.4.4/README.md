# **BSBolt (BiSulfite Bolt)**
## A fast and safe bisulfite sequencing processing platform

[BiSuflite Bolt (BSBolt)](https://github.com/NuttyLogic/BSBolt); a fast and scalable bisulfite sequencing 
processing platform. BSBolt is an integrated analysis platform that offers support for bisulfite sequencing 
read simulation, alignment, methylation calling, data aggregation, and data imputation. BSBolt has been validated 
to work with a wide array of bisulfite sequencing data,including whole genome bisulfite sequencing (WGBS), 
reduced representative bisulfite sequencing data (RRBS), and targeted methylation sequencing data. 
BSBolt utilizes forked versions of [BWA](https://github.com/lh3/bwa) 
and [WGSIM](https://github.com/lh3/wgsim) for read alignment and read simulation respectively. 
BSBolt is released under the MIT license.
 
## Documentation

BSBolt documentation can be found at [bsbolt.readthedocs.io](https://bsbolt.readthedocs.io).

## Release Notes
- BSBolt v1.4.4
    - The default entry point for BSBolt has changed from **BSBolt** to **bsbolt** for conda compatibility 

## Installation

### **PyPi Installation**

Pre-compiled binaries can be installed using PyPi. Binaries are provided for python >=3.6
on unix like systems (macOS >=10.15 and linux).

```shell
pip3 install bsbolt --user
```

### **Conda Installation**

BSBolt can be installed using the conda package manager using the installation instructions below. 

```shell
conda config --add channels bioconda
conda config --add channels conda-forge
conda install -c cpfarrell bsbolt
```

### **Installing from Source**

Dependencies

* zlib-devel >= 1.2.3-29
* GCC >= 8.3.1

```shell
# clone the repository
git clone https://github.com/NuttyLogic/BSBolt.git
cd bsbolt
# compile and install package
pip3 install .
```

### **Installing from Source on macOS**

Dependencies 
* autoconf
* homebrew
* xcode

Installation from source requires xcode command line utilities, [homebrew](https://brew.sh/) macOS package manager, 
and autoconf are installed. Xcode through the mac App Store, running the xcode installation command listed below, 
or as part of the [homebrew](https://brew.sh/) macOS package manager installation. The full installation process
can be completed as outlined below.

```shell script
# install xcode utilities
xcode-select --install
# install homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
# install autoconf
brew install autoconf
# optionally install python
brew install python3.8
# install bsbolt
pip3 install bsbolt
```


