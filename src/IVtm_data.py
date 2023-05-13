import xml.etree.ElementTree as etree
from sklearn.metrics import r2_score
from lmfit import Model
import numpy as np

def data_IV(x):
    voltage_list, current_list = [], []

    xml_file = etree.parse(str(x))
    root = xml_file.getroot()
    for i in root.iter():
        if i.tag == 'Voltage':
            voltage_list = list(map(float, i.text.split(',')))
        elif i.tag == 'Current':
            current_list = list(map(float, i.text.split(',')))

    voltage = np.array(voltage_list)
    current = np.abs(current_list)
    minus1 = current[4]
    plus1 = abs(current[-1])



    def diode_eq(V_D, I_s, n):
        return I_s * (np.exp((V_D / (n * 0.026)) - 1))

    p_num = 7
    af = np.poly1d(np.polyfit(voltage[:10], current[:10], p_num))

    I_s = np.mean(current[:7])


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
    R_squared = r2_score(current, fit_plot)


    return R_squared, minus1, plus1


def data_tm(x):
    wl, tm = [], []

    xml_file = etree.parse(str(x))
    root = xml_file.getroot()
    for i in root.iter():
        if i.tag == 'Modulator':
            if i.attrib.get('Name') == 'DCM_LMZC_ALIGN':
                wl = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('L').text.split(',')))
                tm = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('IL').text.split(',')))

    r2 = []
    for i in range(1, 9):
        afc = np.polyfit(wl, tm, i)
        af = np.polyval(afc, wl)
        R_squared = r2_score(tm, af)
        r2.append(R_squared)
        r2_tm = max(r2)

    for i in r2:
        if i >= 0.95:
            ErrorFlag = 0
            ErrorDescription = "No Error"
        else:
            ErrorFlag = 1
            ErrorDescription = "Ref. spec. Error"

    max_tm = np.max(tm)

    return r2_tm, max_tm, ErrorFlag, ErrorDescription