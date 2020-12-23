# -*- coding: utf-8 -*-
import wordcloud
import jieba
import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2 as cv
from PIL import Image, ImageTk
import re

tag=-1

root = tk.Tk()
root.title("词云展示")
root.geometry("400x700+500+50")
root.resizable(False, False)

books = ["红楼梦", "水浒传", "三国演义"]
tips = ["人物词云图", "章节出场次数图", "人物关系图"]

class File:
    """
    读取文件，获取内容
    """

    def __init__(self, filepath):
        """
        filepath: str
        """
        self.filepath = filepath
        self.__text = ""

    def getText(self):
        f = open(self.filepath, "r", encoding="utf-8")
        text = f.read()
        f.close()
        self.__text = text

    def stop_word(self):
        stop = [line.strip() for line in open("stop.txt", encoding='utf-8').readlines()]
        return stop

    def get_text(self):
        return self.__text


class Articles:
    """
    分析文章，解析并得到相应的数据
    """

    def __init__(self, text):
        """
        text: str
        """
        self.text = text
        self.name = []  # 获取name
        self.appear_time = []  # 0-20name每回合出现次数

    def get_twenty(self, stop):
        """
        获取出现频率最高的20个人

        stop: list
        """
        words = jieba.lcut(self.text.strip())
        counts = {}
        for word in words:
            if len(word) == 1:
                continue
            elif word not in stop:
                if word == "鲁智深" or word == "智深":
                    word = "鲁智深"
                elif word == "关公" or word == "云长":
                    word = "关羽"
                elif word == "宋江道":
                    word = "宋江"
                elif word == "凤姐儿":
                    word = "凤姐"
                elif word == "林黛玉" or word == "林妹妹" or word == "黛玉笑":
                    word = "黛玉"
                elif word == "宝二爷":
                    word = "宝玉"
                elif word == "袭人道":
                    word = "袭人"
                elif word == "小丫头":
                    word = "丫头"
                elif word == "丞相" or word == "孔明曰" or word == "孔明":
                    word = "诸葛亮"
                elif word == "玄德曰" or word == "玄德":
                    word = "刘备"
                counts[word] = counts.get(word, 0) + 1
        items = list(counts.items())
        items.sort(key=lambda x: x[1], reverse=True)
        data = items[:20]
        appear = {x[0]: x[1] for x in data}
        self.name = [x for x in appear]
        return appear  # 人物出现总次数

    def get_chapter(self):
        chapter = re.findall("第[\u4E00-\u9FA5]+回", self.text)
        chapter_start = []
        for x in chapter:
            chapter_start.append(self.text.index(x))
        chapter_end = chapter_start[1:] + [len(self.text)]  # ？？？
        chapter_index = list(zip(chapter_start, chapter_end))
        return chapter_index

    def chapter_appear(self):
        """
        每回合出现次数
        """
        chapter_index = self.get_chapter()
        for i in range(len(self.name)):
            cut_name = []
            for li in range(120):
                start = chapter_index[li][0]
                end = chapter_index[li][1]
                cut_name.append(self.text[start:end].count(self.name[i][0]))
            self.appear_time.append(cut_name)

    def relation(self):
        """
        关系网
        """
        names = self.name
        relation = {}
        para = self.text.split('\n')
        for p in para:
            for name1 in names:
                if name1 in p:
                    for name2 in names:
                        if name2 in p and name1 != name2 and (name2, name1) not in relation:
                            relation[(name1, name2)] = relation.get((name1, name2), 0) + 1
        maxRela = max([v for k, v in relation.items()])
        relations = {k: v / maxRela for k, v in relation.items()}
        return relations


class ShowCloud:
    """
    绘制词云图，统计图， 关系网
    """

    def __init__(self, name, times, appears):
        self.name = name  # list     前20人名字
        self.appear_times = times  # dict   总出场次数
        self.chapter_appear = appears  # list    每回合出现, 索引与name对应

    def words(self):
        wcd = wordcloud.WordCloud(
            background_color="white",
            width=1000,
            max_words=50,
            font_path='C:/Windows/Fonts/simkai.ttf',
            height=860,
            margin=1
        ).fit_words(self.appear_times)
        plt.imshow(wcd)
        plt.axis('off')
        plt.show()

    def appear(self):
        """
        appear_times: list
        """
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(18, 4))
        for i in range(len(self.chapter_appear)):
            plt.plot(self.chapter_appear[i], label=self.name[i])
        plt.xlabel("章节数")
        plt.ylabel("出现次数")
        plt.legend()
        plt.title("人物出现次数")
        plt.show()

    def relative(self, relation):
        plt.figure(figsize=(15, 15))
        G = nx.Graph()
        for k, v in relation.items():
            G.add_edge(k[0], k[1], weight=v)
        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.6]
        emidle = [(u, v) for (u, v, d) in G.edges(data=True) if (d['weight'] > 0.3) & (d['weight'] <= 0.6)]
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.3]
        # 设置布局
        pos = nx.spring_layout(G)
        # 设置节点样式
        nx.draw_networkx_nodes(G, pos, alpha=0.8, node_size=100)
        # 设置高权重边的样式
        nx.draw_networkx_edges(G, pos, edgelist=elarge, width=2.5, alpha=0.9, edge_color='g')
        # 设置中权重边的样式
        nx.draw_networkx_edges(G, pos, edgelist=emidle, width=1.5, alpha=0.6, edge_color='y')
        # 设置低权重边的样式
        nx.draw_networkx_edges(G, pos, edgelist=esmall, width=1, alpha=0.3, edge_color='b', style='dashed')
        nx.draw_networkx_labels(G, pos, font_size=12)
        plt.axis('off')
        plt.title("主要人物社交关系网络图")
        plt.show()


class Show:
    """
    tk演示
    """

    def __init__(self):
        self.name = []  # list     前20人名字
        self.appear = {}  # dict   总出场次数
        self.chapter_appear = []  # list    每回合出现, 索引与name对应
        self.relations={}
        self.passage=""
        self.draw()

    def draw(self):
        choice1 = tk.Button(root, text=books[0], width=30, height=3, command=lambda: self.menu(0))
        choice1.place(x=100, y=200)
        choice2 = tk.Button(root, text=books[1], width=30, height=3, command=lambda: self.menu(1))
        choice2.place(x=100, y=280)
        choice3 = tk.Button(root, text=books[2], width=30, height=3, command=lambda: self.menu(2))
        choice3.place(x=100, y=360)
        root.mainloop()

    def menu(self, index):
        f = File("{}.txt".format(books[index]))
        stop = f.stop_word()
        f.getText()
        text = f.get_text()
        self.passage = Articles(text)
        self.appear = self.passage.get_twenty(stop)  # 出现最多的前20人出现的次数
        self.passage.chapter_appear()  # 每回合出现
        self.chapter_appear = self.passage.appear_time  # 每回合出现
        self.relations = self.passage.relation()  # 关系网
        windows = tk.Tk()
        windows.geometry("400x700+900+50")
        windows.resizable(False, False)
        windows.title("menu")
        button1 = tk.Button(windows, width=30, height=3, bg='orange', font=('楷体', 10), text=tips[0],
                            command=self.show_word_cloud)
        button1.place(x=100, y=200)
        button2 = tk.Button(windows, width=30, height=3, bg='orange', font=('楷体', 10), text=tips[1],
                            command=self.show_appear)
        button2.place(x=100, y=280)
        button3 = tk.Button(windows, width=30, height=3, bg='orange', font=('楷体', 10), text=tips[2],
                            command=self.show_relations)
        button3.place(x=100, y=360)
        windows.mainloop()

    def show_word_cloud(self):
        c = ShowCloud(self.passage.name, self.appear, self.chapter_appear)
        c.words()

    def show_appear(self):
        c = ShowCloud(self.passage.name, self.appear, self.chapter_appear)
        c.appear()

    def show_relations(self):
        c = ShowCloud(self.passage.name, self.appear, self.chapter_appear)
        c.relative(self.relations)


if __name__ == '__main__':
    s = Show()
