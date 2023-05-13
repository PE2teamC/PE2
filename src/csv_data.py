import xml.etree.ElementTree as etree
from datetime import datetime


def Data_csv(x):

    Lot, Wafer, Mask, TestSite, Name, Date, Operator, Row, Column, Analysis_Wavelength = '','','','','','','','','',''

    xml_file = etree.parse(str(x))
    root = xml_file.getroot()

    for data in root.iter():
        if data.tag == 'OIOMeasurement':
            Date= data.get('CreationDate')
            creation_date = datetime.strptime(Date, "%a %b %d %H:%M:%S %Y")
            Date_str = creation_date.strftime("%Y%m%d_%H%M%S")
            Operator= data.get('Operator')

        elif data.tag == 'TestSiteInfo':
            Lot = data.get('Batch')
            Column = data.get('DieColumn')
            Row = data.get('DieRow')
            TestSite = data.get('TestSite')
            substring = str(TestSite).split("_")[1]
            scriptid = "process_" + substring

            Wafer = data.get('Wafer')
            Mask = data.get('Maskset')

        elif data.tag == 'ModulatorSite':
            Name = data.find('Modulator').get('Name')

        elif data.tag == 'DesignParameter':
            if data.attrib.get('Name') == 'Design wavelength':
                Analysis_Wavelength = data.text


    return Lot, Wafer, Mask, TestSite, Name, Date_str, Operator, Row, Column, Analysis_Wavelength, scriptid

