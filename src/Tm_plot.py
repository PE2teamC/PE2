import xml.etree.ElementTree as etree
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
from lmfit import Model
import math

def tm_plot(x):
    xml_file = etree.parse(x)
    root = xml_file.getroot()


    def find_local_maxima_idx(data):
        maxima_idx = []
        for i in range(200, len(data) - 200):
            if data[i] > max(data[i - 200:i]) and data[i] > max(data[i + 1:i + 200]):
                maxima_idx.append(i)
        return maxima_idx

    def find_local_minima_idx(data):
        minima_idx = []
        for i in range(200, len(data) - 200):
            if data[i] < min(data[i - 200:i]) and data[i] < min(data[i + 1:i + 201]):
                minima_idx.append(i)
        return minima_idx

    def find_closest_value_index(data_list, index_list, target_value):
        closest_value = None
        closest_index = None
        for index in index_list:
            if index < len(data_list):
                current_value = data_list[index]
                if closest_value is None or abs(current_value - target_value) < abs(closest_value - target_value):
                    closest_value = current_value
                    closest_index = index
        return closest_index

    def linear_to_db(linear_data):
        # 선형 스케일 데이터에 대한 dB 스케일 변환
        db_data = [10 * math.log10(1000*x) for x in linear_data]
        return db_data

    font_axis = {'weight': 'bold', 'size': 10}
    font_title = {'weight': 'bold', 'size': 12}
    font_legend = {'weight': 'bold', 'size': 10}
    # Wavelength-Transmission(Raw data)------------------------------
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
            plt.legend(loc='lower center', ncol=2, fontsize=8)

        # Reference
        elif i.tag == 'Modulator':
            if i.attrib.get('Name') == 'DCM_LMZC_ALIGN' or i.attrib.get('Name') == 'DCM_LMZO_ALIGN':
                wl_ref = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('L').text.split(',')))
                tm_ref = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('IL').text.split(',')))
                plt.plot(wl_ref, tm_ref, color='#7f7f7f', linestyle=':', label='Reference')

    # Wavelength-Transmission(Fitting)
    rsq_ref = []
    for p in range(1, 9):
        fit = np.polyfit(np.array(wl_ref), np.array(tm_ref), p)
        fit_eq = np.poly1d(fit)
        rsq_ref.append(r2_score(tm_ref, fit_eq(wl_ref)))


    # flat-flat Wavelength-Transmission-------------------------------------------------
    plt.subplot(2, 3, 2)
    DC_bias = -2.0
    linear_x = []
    linear_y = []

    wl_flat_l, tm_flat_l = [], []
    for j in range(6):
        maxidx = find_local_maxima_idx(tm_list[j] - fit_eq(wl_list[j]))
        # print(maxidx)
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

    plt.title('Flat-Flat Transmission spectra - as measured', fontdict=font_title)
    plt.xlabel('Wavelength[nm]', fontdict=font_axis)
    plt.ylabel('Measured transmission[dB]', fontdict=font_axis)
    plt.legend(loc='lower center', ncol=2, fontsize=8)




    plt.subplot(2, 3, 5)
    def fitting_find_n_eff(wave_length, n_eff,I_0):

        delta_l = 40 * 10 ** (-6)
        pi = math.pi
        return I_0 * np.array(list(map(math.sin, pi * delta_l * n_eff / wave_length / 10 ** (-9)))) ** 2
    model = Model(fitting_find_n_eff, independent_vars=["wave_length"],param_names=['n_eff'])
    model.set_param_hint('n_eff',value=4.1,min=0.0,max=10.0)
    model.set_param_hint('I_0',value=0.0005,min=0.0,max=0.001)


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
    I_0_value = result.best_values['I_0']

    bias=[-2.0,-1.5,-1.0,-0.5,0.0,0.5]
    linear_x = []
    linear_y = []
    linear_tm = []
    fit_db_scale=[]
    # print(I_0_value,n_eff_value)
    delta_n_eff_list=[]
    for i, j in zip(bias,range(6)):
        def fitting_delta_n_eff(wave_length,delta_n_eff):
            I_0 = I_0_value
            n_eff= n_eff_value
            delta_l = 40 * 10 ** (-6)
            l = 500 * 10 ** (-6)
            # V=i

            pi = math.pi
            return I_0 * np.array(list(map(math.sin, pi * delta_l * n_eff / wave_length / 10 ** (-9) + pi * l  * delta_n_eff / wave_length / 10 ** (-9)))) ** 2

        fmodel = Model(fitting_delta_n_eff, independent_vars=["wave_length"], param_names=['delta_n_eff'])

        fmodel.set_param_hint('delta_n_eff', value=0.0001, min=-1, max=1)

        maxidx = find_local_maxima_idx(tm_list[j] - fit_eq(wl_list[j]))
        for t in maxidx:
            linear_x.append(wl_list[j][t])
            linear_y.append(tm_list[j][t] - fit_eq(wl_list[j][t]))


        afc = np.polyfit(linear_x, linear_y, 1)
        af = np.poly1d(afc)
        flat_tm_list = [tm - fit_eq(wl) - af(wl) for wl, tm in zip(wl_list[j], tm_list[j])]
        best_fit_db_scale = []
        for k in flat_tm_list:
            linear_tm.append(10 ** (k / 10)/1000)

        fresult = fmodel.fit(linear_tm, wave_length=wl_list[j])

        fit_db_scale=linear_to_db((fresult.best_fit).tolist())
        plt.subplot(2, 3, 3)
        best_fit_db_scale.append(fit_db_scale)

        plt.plot(wl_flat_l[j],best_fit_db_scale[0],label=f'DCBias = {i}V fit')

        plt.subplot(2, 3, 5)

        plt.plot(wl_list[j], fresult.best_fit,label=f'DCBias = {i}V fit')

        delta_n_eff_value = fresult.best_values['delta_n_eff']

        delta_n_eff_list.append(np.array(delta_n_eff_value))

        linear_y = []
        linear_x = []
        linear_tm = []
        fit_db_scale=[]

    plt.subplot(2, 3, 5)
    plt.title('Fitted Itensity Graph', fontdict=font_title)
    plt.xlabel('wavelength [nm]', fontdict=font_axis)
    plt.ylabel('intensity', fontdict=font_axis)
    plt.legend(loc='lower center', ncol=2, fontsize=8)
    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))

    plt.subplot(2, 3, 6)
    if wl_flat_l[0][0] >= 1500:
        V_piL = 1550 * 10 ** (-7) * 2 / 2 / (delta_n_eff_list[0])
        plt.text(0.7, 0.9, f"V_piL: {V_piL:.5f}",
                 transform=plt.gca().transAxes,
                 bbox=dict(facecolor='none', edgecolor='gray', boxstyle='round,pad=0.5'),
                 fontsize=10, fontweight='bold')


    else:
        V_piL = 1310 * 10 ** (-7) * 2 / 2 / (delta_n_eff_list[0])
        plt.text(0.7, 0.9, f"V_piL: {V_piL:.5f}",
                 transform=plt.gca().transAxes,
                 bbox=dict(facecolor='none', edgecolor='gray', boxstyle='round,pad=0.5'),
                 fontsize=10, fontweight='bold')


    plt.plot(bias,delta_n_eff_list)
    plt.grid(True, axis='both', color='gray', alpha=0.5, linestyle='--')  # 가독성을 위해 grid 삽입
    plt.title('n-V graph', fontdict=font_title)
    plt.xlabel('voltage [V]', fontdict=font_axis)
    plt.ylabel('del_n_eff', fontdict=font_axis)
    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    # 1330, 1550 확대(fitting)-------------------------------------------------
    plt.subplot(2, 3, 3)
    DC_bias = -2.0
    for i in range(6):
        if wl_flat_l[i][0] >= 1500:


            plt.xlim(wl_flat_l[i][find_closest_value_index(wl_flat_l[i],find_local_minima_idx(tm_flat_l[i]),1550)]-4,
                      wl_flat_l[i][find_closest_value_index(wl_flat_l[i],find_local_minima_idx(tm_flat_l[i]),1550)]+4)
            plt.scatter(wl_flat_l[i],tm_flat_l[i],s=4)

        else:
            plt.xlim(wl_flat_l[i][find_closest_value_index(wl_flat_l[i],find_local_minima_idx(tm_flat_l[i]),1310)]-4,
                     wl_flat_l[i][find_closest_value_index(wl_flat_l[i],find_local_minima_idx(tm_flat_l[i]),1310)]+4)
            plt.scatter(wl_flat_l[i],tm_flat_l[i],s=4)

    plt.title('Enlarged Transmission spectra', fontdict=font_title)
    plt.xlabel('Wavelength[nm]', fontdict=font_axis)
    plt.ylabel('Measured transmission[dB]', fontdict=font_axis)


    legend1 = plt.legend(['o : raw data', '- : fitted graph'], fontsize=5, ncol=1, loc=(0.01, 0.85), handlelength=0,
                         prop=font_legend)
    plt.gca().add_artist(legend1)
    plt.legend(loc='lower center', ncol=2, fontsize=8)

    return V_piL
