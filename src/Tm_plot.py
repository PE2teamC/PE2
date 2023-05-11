import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import warnings
#
#--------------------Font설정-----------------------------------------
total_font_axis = {'weight': 'bold', 'size': 10}
total_font_title = {'weight': 'bold', 'size': 12}

font_axis = {'weight': 'bold', 'size': 12}
font_title = {'weight': 'bold', 'size': 18}
#---------------------------------------------------------------------

def tm_plot(x):

    xml_file = ET.parse(x)
    root = xml_file.getroot()

    #----- Wavelength-Transmission(Raw data) ------
    plt.subplot(2, 3, 1)
    plot_color = ['lightcoral', 'coral', 'gold', 'lightgreen', 'lightskyblue', 'plum', 'navy', 'black', 'red']
    color_number = 0

    wl, tm = [], []
    DC_bias = -2.0
    for i in root.iter():
        if i.tag == 'WavelengthSweep':
            if i.attrib.get('DCBias') == str(DC_bias):
                wl = list(map(float, i.find('L').text.split(',')))
                tm = list(map(float, i.find('IL').text.split(',')))
                plt.plot(wl, tm, plot_color[color_number], label=f'{DC_bias}V')
                DC_bias += 0.5
                color_number += 1
        elif i.tag == 'Modulator':
            if i.attrib.get('Name') == 'DCM_LMZC_ALIGN':
                wl = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('L').text.split(',')))
                tm = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('IL').text.split(',')))
                plt.plot(wl, tm, color='purple', linestyle=':')


    plt.title('Transmission spectra - as measured', fontdict=total_font_title)
    plt.xlabel('Wavelength [nm]', fontdict=total_font_axis)
    plt.ylabel('Measured transmission [dB]', fontdict=total_font_axis)
    plt.legend(ncol=3,loc='lower center', fontsize=9)
    plt.grid(True,axis='both', color='gray', alpha=0.5, linestyle='--')

    # --------------------------transmission_graph(R_spuared)------------------------------
    plt.subplot(2, 3, 2)

    warnings.filterwarnings('ignore', message='Polyfit may be poorly conditioned')

    best_fit_list = []
    r2=[]
    for i in range(1, 9):
        afc = np.polyfit(wl, tm, i)
        af = np.polyval(afc, wl)
        R_squared = r2_score(tm, af)
        r2.append(R_squared)
        best_fit_list.append((i, af, R_squared))
        plt.plot(wl, af, plot_color[i], lw=2, label=f'{i}th')
        plt.scatter(wl, tm, s=10)

    best_fit_list = sorted(best_fit_list, key=lambda x: abs(x[2] - 1))[:3]

    position_x, position_y = 0.4, 0.5
    for i, af, R_squared in best_fit_list:
        text_color = 'red' if R_squared == max([item[2] for item in best_fit_list]) else 'black'
        plt.text(position_x, position_y, f'Degree: {i}\nR_squared: {R_squared:.15f}',
                 color=text_color,
                 transform=plt.gca().transAxes,
                 fontsize=8, fontweight='bold')
        position_y -= 0.1


    plt.title('Transmission spectra - processed and fitting', fontdict=total_font_title)
    plt.xlabel('Wavelength [nm]', fontdict=total_font_axis)
    plt.ylabel('Measured transmission [dB]', fontdict=total_font_axis)
    plt.legend(ncol=3,loc='lower center', fontsize=9)
    plt.grid(True,axis='both', color='gray', alpha=0.5, linestyle='--')
    #-------------------------Flat Transmission spectra--------------------------------------

    afc = np.polyfit(wl,tm,8)
    af = np.polyval(afc,wl)

    plt.subplot(2,3,3)
    color_number=0
    DC_bias = -2.0

    for i in root.iter():
        if i.tag == 'WavelengthSweep':
            if i.attrib.get('DCBias') == str(DC_bias):
                wl1 = list(map(float, i.find('L').text.split(',')))
                tm1 = list(map(float, i.find('IL').text.split(',')))
                tm_flat = []  #ref 값을 뺸 transmission값
                for k in range(len(tm1)):
                    a = tm1[k] - af[k]
                    tm_flat.append(a)
                plt.plot(wl1, tm_flat, plot_color[color_number], label=f'{DC_bias}V')
                DC_bias += 0.5
                color_number += 1
    ref_flat = [] #ref값도 평평하게 만들기
    for k in range(len(tm)):
        a = tm[k] - af[k]
        ref_flat.append(a)
    plt.plot(wl, ref_flat, color='r', linestyle=':')
    plt.legend(ncol=3, loc='lower center', fontsize=10)
    plt.title('Flat Transmission spectra - as measured', fontdict=total_font_title)
    plt.xlabel('Wavelength [nm]', fontdict=total_font_axis)
    plt.ylabel('Measured transmission [dB]', fontdict=total_font_axis)
    plt.grid(True,axis='both', color='gray', alpha=0.5, linestyle='--')
