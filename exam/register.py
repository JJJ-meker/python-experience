import threading
import tkinter as tk
import cv2 as cv
from PIL import Image, ImageTk
from random import randint
from math import inf

root = tk.Tk()
root.resizable(False, False)
root.title("点名")
root.geometry("500x700+550+50")

filepath = "student.txt"

img = cv.imread('1.jpg', 1)
cv_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
im = Image.fromarray(cv_img)
imgtk = ImageTk.PhotoImage(image=im)

firstName = ["赵", "钱", "张", "李", "王", "白", "乔", "吕", "吴", "曾"]
lastName = ["华", "河", "武", "琪", "郎", "飞英", "凯旋", "雨石", "成文", "刚捷", "鹏鲲", "天赋", "子石", "斯伯", "茂典", "鹏涛", "刚捷", "子石", "康胜",
            "元良", "宙", "列", "实", "新知", "全", "光", "若", "澎", "文昌", "锐达"]


class Student:
    def __init__(self, id, name):
        self.__id = id
        self.__name = name

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name


class File:
    def __init__(self, filepath):
        self.filepath = filepath
        self.__text = []

    def writefile(self, data):
        try:
            file = open(self.filepath, "a")
        except IOError:
            print("打开文件错误")
        else:
            file.write(data)

    def readfile(self):
        try:
            file = open(self.filepath, "r")
        except IOError:
            print("打开文件错误")
        else:
            self.__text = file.readlines()

    def clear(self):
        try:
            file = open(self.filepath, "w")
        except IOError:
            print("打开文件错误")
        else:
            file.write("")

    def get_data(self):
        students = []
        for s in self.__text:
            string = s[:-1]
            student = string.split(',')
            students.append(student)
        return students


class Show:
    def __init__(self, filename):
        self.data = []
        self.get_students(filename)
        self.draw()
        self.flag = 1
        self.t = threading.Thread(target=self.display)

    def draw(self):
        global imgtk
        # 展示图片
        name = self.get_num()
        img = cv.imread(f'{name}.jpg', 1)
        cv_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        im = Image.fromarray(cv_img)
        imgtk = ImageTk.PhotoImage(image=im)
        tk.Label(root, image=imgtk).place(x=50, y=10)
        # 展示选项
        index = randint(1,29)
        stu_id = self.data[index][0]
        stu_name = self.data[index][1]
        student_id = stu_id
        student_name = stu_name
        id = tk.Label(bg='white', text=student_id, height=2, width=20)
        id.place(x=175, y=510)
        student = tk.Label(bg='white', text=student_name, height=2, width=20)
        student.place(x=175, y=560)

    def button(self):
        choose = tk.Button(bg='white', text='选择', font=('楷体', 10), height=2, width=20, command=self.task)
        choose.place(x=175, y=620)

    def get_students(self, filename):
        file = File(filename)
        file.readfile()
        self.data = file.get_data()

    def get_num(self):
        num = randint(1, 10)
        if num > 5:
            return 1
        else:
            return 0

    def task(self):
        self.t.start()

    def display(self):
        count = 20
        while count > 0:
            self.draw()
            count -= 1

    # def stop(self):
    #     pass


class Sign:
    def __init__(self, filename):
        self.init_student(filename)

    def init_student(self,filename):
        file = File(filename)
        for i in range(0, 30):
            id = randint(1000000000, 10000000000)
            f_index = randint(0, 9)
            l_index = randint(0, 29)
            name = firstName[f_index] + lastName[l_index]
            stu = Student(id, name)
            data = f"{stu.get_name()},{stu.get_id()}\n"
            file.writefile(data)

if __name__ == '__main__':
    sign = Sign(filepath) #初始化
    show = Show(filepath) #读取数据
    show.button()
    #s.button()
    root.mainloop()
    #sign.display()