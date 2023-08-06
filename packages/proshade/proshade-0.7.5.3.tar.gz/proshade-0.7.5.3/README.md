![](https://github.com/michaltykac/proshade/blob/experimental/proshade/Logo_small.png)

ProSHADE
========

Protein Shape Description and Symmetry Detection

# Introduction

ProSHADE is a C++ language library and an associated tool providing functionalities for working with structural biology molecular structures. The library implements functions for computing shape-wise structural distances between pairs of molecules, detecting symmetry over the centre of mass (or centre of map) of a single structure, map re-sizing as well as matching density maps and PDB coordinate files to one another. The executable implemented in the ```bin.cpp``` file then allows easy access to these functionalities without the need for library linking, while the python modules provides easy access to the functionality from the python language. For help on how the executable should be used, refer to the ```-h``` option of it. For more details about the functionalities, see below.

# Obtaining ProSHADE

The most recent stable version of ProSHADE is available from the *master* branch of the GitHub repository https://github.com/michaltykac/proshade, from where it can be cloned using the git application or downloaded manually using the interface. More advanced users may be interested in obtaining the *development* or the *experimental* branches, which are available from the same link. The *experimental* branch is where I do all new development and it may or may not be currently compilable and working properly, while the *development* branch should always compile, but is more likely to contain bugs and issues as it is the code before proper testing.

# Index

- [Introduction](#introduction)
- [Obtaining ProSHADE](#obtaining-proshade)
- [Index](#index)
- [Installation](#installation)
    - [Standard System Dependencies](#standard-system-dependencies)
        - [Installing python](#installing-python)
        - [Installing standard system dependencies on MacOS](#installing-standard-system-dependencies-on-macos)
        - [Installing standard system dependencies using apt)](#installing-standard-system-dependencies-using-apt)
        - [Installing standard system dependencies using ZYpp](#installing-standard-system-dependencies-using-zypp)
        - [Installing standard system dependencies using yum](#installing-standard-system-dependencies-using-yum)
    - [Other dependencies](#other-dependencies)
    - [Installing on Windows](#installing-on-windows)
        - [Installing CMake](#installing-cmake)
        - [Installing git](#installing-git)
        - [Installing Build Tools for Visual Studio](#installing-build-tools-for-visual-studio)
        - [Installing ProSHADE](#installing-proshade)
        - [Setting ProSHADE PATH](#setting-proshade-path)
    - [Installing using CMake on Unix](#installing-using-cmake-on-unix)
        - [CMake options](#cmake-options)
        - [Uninstall using CMake](#uninstall-using-cmake)
    - [Installation using pip](#installation-using-pip)
        - [Uninstalling pip installed module](#uninstalling-pip-installed-module)
- [Input PDB files](#input-pdb-files)
    - [Spacegroups](#spacegroups)
    - [Waters](#waters)
    - [Models](#models)
- [Using the ProSHADE binary](#using-the-proshade-binary)
    - [Symmetry Detection](#symmetry-detection)
    - [Shape similarity distances](#shape-similarity-distances)
    - [Re-boxing structures](#re-boxing-structures)
    - [Optimal rotation and translation](#optimal-rotation-and-translation)
- [Using the ProSHADE library](#using-the-proshade-library)
    - [Linking against the ProSHADE library](#linking-against-the-proshade-library)
    - [Examples of ProSHADE library usage](#examples-of-proshade-library-usage)
- [Using the Python module](#using-the-python-module)
    - [Python module examples](#python-module-examples)
        - [Simple access](#simple-access)
        - [Advanced access](#advanced-access)
        - [Direct access](#direct-access)
            - [Reading a structure from file](#reading-a-structure-from-file)
            - [Creating ProSHADE_data object from map](#creating-proshade_data-object-from-map)
            - [3D arrays](#3d-arrays)
            - [Writing out maps](#writing-out-maps)
            - [Getting back the ProSHADE internal representation map](#getting-back-the-proshade-internal-representation-map)
            - [Computing standard ProSHADE tasks](#computing-standard-proshade-tasks)
            - [Computing the spherical harmonics decomposition](#computing-the-spherical-harmonics-decomposition)
            - [Computing the self-rotation function](#computing-the-self-rotation-function)
            - [Computing the optimal rotation function](#computing-the-optimal-rotation-function)
            - [Finding the optimal rotation](#finding-the-optimal-rotation)
            - [Rotating the internal map representation](#rotating-the-internal-map-representation)
            - [Computing the translation function](#computing-the-translation-function)
            - [Writing out resulting structures](#writing-out-resulting-structures)

# Installation

The installation of the ProSHADE software should be done using the CMake system and the supplied CMakeLists.txt file. The minimual requiered version of CMake is 2.6, however, python modules and single source file compilation will not be available unless CMake version 3.4 or higher is used. The CMakeLists.txt file assumes the standard system dependencies are installed in the system folders; for a full list of standard system dependencies, please see the section [Standard System Dependencies](#standard-system-dependencies).
 
 Once all of the standard system dependencies are installed CMake can be run to create the make files as described in the section [Installing using CMake](#installing-using-cmake). Alternatively, ProSHADE also provides *setup.py* script, which wraps the CMake installation - please refer to the [Installation using pip](#installation-using-pip) section of this documentation for more details. The main difference between these two installation approaches is that using CMake allows building the executable and the dynamic C++ library, but will install the python module only locally, while installing using pip will install only the python module, but will install it globally. Combining these two installations is not a problem.
 
Moreover, if CMake is used to build ProSHADE directly, then the user may make use of several options that can be used to modify the default behaviour of the installation; these typically drive the installation locations and dependencies paths in the case of non-standard dependency location. Please see the section [CMake options](#cmake-options)  for details as to how to use these options and what do they do.
 
 Please note that while the ProSHADE code is C++ 98 standard compatible, some of the dependencies do require at least partial support for the C++ 11 standard and building python module requires full C++ 11 support.
 
 ## Standard System Dependencies
 
 Generally, the following list of standard system libraries and utilities are required for successfull installation of ProSHADE on Unix systems:
 
  - **gcc**
  - **g++** 
  - **make**
  - **cmake**
  - **fftw3-dev**
  - **liblapack-dev**
  - **git**
  - **zlib**
  - **python** with **numpy**
  
  This list is somewhat different for Windows systems, as ProSHADE contains 64-bit libraries for most of the dependencies already prepared, thus limiting the list. This, however, means that ProSHADE can only be installed on Windows10 64-bit systems and currently does neither supprt the 32-bit systems, nor the older Windows systems (7, Vista, XP, ...):
  
  - **cl**
  - **cmake**
  - **git**
  - **python** with **numpy**
  
  CMake should complain and issue a reasonably decipherable error messages if any of these dependencies are missing. 
  
  ### Installing python
  
  Python is not required for ProSHADE binary and library installation, but it is necessary to have it installed for successfull ProSHADE python module installation. Now, while most modern Unix systems come with some version of the python language pre-installed (although Windows does not), it seems reasonable to assume that users who are interested in using the ProSHADE python module do have their preferred version of python already installed and set as the default system python (meaning that the ```python``` command points to the python executable that the user wants the ProSHADE module to be installed for).
  
  Should the user not have any python version installed or should the user be interested in having multiple versions, the Anaconda environment ( https://www.anaconda.com/products/individual ) can be recommended for all systems supported by ProSHADE. Of course, there are alternatives for installation of python and management of various environments and ProSHADE does not care which is being used.
  
  ### Installing standard system dependencies on MacOS
  
  Assuming a clean MacOS, the ProSHADE dependencies can be installed as follows: Firstly, the XCode tools should be installed from Apple - this can be achieved by issuing the command:
  
```
    xcode-select --install
```

Next, CMake will need to be installed manually; that is, starting with downloading the source codes from https://github.com/Kitware/CMake/releases/download/v3.19.2/cmake-3.19.2.tar.gz . After moving the downloaded file to where the codes should live and navigating to the same location in Terminal, please use the following commands to install CMake:

```
    tar -zxvf ./cmake-3.19.2.tar.gz
    cd ./cmake-3.19.2
    ./bootstrap 
    make
    sudo make install
```

Finally, some MacOS systems do not have the FFTW3 library pre-installed. If this is your case, then please use the following commands to install FFTW3 manually: Firstly, download the source codes from here: http://www.fftw.org/fftw-3.3.9.tar.gz . After moving the downloaded file to where the codes should live and navigating to the same location in Terminal, please use the following commands to install FFTW3:

```
    tar -zxvf ./fftw-3.3.9.tar 
    cd ./fftw-3.3.9
    ./configure --enable-shared
    make
    sudo make install
```
  
  Now, ProSHADE should be automaically installable using the CMake system.
 
 ### Installing standard system dependencies using apt
 
 The *APT* package manager can be used to install all the system dependencies of ProSHADE using the following command.
 
 ```
    sudo apt-get install gcc g++ make cmake git fftw3-dev liblapack-dev zlib1g-dev
```

After this, ProSHADE should by automatically installable using the CMake system.
 
 ### Installing standard system dependencies using ZYpp
 
 The *ZYpp* package manager and the associated *zypper* command-line tool can be used install all the system dependencies of ProSHADE as follows:
 
 ```
    sudo zypper install gcc gcc-c++ git cmake fftw3-devel lapack-devel zlib-devel
```

After this, ProSHADE should by automatically installable using the CMake system.

### Installing standard system dependencies using yum

Firstly, at least on some systems, the *yum* package manager may not be using the *powertools* repository; however, some of ProSHADE dependencies are kept there. Therefore, the user may need to enable the *powertools* repository by issuing the folloing commands:

```
    sudo yum install dnf-plugins-core
    sudo yum config-manager --set-enabled powertools
```

Then, the *yum* package manager can be used install all the system dependencies of ProSHADE as follows:

```
    sudo yum install gcc gcc-c++ make cmake fftw3-devel lapack-devel zlib-devel
```

After this, ProSHADE should by automatically installable using the CMake system.

## Other dependencies

ProSHADE also depends on the *Gemmi* and *SOFT2.0* libraries. The installation of these libraries is automated in the CMake scripts and therefore does not require any user input (these libraries are supplied with the ProSHADE code and will be installed locally by the ProSHADE CMake installation). Please note that these dependencies do have their own licences (the Mozilla Public License for *Gemmi* and the GPL licence for *SOFT2.0*) and therefore this may limit the ProSHADE usage for some users beyond the ProSHADE copyright and licence itself.

## Installing on Windows

As mentioned above, ProSHADE currently only supports Windows10 64-bit systems and cannot be simply installed on other Windows systems. In order to install ProSHADE on a Windows10 64-bit machine, the user is required to firstly have installed some basic pre-requisities. 

### Installing CMake

CMake can be installed on Windows using the 64-bit MSI installer available from https://cmake.org/download . During the installation, please make sure that the option to *Add CMake to the system PATH* is selected (it does not matter to ProSHADE if it is for all users or just for the current user). 

### Installing git

Git can be installed on Windows by downloading the 64-bit Windows Setup installer from https://git-scm.com/download/win . The installer asks for many options, the only imprtant one for ProSHADE installation is that in the section "Adjusting you PATH environment" it is required that the option *Use Git from Git Bash only* is **NOT** selected. This makes sure that the git executable is in the system PATH.

### Installing Build Tools for Visual Studio

Sadly, the Authors are not aware of any simple way of installing the Microsoft C and C++ compilers and linker controlling tool - **cl.exe** except for installing the full Visual Studio or the Build Tools for Visual Studio. This will require well over 6GB of space on your hard-drive and the download is well over 1.5GB. Nonetheless, it is the main Windows compiler and linker and therefore ProSHADE cannot be installed on Windows without it. 

To install the Build Tools for Visual Studio, please download the installer from Microsoft at https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019 and in the Workload selection screen select the *C++ Build Tools* option. The rest of the installtion should be automatic.

### Installing ProSHADE

Once all of the above dependencies are installed, the ProSHADE python module can now be installed using the pip installation as described in the [Installing using pip ](#installing-using-pip) section. Should the user require installation from the Command Prompt, they will need to open the *Developer Command Prompt for VS 2019* (or the appropriate version the MS Visual Studio they have installed) and type the following commands (replacing the \path\to\proshade with the appropriate path on their machine to the location where they want ProSHADE codes to be stored). Please note that you may need to run the command prompt as administrator in order to be able to install into the system folders (i.e. C:\Program Files). Also, the same CMake options apply as discussed in section [CMake options](#cmake-options):

```
    cd \path\to\proshade
    git clone https://github.com/michaltykac/proshade
    mkdir build
    cd .\build
    cmake ..\proshade\proshade
    cmake --build . --config Release
    cmake --install .
```
 
 ### Setting ProSHADE PATH
 
 Finally, ProSHADE now needs to be able to locate the dependency libraries before it can be run on Windows. The simplest way of allowing for this is the add the ProSHADE libraries folder into the system PATH. This can be done by opening the *Control Panel* and selecting the *System and Security* option. In the new window, please select the *System* option and in the next window click the *Advanced system settings* option on the right-hand side panel. In the next window, please click on the *Environment Variables...* button, which will open the  penultimate window. In here, in the *System variables* section, please click on the variable named *Path* and then click on the *Edit...* button. This opens the last window, where the *New* button needs to be clicked, immediately followed by clicking the *Browse...* button can be clicked. In the file selector screen, please click to the \path\to\proshade location used in the previous section and then select the following folders: proshade\proshade\winLibs\x64\DLLs and then click on the *OK* button on all open windows which have one.

Once the path is set, you can use ProSHADE from any Command Prompt window (not only the Developer Command Prompt used before), although you will have to close and re-open all currently open command prompt windows if you want to use ProSHADE in them.
 
 ## Installing using CMake on Unix
 
 CMake is the default ProSHADE installation tool and if the binary or the library is needed, then it is the only installation option. The python module can also be build using CMake, but it will be installed only locally and all python scripts will need to add the installation location to their PATH. Alternatively, if the python module is what the user is after, then it can be installed globally using pip - please see the [Installation using pip](#installation-using-pip ) section for more details.
 
 In order to install ProSHADE, first please check that all the [Standard System Dependencies](#standard-system-dependencies) are installed, preferably using a package management system such as *apt*, *yum*, *zypper*, *homebrew*, *etc.*. 
 
 Next, please navigate to any folder to which you would like to write the install files; some find it useful to create a ```build``` folder in the ProSHADE folder in order to keep the install files in the same location as the source codes. Then, issue the following set of commands, changing the ```\path\to\ProSHADE``` to the correct path on your system and adding any required [CMake options](#cmake-options) to the first command. Please note that ```sudo``` may be required for the ```make install``` command if you are installing into the system folders.

```
 cmake \path\to\ProSHADE
 make
 make install
```
 
 ### CMake options
 
  **-DINSTALL_LOCALLY=ON** or **OFF**
    - This option is used to decide whether all the installed ProSHADE components are installed in the local source directory (value **ON** ) or whether they are instead installed in the system folders (value **OFF** ) as determined by CMake. This option applies to the binary, the C++ library and the headers as well. Please note that the python module will be installed locally; if it is to be installed globally, please use the pip installation described in the section [Installation using pip](#installation-using-pip ).
 
  **-DINSTALL_BIN_DIR=/path**
  - This option is used to manually specify the folder to which the ProSHADE binary shold be installed into.
 
  **-DINSTALL_LIB_DIR=/path**
  - This option is used to manually specify the folder to which the ProSHADE C++ library should be installed into.
 
  **-DINSTALL_INC_DIR=/path**
  - This option is used to specify the folder to which the ProSHADE header files required by the library should be installed into.
 
  **-DCUSTOM_FFTW3_LIB_PATH=/path**
  - This option is used to supply the path to the libfftw3.a/so/dylib in the case where ProSHADE CMake installation fails to detect the FFTW3 dependency. This is typically the case when FFTW3 is installed outside of the standard FFTW3 installation locations.
 
  **-CUSTOM_FFTW3_INC_PATH=/path**
  - This option is used to supply the path to the fftw3.h file in the case where ProSHADE CMake installation fails to detect the FFTW3 dependency. This is typically the case when FFTW3 is installed outside of the standard FFTW3 installation locations.
 
  **-DCUSTOM_LAPACK_LIB_PATH=/path**
  - This option is used to supply the path to the liblapack.a/so/dylib in the case where ProSHADE CMake installation fails to detect the LAPACK dependency. This is typically the case when the LAPACK is installed outside of the standard LAPACK installation locations.
 
  **-DBUILD_PYTHON=TRUE** or **FALSE**
  - This option controls whether python modules should be build or not. If you have installed ProSHADE python modules using pip or if you are not interested in using the python modules, you may set this option to FALSE, otherwise the python module will be built for the currently used python.
 
 ### Uninstall using CMake
 
  To remove the installed ProSHADE components, the command ```make remove``` needs to be issued to the makefile originally created by the CMake call. Please note that ```sudo``` may need to be used if the installation was done into the system folders and your current user does not have admin rights.
  
 ## Installing using pip 
 
 The ProSHADE python module is also available (as a source distribution) on the PyPi repository. Therefore, the ProSHADE python module can be installed by simply issuing the following command; **however, this assumes that all the system dependencies as discussed in the [Standard System Dependencies](#standard-system-dependencies) section are already installed.** If any of them is missing, then a cryptic error message will ensue - consider yourself warned.
 
 ```
    pip install proshade
 ```
 
 Alternatively, the module can be build and installed using pip directly from the ProSHADE GitHub repository ( https://github.com/michaltykac/proshade ) using the following command. This approach has the advantage that it takes the most current stable version, rather than being dependent on the authors not forgetting to update the PyPi repository.
 
 ```
    pip install git+https://github.com/michaltykac/proshade 
 ```
  
  Again, please note that the pip installation only wraps around the CMake installation and that CMake is still being run by pip in the background. Therefore, the same system dependencies are required. Moreover, if any of the system dependencies is missing or cannot be found, then a bit more cryptic error message will be printed by pip.
  
  ### Uninstalling pip installed module
  
  Should the user require to uninstall the python module and all associated data after they were installed globally using pip, the following standard pip command can achieve this task irrespective as to how exactly the proshade module was installed:
  
  ```
    python -m pip uninstall proshade
 ```
  
 # Input PDB files
  
  There are several caveats to inputting PDB files; most of these have to do with the fact that PDB files encode much more information than ProSHADE is intended to use. Therefore, ProSHADE is by default set to disregard information it does not need; however, if the user so requires, the information may be used, albeit it may pose some unexpected problems.
  
  ## Spacegroups
  
  By default, ProSHADE will ignore the PDB file encoded spacegroup and will instead force the P1 spacegroup onto the input files. The reason for this behaviour is that when computing the theoretical density map, some spacegroups will cause density from other cells to be added as well (*e.g.* P21 21 21). Since ProSHADE is intended to use the structure shape irrespective of the experimental method (*i.e.* irrespective of crystal packaging), having density from other cells would cause ProSHADE to perceive differences where the structures could be identical except for the spacegroup. To force ProSHADE to make use of the spacegroup, please supply the ```-u``` command line option.
  
  ## Waters
  
  By default, ProSHADE will remove all water molecules from any input PDB files. The reason is similar to above, as ProSHADE is intended to compare protein shapes and as waters are in most cases not an integral part of the protein, this behaviour is attempting to avoid situations where two identical structures with one having hundreds of waters and one not would be perceived by ProSHADE as significantly different. Should the user require the water molecules to be used by ProSHADE, please supply the ```-w``` command line option.
  
  ## Models
  
  There are examples of both, PDB files containing multiple models of the same structure (with minor differences,  *e.g.* trajectory files) and PDB files which have their chains (or collections of chains) separated into different models. Given this state of affairs, ProSHADE will by default use only the first model of each input PDB file and will print a warning message (which can be supressed by setting verbosity below 0) for each file it reads which has more than one model. Should the user want to use all available models for the input PDB files, please supply ProSHADE with the ```-x``` command line option.
 
 # Using the ProSHADE binary

The ProSHADE tool was developed in a modular fashion and the usage slightly changes depending on the functionality that is required. Nonetheless, care has been taken to make sure that identical or closely related features are controlled by the same command line arguments in all cases. Moreover, the GNU command-line options standard have been adhered to (through the ```getOpts``` library) and therefore the users familiar with other command-line tools should find the entering of command line arguments simple. The following subsections relate to examples of using different functionalities; for a full list of command line options, please use the **--help** command line option of the ProSHADE binary.

## Symmetry Detection

In order to detect symmetry in either a co-ordinate input file or in a map input file, the ProSHADE executable needs to be supplied with the option **-S** or **--symmetry** and it will also require a single input file to be supplied using the **-f** option. These two options are the only mandatory options, although there are many optional values that the user can supply to supersede the default values and therefore modify the operation fo the ProSHADE executable to fit their purpose.

One particular option regarding the symmetry detection mode should be noted; the **--sym** (or **-u**) option, which allows the user to state which symmetry they believe to exist in the structure. The allowed values for this command line argument are "Cx", "Dx", "T", "O" and "I", where the *x* should be an integer number specifying the fold of the requested symmetry. When this option is used, it removes the default behaviour of returning the "best" detected symmetry and instead the symmetry requested by the user is returned, if it can be found in the structure.

Another noteworthy option is the **--center** or **-c** option, which  tells ProSHADE **NOT** to center the internal map representation over the centre of density before running any processing of the map (default is centering and adding this option will turn centering off). This may be important as ProSHADE detects symmetries over the centre of the co-ordinates and therefore a non-centered map (map which does not have the centre of mass at the centre of box) will be found to have no symmetries even if these are present, just not over the co-ordinate/box centre.

It is also worth noting that there are several extra functionalities available for the symmetry detection mode when accessed programmatically (**i.e.** either through the dynamic C++ library or through the Python language module). These extra functionalities include direct access to a vector/list of all detected cyclic symmetries, list/vector of all other symmetry type detections (meaning a list of all detected dihedral, tetrahedral, ... symmetries and the cyclic axes forming them) and also the ability to compute all point group elements for any point group formed by a combination of ProSHADE detected cyclic point groups. For more details on these functinoalities, the users are invited to consult the *advancedAccess_symmetry.cpp/py* example files in the **examples** folder.

To demonstrate how the tool can be run and the standard output for the symmetry mode of operation, the current version of the ProSHADE executable was used to detect the symmetry of a density map of the bacteriophage T4 portal protein with the PDB accession code 3JA7 (EMDB accession code 6324), which has the *C12* symmetry. The visualisation of the structure is shown in the following figure, while the output of the ProSHADE tool follows:

![T4 Portal Protein](https://github.com/michaltykac/proshade/blob/experimental/proshade/documentation/ProSHADE_3JA7.jpg)

```
 $: ./proshade -S -f ./emd_6324.map -r 8 --sym C12
 ProSHADE 0.7.5.3 (FEB 2021):
 ============================

  ... Starting to read the structure: ./emd_6324.map
  ... Map inversion (mirror image) not requested.
  ... Map normalisation not requested.
  ... Masking not requested.
  ... Centering map onto its COM.
  ... Adding extra 10 angstroms.
  ... Phase information retained in the data.
  ... Starting sphere mapping procedure.
  ... Preparing spherical harmonics environment.
  ... Starting spherical harmonics decomposition.
  ... Starting self-rotation function computation.
  ... Starting detection of cyclic point group C12

 Detected C symmetry with fold 12 .
   Fold       X           Y          Z           Angle        Height
    +12     +0.00000   -0.00000   +1.00000     +0.52360      +0.94620

 However, since the selection of the recommended symmetry needs improvement, here is a list of all detected C symmetries:
   Fold       X           Y          Z           Angle        Height
    +12     +0.00000   -0.00000   +1.00000     +0.52360      +0.94620

 Also, for the same reason, here is a list of all detected D symmetries:

 ======================
 ProSHADE run complete.
 Time taken: 14 seconds.
 ======================
```

## Shape similarity distances

 The distances computation mode is signalled to the ProSHADE executable by the command line argument **-D** or **--distances**. This mode requires two or more structures to be supplied using the **-f** command line option. At least two structures are mandatory for the ProSHADE tool to proceed. Moreover, the resolution of the structures to which the comparison should be done needs to be supplied using the **-r** option. This resolution does not need to be the real resolution to which the structure(s) were resolved, but rather reflects the amount of details which should be taken into accout when comparing shapes. Therefore, higher resolution comparison will focus more on details of the shapes, while lower resolution comparison will focus more on the overall shape ignoring the minor details. Please note that the results are calculated only for the first structure against all the remaining structures, **not** for all against all distance matrix.

 There are a number of useful options for the shape distances computation, please consult the **--help** dialogue for their complete listing.

 To demonstrate the output of the ProSHADE software tool for computing distances between structure shapes, the distances between the BALBES protein domains 1BFO_A_dom_1 and 1H8N_A_dom_1 (which have similar shape) and the 3IGU_A_dom_1 domain which has a different shape, as can be seen from the following figure - the first two domains are both in cluster a), while the last domain is from the cluster b). The output of the ProSHADE software tool is then shown below:

![BALBES domain used for similarity detection](https://github.com/michaltykac/proshade/blob/experimental/proshade/documentation/ProSHADE_dists.png)

```
  $: ./proshade -D -f ./1BFO_A_dom_1.pdb -f ./1H8N_A_dom_1.pdb -f ./3IGU_A_dom_1.pdb -r 6
  ProSHADE 0.7.5.3 (FEB 2021):
  ============================

   ... Starting to read the structure: ./1BFO_A_dom_1.pdb
   ... Map inversion (mirror image) not requested.
   ... Map normalisation not requested.
   ... Masking not requested.
   ... Map centering not requested.
   ... Adding extra 10 angstroms.
   ... Phase information retained in the data.
   ... Starting sphere mapping procedure.
   ... Preparing spherical harmonics environment.
   ... Starting spherical harmonics decomposition.
   ... Starting to read the structure: ./1H8N_A_dom_1.pdb
   ... Map inversion (mirror image) not requested.
   ... Map normalisation not requested.
   ... Masking not requested.
   ... Map centering not requested.
   ... Adding extra 10 angstroms.
   ... Phase information retained in the data.
   ... Starting sphere mapping procedure.
   ... Preparing spherical harmonics environment.
   ... Starting spherical harmonics decomposition.
   ... Starting energy levels distance computation.
   ... Starting trace sigma distance computation.
   ... Starting rotation function distance computation.
  Distances between ./1BFO_A_dom_1.pdb and ./1H8N_A_dom_1.pdb
  Energy levels distance    : 0.895306
  Trace sigma distance      : 0.960468
  Rotation function distance: 0.756167
   ... Starting to read the structure: ./3IGU_A_dom_1.pdb
   ... Map inversion (mirror image) not requested.
   ... Map normalisation not requested.
   ... Masking not requested.
   ... Map centering not requested.
   ... Adding extra 10 angstroms.
   ... Phase information retained in the data.
   ... Starting sphere mapping procedure.
   ... Preparing spherical harmonics environment.
   ... Starting spherical harmonics decomposition.
   ... Starting energy levels distance computation.
   ... Starting trace sigma distance computation.
   ... Starting rotation function distance computation.
  Distances between ./1BFO_A_dom_1.pdb and ./3IGU_A_dom_1.pdb
  Energy levels distance    : 0.559041
  Trace sigma distance      : 0.736592
  Rotation function distance: 0.452545

  ======================
  ProSHADE run complete.
  Time taken: 4 seconds.
  ======================
```
 
 ## Re-boxing structures
 
 Another useful feature of the ProSHADE tool is re-boxing of macromolecular density maps. This mode is signalled to the ProSHADE tool by the command line option **-M** or **--mapManip** followed by the **-R** option to specify that the required map manipulations include re-boxing. Furthermore, a single map structure file needs to be supplied after the **-f** flag. In this mode, ProSHADE will attempt to find a suitable map mask by blurring the map (increasing the overall B-factors). Consequently, it will use the map boundaries to create a new, hopefully smaller, box to which the appropriate part of the map will be copied.
 
 This ProSHADE functionality can be combinaed with other map manipulations, which include the map invertion (signalled by the **--invertMap** option and useful for cases where map reconstruction software mistakes the hands of the structure), the map normalisation (signalled by the **--normalise** option, which makes sure the map mean is 0 and standard deviation is 1), centering of centre of mass to the centre of co-ordinates (using the **--center** or **-c** option) or the phase removal (creating Patterson maps using the **--noPhase** or **-p** options).
 
 The location and filename of where this new map should be saved can be specified using the **--reBoxedFilename** (or **-g** ) command line option followed by the filename.
 
 The following snippet shows the output of the ProSHADE tool when used to re-box the TubZ-Bt four-stranded filament structure (EMDB accession code 5762 and PDB accession code 3J4S), where the original volume can be decreased to 46.9% of the original structure volume and thus any linear processing of such structure will be more than twice faster and the original. The original TubZ-Bt four-stranded filament structure box is shown in the following figure as semi-transparent grey, while the new box is shown in non-transparent yellow.
 
![Re-boxing result for TubZ-Bt four-stranded filament](https://github.com/michaltykac/proshade/blob/experimental/proshade/documentation/ProSHADE_rebox.png)
 
```
$ ./proshade -RMf ./emd_5762.map.gz
ProSHADE 0.7.5.3 (FEB 2021):
============================

 ... Starting to read the structure: ./emd_5762.map.gz
 ... Map inversion (mirror image) not requested.
 ... Map normalisation not requested.
 ... Computing mask.
 ... Map centering not requested.
 ... Adding extra 10 angstroms.
 ... Phase information retained in the data.
 ... Finding new boundaries.
 ... Creating new structure according to the new  bounds.
 ... Saving the re-boxed map into reBoxed_0.map

======================
ProSHADE run complete.
Time taken: 9 seconds.
======================
```

## Optimal rotation and translation

 In order to find the rotation and translation which optimally overlays (or fits) one structure into another, be them co-ordinate files or maps (and any combination thereof), the ProSHADE tool can be used in the Overlay mode. This is signalled to the ProSHADE tool binary by the command line option **--strOverlay** or **-O** and this mode requires exactly two structure files to be supplied using the **-f** command line options. The order of the two files does matter, as the second file will always be moved to match the first structure, which will remain static.
 
 Due to the requirement for the second stucture movement and rotation, it is worth noting that the structure may need to be re-sampled and/or moved to the same viewing position as the first structure. This is done so that only the internal representation is modified, but never the input file. However, when the overlay structure is outputted (a non-default name can be specified by the **--overlayFile** command-line option) the header of this output file may differ from the second structure header. Furthermore, if there is no extra space around the structure, movement and rotation may move pieces of the structure through the box boundaries to the other side of the box. To avoid this, please use the **--extraSpace** option to add some extra space around the structure.
 
 As an example of the Overlay mode, we will be matching a single PDB structure (1BFO_A_dom_1 from the BALBES database, original structure code 1BFO) shown in part a) of the following figure to another PDB structure, this time the 1H8N_A_dom_1 structure from the BALBES database, shown in part b) of the same figure. Please note that ProSHADE can fit any allowed input (map or co-ordinates) to any allowed input, it is just this example which uses two PDB files. Part c) of the figure then shows the match obtained by the internal map representation of the moving structure (1H8N_A_dom_1) after rotation and translation with the static structure (1BFO_A_dom_1). Finally, part d) then shows the original static structure (1BFO_A_dom_1) in brown and the rotated and translated version of the moving structure (1H8N_A_dom_1) in blue. Please note that the optimal rotation matrix and translation vectors are written into the output, but are better accessed programatically (see the following sections) if you are interested in using these further.
 
 Regarding the output, ProSHADE outputs the following information which should be sufficient to apply the correct rotation and translation operations to obtain the optimal overlay:
 
 - **1) The rotation centre to origin translation vector** - This is the vector that needs to be applied to co-ordinates in order to move the ProSHADE computed centre of rotation to the origin. This result can also be understood as the negative value of the position of the centre of rotation (i.e. -rotCen = the centre of rotation position). Please note that this value is in the "real world" (or "visualisation co-ordinates") space, but may not necessarily be identical to the centre of the box of any input map (this is because ProSHADE may apply some modifications to the map during its processing). 
 
 - **2) The rotation matrix about origin** - This is a rotation matrix that will rotate the moving structure (be it map or co-ordinates) so that it will have the same orientation as the static structure. The rotation matrix should be applied over the position given by output **1)**, meaning that for co-ordinates, they should be moved by the vector **1)** to the origin, then have this rotation matrix applied and then be moved back by **- 1)**. For maps, however, the rotation should be applied differently; if position **1)** is the centre of box, they should be rotated about the centre of the box using the rotation matrix and if position **1)** is not the centre of the box, they should be translated within the box by the difference of the centre of the box and the position **1)**. 
 
 - **3) The rotation centre to overlay translation vector** - This vector assumes the structure has been rotated about the position given by **- 1)** by a rotation operation described by **2)**, meaning that if co-ordinates were moved to origin for rotation, the opposite translation to the one used to move them to origin should be applied after the rotation. If this assumption holds, then this vector (*i.e.* **3)** ) is the translation that will optimally overlay the rotated structure with the static structure (*i.e.* the structure inputted first). Again, this vector is in the "real world" (or "visualisation co-ordinates") space. Please note that for maps, this translation may need to move the density outside of the box. Therefore, the box should be moved first by changing the indexing starts to minimise this translation and then the density should be moved inside the box by the remainder of the translation.
 
 **Warning**: In order to allow visualisation of the results of ProSHADE overlap task, the translation is computed in the *real world* or *visualisation co-ordinates* space; this, however, has the implication that if the moving structure is a density, then the densty box may need to be moved in such a way that it contains the static structure's position. Therefore, the **translation computed as described above should not be applied to the density in box, but rather to the box itself** (or possibly if such box translation cannot be done perfectly, then the remainder of the imperfect box translation can be done within the box).
 
 ![ProSHADE Overlay results for 2A2Q_T_dom_2.pdb](https://github.com/michaltykac/proshade/blob/experimental/proshade/documentation/ProSHADE_overlay.jpg)
 
```
 $ ./proshade -O -f ./1BFO_A_dom_1.pdb -f ./1H8N_A_dom_1.pdb -r 4 -kjc
 ProSHADE 0.7.5.3 (FEB 2021):
 ============================

  ... Starting to read the structure: ./1BFO_A_dom_1.pdb
  ... Starting to read the structure: ./1H8N_A_dom_1.pdb
  ... Map inversion (mirror image) not requested.
  ... Map normalisation not requested.
  ... Masking not requested.
  ... Centering map onto its COM.
  ... Adding extra 10 angstroms.
  ... Centering map onto its COM.
  ... Phase information removed from the data.
  ... Map inversion (mirror image) not requested.
  ... Map normalisation not requested.
  ... Masking not requested.
  ... Centering map onto its COM.
  ... Adding extra 10 angstroms.
  ... Centering map onto its COM.
  ... Phase information removed from the data.
  ... Starting sphere mapping procedure.
  ... Preparing spherical harmonics environment.
  ... Starting sphere mapping procedure.
  ... Preparing spherical harmonics environment.
  ... Starting spherical harmonics decomposition.
  ... Starting spherical harmonics decomposition.
  ... Starting rotation function computation.
  ... Starting to read the structure: ./1BFO_A_dom_1.pdb
  ... Starting to read the structure: ./1H8N_A_dom_1.pdb
  ... Map inversion (mirror image) not requested.
  ... Map normalisation not requested.
  ... Masking not requested.
  ... Centering map onto its COM.
  ... Adding extra 10 angstroms.
  ... Phase information retained in the data.
  ... Map inversion (mirror image) not requested.
  ... Map normalisation not requested.
  ... Masking not requested.
  ... Centering map onto its COM.
  ... Adding extra 10 angstroms.
  ... Phase information retained in the data.
  ... Starting sphere mapping procedure.
  ... Preparing spherical harmonics environment.
  ... Starting spherical harmonics decomposition.
  ... Starting translation function computation.

 The rotation centre to origin translation vector is:  -17.5     -21     -24
 The rotation matrix about origin is                 : -0.872     -0.0785     +0.483
                                                     : -0.191     -0.854     -0.483
                                                     : +0.451     -0.514     +0.73
 The rotation centre to overlay translation vector is: +4     +4     -4

 ======================
 ProSHADE run complete.
 Time taken: 4 seconds.
 ======================
```
# Using the ProSHADE library

 ProSHADE allows more programmatic access to its functionality through a C++ dynamic library, which is compiled at the same time as the binary is made. This library can be linked to any C++ project to allow direct access to the ProSHADE objects, functions and results. This section discusses how the ProSHADE library can be linked against and how the basic objects can be accessed.

## Linking against the ProSHADE library

The ProSHADE library can be linked as any other C++ library, that is by using the **-lproshade** option when calling the compiler (tested on *clang* and *g++* ) and including the header file (**ProSHADE.hpp**). However, as the **ProSHADE.hpp** header file includes header files from some of the dependencies, any C++ project linking against the ProSHADE library will need to provide these pedendencies paths to the compiler. Moreover, if the ProSHADE library was not installed in the system folders (which are by default in the compiler paths), any project linking against the ProSHADE library will also need to provide the path to the libproshade.a/so/dylib library file and the RPATH to the same location. The following list states all the paths that may be required for a successfull compilation against the ProSHADE library:

- **-I/path/to/proshade/extern/soft-2.0/include** This path is required for the SOFT2.0 dependency header file to be located correctly (it is confusingly called *fftw_wrapper.h*).
- **-I/path/to/proshade/extern/gemmi/include** This path is required for the Gemi dependency header file to be located correctly. Note that this folder will not exist unless complete ProSHADE installation make was run at least once.
 - **-L/path/to/proshade/install/lib** This is the path the where libproshade.a/so/dylib is installed. If ProSHADE was installed using the CMake -DINSTALL_LOCALLY=TRUE option, then this path may already be available to the compiler and it may not be needed.
 - **-Wl,-rpath,/path/to/proshade/install/lib** or **-rpath /path/to/proshade/install/lib** This compiler option will be required if the proshade library was not installed into a system folder which is already included in the project's RPATH.
 
Overall, a compilation of a C++ project linking against the ProSHADE library may look like the following code:

```
$ clang ./proshadeBinary.cpp -I/path/to/proshade/extern/soft-2.0/include \
                             -I/path/to/proshade/extern/gemmi/include \
                             -L/path/to/proshade/install/lib \
                             -std=c++11 -lproshade -lc++ -lz \
                             -rpath /path/to/proshade/install/lib \
                             -o ./proshadeBinary
```

or

```
$ g++ ./proshadeProject.cpp -I/path/to/proshade/extern/soft-2.0/include \
                            -I/path/to/proshade/extern/gemmi/include \
                            -L/path/to/proshade/install/lib \
                            -lproshade -lz -Wl,-rpath,/path/to/proshade/install/lib \
                            -o ./proshadeProject
```

## Examples of ProSHADE library usage

There are several examples of C++ code which makes use of the ProSHADE dynamic library to compute the standard ProSHADE functionalities and access the results programmatically (*i.e.* without the need for parsing any log files). 

### Simple access

The examples are avaialbe in the **/path/to/proshade/example/libproshade** folder and are divided into two categories of four examples. The source files with names starting with *simpleAccess_...* provide a "*black box*" experience similar to using ProSHADE binary. The user firstly creates a **ProSHADE_settings** object, which provides all the variables that can be set in order to drive which ProSHADE functionality is required and how it should be done. Next, the user needs to create the **ProSHADE_run** object, whose constructor takes the already created and filled **ProSHADE_setings** object as its only argument. This constructor will then proceed to compute all required information according to the settings object and return when complete. While the computation is being done, the execution is with the ProSHADE library and any C++ project using this mode will be waiting for the ProSHADE library to finish. Once the computation is complete, the execution will be returned to the calling C++ project and the results will be accessible through public functions of the **ProSHADE_run** object. The following code shows a very simple example of how ProSHADE can be run in this mode, but for more specific examples the users should review the *simpleAccess_...* example files.

```
#include "ProSHADE.hpp"

int main ( int argc, char **argv )
{
    //================================================ Create the settings object
    ProSHADE_Task task                                = Distances;
    ProSHADE_settings* settings                       = new ProSHADE_settings ( task );

    //================================================ Set the settings object up
    settings->setResolution                           ( 10.0 );
    settings->addStructure                            ( "./str1.pdb" );
    settings->addStructure                            ( "./str2.pdb" );

    //================================================ Run ProSHADE. This may take some time, depending on what computations are required.
    ProSHADE_run* runProshade                         = new ProSHADE_run ( settings );

    //================================================ Access the results
    std::vector< proshade_double > energyDistances    = runProshade->getEnergyLevelsVector     ( );
    std::vector< proshade_double > traceDistances     = runProshade->getTraceSigmaVector       ( );
    std::vector< proshade_double > rotFunDistances    = runProshade->getRotationFunctionVector ( );

    //================================================ Release the memory
    delete runProshade;
    delete settings;

    //================================================ Done
    return EXIT_SUCCESS;
}
```

### Advanced access

The second set of examples of usage of the ProSHADE library are the source files with names starting with *advancedAccess_...*. These files provide examples of how individual ProSHADE functions can be arranged to provide the results of the main ProSHADE functionalities. Using the ProSHADE tool in the manner shown in these example codes gives the user more control over the execution and it also allows the user to modify the behaviour directly. On the other hand, using ProSHADE in this way requires a bit more understanding than the simple "*black box*" approach and the DOxygen documentation supplied with the code should be helpful for all who wish to use ProSHADE this way. Interested users are advised to review all the *advancedAccess_...* source files as well as the following basic example code.

```
#include "ProSHADE.hpp"

int main ( int argc, char **argv )
{
    //================================================ Create the settings object
    ProSHADE_Task task                                = Symmetry;
    ProSHADE_settings* settings                       = new ProSHADE_settings ( task );

    //================================================ Create the structure objects
    ProSHADE_internal_data::ProSHADE_data* simpleSym  = new ProSHADE_internal_data::ProSHADE_data ( settings );

    //================================================ Read in the structures
    simpleSym->readInStructure                        ( "./emd_6324.map", 0, settings );

    //================================================ Process internal map
    simpleSym->processInternalMap                     ( settings );

    //================================================ Map to spheres
    simpleSym->mapToSpheres                           ( settings );

    //================================================ Compute spherical harmonics decompostion
    simpleSym->computeSphericalHarmonics              ( settings );

    //================================================ Compute self-rotation function
    simpleSym->computeRotationFunction                ( settings );

    //================================================ Detect the recommended symmetry
    std::vector< proshade_double* > symAxes;
    std::vector< std::vector< proshade_double > > allCsFromSettings;
    simpleSym->detectSymmetryInStructure              ( settings, &symAxes, &allCsFromSettings );
    std::string symmetryType                          = simpleSym->getRecommendedSymmetryType ( settings );
    proshade_unsign symmetryFold                      = simpleSym->getRecommendedSymmetryFold ( settings );

    //================================================ Write out the symmetry detection results
    std::cout << "Detected symmetry: " << symmetryType << "-" << symmetryFold << " with axes:" << std::endl;
    for ( proshade_unsign axIt = 0; axIt < static_cast<proshade_unsign> ( symAxes.size() ); axIt++ )
    {
       std::cout << "Symmetry axis number " << axIt << std::endl;
       std::cout << " ... Fold             " << symAxes.at(axIt)[0] << std::endl;
       std::cout << " ... XYZ:             " << symAxes.at(axIt)[1] << " ; " << symAxes.at(axIt)[2] << " ; " << symAxes.at(axIt)[3] << std::endl;
       std::cout << " ... Angle (radians): " << symAxes.at(axIt)[4] << std::endl;
       std::cout << " ... Axis peak:       " << symAxes.at(axIt)[5] << std::endl;
    }
    
    //================================================ Find all C axes
    std::vector < std::vector< proshade_double > > allCs = settings->allDetectedCAxes;
    std::cout << "Found total of " << allCs.size() << " cyclic symmetry axes." << std::endl;
    
    //================================================ Get group elements for the first axis (or any other axis)
    std::vector< proshade_unsign > axesList;
    axesList.emplace_back ( 0 );
    std::vector<std::vector< proshade_double > > groupElementsGrp0 = simpleSym->getAllGroupElements ( settings, axesList, "C" );
    std::cout << "Group 0 has fold of " << allCs.at(0)[0] << " and ProShade computed " << groupElementsGrp0.size() << " group element (including the identity one), the second being the rotation matrix:" << std::endl;
    std::cout << groupElementsGrp0.at(1).at(0) << " x " << groupElementsGrp0.at(1).at(1) << " x " << groupElementsGrp0.at(1).at(2) << std::endl;
    std::cout << groupElementsGrp0.at(1).at(3) << " x " << groupElementsGrp0.at(1).at(4) << " x " << groupElementsGrp0.at(1).at(5) << std::endl;
    std::cout << groupElementsGrp0.at(1).at(6) << " x " << groupElementsGrp0.at(1).at(7) << " x " << groupElementsGrp0.at(1).at(8) << std::endl;

    //================================================ Release the memory
    delete simpleSym;
    delete settings;

    //================================================ Done
    return EXIT_SUCCESS;
}
```

# Using the Python module

ProSHADE also provides a module which allows the same programmatical access to the ProSHADE tool as the dynamic C++ library. This module is produced using the PyBind11 tool ( https://github.com/pybind/pybind11 ) and supports the numpy array data types as both input and output of the C++ function calls.

## Python module examples

Similarly to the ProSHADE dynamic library, the python code examples are available in the  **/path/to/proshade/examples/python** folder. They are, again similarly to the dynamic C++ library examples, divided into different categories.

### Simple access

Similarly to the dynamic library case, there are three types of examples available for the python modules. The first set of examples (files named *simpleAccess_...* ) show the *black box* experience, which is similar to using ProSHADE binary. The user needs to create the **ProSHADE_settings** object and can then supply it with all the settings values which will then drive the ProSHADE computations. The same settings are available in the python modules as in the ProSHADE library; the example code below shows only a small selection of these (for full selection, please see the example files). Next, the user creates the **ProSHADE_run** object, constructor of which takes the settings object as its only argument and then proceeds to do all computations required by the settings in the settings object. The computations are done on this one line and if they take time, the execution of the script will be halted until ProSHADE is done computing. Once completed, the results can be retrieved from the **ProSHADE_run** object using the public accessor functions; the example code below shows how the symmetry functionality can be run and results retrieved - for examples of other functionalities and for more details, please see the *simpleAccess_...* example files.

```
""" Import numpy """
import numpy

""" Import ProSHADE (assumes installation through pip) """
import proshade

""" Create the settings object """
ps                                    = proshade.ProSHADE_settings ( )

""" Set up the run """
ps.task                               = proshade.Symmetry
ps.verbose                            = -1;                      
ps.setResolution                      ( 8.0 );                   
ps.addStructure                       ( "/path/to/emd_5762.map" );

""" Run ProSHADE """
rn                                    = proshade.ProSHADE_run ( ps )

""" Retrieve results """
symType                               = rn.getSymmetryType ( )
symFold                               = rn.getSymmetryFold ( )
symAxis                               = rn.getSymmetryAxis ( 0 )
allCs                                 = rn.getAllCSyms     ( )

""" Print results (part I) """
print                                 ( "Found a total of " + str ( len ( allCs ) ) + " cyclic symmetries." )

""" Print results (part II) """
print                                 ( "Detected symmetry " + str( symType ) + "-" + str( symFold ) + " with axes: " )
print                                 ( "Fold      x         y         z       Angle     Height" )
print                                 ( "  %s    %+1.3f    %+1.3f    %+1.3f    %+1.3f    %+1.4f" % ( float ( symAxis[0] ),
                                                                                                     float ( symAxis[1] ),
                                                                                                     float ( symAxis[2] ),
                                                                                                     float ( symAxis[3] ),
                                                                                                     float ( symAxis[4] ),
                                                                                                     float ( symAxis[5] ) ) )
                                                                                                     
""" Release memory """
del rn
del ps
```

### Advanced access

If the user needs more control over the ProSHADE exectution, or simply wants any behaviour not simply available by variables in the settings object, then there are the *advancedAccess_...* examples. These showcase the ability to call internal ProSHADE functions and by ordering them correctly, achieving the requested functionality. This usage of the python modules does required a better understanding the of the ProSHADE tool and the functions it implements. This documentation is a good starting point as to which functions are available and the **ProSHADE_tasks.cpp** source file shows how the internal functions can be arranged to achieve the standard ProSHADE tasks. Please be aware that most of the functions do require that a pre-requisite function is run before it, but not all of these pre-requisites have their own warning or error messages. Therefore, if any code causes segmentation error (which usually kills the python interpreter), it is likely that you forgot to call some pre-requisite function.

The following code is an example of how this approach to the ProSHADE python module can be used to compute the shape-wise distances between two structures. After importing the required modules, the code creates the setings object and sets the basic settings (for a full list of settings, please see the example files). It then proceeds to create the **ProSHADE_data** objects for each structure, reads in the structures from files on the hard-drive (PDB and MAP formats are supported, the mmCIF should work as well). Next, the code processes the data - this is where map centering, masking, normalisation, axis inversion, etc. happens - onto an internal ProSHADE data representation. This representation can then be mapped onto a set of concentric spheres, which can in turn have their spherical harmonics decomposition computed. Once this is done, the shape distances can be computed using the three functions shown.

```
""" Import the system modules """
import sys
import numpy

""" Import ProSHADE """
sys.path.append                                       ( "/path/to/proshade/install/pythonModule" ) # only needed if ProSHADE was installed locally
import proshade

""" Create the ProSHADE_settings object """
pSet                                                  = proshade.ProSHADE_settings ()

""" Set the settings for Distances detection """
pSet.task                                             = proshade.Distances
pSet.verbose                                          = -1
pSet.setResolution                                    ( 6.0 )

""" Create the structure objects """
pStruct1                                              = proshade.ProSHADE_data ( pSet )
pStruct2                                              = proshade.ProSHADE_data ( pSet )

""" Read in the structure """
pStruct1.readInStructure                              ( "/Users/mysak/LMB/1_ProteinDomains/0_DOMS/bf/1BFO_A_dom_1.pdb", 0, pSet )
pStruct2.readInStructure                              ( "/Users/mysak/LMB/1_ProteinDomains/0_DOMS/h8/1H8N_A_dom_1.pdb", 1, pSet )

""" Process maps into internal representations """
pStruct1.processInternalMap                           ( pSet )
pStruct2.processInternalMap                           ( pSet )

""" Map to spheres """
pStruct1.mapToSpheres                                 ( pSet )
pStruct2.mapToSpheres                                 ( pSet )

""" Compute spherical harmonics """
pStruct1.computeSphericalHarmonics                    ( pSet )
pStruct2.computeSphericalHarmonics                    ( pSet )

""" Get the distances """
energyLevelsDescriptor                                = proshade.computeEnergyLevelsDescriptor    ( pStruct1, pStruct2, pSet )
traceSigmaDescriptor                                  = proshade.computeTraceSigmaDescriptor      ( pStruct1, pStruct2, pSet )
fullRotationFunctionDescriptor                        = proshade.computeRotationunctionDescriptor ( pStruct1, pStruct2, pSet )

""" Print results """
print                                                 ( "The energy levels distance is          %+1.3f" % ( energyLevelsDescriptor ) )
print                                                 ( "The trace sigma distance is            %+1.3f" % ( traceSigmaDescriptor ) )
print                                                 ( "The rotation function distance is      %+1.3f" % ( fullRotationFunctionDescriptor ) )

""" Delete the C++ pointers """
del pStruct1
del pStruct2
del pSet
```

One of the advantages of this mode of operating the ProSHADE python modules is that the execution only takes the time required to compute the specific computation the function provides and therefore if the user only needs some preliminary results, or can prepare the data for execution later, this is all allowed by this mode.

### Direct access

This is the most advanced mode of using the ProSHADE tool, as it allows direct access into the internal ProSHADE working. This in turn allows supplying non-standard values as well as retrieving any partial results for alternative processing by a different code; however, it also requires the deepest understanding of how ProSHADE works, what data are available at which point in the execution and it may require some data format manipulations on the side of the executing code. The following tutorial as well as the DOxygen documentation should be a good starting point, as well as the **directAccess.py** file.

In order to showcase this approach, we will import the required modules:

```
""" System modules """
import sys

""" Numpy """"
import numpy

""" Import ProSHADE from non-system folder (local installation assumed - if ProSHADE is installed globally, ignore the next line) """
sys.path.append                                       ( "/Users/mysak/BioCEV/proshade/experimental/install/pythonModule" )
import proshade
```

#### Reading a structure from file

The first step of most ProSHADE workflows will be reading a structure (be it co-ordinates or map) from a file on the hard-drive. This can be done in the same manner as shown in the [Advanced access](#advanced-access) section of this tutorial, that is: Firstly we create the **ProSHADE_settings** object, which needs to be filled with the initial data. It does not really matter which task you select at this stage, but it may affect some of the default values and therefore it is recommended to use the correct taks. Next, the **ProSHADE_data** object is created and finally the structure is read in. Please note that on some systems using relative paths may not work and it may result in ProSHADE error stating that the file type cannot be recognised. If this is the case, please use the full path.

```
""" Create the ProSHADE_settings object """
pSet                                                  = proshade.ProSHADE_settings ()

""" Set the settings for Distances detection """
pSet.task                                             = proshade.Distances
pSet.verbose                                          = 1
pSet.setMapResolutionChange                           ( False )

""" Create the structure objects """
pStruct                                               = proshade.ProSHADE_data ( pSet )

""" Read in the structure """
pStruct.readInStructure                               ( "./C3.pdb", 0, pSet )

""" Delete the structure as we will proceed with a different object created later """
del pStruct
```

#### Creating ProSHADE_data object from map

Alteratively, **ProSHADE_data** object can be created from an already existing map and some of the basic map information data. As an example,  we will create a 1D numpy.array, which will hold the density values of a map that we would like to supply to ProSHADE. Of course this array can be the result of any other python module, the only requirement is that the data type is 1D numpy.ndarray with dtype of *float64* with the XYZ axis order.

```
 """ Set the density map description values """
 xDimIndices                                           = 100                            # Number of indices along the x-axis.
 yDimIndices                                           = 120                            # Number of indices along the y-axis.
 zDimIndices                                           = 60                             # Number of indices along the z-axis.
 xDimAngstroms                                         = xDimIndices * 1.3              # X-axis size in Angstroms.
 yDimAngstroms                                         = yDimIndices * 1.3              # Y-axis size in Angstroms.
 zDimAngstroms                                         = zDimIndices * 1.3              # Z-axis size in Angstroms.
 xFrom                                                 = int ( -xDimIndices/2 )         # Starting index of the x-axis.
 yFrom                                                 = int ( -yDimIndices/2 )         # Starting index of the y-axis.
 zFrom                                                 = int ( -zDimIndices/2 )         # Starting index of the z-axis.
 xTo                                                   = int ( (xDimIndices/2)-1 )      # Last index of the x-axis.
 yTo                                                   = int ( (yDimIndices/2)-1 )      # Last index of the y-axis.
 zTo                                                   = int ( (zDimIndices/2)-1 )      # Last index of the z-axis.
 ord                                                   = 0                              # The order of the MAP file (the binary writting style, leave 0 unless you strongly prefer different type).

 """ Create an example map (this will be a ball in the middle of the map) """
 testMap = numpy.empty ( [ ( xDimIndices * yDimIndices * zDimIndices ) ] )
 for xIt in range( 0, xDimIndices ):
    for yIt in range( 0, yDimIndices ):
        for zIt in range( 0, zDimIndices ):
            ind                                       = zIt + zDimIndices * ( yIt + yDimIndices * xIt )
            testMap[ind]                              = 1.0 / ( numpy.sqrt( numpy.power ( (xDimIndices/2) - xIt, 2.0 ) +
                                                                numpy.power ( (yDimIndices/2) - yIt, 2.0 ) +
                                                                numpy.power ( (zDimIndices/2) - zIt, 2.0 ) ) + 0.01 )
```

with an example map created as an 1D numpy.ndarray, it can now be supplied to a **ProSHADE_data** object, which will then be in the same state as if the data were read in from a file. This can be done with the following call:

```
""" Create ProSHADE_data object from numpy.ndarray """
pStruct                                               = proshade.ProSHADE_data ( pSet,                  # The settings objectt
                                                                                 "python_map_test",     # Structure name
                                                                                 testMap,               # The density map
                                                                                 xDimAngstroms,         # The size of x-axis in Angstroms
                                                                                 yDimAngstroms,         # The size of y-axis in Angstroms
                                                                                 zDimAngstroms,         # The size of z-axis in Angstroms
                                                                                 xDimIndices,           # The number of indices along the x-axis
                                                                                 yDimIndices,           # The number of indices along the y-axis
                                                                                 zDimIndices,           # The number of indices along the z-axis
                                                                                 xFrom,                 # The starting x-axis index
                                                                                 yFrom,                 # The starting y-axis index
                                                                                 zFrom,                 # The starting z-axis index
                                                                                 xTo,                   # The last x-axis index
                                                                                 yTo,                   # The last y-axis index
                                                                                 zTo,                   # The last z-axis index
                                                                                 ord )                  # The map file binary order
```

There are several assumption that the **ProSHADE_data** constructor shown above makes and not all of these are currently checked with a warning or error message. Some of these are described in the **directAccess.py** file, but the most common things to consider are the following:
- The constructor assumes that the angles between all three axes are 90 degrees. If this is not the case, it is the users responsibility to transform and re-sample the map before submitting it to ProSHADE (support for non-orthogonal maps is on the TODO list).
- The map dimensions needs to be the same as the x/y/zDimIndices variables.
- The following equality should hold: x/y/zTo - x/y/zFrom + 1 = x/y/zDimIndices.
- The constructor assumes that axis grids are equal to indices and that the origins are equal to the starting indices of each axis.
- The axis order is XYZ

If some of these assumptions do not hold, the **ProSHADE_data** object is likely to still be created, but it is the users responsibility to change the **pStruct** (ProSHADE_data) object internal variables to reflect the reality or face the consequences.

#### 3D arrays

It is possible that instead of 1D arrays as shown above, some other python module would work with maps using 3D arrays. This poses no problem for ProSHADE as the very same constructor accepts 3D numpy.ndarrys instead of 1D numpy.ndarrays and all functionality remains equal, as do the caveats. An example of using 3D instead of 1D map follows:

```
testMap3D = numpy.empty ( ( xDimIndices, yDimIndices, zDimIndices ) )
for xIt in range( 0, xDimIndices ):
    for yIt in range( 0, yDimIndices ):
        for zIt in range( 0, zDimIndices ):
            testMap3D[xIt][yIt][zIt]                  = 1.0 / ( numpy.sqrt( numpy.power ( (xDimIndices/2) - xIt, 2.0 ) +
                                                                            numpy.power ( (yDimIndices/2) - yIt, 2.0 ) +
                                                                            numpy.power ( (zDimIndices/2) - zIt, 2.0 ) ) + 0.01 )

pStruct2                                      = proshade.ProSHADE_data ( pSet,
                                                                         "python_map_test",
                                                                         proshade.convert3Dto1DArray ( testMap3D ),
                                                                         xDimAngstroms,
                                                                         yDimAngstroms,
                                                                         zDimAngstroms,
                                                                         xDimIndices,
                                                                         yDimIndices,
                                                                         zDimIndices,
                                                                         xFrom,
                                                                         yFrom,
                                                                         zFrom,
                                                                         xTo,
                                                                         yTo,
                                                                         zTo,
                                                                         ord )

del pStruct2
```

#### Writing out maps

Now, it is possible to write out the internal map representation at any point since the **ProSHADE_data** object has been filled in. To demonstrate this functionality, it is immediately possible to issue the following command, which will write an *initialMap.map* file onto the hard-drive.

```
""" Write out the initial map """
pStruct.writeMap                                      ( "initialMap.map" )
```

#### Getting back the ProSHADE internal representation map

Here, we will demonstrate how the user can access the ProSHADE internal representation map from the **ProSHADE_data** object. Please note that this is not limitted to the initial map, this will work for any **ProSHADE_data** object which has map data in any stage of ProSHADE computations. The map will be returned as a 3D numpy.ndarray of dtype *float64* ordered with the XYZ axis ordering.

```
""" Get back the ProSHADE internal map representation """
initialMap                                            = pStruct.getMap ( )
```

#### Initial map procesing

Once the map is read into the **ProSHADE_data** object, it needs to be processed in order to make sure ProSHADE will be able to use it for any further computations. While processing, ProSHADE offers the following map modifications through the **ProSHADE_setting** object variables: *map invertion* (this will invert the map indices along each dimension), *map normalisation* (making the map density values mean 0 and standard deviation 1), *map masking* (computing a map mask by blurring and then setting mask as all values above threshold), *map centering* (moving the map into the centre of mass), *adding extra space* (in case the map density is close to map edge, what can lead to map artefacts and lower accuracy of further processing) and *map phase removal* (removing the phase of the map density, effectively producing Patterson maps). The user can choose any, all or none of these, but the processing function needs to be called before any further processing is possible. The following example code showcases how some of the processing functionalities can be chosen and how the map can be processed.

```
""" Set which processing should be done """
pSet.setMapInversion                                  ( False )  # Should all map positions x,y,z be swapped to -x,-y,-z? Use this only if your helices have the wrong hand ...
pSet.setNormalisation                                 ( False )  # Should internal map representation be normalised to mean 0 and standard deviation 1?
pSet.setMasking                                       ( False )  # Should maps be masked by blurring?
pSet.setMapCentering                                  ( False )  # Move structure COM to the centre of map box?
pSet.setExtraSpace                                    ( 10.0 )   # Extra space in Angs to be added when creating internap map representation.
pSet.setPhaseUsage                                    ( True )   # Use full maps, or Patterson-like maps?

""" Process the internal map representation """
pStruct.processInternalMap                            ( pSet )
```

#### Computing standard ProSHADE tasks

If the user now wants to use ProSHADE to compute some of the standard ProSHADE taks, *i.e.* Distances computation, Symmetry detection, Re-boxing or Map overlay, it is recommended that the user proceeds in the same fashion as shown in the the *advancedAccess_...* example files. Moreover, these are also demonstrated in the **directAccess.py** file available in the examples folder. Therefore, none of these tasks will be shown here in a step-wise manner; instead, the rest of this tutorial will focus on how partial information and results can be obtained from ProSHADE.

#### Computing the spherical harmonics decomposition

ProSHADE can compute the spherical harmonics decomposition of the internal map. However, instead of using the spherical-Bessel functions, it firstly creates a set of concentric spheres centered on the centre of indices (xDimIndices/2, yDimIndices/2, zDimIndices/2) point and spaced 2 indices apart, then it maps the density map data onto these spheres and then it computes the spherical harmonics decomposition on each of these spheres independently. There is quite a few settings that relate to the spherical harmonics decompostion computation, such as the bandwidth of the computation, the sphere placement and spacing, the resolution on the spheres, etc.; these arre mostly inter-related and ProSHADE will set them up automatically, unless the user specifies otherwise. Since these are quite technical, the interested users are referred to the second chapter of my Ph.D. thesis, which specifies all the technical details: https://www.repository.cam.ac.uk/handle/1810/284410 . To issue this computation, please use the functions shown in the following example code:

```
""" Map the internal map representation onto a set of concentric spheres """
pStruct.mapToSpheres                                  ( pSet )

""" Compute the spherical harmonics decomposition """
pStruct.computeSphericalHarmonics                     ( pSet )
```

If the user is interested in the spherical harmonics values (and possibly does not need any further computations from ProSHADE), these can be accessed using the function showcased below. It is worth noting that the organisation of the spherical harmonics is as follows: The *getSphericalHarmonics()* function's output is a 2D numpy.ndarray of dtype *complex128*. The first dimension of this array is the sphere index, while the second dimension contains all the spherical harmonics values for the given sphere wrapped into a 1D array. This saves memory, as this packaging does not result in sparse matrix (there is different number of orders for each band), but on the other hand the user needs to use another function ( *findSHIndex()* ) to obtain any particular value from this 1D array. The following code shows how all spherical harmonics values can be obtained from ProSHADE and how any particular value can be identified in the ProSHADE output.

```
""" Obtain all the spherical harmonics values for all shells """
sphericalHarmonics                                    = pStruct.getSphericalHarmonics ( )

""" Retrieve s specific value for shell 3, band 4 and order -2 """
shell =  3
band  =  4
order = -2
Shell3Band4OrderMin2Value                             = sphericalHarmonics[shell][pStruct.findSHIndex(shell, band, order)]
```

#### Computing the self-rotation function

ProSHADE also allows computing the (self) rotation function. More specifically, it firstly computes the so called E matrices, which are matrices of the integral over all the concentric spheres of the spherical harmonics coefficients of order1 and order2, or in mathematical (LaTeX) form: *Integral _0 ^rMAX ( c^lm * c'^lm )*. It then proceeds to normalise these E matrices, resulting in the SO(3) decomposition (Wigner D based decomposition) coefficients. Finally, by computing the inverse SO(3) Fourier transform (SOFT) on these coefficients, ProSHADE obtains the (self) rotation function. In order to isue this computaion, the following code can be used:

```
""" Compute the self-rotation function """
pStruct.computeRotationFunction                       ( pSet )
```

Once the self-rotation function is computed, ProSHADE allows the user to access all of its interim results as well as the rotation function map. Specifically the E matrices, which are ordered by the band, order1 and order2 (in this order) can be obtained as shown in the following code. The E matrices are 3D numpy.ndarrays of dtype *complex128*, which suffer from the different number of orders for different bands feature of spherical harmonics. Therefore, the order dimensions of the arrays are zero padded; furthermore, as the order indexing goes from -band to +band, but the array indexing starts from zero, the correction to the array indices is necessary. Regarding the SO(3) coefficients, they have the same technical structure as the E matrices and suffer from the same caveats. Finally, the self-rotation function map can be accessed as a 3D numpy.ndarray of dtype *complex128* using the function shown in the example code below. For the users convenience, ProSHADE also provides a function for converting any rotation function position (as given by three indices) onto corresponding rotation matrix - this is shown in the last part of the following example code.

```
""" Obtain the E matrices """
eMat                                                  = pStruct.getEMatrix ( )
Band4OrderOneMin2OrderTwo3EMatrixValue                = eMat[4][2][7] # Band = 4, Order1 = -2 and Order2 = 3

""" Obtain the SO(3) coefficients """
so3Coeffs                                             = pStruct.getSO3Coefficients ( )
Band4OrderOneMin2OrderTwo3SO3CoeffsValue              = so3Coeffs[4][2][7] # Band = 4, Order1 = -2 and Order2 = 3

""" Obtain the self-rotation function """
selfRotationFunction                                  = pStruct.getRotationFunctionMap ( )

""" Convert self-rotation function indices to rotation matrix """
rotMapMax                                             = numpy.where ( selfRotationFunction == numpy.amax ( selfRotationFunction ) )
rotMatMaxVal                                          = pStruct.getRotationMatrixFromSOFTCoordinates ( rotMapMax[0][0], rotMapMax[1][0], rotMapMax[2][0] )
```

#### Computing the optimal rotation function

A related ProSHADE functionality is the computation of an optimal rotation function for two input structures. In the standard ProSHADE tasks, this is done for two phase-less structure maps (the phase is removed to achive identical centering on the maps) in order to find the optimal rotation, which overlays the two maps, but the user is free to call this function for any two **ProSHADE_data** objects which both have their spherical harmonics values computed. To do this, we will create two new **ProSHADE_data** objects, read in some structures, process them, map them onto spheres, compute their spherical harmonics values and then we call the *getOverlayRotationFunction()*. This function works similarly to the *computeRotationFunction()* used above, but it uses spherical harmonics coefficients from two different structures as opposed to the same structures.

```
""" Modify the settings object for optimal rotation function computation """
pSet.task                                             = proshade.OverlayMap
pSet.verbose                                          = 4
pSet.requestedResolution                              = 4.0
pSet.usePhase                                         = False
pSet.changeMapResolution                              = True
pSet.maskMap                                          = False
pSet.moveToCOM                                        = False
pSet.normaliseMap                                     = False
pSet.reBoxMap                                         = False

""" Create the two new ProSHADE_data objects """
pStruct_static                                        = proshade.ProSHADE_data ( pSet )
pStruct_moving                                        = proshade.ProSHADE_data ( pSet )

""" Read in two structures """
pStruct_static.readInStructure                        ( "/Users/mysak/LMB/1_ProteinDomains/0_DOMS/bf/1BFO_A_dom_1.pdb", 0, pSet ) 
pStruct_moving.readInStructure                        ( "/Users/mysak/LMB/1_ProteinDomains/0_DOMS/h8/1H8N_A_dom_1.pdb", 1, pSet ) 

""" Process, map and get spherical harmonics for both structures """
pStruct_static.processInternalMap                     ( pSet )
pStruct_moving.processInternalMap                     ( pSet )
        
pStruct_static.mapToSpheres                           ( pSet )
pStruct_moving.mapToSpheres                           ( pSet )
        
pStruct_static.computeSphericalHarmonics              ( pSet )
pStruct_moving.computeSphericalHarmonics              ( pSet )

""" Compute the optimal rotation function """
pStruct_moving.getOverlayRotationFunction             ( pSet, pStruct_static )
```

The very same functions with the same return values can now be used to obtain the E matrices, the SO(3) coefficients and the rotation function as were used above for the self-rotation function. The following example code recapitulates these functions for the rotation function computed just now.

```
""" Obtain E matrices """
eMat                                                  = pStruct_moving.getEMatrix ( )
Band4OrderOneMin2OrderTwo3EMatrixValue                = eMat[4][2][7] # Band = 4, Order1 = -2 and Order2 = 3

""" Obtain the SO(3) coefficients """
so3Coeffs                                             = pStruct_moving.getSO3Coefficients ( )
Band4OrderOneMin2OrderTwo3SO3CoeffsValue              = so3Coeffs[4][2][7] # Band = 4, Order1 = -2 and 

""" Get the rotation function """
rotationFunction                                      = pStruct_moving.getRotationFunctionMap ( )
```

#### Finding the optimal rotation

Once the rotation map is computed, the user may be interested in the highest value in the map and the corresponding rotation matrix (or Euler angles), as these will represent the rotation which overlays most of the two structures (within the error of the map sampling). To facilitate this taks, ProSHADE contains functions returning the Euler angles or the rotation matrix associated with the highest peak in the rotation function. The following example code shows how they can be used:

```
""" Find the highest peak in the map, associated Euler angles and rotation matrix """
optimalRotationAngles                                 = pStruct_moving.getBestRotationMapPeaksEulerAngles ( pSet )
optimalRotationMatrix                                 = pStruct_moving.getBestRotationMapPeaksRotationMatrix ( pSet )
```

#### Rotating the internal map representation

Once the optimal rotation angles are obtained, it is the next logical step to rotate the structure by these angles to get the two structures in identical orientation. This can also be done with ProSHADE function *rotateMap()*, which works with the Euler angles as reported by ProSHADE. The rotation is done using the spherical harmonics coefficients, which are multiplied by the Wigner D matrices for the required rotation and the resulting rotated coefficients are then inverted back and interpolated to a new map. This process has two side effects: Firstly, the resulting maps tend to suffer from minor artefacts resulting from the sequence termination errors and the interpolation to and from spheres to cartesian co-ordinates. And secondly, the input maps need to have their spherical harmonics coefficients computed. Therefore, this approach is not recommended for any maps that are to be deposited or fitted into, but they are sufficient for computation of most ProSHADE standard tasks as the shape is still almost identical.

In terms of this tutorial, since we have already computed the optimal rotation between two structures, we will continue to show how this result can be used to rotate a new structure. This will allow us to demonstrate the next functionality of ProSHADE in the later sections of this tutorial in a more streamlined fashion. To cause **ProSHADE_data** map rotation, the function in the example code can be used.

```
""" Delete the old structure objects so that new can be created """
del pStruct_static
del pStruct_moving

""" Change the settings """
pSet.usePhase                                         = True
pSet.changeMapResolution                              = True

""" Create the structure objects """
pStruct_static                                        = proshade.ProSHADE_data ( pSet )
pStruct_moving                                        = proshade.ProSHADE_data ( pSet )

""" Read in the structures with phases """
pStruct_static.readInStructure                        ( "/Users/mysak/LMB/1_ProteinDomains/0_DOMS/bf/1BFO_A_dom_1.pdb", 0, pSet ) # This is a BALBES domain 1BFO_A_dom_1.
pStruct_moving.readInStructure                        ( "/Users/mysak/LMB/1_ProteinDomains/0_DOMS/h8/1H8N_A_dom_1.pdb", 1, pSet ) # This is a BALBES domain 1H8N_A_dom_1.

""" Process the structures and get spherical harmonics for moving structure only """
pStruct_static.processInternalMap                     ( pSet )
        
pStruct_moving.processInternalMap                     ( pSet )
pStruct_moving.mapToSpheres                           ( pSet )
pStruct_moving.computeSphericalHarmonics              ( pSet )

""" Rotate the moving structure by the pre-determined Euler angles of the best rotation map peak """
pStruct_moving.rotateMap                              ( pSet, optimalRotationAngles[0], optimalRotationAngles[1], optimalRotationAngles[2] )
```

#### Computing the translation function

Similarly to the rotation function, the user may be interested in the optimal translation required to overlay two structures. ProSHADE can compute such an optimal translation using the translation function; however, in order to compute it, it requires that the two internal map representation have the same dimensions in terms of map indices and map sampling; identical map sampling is achieved by setting the **changeMapResolution** setting to true. Still, as the identical number of indices will not generally be the case, ProSHADE provides a padding function, which can add zeroes around the internal representation map to make sure that it has given dimensions. Therefore, in order to compute the translation function, it is required that the two structures are modified by the *zeroPaddToDims()* function to both have the same dimensions; the higher of the two structures are chosen in order to avoid loss of information.

```
""" Add zeroes around he structure to achieve given number of indicel along each dimension """
pStruct_static.zeroPaddToDims                         ( int ( numpy.max ( [ pStruct_static.getXDim(), pStruct_moving.getXDim() ] ) ),
                                                        int ( numpy.max ( [ pStruct_static.getYDim(), pStruct_moving.getYDim() ] ) ),
                                                        int ( numpy.max ( [ pStruct_static.getZDim(), pStruct_moving.getZDim() ] ) ) )
pStruct_moving.zeroPaddToDims                         ( int ( numpy.max ( [ pStruct_static.getXDim(), pStruct_moving.getXDim() ] ) ),
                                                        int ( numpy.max ( [ pStruct_static.getYDim(), pStruct_moving.getYDim() ] ) ),
                                                        int ( numpy.max ( [ pStruct_static.getZDim(), pStruct_moving.getZDim() ] ) ) )
```

Once the structures have the same dimensions, it is possible to compute the translation function. This function will compute the Fourier transforms of both maps, combine the Fourier coefficients and compute the inverse Fourier transform on the resulting combined coefficients map, thus obtaining the translation map. Once computed, this map can be accessed from the ProSHADE python module as shown in the following example code.

```
""" Compute the translation function """
pStruct_moving.computeTranslationMap                  ( pStruct_static )

""" Access the translation map as a 3D numpy.ndarray """
translationFunction                                   = pStruct_moving.getTranslationFunctionMap ( )
```

Also, similarly to the rotation function, ProSHADE provides a useful function for detecting the highest peak in the translation map and computing the corresponding translation in Angstroms. However, this translation is computed from the current position and not from the orginal starting position of the read in structure. To allow the user to properly apply the rotation and translation to the structure, ProSHADE provides a function that finds the translation function highest peak as well as the rotation centre and then outputs two vectors; one specifying the rotation centre, about which any rotations should be done and at which the structure should be centered before the second vector, translation to optimal overlay position is applied. The following code shows how both vectors can be obtained from ProSHADE.

```
""" Find the optimal translation vectors """
translationVecs                                       = pStruct_moving.getOverlayTranslations ( pStruct_static,
                                                                                                optimalRotationAngles[0],
                                                                                                optimalRotationAngles[1],
                                                                                                optimalRotationAngles[2] )
```

#### Writing out resulting structures

Finally, it is worth noting that while the MAP formatted data can be written out of the **ProSHADE_data** object at any time (albeit their quality may be decreased if the rotation was applied as discussed in the rotating internal representation map section), ProSHADE can also write out the co-ordinate data for input structures, which were read in from a co-ordinate file. Please note that ProSHADE cannot generate co-ordinate data from maps, the co-ordinate data need to pre-exist ProSHADE run. Nonetheless, in the case of, for example, finding the optimal rotation and translation of one structure to overlay with another structure, the user may be interested in writing out the modified co-ordinates. To do this, ProSHADE contains the *writePdb()* function, which needs to be supplied with the file name, the required rotation and translation and it will write out the PDB file with these modifications applied.
```
""" Write out the rotated and translated map and co-ordinates """
pStruct_moving.writeMap                               ( "/Users/mysak/Desktop/movedPy.map" )
pStruct_moving.writePdb                               ( "/Users/mysak/Desktop/movedPy.pdb",
                                                        optimalRotationAngles[0],
                                                        optimalRotationAngles[1],
                                                        optimalRotationAngles[2],
                                                        translationVecs["rotCenToOverlay"][0],
                                                        translationVecs["rotCenToOverlay"][1],
                                                        translationVecs["rotCenToOverlay"][2],
                                                        pSet.firstModelOnly )
```

# The End

![](https://github.com/michaltykac/proshade/blob/experimental/proshade/Logo_small.png)
