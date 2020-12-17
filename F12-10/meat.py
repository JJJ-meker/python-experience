import csv
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root=tk.Tk()
root.title("各国肉类消费情况")
root.geometry("1500x700+50+50")
root.resizable(0, 0)

filename="meat_consumption_worldwide.csv"
meat=['BEEF', 'PIG', 'POULTRY', 'SHEEP']
# 每个国家36条数据

iv_command = tk.IntVar()

class File:
    def __init__(self, filepath):
        self.filepath=filepath
        self.meats=[] # 所有的肉类信息
        self.country=[] # 国家名
        self.data={} # 存储绘制的数据

    def readfile(self):
        with open(self.filepath, "r") as stucsv:
            reader=csv.reader(stucsv)
            for row in reader:
                if row[0] not in self.country:
                    self.country.append(row[0]) # 存放国家名
                self.meats.append(row) # 所有的肉类信息
        self.country.pop(0)  # 删除LOCATION
        self.meats.pop(0) # 删除第一条


    # row = ['AUS', 'BEEF', 'KG_CAP', '1991', '27.7218154779186']
    # [国家 肉类 统计方式 年份 值]

    def get_data(self):
        self.data['BEEF']=[]
        self.data['PIG'] = []
        self.data['POULTRY'] = []
        self.data['SHEEP'] = []
        nums=[]
        i=0;j=0
        bugs=0
        # for row in self.meats:
        #     print(row)
        for row in self.meats:
            nums.append(float(row[-1]))
            j+=1
            if bugs < 2:
                # 处理前两个
                if j%36==0:
                    #已经收集了36个数据
                    n=i%4
                    self.data[meat[n]].append(nums.copy())
                    self.data[meat[n]][0].insert(0,0)
                    # 清空数组 nums
                    nums.clear()
                    i+=1
                    bugs+=1
                    if bugs==2:
                        j=0
            else:
                if j%37==0:
                    n=i%4
                    self.data[meat[n]].append(nums.copy())
                    nums.clear()
                    i+=1


class Show():
    def __init__(self,name, beef, sheep, pig, poultry):
        self.name=name
        self.beef=beef
        self.sheep=sheep
        self.pig=pig
        self.poultry=poultry
        self.display=tk.Canvas
        self.canvas=tk.Canvas
        self.draw()

    def draw(self):
        menu=tk.Canvas(root, width=200, height=700, bg='white')
        menu.place(x=0,y=0)
        # frame=tk.Frame(menu, width=100, height=500)
        # frame.place(x=50, y=100)
        for i in range(len(self.name)):
            button=tk.Radiobutton(root, bg='white', text=self.name[i], value=i, variable=iv_command, command=self.show)
            button.place(x=0,y=i*25)
            if i > 25:
                button.place(x=100, y=(i-26)*25)
        replace=tk.Canvas(root, width=1300, height=200, bg='white')
        replace.place(x=200,y=0)
        self.update()
        root.mainloop()

    def update(self):
        self.display = tk.Canvas(root, width=1300, height=700, bg='white')
        self.display.place(x=200, y=150)

    def show(self):
        index=iv_command.get()
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['savefig.dpi'] = 100  # 图片像素
        plt.rcParams['figure.dpi'] = 80
        print(index)
        b=self.beef[index]
        p=self.pig[index]
        s=self.sheep[index]
        y=self.poultry[index]
        pic=plt.figure(figsize=(18, 4))
        x=np.arange(1990, 2027)
        plt.plot(x, b, "ks-",label='BEEF')
        plt.plot(x, p, "gv-",label='PIG')
        plt.plot(x, s, "bo-",label='SHEEP')
        plt.plot(x, y, "y*-", label="POULTRY")
        plt.xticks(x)
        plt.xlabel("年份")
        plt.ylabel("消费量")
        plt.legend()
        plt.title("肉类消费图")
        plt.show()
        self.update()
        self.canvas = FigureCanvasTkAgg(pic, self.display)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)


if __name__ == '__main__':
    f=File(filename)
    f.readfile()
    f.get_data()
    data=f.data
    b=data['BEEF']
    p=data['PIG']
    s=data['SHEEP']
    y=data['POULTRY']
    s=Show(f.country, b, p, s, y)