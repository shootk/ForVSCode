import sys
import tkinter as tk
from tkinter import font
import threading
import socket
import time
import PyQt5.QtWidgets.QtWidgets as QtWidgets


Value = 0

# メインウィンドウ作成
root = tk.Tk()
root.title("select shape")
# メインウィンドウを640x480にする
root.geometry("670x500")
# サイズ・太文字設定
font1 = font.Font(family='Helvetica', size=40, weight='bold')
# ラベルを追加
label = tk.Label(root, text="どんな図形を描きますか", font=font1)
# 表示
label.grid()
# 場所を指定
label.pack(side="top")


# ページ切り替え(長方形)
def push1():
    rectangle_window = tk.Toplevel(root)
    rectangle_window.title("rectangle_size")
    rectangle_window.geometry("670x580")
    # サイズ・太文字設定
    font2 = font.Font(family='Helvetica', size=40, weight='bold')
    # ラベルを追加
    label = tk.Label(rectangle_window, text="サイズを入力して下さい", font=font2)
    # 表示
    label.grid()
    # 場所を指定
    # label.place()
    # 画像の取得
    img1 = tk.PhotoImage(file='rectangle.png')
    logo_lab = tk.Label(rectangle_window, image=img1)
    logo_lab.photo = img1
    logo_lab.place(x=10, y=45)

    # label1=tk.Label(rectangle_window, image=img1)
    # label1.grid()
    # 数値入力フォーム作成
    font3 = font.Font(size=40, weight='bold')
    lbl = tk.Label(rectangle_window, text='縦(m):', font=font3)
    lbl.place(x=120, y=310)
    font4 = font.Font(size=40, weight='bold')
    lbl = tk.Label(rectangle_window, text='横(m):', font=font4)
    lbl.place(x=120, y=400)
    # テキストボックス
    txt1 = tk.Entry(rectangle_window, width=30)
    txt1.place(x=240, y=332)
    txt2 = tk.Entry(rectangle_window, width=30)
    txt2.place(x=240, y=422)

    def tello1():
        tello1_window = tk.Toplevel(rectangle_window)
        tello1_window.title("command_rectangle")
        tello1_window.geometry("670x580")

    # 以下ドローン制御のプログラム
        class TelloController1(QtWidgets.QtWidgets.QtWidgets.QtWidget):
            def __init__(self):
                QtWidgets.QtWidgets.QtWidgets.QtWidget.__init__(self)
                self.initConnection()
                self.initUI()
                # 通信の設定

            def initConnection(self):
                host = ''
                port = 9000
                locaddr = (host, port)
                self.tello = ('192.168.10.1', 8889)
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sock.bind(locaddr)
                # 受信スレッド起動
                recvThread = threading.Thread(target=self.recvSocket)
                recvThread.setDaemon(True)
                recvThread.start()

                # 最初にcommandコマンドを送信
                try:
                    sent = self.sock.sendto(
                        'command'.encode(encoding="utf-8"), self.tello)
                except:
                    pass
            # UIの作成

            def initUI(self):
                self.label = QtWidgets.QtWidgets.QtWidgets.QLabel('')
                self.label.setFrameStyle(
                    QtWidgets.QtWidgets.QtWidgets.QFrame.Box | QtWidgets.QtWidgets.QtWidgets.QFrame.Plain)

            # 入力フォーム
                # self.textbox=QLineEdit(self)
                # self.textbox.move(20, 20)

            # 決定ボタン
                # decideBtn=QtWidgets.QtWidgets.QPushButton("決定")
                # decideBtn.clicked.connect(self.decideBtnClicked)

            # 終了ボタン
                endBtn = QtWidgets.QtWidgets.QtWidgets.QtWidgets.QPushButton(
                    "End")
                endBtn.clicked.connect(self.endBtnClicked)

            # 離着陸ボタン
                takeoffBtn = QtWidgets.QtWidgets.QPushButton("Takeoff")
                takeoffBtn.clicked.connect(self.takeoffBtnClicked)
                landBtn = QtWidgets.QtWidgets.QPushButton("Land")
                landBtn.clicked.connect(self.landBtnClicked)

            # startボタン
                startBtn = QtWidgets.QtWidgets.QPushButton("start")
                startBtn.clicked.connect(self.startBtnClicked, Value)

            # ボタンのレイアウト
                layout = QtWidgets.QtWidgets.QGridLayout()
                # layout.addWidget(self.textbox,0,0)
                # layout.addWidget(decideBtn,0,1)
                # layout.addWidget(self.label,1,0)
                layout.addWidget(endBtn, 3, 1)
                layout.addWidget(takeoffBtn, 1, 0)
                layout.addWidget(landBtn, 1, 1)
                layout.addWidget(startBtn, 2, 0)
                self.setLayout(layout)
            # 値取得
            # def decideBtnClicked(self):
                # value=self.textbox.text()
                # print(value)

            # 終了処理
            def endBtnClicked(self):
                sys.exit()

            # takeoffコマンド送信
            def takeoffBtnClicked(self):
                try:
                    sent = self.sock.sendto(
                        'takeoff'.encode(encoding="utf-8"), self.tello)
                except:
                    pass
            # landコマンド送信

            def landBtnClicked(self):
                try:
                    sent = self.sock.sendto(
                        'land'.encode(encoding="utf-8"), self.tello)
                except:
                    pass

            # forwardコマンド送信
            def startBtnClicked(self, value):
                try:
                    sent = self.sock.sendto(
                        'start' + value.encode(encoding="utf-8"), self.tello)
                except:
                    pass

            # Telloからのレスポンス受信
            def recvSocket(self):
                while True:
                    try:
                        data, server = self.sock.recvfrom(1518)
                        self.label.setText(data.decode(encoding="utf-8"))
                    except:
                        pass
        if __name__ == '__main__':
            app = QtWidgets.QtWidgets.QApplication(sys.argv)
            window = TelloController1()
            window.show()
            sys.exit(app.exec_())
    # 以上ドローン制御のプログラム

    # ボタンを設置(長方形)
    Buttonx = tk.Button(rectangle_window, text='決定', command=tello1)
    Buttonx.place(x=580, y=480)

# ページ切り替え(正方形)


def push2():
    square_window = tk.Toplevel(root)
    square_window.title("square_size")
    square_window.geometry("670x580")
    # サイズ・太文字設定
    font3 = font.Font(family='Helvetica', size=40, weight='bold')
    # ラベルを追加
    label = tk.Label(square_window, text="サイズを入力して下さい", font=font3)
    # 表示
    label.grid()
    # 場所を指定
    label.place(x=10, y=200)
    # 画像の取得
    img2 = tk.PhotoImage(file='square.png')
    logo_lab = tk.Label(square_window, image=img2)
    logo_lab.photo = img2
    logo_lab.place(x=60, y=27)
    # 数値入力フォーム作成
    font3 = font.Font(size=40, weight='bold')
    lbl = tk.Label(square_window, text='一辺(m):', font=font3)
    lbl.place(x=120, y=300)
    font4 = font.Font(size=40, weight='bold')
    # テキストボックス
    txt1 = tk.Entry(square_window, width=30)
    txt1.place(x=270, y=322)

    def tello2():
        tello2_window = tk.Toplevel(square_window)
        tello2_window.title("command_square")
        tello2_window.geometry("670x580")
    # 以下ドローン制御のプログラム

        class TelloController1(QtWidgets.QtWidget):
            def __init__(self):
                QtWidgets.QtWidget.__init__(self)
                self.initConnection()
                self.initUI()
            # 通信の設定

            def initConnection(self):
                host = ''
                port = 9000
                locaddr = (host, port)
                self.tello = ('192.168.10.1', 8889)
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sock.bind(locaddr)
                # 受信スレッド起動
                recvThread = threading.Thread(target=self.recvSocket)
                recvThread.setDaemon(True)
                recvThread.start()

                # 最初にcommandコマンドを送信
                try:
                    sent = self.sock.sendto(
                        'command'.encode(encoding="utf-8"), self.tello)
                except:
                    pass
            # UIの作成

            def initUI(self):
                self.label = QtWidgets.QLabel('')
                self.label.setFrameStyle(
                    QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)

            # 入力フォーム
                # self.textbox=QLineEdit(self)
                # self.textbox.move(20, 20)

            # 決定ボタン
                # decideBtn=QtWidgets.QtWidgets.QPushButton("決定")
                # decideBtn.clicked.connect(self.decideBtnClicked)

            # 終了ボタン
                endBtn = QtWidgets.QtWidgets.QPushButton("End")
                endBtn.clicked.connect(self.endBtnClicked)

            # 離着陸ボタン
                takeoffBtn = QtWidgets.QtWidgets.QPushButton("Takeoff")
                takeoffBtn.clicked.connect(self.takeoffBtnClicked)
                landBtn = QtWidgets.QtWidgets.QPushButton("Land")
                landBtn.clicked.connect(self.landBtnClicked)

            # startボタン
                startBtn = QtWidgets.QtWidgets.QPushButton("start")
                startBtn.clicked.connect(self.startBtnClicked, Value)

            # ボタンのレイアウト
                layout = QtWidgets.QtWidgets.QGridLayout()
                # layout.addWidget(self.textbox,0,0)
                # layout.addWidget(decideBtn,0,1)
                # layout.addWidget(self.label,1,0)
                layout.addWidget(endBtn, 3, 1)
                layout.addWidget(takeoffBtn, 1, 0)
                layout.addWidget(landBtn, 1, 1)
                layout.addWidget(startBtn, 2, 0)
                self.setLayout(layout)
            # 値取得
            # def decideBtnClicked(self):
                # value=self.textbox.text()
                # print(value)

            # 終了処理
            def endBtnClicked(self):
                sys.exit()

            # takeoffコマンド送信
            def takeoffBtnClicked(self):
                try:
                    sent = self.sock.sendto(
                        'takeoff'.encode(encoding="utf-8"), self.tello)
                except:
                    pass
            # landコマンド送信

            def landBtnClicked(self):
                try:
                    sent = self.sock.sendto(
                        'land'.encode(encoding="utf-8"), self.tello)
                except:
                    pass

            # forwardコマンド送信
            def startBtnClicked(self, value):
                try:
                    sent = self.sock.sendto(
                        'start' + value.encode(encoding="utf-8"), self.tello)
                except:
                    pass

            # Telloからのレスポンス受信
            def recvSocket(self):
                while True:
                    try:
                        data, server = self.sock.recvfrom(1518)
                        self.label.setText(data.decode(encoding="utf-8"))
                    except:
                        pass
    if __name__ == '__main__':
        app = QtWidgets.QtWidgets.QApplication(sys.argv)
        window = TelloController1()
        window.show()
        sys.exit(app.exec_())
    # 以上ドローン制御のプログラム
    # ボタンを設置(正方形)
    Buttony = tk.Button(square_window, text='決定', command=tello2)
    Buttony.place(x=580, y=480)

# ページ切り替え(円)


def push3():
    circle_window = tk.Toplevel(root)
    circle_window.title("circle_size")
    circle_window.geometry("670x580")
    # サイズ・太文字設定
    font4 = font.Font(family='Helvetica', size=40, weight='bold')
    # ラベルを追加
    label = tk.Label(circle_window, text="サイズを入力して下さい", font=font4)
    # 表示
    label.grid()
    # 場所を指定
    label.place(x=10, y=200)
    # 画像の取得
    img3 = tk.PhotoImage(file='circle.png')
    logo_lab = tk.Label(circle_window, image=img3)
    logo_lab.photo = img3
    logo_lab.place(x=60, y=27)
    # 数値入力フォーム作成
    font3 = font.Font(size=40, weight='bold')
    lbl = tk.Label(circle_window, text='半径(m):', font=font3)
    lbl.place(x=120, y=300)
    # テキストボックス
    txt1 = tk.Entry(circle_window, width=30)
    txt1.place(x=280, y=322)

    def tello3():
        tello3_window = tk.Toplevel(circle_window)
        tello3_window.title("command_circle")
        tello3_window.geometry("670x580")
    # 以下ドローン制御のプログラム

        class TelloController1(QtWidgets.QtWidget):
            def __init__(self):
                QtWidgets.QtWidget.__init__(self)
                self.initConnection()
                self.initUI()
            # 通信の設定

            def initConnection(self):
                host = ''
                port = 9000
                locaddr = (host, port)
                self.tello = ('192.168.10.1', 8889)
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sock.bind(locaddr)
                # 受信スレッド起動
                recvThread = threading.Thread(target=self.recvSocket)
                recvThread.setDaemon(True)
                recvThread.start()

                # 最初にcommandコマンドを送信
                try:
                    sent = self.sock.sendto(
                        'command'.encode(encoding="utf-8"), self.tello)
                except:
                    pass
            # UIの作成

            def initUI(self):
                self.label = QtWidgets.QLabel('')
                self.label.setFrameStyle(
                    QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)

            # 入力フォーム
                # self.textbox=QLineEdit(self)
                # self.textbox.move(20, 20)

            # 決定ボタン
                # decideBtn=QtWidgets.QtWidgets.QPushButton("決定")
                # decideBtn.clicked.connect(self.decideBtnClicked)

            # 終了ボタン
                endBtn = QtWidgets.QtWidgets.QPushButton("End")
                endBtn.clicked.connect(self.endBtnClicked)

            # 離着陸ボタン
                takeoffBtn = QtWidgets.QtWidgets.QPushButton("Takeoff")
                takeoffBtn.clicked.connect(self.takeoffBtnClicked)
                landBtn = QtWidgets.QtWidgets.QPushButton("Land")
                landBtn.clicked.connect(self.landBtnClicked)

            # startボタン
                startBtn = QtWidgets.QtWidgets.QPushButton("start")
                startBtn.clicked.connect(self.startBtnClicked, Value)

            # ボタンのレイアウト
                layout = QtWidgets.QtWidgets.QGridLayout()
                # layout.addWidget(self.textbox,0,0)
                # layout.addWidget(decideBtn,0,1)
                # layout.addWidget(self.label,1,0)
                layout.addWidget(endBtn, 3, 1)
                layout.addWidget(takeoffBtn, 1, 0)
                layout.addWidget(landBtn, 1, 1)
                layout.addWidget(startBtn, 2, 0)
                self.setLayout(layout)
            # 値取得
            # def decideBtnClicked(self):
                # value=self.textbox.text()
                # print(value)

            # 終了処理
            def endBtnClicked(self):
                sys.exit()

            # takeoffコマンド送信
            def takeoffBtnClicked(self):
                try:
                    sent = self.sock.sendto(
                        'takeoff'.encode(encoding="utf-8"), self.tello)
                except:
                    pass
            # landコマンド送信

            def landBtnClicked(self):
                try:
                    sent = self.sock.sendto(
                        'land'.encode(encoding="utf-8"), self.tello)
                except:
                    pass

            # forwardコマンド送信
            def startBtnClicked(self, value):
                try:
                    sent = self.sock.sendto(
                        'start' + value.encode(encoding="utf-8"), self.tello)
                except:
                    pass

            # Telloからのレスポンス受信
            def recvSocket(self):
                while True:
                    try:
                        data, server = self.sock.recvfrom(1518)
                        self.label.setText(data.decode(encoding="utf-8"))
                    except:
                        pass
    if __name__ == '__main__':
        app = QtWidgets.QtWidgets.QApplication(sys.argv)
        window = TelloController1()
        window.show()
        sys.exit(app.exec_())
    # 以上ドローン制御のプログラム
    # ボタンを設置(円)
    Buttonz = tk.Button(circle_window, text='決定', command=tello3)
    Buttonz.place(x=580, y=480)

# ページ切り替え(直線)


def push4():
    # print(Value)
    straight_window = tk.Toplevel(root)
    straight_window.title("straight_size")
    straight_window.geometry("670x580")
    # サイズ・太文字設定
    font5 = font.Font(family='Helvetica', size=40, weight='bold')
    # ラベルを追加
    label = tk.Label(straight_window, text="サイズを入力して下さい", font=font5)
    # 表示
    label.grid()
    # 場所を指定
    label.place(x=10, y=200)
    # 数値入力フォーム作成
    font3 = font.Font(size=40, weight='bold')
    lbl = tk.Label(straight_window, text='m', font=font3)
    lbl.place(x=280, y=300)

    # テキストボックス
    txt1 = tk.Entry(straight_window, width=20)
    txt1.place(x=90, y=322)

    def tello4():
        tello4_window = tk.Toplevel(straight_window)
        tello4_window.title("command_straight")
        tello4_window.geometry("670x580")
    # 以下ドローン制御のプログラム
        # class TelloController1(QtWidgets.QtWidget):

        def __init__(self):
            QtWidgets.QtWidget.__init__(self)
            self.initConnection()
            self.initUI()
        # 通信の設定

        def initConnection(self):
            host = ''
            port = 9000
            locaddr = (host, port)
            self.tello = ('192.168.10.1', 8889)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(locaddr)
            # 受信スレッド起動
            recvThread = threading.Thread(target=self.recvSocket)
            recvThread.setDaemon(True)
            recvThread.start()

            # 最初にcommandコマンドを送信
            try:
                sent = self.sock.sendto(
                    'command'.encode(encoding="utf-8"), self.tello)
            except:
                pass
        # UIの作成
        # def initUI(self):
            # print(Value)
            # self.label=QtWidgets.QLabel('')
            # self.label.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)

        # 入力フォーム
            # self.textbox=QLineEdit(self)
            # self.textbox.move(20, 20)

        # 決定ボタン
            # decideBtn=QtWidgets.QtWidgets.QPushButton("決定")
            # decideBtn.clicked.connect(self.decideBtnClicked)

        # 終了ボタン
            endBtn = QtWidgets.QtWidgets.QPushButton("End")
            endBtn.clicked.connect(self.endBtnClicked)

        # 離着陸ボタン
            takeoffBtn = QtWidgets.QtWidgets.QPushButton("Takeoff")
            takeoffBtn.clicked.connect(self.takeoffBtnClicked)
            landBtn = QtWidgets.QtWidgets.QPushButton("Land")
            landBtn.clicked.connect(self.landBtnClicked)

        # startボタン
            startBtn = QtWidgets.QtWidgets.QPushButton("start")
            startBtn.clicked.connect(self.startBtnClicked, Value)

        # ボタンのレイアウト
            layout = QtWidgets.QtWidgets.QGridLayout()
            # layout.addWidget(self.textbox,0,0)
            # layout.addWidget(decideBtn,0,1)
            # layout.addWidget(self.label,1,0)
            layout.addWidget(endBtn, 3, 1)
            layout.addWidget(takeoffBtn, 1, 0)
            layout.addWidget(landBtn, 1, 1)
            layout.addWidget(startBtn, 2, 0)
            self.setLayout(layout)
        # 値取得
        # def decideBtnClicked(self):
            # value=self.textbox.text()
            # print(value)

        # 終了処理
        def endBtnClicked(self):
            sys.exit()

        # takeoffコマンド送信
        def takeoffBtnClicked(self):
            try:
                sent = self.sock.sendto(
                    'takeoff'.encode(encoding="utf-8"), self.tello)
            except:
                pass

        # landコマンド送信
        def landBtnClicked(self):
            try:
                sent = self.sock.sendto(
                    'land'.encode(encoding="utf-8"), self.tello)
            except:
                pass

        # forwardコマンド送信
        def startBtnClicked(self, value):
            try:
                sent = self.sock.sendto(
                    'start' + value.encode(encoding="utf-8"), self.tello)
            except:
                pass

        # Telloからのレスポンス受信
        def recvSocket(self):
            while True:
                try:
                    data, server = self.sock.recvfrom(1518)
                    self.label.setText(data.decode(encoding="utf-8"))
                except:
                    pass
    if __name__ == '__main__':
        app = QtWidgets.QtWidgets.QApplication(sys.argv)
        window = TelloController1()
        window.show()
        sys.exit(app.exec_())
# 以上ドローン制御のプログラム
    # ボタンを設置(直線)
    Buttonw = tk.Button(straight_window, text='決定', command=tello4)
    Buttonw.place(x=580, y=480)


# ボタンを設置(長方形)
Button1 = tk.Button(text='長方形', width=20, height=10, command=push1)
Button1.place(x=90, y=100)

# ボタンを設置(正方形)
Button2 = tk.Button(text='正方形', width=20, height=10, command=push2)
Button1.place(x=280, y=100)

# ボタンを設置(円)
Button3 = tk.Button(text='円', width=20, height=10, command=push3)
Button1.place(x=90, y=270)
# ボタンを設置(直線)
Button4 = tk.Button(text='直線', width=20, height=10, command=push4)
Button1.place(x=280, y=270)

# rootを表示し無限ループ
root.mainloop()
