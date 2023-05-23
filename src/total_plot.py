from IV_plot import *
from Tm_plot import *
from New_Folder import *


def show_plot(x):
    plt.figure(figsize=(20, 10))
    plt.suptitle(x[33:], fontsize=20, weight='bold')
    plt.subplots_adjust(hspace=0.3)

    tm_plot(x)
    IV_plot(x)

    plt.show()


def save_plot(x):
    plt.figure(figsize=(20, 10))
    plt.suptitle(x[33:], fontsize=20, weight='bold')
    plt.subplots_adjust(hspace=0.3)

    tm_plot(x)
    IV_plot(x)



    date = now.strftime('%Y%m%d_%H%M%S')
    path = './res/png_files/'
    path1 = path +  f'{date}/'
    path2 = path1 + f'{x[4:12]}'
    path3 = path2 + f'{x[12:16]}'
    path4 = path3 + f'{x[16:32]}'
    NewFolder(path4)

    plt.savefig(path4 + '/' + x[x.find('(') - 13:x.find(')') + 16] + '.png')




