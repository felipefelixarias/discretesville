# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMainWindow
# import sys
# from PyQt5.QtGui import QImage

# class Window(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         top = 400
#         left = 400
#         width = 800
#         height = 600

#         self.setWindowTitle("Discretesville")
#         self.setGeometry(top,left,width,height)
#         self.setStyleSheet("background-color:black;")
        


# #if __name__ == "main":
# app = QApplication([])
# window = Window()
# window.show()
# app.exec_()

import Tkinter as tk

board = [ [None]*10 for _ in range(10) ]

counter = 0

root = tk.Tk()

def on_click(i,j,event):
    global counter
    color = "red" if counter%2 else "black"
    event.widget.config(bg=color)
    board[i][j] = color
    counter += 1


for i,row in enumerate(board):
    for j,column in enumerate(row):
        L = tk.Label(root,text='    ',bg='grey')
        L.grid(row=i,column=j)
        L.bind('<Button-1>',lambda e,i=i,j=j: on_click(i,j,e))

root.mainloop()