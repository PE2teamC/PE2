# PE2_C
**Programming for Engineer Ⅱ**   


## Overview
This software is programed to analyze measured data of semiconductor wafers.

## Contents
1. [Info](#Info)
2. [Project](#Project)
3. [Requirements](#Requirements)
4. [Instructions](#Instructions)
5. [Collaborators](#Collaborators)
* * *


## Info
- `python 3.9`
- `Windows 11`
* * *

## Project
- dat: a folder contains XML data
- doc: a folder contains documentation- Jupyter notebook file describing data analysis results and powerpoint file for presentation
- res: a folder contains result figures and csv files
- src: a folder contains codes of the software
- README.md: brief introduction of this software repository
- run.py: execution python file of this software   

![image](https://user-images.githubusercontent.com/127359402/236680428-3d8cf99c-d164-4a9d-a818-274bbd423bff.png)
* * *

## Requirements
- NumPy
- xml.etree.ElementTree
- matplotlib
- scikit-learn
- pandas
- lmfit
- tqdm
- glob

To install all requirements, use the following command.   
```
pip install -r requirements.txt
```
* * *

## Instructions
1. Run run.py
2. Select the desired device type (ex. `LMZC`, `LMZO`, `LMZ`)
3. Enter the desired wafer number in the form "D##" (ex. `D07`, `D08`, `D23`, `D24`, `all`)
4. Enter the date of measurement (`20YYMMDD`, `all`)
5. Enter Wafer's row and column in the form of "#,#" (ex. `0,0`)
6. Enter your name
7. Enter y/n whether to see the data as png file or not
8. Enter y/n whether to save the data as png file or not
9. Enter y/n whether to save the data as csv file or not
10. [Exit the program]

![image](https://github.com/KyoRyoung/PE2/assets/127359402/1c04f06e-9f32-4288-9836-cca99122d13d)
![image](https://github.com/KyoRyoung/PE2/assets/127359402/da651467-073e-4046-b534-7986311f88b3)

* * *

## Collaborators
- 2019030455 고주환   
- 2019052415 윤석현   
- 2019080973 이동현   
- 2020027192 김교령
* * *
