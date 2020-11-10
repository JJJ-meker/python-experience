import tkinter as tk
import tkinter.messagebox

root = tk.Tk()
root.title("动态演示")
root.geometry("1000x800+50+0")
root.resizable(False, False)
canvas = tk.Canvas(root, width = 1000, height = 900, bg = "white")

class circle():
    """
    定义圆类
    @param position 位置
    @param color    填充颜色
    """
    def __init__(self, *position, color) -> None:
        self.position = position
        self.color = color
        canvas.create_oval(position, fill = color)

def draw():
    """
    绘制基本图形
    """
    canvas.pack()
    # 画连接线
    canvas.create_line(100, 350, 250, 250, fill="black", width=5)
    canvas.create_line(100, 350, 250, 450, fill="black", width=5)
    canvas.create_line(250, 250, 550, 250, fill="black", width=5)
    canvas.create_line(250, 450, 550, 450, fill="black", width=5)
    canvas.create_line(525, 250, 400, 350, fill="black", width=5)
    canvas.create_line(400, 350, 525, 450, fill="black", width=5)
    canvas.create_line(525, 450, 700, 350, fill="black", width=5)
    canvas.create_line(525, 250, 700, 350, fill="black", width=5)

    #画圆
    c0 = circle(50, 300, 150, 400, color="yellow")
    canvas.create_text(100, 350, text = 0, font = ("楷体", 20), fill = "black")
    c1 = circle(200, 200, 300, 300, color = "yellow")
    canvas.create_text(250, 250, text = 1, font = ("楷体", 20), fill = "black")
    c2 = circle(200, 400, 300, 500, color = "yellow")
    canvas.create_text(250, 450, text = 2, font = ("楷体", 20), fill = "black")
    c3 = circle(350, 300, 450, 400, color = "yellow")
    canvas.create_text(400, 350, text = 3, font = ("楷体", 20), fill = "black")
    c4 = circle(500, 200, 600, 300, color = "yellow")
    canvas.create_text(550, 250, text = 4, font = ("楷体", 20), fill = "black")
    c5 = circle(500, 400, 600, 500, color = "yellow")
    canvas.create_text(550, 450, text = 5, font = ("楷体", 20), fill = "black")
    c6 = circle(650, 300, 750, 400, color = "yellow")
    canvas.create_text(700, 350, text = 6, font = ("楷体", 20), fill = "black")
    global circles
    circles = {0:c0, 1:c1, 2:c2, 3:c3, 4:c4, 5:c5, 6:c6}

    BFSButton = tk.Button(bg="grey", fg="blue", text="广度优先搜索", font=("楷体", 20), command=BFS)
    DFSButton = tk.Button(bg="grey", fg="blue", text="深度优先搜索", font=("楷体", 20), command=DFS)
    BFSButton.place(x=100, y=700, width=180, height=50)
    DFSButton.place(x=500, y=700, width=180, height=50)

index = 0

def BFS():
    """
    广搜 （草率一点）
    """
    drawList=[[0],[1,2],[4,5],[5,3,6]]
    def stepBFS(event):
        """
        绘制每一步
        """
        global index
        for i in range(len(drawList[index])):
            circle(circles.get(drawList[index][i]).position, color="pink")
        index +=1
        if index > 3:
            tkinter.messagebox.showinfo("tip", "演示结束，谢谢观看！")
            draw()
            index = 0
    root.bind("<Button-1>",stepBFS)

num = 0

def DFS():
    """
    深搜（依旧草率）
    """
    #canvas.create_line(900, 10, 900, 700, fill = "orange", width = 100)
    global num
    drawList = [0, 1, 4, 3, 4, 6] 
    def back(n):
        circle(circles.get(n).position, color = "yellow")
        canvas.create_text(400, 350, text = n, font = ("楷体", 20), fill = "black")
    def stepDFS(event):
        """
        绘制每一步
        """
        global num
        circle(circles.get(drawList[num]).position, color = "blue")
        if drawList[num] in drawList[:num]:
            back(drawList[num - 1])
        num +=1
        if num==6:
            tk.messagebox.showinfo('tip', '演示结束，谢谢观看！')
            draw()
            num = 0
    root.bind("<Button-1>",stepDFS)
    
    #canvas.create_line(900, 10, 900, 700, fill = "white", width = 100)

def main():
    draw()
    canvas.mainloop()

if __name__ == '__main__':
    main()