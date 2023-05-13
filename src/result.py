from filter import *
from total_plot import *
from save_csv import *
import time
from tqdm import tqdm
import sys
import warnings
warnings.filterwarnings('ignore')

initial_files, sec_files, thir_files, four_files = [], [], [], []
coord_list = []
wafer_list = ['D07', 'D08', 'D23', 'D24']
show, png, csv = 0, 0, 0


for row in range(-4, 4):
    for column in range(-4, 4):
        coord_list.append('('+str(row)+','+str(column)+')')

device_type = str(input('원하는 장치 유형을 입력하세요. (ex. LMZC, LMZO, LMZ): '))
if device_type == 'LMZ':
    initial_files = LMZ_files
elif device_type == 'LMZO':
    for file in LMZ_files:
        if device_type in file:
            initial_files.append(file)
elif device_type == 'LMZC':
    for file in LMZ_files:
        if device_type in file:
            initial_files.append(file)
else:
    print(f'Error : {device_type}은(는) 존재하지 않습니다.')
if not initial_files:
    print('\n[Data가 존재하지 않습니다.]')
    sys.exit()

wafer_num = list(map(str, input('원하는 웨이퍼 번호를 "D##" 형태로 입력하세요.'
                                ' (ex. D07, D08, D23, D24, all): ').split()))
d_list = []
if wafer_num[0] == 'all':
    for wafer in wafer_list:
        for i_file in initial_files:
            if wafer in i_file:
                sec_files.append(i_file)
else:
    for wafer in wafer_num:
        if wafer in wafer_list:
            for i_file in initial_files:
                if wafer in i_file:
                    sec_files.append(i_file)
                    d = str(i_file)[8:16]
                    if d not in d_list:
                        d_list.append(d)
                        d_str = ', '.join(d_list)

        else:
            print(f'Error : {wafer}은(는) 존재하지 않습니다.')
if not sec_files:
    print('\n[Data가 존재하지 않습니다.]')
    sys.exit()

Date_file = list(map(str,input(f'측정 날짜를 입력하세요. ({d_str}, all) : ').split()))

if Date_file[0] == 'all':
    for s_file in sec_files:
        thir_files.append(s_file)
else:
    for date in Date_file:
        for s_file in sec_files:
            if date in s_file:
                thir_files.append(s_file)
            else:
                print(f'Error : {date}은(는) 존재하지 않습니다.')
if not thir_files:
    print('\n[Data가 존재하지 않습니다.]')
    sys.exit()

#-------------------------------------------------------------------------------------
rowcolumn = list(map(str, input('wafer의 row와 column을 "#,#"의 형태로 입력하세요. (ex. 0,0) : ')
                 .split('/')))
if rowcolumn[0] == 'all':
    for t_file in thir_files:
        for all_coord in coord_list:
            if all_coord in s_file:
                four_files.append(s_file)
else:
    for coord in rowcolumn:
        coord = '('+coord+')'
        if coord in coord_list:
            for s_file in thir_files:
                if coord in s_file:
                    four_files.append(s_file)
        else:
            print(f'Error : {coord}은(는) 존재하지 않습니다.')
if not four_files:
    print('\n[Data가 존재하지 않습니다.]')
    sys.exit()

Owner = str(input('이름을 입력하시오. : '))

if not four_files:
    print('\n[Data가 존재하지 않습니다.]')
    sys.exit()

while True:
    show_png = str(input('png 파일을 보시겠습니까? (y/n): '))
    if show_png == 'y':
        show = 1
        break
    elif show_png == 'n':
        break
    else:
        print('Error : y와 n만 입력할 수 있습니다.')
        continue

while True:
    save_png = str(input('png 파일을 저장하겠습니까? (y/n): '))
    if save_png == 'y':
        png = 1
        break
    elif save_png == 'n':
        break
    else:
        print('Error : y와 n만 입력할 수 있습니다.')
        continue
while True:
    save_csv = str(input('csv 파일을 저장하시겠습니까? (y/n) : '))
    if save_csv == 'y':
        csv = 1
        break
    elif save_csv == 'n':
        break
    else:
        print('Error : y와 n만 입력할 수 있습니다.')
        continue


if show == 0 and png == 0 and csv == 0:
    print('\n[프로그램을 종료합니다.]')

elif show == 1 and png == 0 and csv == 0:
    for final_file in tqdm(four_files, desc='Showing png files '):
        show_plot(final_file)
        time.sleep(0.1)
    print('\n[프로그램을 종료합니다.]')

elif show == 0 and png == 1 and csv == 0:
    for final_file in tqdm(four_files, desc='Saving png files '):
        save_plot(final_file)
        time.sleep(0.1)
    print('\n[프로그램을 종료합니다.]')

elif show == 0 and png == 0 and csv == 1:
    Create_csv(four_files,Owner)
    print('\n[프로그램을 종료합니다.]')

elif show == 1 and png == 1 and csv == 0:
    for final_file in tqdm(four_files, desc='Showing png files '):
        show_plot(final_file)
        time.sleep(0.1)
    for final_file in tqdm(four_files, desc='Saving png files '):
        save_plot(final_file)
        time.sleep(0.1)
    print('\n[프로그램을 종료합니다.]')

elif show == 0 and png == 1 and csv == 1:
    for final_file in tqdm(four_files, desc='Saving png files '):
        save_plot(final_file)
        time.sleep(0.1)
    Create_csv(four_files,Owner)
    print('\n[프로그램을 종료합니다.]')

elif show == 1 and png == 0 and csv == 1:
    for final_file in tqdm(four_files, desc='Showing png files '):
        show_plot(final_file)
        time.sleep(0.1)
    Create_csv(four_files,Owner)
    print('\n[프로그램을 종료합니다.]')

elif show == 1 and png == 1 and csv == 1:
    for final_file in tqdm(four_files, desc='Showing png files '):
        show_plot(final_file)
        time.sleep(0.1)
    for final_file in tqdm(four_files, desc='Saving png files '):
        save_plot(final_file)
        time.sleep(0.1)
    Create_csv(four_files,Owner)
    print('\n[프로그램을 종료합니다.]')
