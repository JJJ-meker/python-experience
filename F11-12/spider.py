# 爬取4~10部电影信息（电影名、导演、演员、海报url链接，预报片视频链接)

# url = https://movie.douban.com/
import requests
from bs4 import BeautifulSoup
import tkinter as tk
import cv2 as cv
from PIL import Image, ImageTk

url = "https://movie.douban.com/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}

root = tk.Tk()
root.geometry('1200x660')
root.title('电影爬取演示')
root.resizable(False, False)

iv_command = tk.IntVar()


class Spider():
    """
    爬虫，不通用，主要针对豆瓣进行爬取
    """

    def __init__(self, target):
        self.target = target
        # 电影名(展示会用)
        self.movie = []  # 完成
        # 存放要访问的url
        self.urls = []  # 完成
        # 存放海报链接
        self.poster = []  # 完成
        # 存放预告片链接
        self.video = []
        # 存放演员表(展示会用)
        self.actors = {}

    def get_url(self):
        request = requests.get(self.target, headers=headers)
        request.encoding = request.apparent_encoding
        # print(request.status_code)
        # print(request.text)
        data = request.text
        # 解析
        soup = BeautifulSoup(data, 'html.parser')
        # 获取正在热映栏内容(取其中几个）
        links = soup.find_all('a')
        # 电影链接
        for link in links[31:46:3]:
            self.urls.append(link['href'])
        # 海报链接
        posters = soup.find_all('img', class_='')
        for post in posters[:5]:
            self.poster.append(post['src'])
            self.movie.append(post['alt'])

    def download_poster(self, urls):
        index = 1
        for target in urls:
            response = requests.get(target, headers=headers)
            with open(f'movie{index}-poster.jpg', 'wb') as f:
                f.write(response.content)
                index += 1

    def download_context(self, urls):
        index = 0
        for url in urls:
            response = requests.get(url, headers=headers)
            data = response.text
            soup = BeautifulSoup(data, 'html.parser')
            actors = soup.find('ul', class_='celebrities-list')
            actor = actors.find_all('li', class_='celebrity')
            # 存放演员列表，0号位是导演
            people = []
            for elem in actor:
                person = elem.find('a', class_='name')
                name = person.get_text()
                people.append(name)
            self.actors[f'movie{index + 1}'] = people
            index += 1
            pre_video = soup.find('a', class_='related-pic-video')
            self.video.append(pre_video['href'])

    def download_vedio(self, urls):
        index = 1
        for url in urls:
            res = requests.get(url, headers=headers)
            data = res.text
            soup = BeautifulSoup(data, 'html.parser')
            mp4_target = soup.find('video')
            # print(mp4_target)
            src = mp4_target.source['src']
            new_res = requests.get(src, headers=headers)
            with open(f'movie{index}-pre.mp4', 'wb') as f:
                f.write(new_res.content)
            index += 1


class Show:
    """
    展示
    """

    def __init__(self, list, dic):
        """
        list 展示的电影名列表
        """
        self.showlist = list
        self.showdic = dic
        self.draw(list)

    def draw(self, list):
        # 海报
        poster = tk.Canvas(root, width=280, height=400, bg='white')
        # 菜单
        menu = tk.Canvas(root, width=280, height=160, bg='white')
        # 演员表
        actor = tk.Canvas(root, width=280, height=100, bg='white')
        # 预告片
        movie = tk.Canvas(root, width=900, height=800, bg='white')

        poster.place(x=0, y=0)
        menu.place(x=0, y=400)
        actor.place(x=0, y=560)
        movie.place(x=280, y=0)

        for i in range(0, len(list)):
            radio = tk.Radiobutton(root, text=list[i], value=i + 1, variable=iv_command, command=self.display)
            radio.place(x=0, y=400 + i * 30)
        root.mainloop()

    def display(self):
        re = iv_command.get()
        movie = self.showdic.keys()
        m = list(movie)
        name = m[re - 1]
        self.show(name)

    def show(self, name):
        # 展示海报
        # print(name)
        label = tk.Label(root, width=31, height=22, bg='white')
        label.place(x=0, y=0)
        img = cv.imread(f'{name}-poster.jpg', 1)
        cv_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        im = Image.fromarray(cv_img)
        imgtk = ImageTk.PhotoImage(image=im)
        tk.Label(root, image=imgtk).place(x=0, y=0)

        lists = self.showdic[name]
        # 展示演员表
        director = tk.Label(root, text="导演:")
        director.place(x=0, y=570)
        dv = tk.Label(root, text=lists[0])
        dv.place(x=50, y=570)

        actors = tk.Label(root, text="演员:")
        actors.place(x=0, y=600)
        actor1 = tk.Label(root, text=lists[1:4])
        actor1.place(x=50, y=600)
        actor2 = tk.Label(root, text=lists[4:])
        actor2.place(x=50, y=620)

        # 展示预告片
        movie_pre = tk.Label(root, width=900, height=500)
        movie_pre.place(x=300, y=50)
        video = cv.VideoCapture(f'{name}-pre.mp4')
        while video.isOpened():
            ret, frame = video.read()
            if ret:
                cv.waitKey(25)
                image_cv = Image.fromarray(frame)
                image_tk = ImageTk.PhotoImage(image=image_cv)
                movie_pre.config(image=image_tk)
                movie_pre.image = image_tk
                movie_pre.update()
            else:
                break


if __name__ == '__main__':
    spider = Spider(url)
    spider.get_url()
    spider.download_poster(spider.poster)
    spider.download_context(spider.urls)
    spider.download_vedio(spider.video)
    print("下载完成")
    l = spider.movie
    dic = spider.actors
    display = Show(l, dic)
