
# Software: Image histogram equalization  

##  Statements of purpose and maturity
The purpose of this work is to adjust image intensities for visualization purposes

  
##  Description of the repository contents

- `src`: contains the source python file
    **src/histogram_equalization.py** - implementation of standard and 
    Contrast Limited Adaptive Histogram Equalization (CLAHE) histogram equalization. 
    It support 8 BPP and 16 BPP grayscale images and RGB color images.
- `Dockerfile`
- `plugin.json` manifest
- `sample-data` folder with test data

###   Technical installation instructions, including operating system or software dependencies

The project is leveraging numpy, tifffile, imagecodecs, and opencv libraries. 
It has been developed on Windows 11 and tested on MacOSX.

## Installation

### Build Python Virtual Environment 
```
conda create --name hist_equ python=3.7
conda activate hist_equ 
conda install numpy, opencv-python-headless, tifffile, imagecodecs
```
Note: The current version outputs **compressed** intensity adjusted images using LZW compression. 
This requires using Python 10.x and up 
(tested with  10.x and 11.x). If a previous version of Python is used, then the imwrite function must change to 'none' compression flag
since the 'lzw' flag is not supported on Windows 11 in imagecodes: 
 [see](https://github.com/cgohlke/imagecodecs/blob/f38d0d4e5db1d08d92742a5d899325fc7c7b56e7/imagecodecs/_imcd.pyx#L854-L856) 
 
### Build the Docker image
```
docker build . -t wipp/wipp-hist-equalize-python:0.0.1
```

### Build the Web Image Processing (WIPP) Plugin Manifest
	- open URL:  https://usnistgov.github.io/WIPP-Plugin-Manifest-generator/
	- type all relevant information into web form
	- save the file as plugin.json
	
## Execution

### Run the Python code

From this directory:
```
python ./src/histogram_equalization.py \
--inputImages ./sample-data/inputs \
--output ./sample-data/outputs
```

### Run the Docker image
From this directory:
```
docker run -v "$PWD"/sample-data:/data \
	wipp/wipp-hist-equalize-python:0.0.1 \
	--inputImages /data/inputs \
	--output /data/outputs
```
`-v`: mounts a volume/folder from your machine inside of the Docker container

### Run the WIPP plugin
	- register the plugin.json in a deployed WIPP instance - see https://github.com/usnistgov/WIPP
	- upload images from sample-data/inputs as WIPP image collection
	- create a workflow by adding one step called histogram equalization
	- run and monitor the workflow execution
	- download resulting WIPPP image colection

## Additional Information

###    Contact information
-   Peter Bajcsy, ITL NIST, Software and System Division, Information Systems Group
-   Contact email address at NIST: peter.bajcsy@nist.gov

###    Credits: 
- The contributions to the code in this repository came from:
    - *Peter Bajcsy*
    - *Mylene Simon*
 
###    Related Material
-    URL for opencv tutorial: https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html

[comment]: # ( References to user guides if stored outside of GitHub)

###    Citation: 
R. C. Gonzalez and R. E. Woods, Digital Image Processing, Third. Upper Saddle River, NJ, USA: Prentice Hall, 2008

[comment]: # ( References to any included non-public domain software modules, and additional license language if needed, e.g. BSD, GPL, or MIT)


