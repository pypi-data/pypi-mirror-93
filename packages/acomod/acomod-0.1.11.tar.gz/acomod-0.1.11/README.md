# Acoustic Modes Viewer

This program is a simple viewer of power spectral density of sound. 
The package provides a module and a program to trace Fourier acoustic modes and resonance frequencies of excited bodies.

## Use cases
* estimate length of an excited metal bar, guitar string, or 
* measure frequency of flute tones, 
* identify resonance frequencies and through provided sound speed the corresponding length scales of mechanical components that generate unwanted resonances (e.g. in a car as a function of speed cs)
* test 1/f noise and microphonic effects in electrical devices the program runs on.


## Features
* Analysis of sound from microphone or from a file (WAV format)
* In order to analyze transient signals, the program keeps track of maximal peaks detected in the instantaneous  spectra 
* Saves recorded and processed data to files for further analysis
* Outputs list of peak frequencies (f) and associated wavelengths (l=cs/f)

## Installation

### Virtualenv installation

```sh
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install acomod
```

You need to specify the LD_LIBRARY_PATH environment variable to point to the location where appropriate Qt libraries can be found. Let's store these settings in your virtual environment activaton script.

```sh
$ echo 'LD_LIBRARY_PATH='`find "$VIRTUAL_ENV" -name "*libQt5Core.so.5*" -exec dirname "{}" \;`:$LD_LIBRARY_PATH >> venv/bin/activate
```



## Screenshots

![Screenshot](screenshot.png)

![Screenshot](https://github.com/bslew/acomod/blob/master/screenshot.png)


## Troubleshooting
##### 	**acoustic_mode_viewer gives core dump on start**

When you pip3 install acomod in virtual environment or locally via --user option Qt platform plugin may fail to be properly initialized due to incorrect configuration of LD_LIBRARY_PATH environment variable (under Linux) and pointing locations of Qt libraries installed most likely somewhere in the system directories. If the version of those is not the one required by the PyQt5 the program will fail with

	"This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.",
	
a message that typically is not even printed out to the terminal.

**Solution**:
		Provide the correct path to the Qt shared libraries: e.g.
				
```sh
$ export LD_LIBRARY_PATH=`find ./venv -name "*libQt5Core.so.5*" -exec dirname '{}' \;`:$LD_LIBRARY_PATH
```

or in case of `pip install acomod --user`
				
```sh
$ export LD_LIBRARY_PATH=`find $HOME/.local -name "*libQt5Core.so.5*" -exec dirname '{}' \;`:$LD_LIBRARY_PATH
```


## Authors
Bartosz Lew (bartosz.lew@protonmail.com)
