from IV_plot import *
from Tm_plot import *
from New_Folder import *


def show_plot(x):
    plt.figure(figsize=(20, 10))
    plt.suptitle(x[24:], fontsize=20, weight='bold')
    plt.subplots_adjust(hspace=0.3)

    tm_plot(x)
    IV_plot(x)

    plt.show()


def save_plot(x):
    plt.figure(figsize=(20, 10))
    plt.suptitle(x[24:], fontsize=20, weight='bold')
    plt.subplots_adjust(hspace=0.3)

    tm_plot(x)
    IV_plot(x)

    path1 = './res/' + f'{x[4:12]}'
    path2 = path1 + f'{x[12:16]}'
    path3 = path2 +  f'{x[16:32]}'
    NewFolder(path3)

    plt.savefig(path3+'/'+x[x.find('(')-13:x.find(')')+16]+'.png')







