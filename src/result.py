from filter import *
from total_plot import *
import time
from tqdm import tqdm
import sys
import warnings
warnings.filterwarnings('ignore')
#
first_files, mid_files, final_files = [], [], []
coord_list = []
wafer_list = ['D07', 'D08', 'D23', 'D24']
wavelength_list = ['LMZ', 'LMZO', 'LMZC']
float_count = 0
png_count = 0
xlsx_count = 0

for row in range(-4, 4):
    for column in range(-4, 4):
        coord_list.append('('+str(row)+','+str(column)+')')

device_type = str(input('원하는 장치 유형을 입력하세요. (ex. LMZC, LMZO, LMZ): '))
if device_type == 'LMZ':
    first_files = LMZ_files
elif device_type == 'LMZO':
    for file in LMZ_files:
        if device_type in file:
            first_files.append(file)
elif device_type == 'LMZC':
    for file in LMZ_files:
        if device_type in file:
            first_files.append(file)
else:
    print(f'Error : {device_type}은(는) 존재하지 않습니다.')
if not first_files:
    print('\n[Nothing Data]')
    sys.exit()

wafer_num = list(map(str, input('원하는 웨이퍼 번호를 "D##" 형태로 입력하세요.'
                                ' (ex. D07, D08, D23, D24, all): ').split()))
if wafer_num[0] == 'all':
    for selected_wafer in wafer_list:
        for first_file in first_files:
            if selected_wafer in first_file:
                mid_files.append(first_file)
else:
    for selected_wafer in wafer_num:
        if selected_wafer in wafer_list:
            for first_file in first_files:
                if selected_wafer in first_file:
                    mid_files.append(first_file)
        else:
            print(f'Error : {selected_wafer}은(는) 존재하지 않습니다.')
if not mid_files:
    print('\n[Nothing Data]')
    sys.exit()

coord = list(map(str, input('wafer의 좌표를 "#,#"의 형태로 입력하세요. (ex. 0,0) : ')
                 .split('/')))
if coord[0] == 'all':
    for mid_file in mid_files:
        for all_coord in coord_list:
            if all_coord in mid_file:
                final_files.append(mid_file)
else:
    for selected_coord in coord:
        selected_coord = '('+selected_coord+')'
        if selected_coord in coord_list:
            for mid_file in mid_files:
                if selected_coord in mid_file:
                    final_files.append(mid_file)
        else:
            print(f'Error : {selected_coord}은(는) 존재하지 않습니다.')
if not final_files:
    print('\n[Nothing Data..]')
    sys.exit()


while True:
    float_png = str(input('png 파일을 보시겠습니까? (y/n): '))
    if float_png == 'y':
        float_count = 1
        break
    elif float_png == 'n':
        break
    else:
        print('Error : y와 n만 입력할 수 있습니다.')
        continue

while True:
    save_png = str(input('png 파일을 저장하겠습니까? (y/n): '))
    if save_png == 'y':
        png_count = 1
        break
    elif save_png == 'n':
        break
    else:
        print('Error : y와 n만 입력할 수 있습니다.')
        continue



if float_count == 0 and png_count == 0 :
    print('\n[프로그램을 종료합니다.]')

elif float_count == 1 and png_count == 0 :
    for final_file in tqdm(final_files, desc='floating png files '):
        show_plot(final_file)
        time.sleep(0.1)
    print('\n[프로그램을 종료합니다.]')

elif float_count == 0 and png_count == 1 :
    for final_file in tqdm(final_files, desc='Saving png files '):
        save_plot(final_file)
        time.sleep(0.1)
    print('\n[프로그램을 종료합니다.]')



elif float_count == 1 and png_count == 1 :
    for final_file in tqdm(final_files, desc='Floating png files '):
        show_plot(final_file)
        time.sleep(0.1)
    for final_file in tqdm(final_files, desc='Saving png files '):
        save_plot(final_file)
        time.sleep(0.1)
    print('\n[프로그램을 종료합니다.]')
