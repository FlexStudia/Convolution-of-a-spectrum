# Convolution-of-a-spectrum
Program for convolving a spectrum with destination data


**Description**
- it is a program 
- it is coded in Python 3.7.6 (all used modules are in requirements.txt)
- this code creates a cross-platform executable to convolve a spectrum with destination spectral data


**Convolution features**
- the spectrum for convolution must be in a text file (.txt, .csv, .tsv) and its units must be A, µm, nm, or cm-1
- the destination wavelength must be in A, µm, nm, or cm-1 and can be in a text file or generated as a linear function (with start, end, and step values)
- three convolution functions are provided: Gaussian, Triangle and Trapeze
- parameter of the convolution function (the width for all functions and the top for Trapeze) can be in a text file, generated as a linear function or be defined as constants
- once the spectral and destination data is defined, it is possible to test them (mainly for the purpose of signaling if there are any edge effects)
- once the convolution has been calculated, it is possible to plot the result (with the initial spectrum) or to save it as a text file (.txt)


**Usage**

in any python 3 environment
1. to be able to run this python file, you must have python 3 installed ([python.org](www.python.org/downloads))
2. after it is necessary to install all the required packages (listed in requirements.txt provided with the py code file and this readme) for example via a virtual environment:

		python3 -m venv .venv
		source .venv/bin/activate
		pip install --upgrade pip setuptools wheel
		pip install --upgrade -r requirements.txt
    
3. it is possible to read and run the code in the native python environment, via bash 

		python3 convolution.py
      
or by installing an IDE, for example "PyCharm"


**Compilation**

it is possible to create a single executable file with PyInstaller with the following command line

for Mac:

	pyinstaller --noconsole --onefile --icon="icon.icns" convolution.py
    
for Linux:

	pyinstaller --noconsole --onefile convolution.py
      
for Windows:

	pyinstaller --hidden-import="pkg_resources.py2_warn" --noconsole --onefile --icon="icon.ico" convolution.py
      
where "icon.ico"/"icon.icns" is an option to include an icon for the executable (provided)


**Authors and acknowledgment**
- program code is by Maria Gorbacheva (flex.studia.dev@gmail.com)
- scientific base is by Bernard Schmitt (bernard.schmitt@univ-grenoble-alpes.fr)


**Contributing**

for any questions, proposals and bug reports, please write to convolution.of.a.spectrum@gmail.com


**License**

CC-BY 4.0 (Authors attribution alone required)

for more information [creativecommons.org](https://creativecommons.org/licenses/by/4.0/deed.fr)

