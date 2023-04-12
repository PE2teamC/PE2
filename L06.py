import xml.etree.ElementTree as ET  # XML 파일 parsing에 필요한 모듈
import numpy as np  # 배열 연산에 필요한 모듈
import matplotlib.pyplot as plt  # 그래프를 그리기 위한 모듈
from sklearn.metrics import r2_score

#####추가#####ddd
# XML 파일 parsing
tree = ET.parse("HY202103_D07_(0,0)_LION1_DCM_LMZC.xml")
root = tree.getroot()

# 축 레이블과 제목에 적용될 폰트 설정을 변수로 저장
font_axis = {'weight': 'bold', 'size': 12}
font_title = {'weight': 'bold', 'size': 18}


for i in root.iter():  # XML 파일의 모든 요소에 대해서 반복문 수행
    if  i.tag == 'Modulator':  # 요소의 이름이 'Modulator'인 경우
        if i.attrib.get('Name') == 'DCM_LMZC_ALIGN':  # 해당 요소의 속성 중 'Name' 속성의 값이 'DCM_LMZC_ALIGN'인 경우
            wl = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('L').text.split(',')))    # 해당 요소에서 'L'이라는 이름을 가진 하위 요소의 값의 list를 wl 변수에 할당
            tm = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('IL').text.split(',')))   # 해당 요소에서 'IL'이라는 이름을 가진 하위 요소의 값의 list를 tm 변수에 할당
            plt.plot(wl, tm, color='purple', linestyle=':')  # wl, tm list에 대응하는 값들을 x, y 값으로 해서 plot

best_fit_list = []
for i in range(1, 9):
    afc = np.polyfit(wl, tm, i)
    af = np.polyval(afc, wl)
    R_squared = r2_score(tm, af)
    best_fit_list.append((i, af, R_squared))

best_fit_list = sorted(best_fit_list, key=lambda x: abs(x[2] - 1))[:3]

position_x, position_y = 0.4, 0.6
for i, af, R_squared in best_fit_list:
    plt.plot(wl, af, 'r--', lw=2, label=f'degree={i}')
    plt.scatter(wl, tm, s=10, label='data')
    plt.text(position_x, position_y, f'Degree: {i}\nR_squared: {R_squared:.10f}',
             transform=plt.gca().transAxes,
             fontsize=8, fontweight='bold')
    position_y -= 0.1
#전체 박스 추가하면 좋을듯

#-----------------------------------------------------------------------------------
# 범례, 제목, 축 레이블, 그리드 설정을 적용합니다.
plt.title('Transmission spectra - as measured', fontdict=font_title)
plt.xlabel('Wavelength [nm]', fontdict=font_axis)
plt.ylabel('Measured transmission [dB]', fontdict=font_axis)
plt.legend(ncol=3,loc='lower center', fontsize=9)  # 범례 위치 설정
plt.grid(True,axis='both', color='gray', alpha=0.5, linestyle='--')  # 가독성을 위해 gird 삽입
plt.savefig('IV-analysis_trans.png')      # 저장
plt.show()                          # 출력

#-----------------------------------------------------------------------------------