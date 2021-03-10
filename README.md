# OpenPulse: Open Source Software for Pulsation Analysis of Pipeline Systems

*Alpha Version* (March 12th 2021)

![alt text](https://open-pulse.github.io/OpenPulse/doc/system3.jpeg?raw=true)

OpenPulse is a software written in Python for numerical modelling of low-frequency acoustically induced vibration in gas pipeline systems. It allows to import the geometry of the pipe system (lines in IGES), insert materials properties, set sections, and import pressure/acceleration/force loads (from measurements or theory). OpenPulse performs an acoustic time harmonic response analysis of the respective 1D acoustic domain using the Finite Element Transfer Method (FETM). The resulting pressure field is applied as a distributed load over the respective structural piping system, modeled with the Timoshenko beam theory and the Finite Element Method (FEM), in order to run a structural time harmonic response analysis. In addition to simply boundary conditions as constraints on displacements, OpenPulse allows to insert lumped springs, masses and dampers along the domain.

After defining the FEM mesh for the model, you can plot the piping system geometry and run simulations such as modal analysis and harmonic analysis. It is possible to plot deformed shapes, frequency plots of acoustical and structural responses, stress fields and local stresses of desired sections.

You can try it out now by running the tutorial on binder.

## Installing

- **Install Python 3.7.7** ([download](https://www.python.org/downloads/release/python-377/)).

- **Install OpenPulse**.
Clone or download [OpenPulse](https://github.com/open-pulse/OpenPulse) files. In the case of download, unzip the received file and open a terminal in the main folder (an easy way to do this is to enter the folder, press shift and right click, then "Open PowerShell here"). So, enter the command: 
```
pip install -r requirements.txt
```

- **Run OpenPulse**.
In the same folder, enter the following command in the terminal:
```
python pulse.py
```

## Requirements

    Python v. 3.7.7 
    scipy
    matplotlib
    numpy
    PyQt5
    vtk
    gmsh-sdk
    h5py
    
## Documentation
- You can read the API reference [here](https://open-pulse.readthedocs.io/en/latest/index.html).

- Theory Reference for [1D Acoustics](https://open-pulse.github.io/OpenPulse/doc/Acoustics.pdf), [Structural Vibration of Timoshenko Beams using FEM](https://open-pulse.github.io/OpenPulse/doc/Theory_Structural.pdf), [Weak Fluid-Structure-Coupling FETM-FEM](https://github.com/open-pulse/OpenPulse/blob/master/doc/OpenPulse___Report_D___Weak_Coupling.pdf), [Solution Types (April, 15th 21)](https://), [Matrix Assembly Technique using Python](https://open-pulse.github.io/OpenPulse/doc/Assembly.pdf) and [Stress Stiffening (Prestress)](https://github.com/open-pulse/OpenPulse/blob/master/doc/OpenPulse___Report_E___Prestress.pdf).

- [User Guide for Structural Analysis (April, 1st 21)](https://).

- [User Guide for Acoustic Analysis (April, 1st 21)](https://).

- [User Guide for Coupled Analysis (April, 1st 21)](https://).

- Project page on [Researchgate](https://www.researchgate.net/project/Acoustically-Induced-Vibration-in-Pipeline-Systems).

## ISMA2020 - International Conference on Noise and Vibration Engineering

- [Presentation](https://www.youtube.com/watch?v=iarKDAei6fg&t).
- [Full Paper](https://github.com/open-pulse/OpenPulse/blob/master/doc/ISMA_2020_PRE.pdf).

## ASA Meeting 2020 - The 179th Meeting of the Acoustical Society of America

- [Effect of flow on the acoustic length correction factor of a Helmholtz resonator neck at high Strouhal number: a symmetric three-dimensional parametric study](https://asa.scitation.org/doi/10.1121/1.5147459). 

## Next events

- The 27th International Congress on Sound and Vibration. July 11-15, 2021. [ICSV27](https://www.icsv27.org/).
- The 12th Congresso Iberoamericano de Acústica. August 29 -September 01, 2021. [FIA2020/1](https://fia2020.com.br/).

## Questions
If you have any questions you can open a new issue with the tag 'question'.

## Authors

The authors are members of MOPT - Multidisciplinary Optimization Group, from Federal University of Santa Catarina (Florianópolis, SC, Brazil).

   [Olavo M. Silva](https://www.linkedin.com/in/olavo-m-silva-5822a5151/) - Engineer;
   [Jacson G. Vargas](https://www.linkedin.com/in/jacson-gil-vargas-a54b0768/) - Engineer;
   [Diego M. Tuozzo](https://www.linkedin.com/in/martintuozzo/) - Engineer;
   [Lucas V. Q. Kulakauskas](https://www.linkedin.com/in/lucas-kulakauskas-5a0314182/) - Engineer;
   [Ana P. Rocha](https://www.linkedin.com/in/ana-paula-da-rocha-55520a176/) - Engineer;
   [Andre F. Fernandes](https://www.linkedin.com/in/andrefernandes2001/) - Computer Scientist; 
   [José L. Souza](https://www.linkedin.com/in/jos%C3%A9-luiz-de-souza-8669b5114/) - Computer Scientist.

![alt text](https://open-pulse.github.io/OpenPulse/doc/MOPT.JPG?raw=true)

**
