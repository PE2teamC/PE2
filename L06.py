import xml.etree.ElementTree as ET  # XML 파일 parsing에 필요한 모듈
import numpy as np  # 배열 연산에 필요한 모듈
import matplotlib.pyplot as plt  # 그래프를 그리기 위한 모듈
from sklearn.metrics import r2_score
#살짝 수정함 다시함.
#그래프를 모았을 때 폰트설정
total_font_axis = {'weight': 'bold', 'size': 10}
total_font_title = {'weight': 'bold', 'size': 12}

# 축 레이블과 제목에 적용될 폰트 설정을 변수로 저장
font_axis = {'weight': 'bold', 'size': 12}
font_title = {'weight': 'bold', 'size': 18}

# XML 파일 parsing
tree = ET.parse("HY202103_D07_(0,0)_LION1_DCM_LMZC.xml")
root = tree.getroot()
# ------------------IV_graph-------------------------------------------
plt.subplot(2, 3, 4)
# Voltage 태그와 Current 태그에서 데이터를 추출
voltage_list, current_list=[], []
for i in root.iter():   # XML 파일의 모든 요소에 대해서 반복문 수행
    if i.tag == 'Voltage':  #요소의 이름이 'Voltage'일 경우
        voltage_list = list(map(float, i.text.split(',')))  # voltage data list 변환
    elif i.tag == 'Current':    #요소의 이름이 'Current'일 경우
        current_list = list(map(float, i.text.split(',')))  # current data list 변환

# 추출한 데이터를 NumPy 배열로 변환
voltage = np.array(voltage_list)
current = np.abs(current_list)  # data 절댓값
# 12차 다항식을 이용해 근사함수(best-fit) 함수 생성
afc = np.polyfit(voltage, current, 12)
af = np.polyval(afc,voltage)

plt.plot(voltage, af, 'r--', lw=2, label='best-fit')
plt.scatter(voltage, current, s=50, label='data')
#R_squared
R_squared = r2_score(current,af)

position_x, position_y=0.05,0.6  # 초기 위치
for x, y in zip([-2, -1, 1], [current[voltage == -2][0], current[voltage == -1][0], current[voltage == 1.0][0]]):
    # x,y 값이 주어진 배열에 따라 결정됨 (x는 voltage값, y는 current값)
    if y < 1e-3:    # 값이 1e-3보다 작은 경우
        # 지수 형태로 소수점 10번째 자리까지 출력
        plt.text(position_x, position_y, f"{x}V: {y:.10e}A", transform=plt.gca().transAxes, fontsize=10)
        # 실수 형태로 소수점 10번째 자리까지 출력
    else:
        plt.text(position_x, position_y, f"{x}V: {y:.10f}A", transform=plt.gca().transAxes, fontsize=10)
    position_y-=0.1  # y 위치를 변경하여 다음에 표시될 위치 결정
# R_squared 출력
plt.text(0.05, 0.7, f"R-squared: {R_squared:.20f}", # 위치 설정, 소수점 20번째 자리까지 출력
         transform=plt.gca().transAxes, #  Axes 좌표계(transform)를 반환, 축의 상대적인 위치로 0~1의 좌표를 지정
         bbox=dict(facecolor='none', edgecolor='gray', boxstyle='round,pad=0.5'),    # 둥근 모서리 박스 생성
         fontsize=10,fontweight='bold') # 글씨 크기, bold체 적용
# 범례, 제목, 축 레이블, 그리드 설정을 적용합니다.
plt.title('IV-analysis - with fitting', fontdict= total_font_title)
plt.xlabel('Voltage [V]', fontdict=total_font_axis)
plt.ylabel('Current [A]', fontdict=total_font_axis)
plt.yscale('logit') # y축 스케일을 로그 스케일로 변경합니다.
plt.legend(loc='best') # 범례 위치를 최적화합니다.
plt.grid(True,axis='both', color='gray', alpha=0.5, linestyle='--') # 가독성을 위해 gird 삽입

# ----------------------Transmission_graph----------------------------------

plt.subplot(2, 3, 1)
plot_color = ['lightcoral', 'coral', 'gold', 'lightgreen', 'lightskyblue', 'plum', 'navy', 'black', 'red']  # 색 list 생성
color_number = 0    # 초기 색 설정

# WavelengthSweep 태그와 Modulator 태그에서 데이터를 추출
wl, tm = [], []
DC_bias = -2.0  # 초기 DC_bias 설정
for i in root.iter():  # XML 파일의 모든 요소에 대해서 반복문 수행
    if i.tag == 'WavelengthSweep':  # 요소의 이름이 'WavelengthSweep'인 경우
        if i.attrib.get('DCBias') == str(DC_bias):  # 해당 요소의 속성 중 'DCBias' 속성의 값이 DC_bias와 같은 경우
            wl = list(map(float, i.find('L').text.split(',')))  # 해당 요소에서 'L'이라는 이름을 가진 하위 요소의 값의 list를 wl 변수에 할당
            tm = list(map(float, i.find('IL').text.split(',')))  # 해당 요소에서 'IL'이라는 이름을 가진 하위 요소의 값의 list를 tm 변수에 할당
            plt.plot(wl, tm, plot_color[color_number], label=f'{DC_bias}V')  # wl, tm list에 대응하는 값들을 x, y 값으로 해서 plot
            DC_bias += 0.5  # DC_bias 값을 0.5 증가
            color_number += 1  # 다음 색 설정
    elif i.tag == 'Modulator':  # 요소의 이름이 'Modulator'인 경우
        if i.attrib.get('Name') == 'DCM_LMZC_ALIGN':  # 해당 요소의 속성 중 'Name' 속성의 값이 'DCM_LMZC_ALIGN'인 경우
            wl = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('L').text.split(',')))    # 해당 요소에서 'L'이라는 이름을 가진 하위 요소의 값의 list를 wl 변수에 할당
            tm = list(map(float, i.find('PortCombo').find('WavelengthSweep').find('IL').text.split(',')))   # 해당 요소에서 'IL'이라는 이름을 가진 하위 요소의 값의 list를 tm 변수에 할당
            plt.plot(wl, tm, color='purple', linestyle=':')  # wl, tm list에 대응하는 값들을 x, y 값으로 해서 plot


# 범례, 제목, 축 레이블, 그리드 설정을 적용합니다.
plt.title('Transmission spectra - as measured', fontdict=total_font_title)
plt.xlabel('Wavelength [nm]', fontdict=total_font_axis)
plt.ylabel('Measured transmission [dB]', fontdict=total_font_axis)
plt.legend(ncol=3,loc='lower center', fontsize=9)  # 범례 위치 설정
plt.grid(True,axis='both', color='gray', alpha=0.5, linestyle='--')  # 가독성을 위해 gird 삽입

# --------------------------transmission_graph(R_spuared)------------------------------

plt.subplot(2, 3, 2) # 1행 2열의 그래프 중 첫 번째 그래프를 생성

import warnings
warnings.filterwarnings('ignore', message='Polyfit may be poorly conditioned')

best_fit_list = []
for i in range(1, 9):
    afc = np.polyfit(wl, tm, i)
    af = np.polyval(afc, wl)
    R_squared = r2_score(tm, af)
    best_fit_list.append((i, af, R_squared))
    plt.plot(wl, af, plot_color[i], lw=2, label=f'{i}th')
    plt.scatter(wl, tm, s=10)

best_fit_list = sorted(best_fit_list, key=lambda x: abs(x[2] - 1))[:3]

position_x, position_y = 0.4, 0.5
for i, af, R_squared in best_fit_list:
    text_color = 'red' if R_squared == max([item[2] for item in best_fit_list]) else 'black'
    plt.text(position_x, position_y, f'Degree: {i}\nR_squared: {R_squared:.15f}',
             color=text_color,  # 텍스트 색상을 위에서 설정한 값으로 설정
             transform=plt.gca().transAxes,
             fontsize=8, fontweight='bold')
    position_y -= 0.1


plt.title('Transmission spectra - processed and fitting', fontdict=total_font_title)
plt.xlabel('Wavelength [nm]', fontdict=total_font_axis)
plt.ylabel('Measured transmission [dB]', fontdict=total_font_axis)
plt.legend(ncol=3,loc='lower center', fontsize=9)  # 범례 위치 설정
plt.grid(True,axis='both', color='gray', alpha=0.5, linestyle='--')  # 가독성을 위해 gird 삽입

plt.suptitle('Total Graph', fontsize= 15, weight='bold')


plt.savefig('total.png')      # 저장
plt.show()