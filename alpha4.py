from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizePolicy, QWidget
from numpy import arange
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import sys


class MyMplCanvas(FigureCanvas):
    figuresShow = "12345"

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # 设置中文
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 新建一个绘制对象
        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)

        if "1" in self.figuresShow:
            # build axes1
            self.axes1 = self.fig.add_subplot(511)

        if "2" in self.figuresShow:
            # build axes2
            self.axes2 = self.fig.add_subplot(512)

        if "3" in self.figuresShow:
            # build axes3
            self.axes3 = self.fig.add_subplot(513)

        if "4" in self.figuresShow:
            # build axes4
            self.axes4 = self.fig.add_subplot(514)

        if '5' in self.figuresShow:
            # build axes5
            self.axes5 = self.fig.add_subplot(515)

        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def start_static_plot(self):
        #        self.fig.suptitle('图')
        figure1 = Figure1()
        figure2 = Figure2()
        figure3 = Figure3()
        figure4 = Figure4()
        figure5 = Figure5()
        with open("data3.txt") as file:
            # print('打开文件')
            while True:
                line = file.readline()
                if not line:
                    # print('停止')
                    break
                else:
                    # 两种格式
                    if "[" in line:
                        singleline = line.replace(" ", "")

                        bytelist = singleline[:singleline.index("[")]
                        # print('去掉[', bytelist)
                    else:
                        bytelist = line

                    bytelist = bytelist.replace("0d0a", '')

                    LD = word_num(bytelist[0:4], bytelist[18:22])
                    LU = word_num(bytelist[4:8], bytelist[22:26])
                    RD = word_num(bytelist[8:12], bytelist[26:30])
                    RU = word_num(bytelist[12:16], bytelist[30:34])

                    J = byte_num(bytelist[-2:], '0')

                    E = byte_num(bytelist[16:18], bytelist[34:36])

                    figure1.add_data(LD, LU, E, J)
                    figure2.add_data(RD, RU, E, J)
                    figure3.add_data(LD, LU, RD, RU, E, J)
                    figure4.add_data(LD, LU, RD, RU, E, J)
                    figure5.add_data(LU, RU, E, J)

        alist, blist, elist, flist = figure1.get_data()

        clist, dlist, elist, flist = figure2.get_data()

        a_blist, c_dlist, elist, flist = figure3.get_data()

        a_b_oldlist, c_d_oldlist, elist, flist = figure4.get_data()

        lulist, rulist, elist, flist = figure5.get_data()

        t = arange(0, len(alist) * 0.02, 0.02)

        if "1" in self.figuresShow:
            # 图1
            self.axes1.plot(t, alist, '-', label='左腿小腿')
            self.axes1.plot(t, blist, '-', label='左腿大腿')
            self.axes1.plot(t, elist, '-', label='工况')
            self.axes1.plot(t, flist, '-', label='状态')

            #            self.axes1.set_ylabel('X')
            #            self.axes1.set_xlabel('Y')
            self.axes1.grid(True)
            self.axes1.legend()

        if "2" in self.figuresShow:
            # 图2
            self.axes2.plot(t, clist, '-', label='右腿小腿')
            self.axes2.plot(t, dlist, '-', label='右腿大腿')
            self.axes2.plot(t, elist, '-', label='工况')
            self.axes2.plot(t, flist, '-', label='状态')
            #            self.axes2.set_ylabel('X')
            #            self.axes2.set_xlabel('Y')
            self.axes2.grid(True)
            self.axes2.legend()

        if "3" in self.figuresShow:
            # 图3
            self.axes3.plot(t, a_blist, '-', label='左关节角度')
            self.axes3.plot(t, c_dlist, '-', label='右关节角度')
            self.axes3.plot(t, elist, '-', label='工况')
            self.axes3.plot(t, flist, '-', label='状态')

            #            self.axes3.set_ylabel('X')
            #            self.axes3.set_xlabel('Y')
            self.axes3.grid(True)
            self.axes3.legend()

        if "4" in self.figuresShow:
            # 图4
            self.axes4.plot(t, a_b_oldlist, '-', label='左关节角速度')
            self.axes4.plot(t, c_d_oldlist, '-', label='右关节角速度')
            self.axes4.plot(t, elist, '-', label='工况')
            self.axes4.plot(t, flist, '-', label='状态')

            #            self.axes4.set_ylabel('X')
            # self.axes4.set_xlabel('time(s)')
            self.axes4.grid(True)
            self.axes4.legend()

        if '5' in self.figuresShow:
            # fig 5
            self.axes5.plot(t, lulist, '-', label='左腿大腿')
            self.axes5.plot(t, rulist, '-', label='右腿大腿')
            self.axes5.plot(t, elist, '-', label='工况')
            self.axes5.plot(t, flist, '-', label='状态')

            self.axes5.set_xlabel('time(s)')
            self.axes5.grid(True)
            self.axes5.legend()


# 字转化为int - check
def word_num(word, check):
    print('word:%s,check:%s' % (word, check))
    # 最高位为1  负数处理
    if int(word[0], 16) >= 8:
        # 现将除了第一位转换为数字

        # 转换为10进制数字
        result = int(word, 16)

        # 转化为源码 （按位取反后 + 1）
        result = ~result & 0xffff
        result += 1
        result = -result
    else:
        # 正数 原反补都相同
        result = int(word, 16)

    result -= int(check, 16)

    # print('补码：%s -> 源码：%d' % (word, result))
    return result / 100


# 字节转化为int - check
def byte_num(byte, check):
    # 最高位为1  负数处理
    if int(byte[0], 16) >= 8:
        # 现将除了第一位转换为数字

        # 转换为10进制数字
        result = int(byte, 16)

        # 转化为源码 （按位取反后 + 1）
        result = ~result & 0xff
        result += 1
        result = -result
    else:
        # 正数 原反补都相同
        result = int(byte, 16)

    result -= int(check, 16)
    return result


class MatplotlibWidget(QWidget):

    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self, width=5, height=4, dpi=100)

        self.mpl_ntp = NavigationToolbar(self.mpl, self)

        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntp)

        self.showMaximized()


class Figure1(object):
    def __init__(self):
        self.Alist = []
        self.Blist = []
        self.Elist = []
        self.Flist = []

    def add_data(self, A, B, E, F):
        self.Alist.append(A)
        self.Blist.append(B)
        self.Elist.append(E)
        self.Flist.append(F)

    def get_data(self):
        return self.Alist, self.Blist, self.Elist, self.Flist


class Figure2(object):
    def __init__(self):
        self.Clist = []
        self.Dlist = []
        self.Elist = []
        self.Flist = []

    def add_data(self, C, D, E, F):
        self.Clist.append(C)
        self.Dlist.append(D)
        self.Elist.append(E)
        self.Flist.append(F)

    def get_data(self):
        return self.Clist, self.Dlist, self.Elist, self.Flist


class Figure3(object):
    def __init__(self):
        self.A_Blist = []
        self.C_Dlist = []
        self.Elist = []
        self.Flist = []

    def add_data(self, LD, LU, RD, RU, E, F):
        self.A_Blist.append(LU - LD)
        self.C_Dlist.append(RD - RU)
        self.Elist.append(E)
        self.Flist.append(F)

    def get_data(self):
        return self.A_Blist, self.C_Dlist, self.Elist, self.Flist


class Figure4(object):
    def __init__(self):
        self.A_B_oldlist = []
        self.C_D_oldlist = []
        self.Elist = []
        self.Flist = []

    def add_data(self, LD, LU, RD, RU, E, F):
        if len(self.A_B_oldlist) == 0:
            self.A_B_oldlist.append(LU - LD)
            self.C_D_oldlist.append(RD - RU)
        else:
            self.A_B_oldlist.append(LU - LD - self.A_B_oldlist[-1])
            self.C_D_oldlist.append(RD - RU - self.C_D_oldlist[-1])

        self.Elist.append(E)
        self.Flist.append(F)

    def get_data(self):
        return self.A_B_oldlist, self.C_D_oldlist, self.Elist, self.Flist


class Figure5(object):
    def __init__(self):
        self.fig5LUlist = []
        self.fig5RUlist = []
        self.Elist = []
        self.Flist = []

    def add_data(self, LU, RU, E, F):
        self.fig5LUlist.append(LU)
        self.fig5RUlist.append(RU)
        self.Elist.append(E)
        self.Flist.append(F)

    def get_data(self):
        return self.fig5LUlist, self.fig5RUlist, self.Elist, self.Flist


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotlibWidget()
    ui.mpl.start_static_plot()

    ui.show()
    sys.exit(app.exec_())
