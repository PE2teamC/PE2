import xml.etree.ElementTree as etree
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
from lmfit import Model
import math

def tm_plot(x):
    xml_file = etree.parse(x)
    root = xml_file.getroot()




    font_axis = {'weight': 'bold', 'size': 10}
    font_title = {'weight': 'bold', 'size': 12}
    # Wavelength-Transmission(Raw data)
    wl_list, tm_list = [], []
    wl_ref, tm_ref = [], []
    DC_bias = -2.0
    plot_color = ['lightcoral', 'coral', 'gold', 'lightgreen', 'lightskyblue', 'plum']
    color_number = 0

    plt.subplot(2, 3, 1)
    for i in root.iter():
        if i.tag == 'WavelengthSweep':
            if i.attrib.get('DCBias') == str(DC_bias):
                wl = list(map(float, i.find('L').text.split(',')))
                wl_list.append(wl)
                tm = list(map(float, i.find('IL').text.split(',')))
                tm_list.append(tm)
                plt.plot(wl, tm, plot_color[color_number], label=f'DCBias = {DC_bias}V')
                DC_bias += 0.5
                color_number += 1

            plt.title('Transmission spectra - as measured', fontdict=font_title)
            plt.xlabel('Wavelength[nm]', fontdict=font_axis)
            plt.ylabel('Measured transmission[dB]', fontdict=font_axis)
            plt.legend(loc='lower center', ncol=2, fontsize=6)

        # Reference
        elif i.tag == 'Modulator':
            if i.attrib.get('Name') == 'DCM_LMZC_ALIGN' or i.attrib.get('Name') == 'DCM_LMZO_ALIGN':
                wl_ref = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('L').text.split(',')))
                tm_ref = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('IL').text.split(',')))
                plt.plot(wl_ref, tm_ref, color='#7f7f7f', linestyle=':', label='Reference')

                # plt.plot(wl_ref, tm_ref, color='#7f7f7f', linestyle=':', label='Reference')

    # Wavelength-Transmission(Fitting)
    rsq_ref = []
    for p in range(1, 9):
        fit = np.polyfit(np.array(wl_ref), np.array(tm_ref), p)
        fit_eq = np.poly1d(fit)
        rsq_ref.append(r2_score(tm_ref, fit_eq(wl_ref)))
        # plt.plot(wl_ref, fit_eq(wl_ref), label=f'{p}th R² : {r2_score(tm_ref, fit_eq(wl_ref))}')

    # plt.title('Transmission spectra - as measured', fontdict=font_title)
    # plt.xlabel('Wavelength[nm]', fontdict=font_axis)
    # plt.ylabel('Measured transmission[dB]', fontdict=font_axis)
    # plt.legend(loc='lower center', fontsize=8)


    plt.subplot(2, 3, 2)
    DC_bias = -2.0
    linear_x = []
    linear_y = []
    def find_local_maxima_idx(data):
        maxima_idx = []
        for i in range(200, len(data) - 200):
            if data[i] > max(data[i - 200:i]) and data[i] > max(data[i + 1:i + 200]):
                maxima_idx.append(i)
        return maxima_idx

    wl_flat_l, tm_flat_l = [], []
    for j in range(6):
        maxidx = find_local_maxima_idx(tm_list[j] - fit_eq(wl_list[j]))
        for i in maxidx:
            linear_x.append(wl_list[j][i])
            linear_y.append(tm_list[j][i] - fit_eq(wl_list[j][i]))

        afc = np.polyfit(linear_x, linear_y, 1)

        af = np.poly1d(afc)

        wl_flat = wl_list[j]
        wl_flat_l.append(wl_flat)

        tm_flat = tm_list[j] - fit_eq(wl_list[j]) - af(wl_list[j])
        tm_flat_l.append((tm_flat))

        plt.plot(wl_flat, tm_flat, label=f'DC_bias={DC_bias}V')

        DC_bias += 0.5

    plt.title('Flat Transmission spectra - as measured', fontdict=font_title)
    plt.xlabel('Wavelength[nm]', fontdict=font_axis)
    plt.ylabel('Measured transmission[dB]', fontdict=font_axis)
    plt.legend(loc='lower center', ncol=2, fontsize=6)

    plt.subplot(2, 3, 3)
    DC_bias = -2.0
    for i in range(6):
        if wl_flat_l[i][0] >= 1500:
            wl_a, tm_a = [], []
            for a in wl_flat_l[i]:
                if (1549 < a < 1551):
                    wl_a.append(a)
                    wl_index = wl_flat_l[i].index(wl_a[0])

            for b in tm_flat_l[i][wl_index:(wl_index + len(wl_a))]:
                tm_a.append(b)

            plt.plot(wl_a, tm_a, ':', label=f'DC_bias={DC_bias}V')
            DC_bias += 0.5

        else:
            wl_a, tm_a = [], []
            for a in wl_flat_l[i]:
                if (1309 < a < 1311):
                    wl_a.append(a)
                    wl_index = wl_flat_l[i].index(wl_a[0])

            for b in tm_flat_l[i][wl_index:(wl_index + len(wl_a))]:
                tm_a.append(b)

            plt.plot(wl_a, tm_a, ':', label=f'DC_bias={DC_bias}V')
            DC_bias += 0.5

    plt.title('Flat Transmission spectra - as measured', fontdict=font_title)
    plt.xlabel('Wavelength[nm]', fontdict=font_axis)
    plt.ylabel('Measured transmission[dB]', fontdict=font_axis)
    plt.xticks(np.arange(1549, 1551.1, 0.5))
    plt.legend(loc='upper right', ncol=2, fontsize=6)


    plt.subplot(2, 3, 5)
    def fitting_find_n_eff(wave_length, n_eff):
        I_0=0.001
        delta_l = 40 * 10 ** (-6)
        pi = math.pi
        return I_0 * np.array(list(map(math.sin, pi * delta_l * n_eff / wave_length / 10 ** (-9)))) ** 2
    model = Model(fitting_find_n_eff, independent_vars=["wave_length"],param_names=['n_eff'])
    model.set_param_hint('n_eff',value=4.2,min=0.0,max=10.0)



    linear_x = []
    linear_y = []
    linear_tm = []

    bias=[-2.0,-1.5,-1.0,-0.5,0.0,0.5]
    v0ind=bias.index(0)

    maxidx = find_local_maxima_idx(tm_list[v0ind] - fit_eq(wl_list[v0ind]))
    for i in maxidx:
        linear_x.append(wl_list[v0ind][i])
        linear_y.append(tm_list[v0ind][i] - fit_eq(wl_list[v0ind][i]))


    afc = np.polyfit(linear_x, linear_y, 1)


    af = np.poly1d(afc)
    flat_tm_list = [tm - fit_eq(wl) - af(wl) for wl, tm in zip(wl_list[v0ind], tm_list[v0ind])]


    for k in flat_tm_list:
        linear_tm.append(10**(k/10)/1000)

    result = model.fit(linear_tm, wave_length=wl_list[v0ind])
    n_eff_value = result.best_values['n_eff']


    bias=[-2.0,-1.5,-1.0,-0.5,0.0,0.5]
    linear_x = []
    linear_y = []
    linear_tm = []
    delta_n_eff_list=[]
    for i, j in zip(bias,range(6)):
        def fitting_delta_n_eff(wave_length, n_eff ,delta_n_eff):
            I_0 = 0.001
            delta_l = 40 * 10 ** (-6)
            l = 500 * 10 ** (-6)
            V=bias[j]

            pi = math.pi
            return I_0 * np.array(list(map(math.sin, pi * delta_l * n_eff / wave_length / 10 ** (-9))) + pi * l * V * delta_n_eff / wave_length / 10 ** (-9)) ** 2

        fmodel = Model(fitting_delta_n_eff)
        params = fmodel.make_params(delta_n_eff=0, n_eff=n_eff_value)

        maxidx = find_local_maxima_idx(tm_list[j] - fit_eq(wl_list[j]))
        for t in maxidx:
            linear_x.append(wl_list[j][t])
            linear_y.append(tm_list[j][t] - fit_eq(wl_list[j][t]))


        afc = np.polyfit(linear_x, linear_y, 1)


        af = np.poly1d(afc)
        flat_tm_list = [tm - fit_eq(wl) - af(wl) for wl, tm in zip(wl_list[j], tm_list[j])]

        for k in flat_tm_list:
            linear_tm.append(10 ** (k / 10)/1000)
        plt.plot(wl_list[j],linear_tm,label=f'DCBias = {DC_bias}V')

        fresult = fmodel.fit(linear_tm, params, wave_length=wl_list[j])
        plt.plot(wl_list[j], fresult.best_fit,label=f'DCBias = {DC_bias}V fit')
        delta_n_eff_value = fresult.best_values['delta_n_eff']

        delta_n_eff_list.append(delta_n_eff_value)

        linear_y = []
        linear_x = []
        linear_tm = []

    plt.title('Flat-Flat linear Transmission spectra', fontdict=font_title)
    plt.xlabel('wavelength [nm]', fontdict=font_axis)
    plt.ylabel('intensity', fontdict=font_axis)
    plt.legend(loc='lower center', ncol=2, fontsize=6)

    plt.subplot(2, 3, 6)
    plt.plot(bias,delta_n_eff_list)
    plt.grid(True, axis='both', color='gray', alpha=0.5, linestyle='--')  # 가독성을 위해 grid 삽입
    plt.title('n-V graph', fontdict=font_title)
    plt.xlabel('voltage [V]', fontdict=font_axis)
    plt.ylabel('del_n_eff', fontdict=font_axis)

