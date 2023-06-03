import pandas as pd
from csv_data import *
from New_Folder import *
from IVtm_data import *
from Tm_plot import *
import time
from tqdm import tqdm


def Create_csv(file, Owner):

    data = []
    for x in tqdm(file, desc='Saving xlsx files '):
        element = [Data_csv(x)[0], Data_csv(x)[1], Data_csv(x)[2], Data_csv(x)[3], Data_csv(x)[4], Data_csv(x)[5],
             Data_csv(x)[6], Data_csv(x)[10], 'Version 1', Owner,  Data_csv(x)[7], Data_csv(x)[8], data_tm(x)[2],
             data_tm(x)[3], Data_csv(x)[9], data_tm(x)[0], data_tm(x)[1], data_IV(x)[0], data_IV(x)[1], data_IV(x)[2], tm_plot(x)]
        data.append(element)
        time.sleep(0.1)
    Excel_data = pd.DataFrame(np.array(data),
                      columns=["Lot", "Wafer", "Mask", "TestSite", "Name", "Date", "Operator","Script ID", "Script Version",
                               "Script Owner", "Row", "Column", "Error Flag", "Error Description", "Analysis Wavelength(nm)",
                               "Rsq of Ref.spectrum(Nth)", "Max transmission of Ref spec. (dB)", "Rsq of IV", "I at -1V[A]", "I at 1V[A]", "V_piL"])

    path = './res/'

    with pd.ExcelWriter(path + f"/Analysis_Result_({now.strftime('%Y%m%d_%H%M%S')}).xlsx") as writer:
        Excel_data.to_excel(writer)

