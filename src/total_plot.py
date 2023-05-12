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

    path = './res/png_files/'+now.strftime('%Y%m%d_%H%M%S')
    NewFolder(path)
    plt.savefig(path+'/'+x[x.find('(')-13:x.find(')')+16]+'.png')







