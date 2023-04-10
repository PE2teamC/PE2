import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt

# XML 파일을 읽어서 ElementTree 객체를 생성합니다.
tree = ET.parse("HY202103_D07_(0,0)_LION1_DCM_LMZC.xml")
root = tree.getroot()

# 축 레이블과 제목에 적용될 폰트 설정을 변수로 저장합니다.
font_axis = {'weight': 'bold', 'size': 12}
font_title = {'weight': 'bold', 'size': 18}

# 1행 2열의 그래프 중 첫 번째 그래프를 생성합니다.
plt.subplot(1, 2, 1)




# Voltage 태그와 Current 태그에서 데이터를 추출합니다.
voltage_list=[]
current_list=[]
for i in root.iter():
    if i.tag == 'Voltage':
        voltage_list = list(map(float, i.text.split(',')))
    elif i.tag == 'Current':
        current_list = list(map(float, i.text.split(',')))

# 추출한 데이터를 NumPy 배열로 변환합니다.
voltage = np.array(voltage_list)
current = np.abs(current_list)

def calc_R_squared():
    afc = np.polyfit(voltage, current, 12)
    af = np.poly1d(afc)
    SSE = np.sum((af(voltage) - np.mean(current)) ** 2)
    SST = np.sum((current - np.mean(current)) ** 2)
    return SSE/SST
r_squared = calc_R_squared()
# 12차 다항식을 이용해 best-fit 곡선을 구합니다.
f = np.poly1d(np.polyfit(voltage, current, 12))

# best-fit 곡선과 데이터를 그래프에 그립니다.
plt.plot(voltage, f(voltage), linestyle='--', lw=2, color='r', label='best-fit')
plt.scatter(voltage, current, s=15, label='data')

# 범례, 제목, 축 레이블, 그리드 설정을 적용합니다.
plt.legend(loc='best') # 범례 위치를 최적화합니다.
plt.title('IV-analysis', fontdict=font_title)
plt.xlabel('Voltage [V]', fontdict=font_axis)
plt.ylabel('Current [A]', fontdict=font_axis)
plt.grid(True,axis='both', color='gray', alpha=0.5, linestyle='--') # 가독성을 위해 그리드를 삽입합니다.
plt.yscale('logit') # y축 스케일을 로그 스케일로 변경합니다.

# 주어진 voltage 값에 해당하는 current 값을 출력합니다.
position_x, position_y=0.05,0.7  # 주석: 현재 위치
for x, y in zip([-2, -1, 1], [current[voltage == -2][0], current[voltage == -1][0], current[voltage == 1.0][0]]):
    # 주석: x,y 값이 주어진 배열에 따라 결정됨
    if y < 1e-3:
        plt.text(position_x, position_y, f"{x}V: {y:.10e}A", transform=plt.gca().transAxes, fontsize=10)  # 주석: 텍스트로 표시될 값 지정
    else:
        plt.text(position_x, position_y, f"{x}V: {y:.10f}A", transform=plt.gca().transAxes, fontsize=10)  # 주석: 텍스트로 표시될 값 지정
    position_y-=0.1  # 주석: 위치를 변경하여 다음에 표시될 위치 결정
plt.text(0.05, 0.8, f"R-squared: {r_squared:.20f}", transform=plt.gca().transAxes, bbox=dict(facecolor='none', edgecolor='white', boxstyle='round,pad=0.5'), fontsize=10)  # 주석: 텍스트로 표시될 값 지정


plt.subplot(1, 2, 2)  # 주석: 그래프 위치 설정

wl, tm = [], []
DC_bias = -2.0
plot_color = ['lightcoral', 'coral', 'gold', 'lightgreen', 'lightskyblue', 'plum']
color_number = 0

for i in root.iter():  # XML 파일의 모든 요소에 대해서 반복문 수행
    if i.tag == 'WavelengthSweep':  # 요소의 이름이 'WavelengthSweep'인 경우
        if i.attrib.get('DCBias') == str(DC_bias):  # 해당 요소의 속성 중 'DCBias' 속성의 값이 DC_bias와 같은 경우
            wl = list(map(float, i.find('L').text.split(',')))  # 해당 요소에서 'L'이라는 이름을 가진 하위 요소의 문자열 값을 ','를 기준으로 분리하여 실수형으로 변환한 리스트를 wl 변수에 할당
            tm = list(map(float, i.find('IL').text.split(',')))  # 해당 요소에서 'IL'이라는 이름을 가진 하위 요소의 문자열 값을 ','를 기준으로 분리하여 실수형으로 변환한 리스트를 tm 변수에 할당
            plt.plot(wl, tm, plot_color[color_number], label=f'{DC_bias}V')  # wl과 tm 리스트에 대응하는 값들을 x, y 값으로 해서 그래프를 그리고, DC_bias와 'V' 문자열을 결합하여 label로 설정
            DC_bias += 0.5  # DC_bias 값을 0.5 증가시킴
            color_number += 1  # color_number 값을 1 증가시킴
    elif i.tag == 'Modulator':  # 요소의 이름이 'Modulator'인 경우
        if i.attrib.get('Name') == 'DCM_LMZC_ALIGN':  # 해당 요소의 속성 중 'Name' 속성의 값이 'DCM_LMZC_ALIGN'인 경우
            wl = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('L').text.split(',')))  # 해당 요소에서 'PortCombo' -> 'WavelengthSweep' -> 'L'이라는 하위 요소의 문자열 값을 ','를 기준으로 분리하여 실수형으로 변환한 리스트를 wl 변수에 할당
            tm = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('IL').text.split(',')))  # 해당 요소에서 'PortCombo' -> 'WavelengthSweep' -> 'IL'이라는 하위 요소의 문자열 값을 ','를 기준으로 분리하여 실수형으로 변환한 리스트를 tm 변수에 할당
            plt.plot(wl, tm, color='purple', linestyle=':')  # wl과 tm 리스트에 대응하는 값들을 x, y 값으로 해서 그래프를 그리고, 색상을 purple, 선스타일을 점선으로 설정



plt.legend(ncol=3,loc='lower center', fontsize=14)  # 주석: 범례 표시

plt.title('Transmission spectra - as measured', fontdict=font_title)  # 주석: 그래프 제목
plt.xlabel('Wavelength [nm]', fontdict=font_axis)  # 주석: x축 레이블
plt.ylabel('Measured transmission [dB]', fontdict=font_axis)  # 주석: y축 레이블

plt.grid(True,axis='both', color='gray', alpha=0.5, linestyle='--')  # 주석: 그리드 추가
plt.savefig('IV-analysis.png')                                     # 저장
plt.show()

