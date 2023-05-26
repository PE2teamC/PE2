import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from lmfit import Model

#--------------------Font설정-----------------------------------------
total_font_axis = {'weight': 'bold', 'size': 10}
total_font_title = {'weight': 'bold', 'size': 12}

font_axis = {'weight': 'bold', 'size': 12}
font_title = {'weight': 'bold', 'size': 18}
#---------------------------------------------------------------------


def IV_plot(x):

    xml_file = ET.parse(str(x))
    root = xml_file.getroot()

    plt.subplot(2, 3, 4)
    voltage_list, current_list=[], []

    for i in root.iter():
        if i.tag == 'Voltage':
            voltage_list = list(map(float, i.text.split(',')))
        elif i.tag == 'Current':
            current_list = list(map(float, i.text.split(',')))

    voltage = np.array(voltage_list)
    current = np.abs(current_list)

    def diode_eq(V_D, I_s, n):
        return I_s*(np.exp((V_D/(n*0.026))-1))

    p_num = 7
    af = np.poly1d(np.polyfit(voltage[:10], current[:10], p_num))

    I_s=np.mean(current[:7])

    Cmodel = Model(diode_eq)
    params = Cmodel.make_params(I_s=I_s, n=2)
    result = Cmodel.fit(current[10:], params, V_D=voltage[10:])

    fit_plot = []
    n1, n2 = 0, 0
    for v in voltage:
        if v <= 0.25:
            fit_plot.append(af(voltage[n1]))
            n1 += 1
        else:
            fit_plot.append(result.best_fit.tolist()[n2])
            n2 += 1
    R_squared=r2_score(current, fit_plot)

    plt.plot(voltage, fit_plot, 'r--', label='best-fit')
    plt.scatter(voltage, current, c='k',s=20, label='data')

    position_x, position_y=0.05,0.6

    for x, y in zip([-2, -1, 1], [current[voltage == -2][0], current[voltage == -1][0], current[voltage == 1.0][0]]):
        if y < 1e-3:
            plt.text(position_x, position_y, f"{x}V: {y:.10e}A", transform=plt.gca().transAxes, fontsize=10)
        else:
            plt.text(position_x, position_y, f"{x}V: {y:.10f}A", transform=plt.gca().transAxes, fontsize=10)
        position_y-=0.1
    # R_squared 출력
    plt.text(0.05, 0.7, f"R-squared: {R_squared:.15f}",
             transform=plt.gca().transAxes,
             bbox=dict(facecolor='none', edgecolor='gray', boxstyle='round,pad=0.5'),
             fontsize=10,fontweight='bold')

    plt.title('IV-analysis - with fitting', fontdict= total_font_title)
    plt.xlabel('Voltage [V]', fontdict=total_font_axis)
    plt.ylabel('Current [A]', fontdict=total_font_axis)
    plt.yscale('logit')
    plt.legend(loc='best')
    plt.grid(True,axis='both', color='gray', alpha=0.5, linestyle='--')



  