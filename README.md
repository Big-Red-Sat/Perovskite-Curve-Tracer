# Perovskite Curve Tracer
This project contains the hardware and software source for the curve tracer developed to evaluate perovskite solar cell samples during the [Big Red Sat-1 project](https://github.com/Big-Red-Sat/Big-Red-Sat-1).

## Hardware
The hardware is licensed under a CERN Open Hardware Licence Version 2 - Strongly Reciprocal license.  The developed hardware performs a passive curve tracing process that utilizes a low-Ohm resistor ladder, realized through analog switches and precision resistors.  The multiplexing of the perovskite solar cells is achieved through a low-Ohm analog SPDT relay.  Provisions are also made for an I2C connection to a temperature sensor on the sample holder.  A simple control interface is provisioned through USB for controlling the hardware and retrieve readings.

![Overhead hardware](https://github.com/Big-Red-Sat/Perovskite-Curve-Tracer/blob/main/images/overhead.jpg)

## Software
The software is licensed under an MIT license.  The software is operated using a single Python script under the software directory, `curve_tracer.py`.  
1. Clone this repository to a local directory,
2. Create a Python 3.9 virtual environment in the software folder,
3. Install all packages using the requirements.txt file,
4. Run curve_tracer.py.

## Performance
The collected data can be saved to the software folder under a directory called curves.  In that folder are numerous experiments from the Big Red Sat-1 project.  The plotted curves will look like the image below.
![X018 Curve](https://github.com/Big-Red-Sat/Perovskite-Curve-Tracer/blob/main/software/curves/3.%20Final%20Round/X018_LM/X018_LM_plotted_Reverse.png)

## Citation
If this repository was useful to your research, then please cite this repository using the BibTeX definition below.
```
@software{
  Arce_Perovskite_Curve_Tracer_2023,
  author = {Arce, Walker},
  month = aug,
  title = {{Perovskite Curve Tracer}},
  url = {https://github.com/wsarce/Perovskite-Curve-Tracer},
  version = {v1.0.0},
  year = {2023}
}
```
## Contact
For additional information or questions, please contact Walker Arce (wsarcera@gmail.com).

## License
The hardware is licensed under a CERN Open Hardware Licence Version 2 - Strongly Reciprocal, the software and firmware is licensed under an MIT license, and the documentation is licensed under a Creative Commons Attribution-ShareAlike 4.0 International Public License.
