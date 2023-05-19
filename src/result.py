from filter import *
from total_plot import *
from save_csv import *
import time
from tqdm import tqdm
import sys
import warnings
warnings.filterwarnings('ignore')

files = []
show, png, csv = 0, 0, 0

device_type = str(input('원하는 장치 유형을 입력하세요. (ex. LMZC, LMZO, a(all)): '))
if device_type == 'a':
    files = LMZ_files
elif device_type == 'LMZO':
    for file in LMZ_files:
        if device_type in file:
            files.append(file)
elif device_type == 'LMZC':
    for file in LMZ_files:
        if device_type in file:
            files.append(file)
else:
    print(f'Error : {device_type}은(는) 존재하지 않습니다.')
if not files:
    print('\n[Data가 존재하지 않습니다.]')
    sys.exit()


Owner = str(input('사용자 이름을 입력하시오. : '))


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
    for f in tqdm(files, desc='Showing png files '):
        show_plot(f)
        time.sleep(0.1)
    print('\n[프로그램을 종료합니다.]')

elif show == 0 and png == 1 and csv == 0:
    for f in tqdm(files, desc='Saving png files '):
        save_plot(f)
        time.sleep(0.1)
    print('\n[프로그램을 종료합니다.]')

elif show == 0 and png == 0 and csv == 1:
    Create_csv(files,Owner)
    print('\n[프로그램을 종료합니다.]')

elif show == 1 and png == 1 and csv == 0:
    for f in tqdm(files, desc='Showing png files '):
        show_plot(f)
        time.sleep(0.1)
    for f in tqdm(files, desc='Saving png files '):
        save_plot(f)
        time.sleep(0.1)
    print('\n[프로그램을 종료합니다.]')

elif show == 0 and png == 1 and csv == 1:
    for f in tqdm(files, desc='Saving png files '):
        save_plot(f)
        time.sleep(0.1)
    Create_csv(files,Owner)
    print('\n[프로그램을 종료합니다.]')
    

elif show == 1 and png == 0 and csv == 1:
    for f in tqdm(files, desc='Showing png files '):
        show_plot(f)
        time.sleep(0.1)
    Create_csv(files,Owner)
    print('\n[프로그램을 종료합니다.]')

elif show == 1 and png == 1 and csv == 1:
    for f in tqdm(files, desc='Showing png files '):
        show_plot(f)
        time.sleep(0.1)
    for f in tqdm(files, desc='Saving png files '):
        save_plot(f)
        time.sleep(0.1)
    Create_csv(files,Owner)
    print('\n[프로그램을 종료합니다.]')