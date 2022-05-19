# -*- coding:utf-8 -*-
"""
    Tic Tac Toe on PyQt5 Python3.10(conda)
    System Development A 2022/05/17

    quote :
    Window : https://www.sejuku.net/blog/75467
    Widgets,Graphics :https://qiita.com/kenasman/items/73d01df973a25ae704e4
    MsgBox : https://webbibouroku.com/Blog/Article/qgis3-python-messagebox , https://doc.qt.io/qtforpython/PySide2/QtWidgets/QMessageBox.html
"""

import sys
from PyQt5.QtCore import QLineF, QPointF, QRectF, Qt
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QMessageBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QBrush, QColor, QPainter



class Ox(QGraphicsItem):
    '''
    描画アイテム : ○と✗(QGraphicsItemを継承)
    [マス目の状態:Ox.board[] ]
    空 : -1
    ○ (ItemO): 0
    ✗ (ItemX): 1
    現在の手番 : Ox.turn -> 0 OR 1
    '''
    def __init__(self):
        # 初期化
        super(Ox, self).__init__()
        self.board = [[-1, -1, -1],
                      [-1, -1, -1],
                      [-1, -1, -1]]  # 3x3盤面状態
        self.ItemO = 0  # 定義 O : 0
        self.ItemX = 1  # 定義 X : 1
        self.turn = self.ItemO  # 先手 : O


    def replay(self):
        # もう一度最初からプレイ
        for y in range(3):
            for x in range(3):
                self.board[y][x] = -1  # 全マス目を空にして再スタート
        self.turn = self.ItemO  # 先手 : O
        self.update() # 描画の更新

    def put(self, x, y):
        '''
        OかXを置く
        :param x: 盤面上での置く位置のx座標(0~3)
        :param y: 盤面上での置く位置のy座標(0~3)
        :return:  none
        '''
        if x < 0 or y < 0 or x >= 3 or y >= 3:
            # 盤面の範囲外 選択不可
            return
        if self.board[y][x] == -1:
            # 空状態 -> oかxへ(0か1)
            self.board[y][x] = self.turn
            self.turn = 1 - self.turn  # 手番を相手の番へ

    def paint(self, painter, option, widget):
        '''
        3x3盤面の格子を描画する(paint():overridden)
        :param painter:widget上に描画できるPen
        :param option:
        :param widget:
        :return:
        '''
        painter.setPen(Qt.black)  # Pen 黒色
        painter.drawLine(0, 100, 300, 100)  # (0,100)から(300,100)まで線を引く
        painter.drawLine(0, 200, 300, 200)
        painter.drawLine(100, 0, 100, 300)
        painter.drawLine(200, 0, 200, 300)

        # 盤面上にて OXを描画
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == self.ItemO:
                    # Oが置かれているマス目:
                    painter.setPen(Qt.red)  # Pen 赤色
                    painter.drawEllipse(QPointF(50 + x*100, 50 + y*100), 30, 30)  # 座標QPointF(...)中心に 短径長径30の赤い丸を描く
                elif self.board[y][x] == self.ItemX:
                    # Xが置かれているマス目:
                    painter.setPen(Qt.blue)  # Pen 青色
                    painter.drawLine(20 + x*100, 20 + y*100, 80 + x*100, 80 + y*100)
                    painter.drawLine(20 + x*100, 80 + y*100, 80 + x*100, 20 + y*100)  # Xを描く


    def mousePressEvent(self, event):
        '''
        マウスカーソルの位置座標とイベント取得:
        :param event: QtCore.QEvent -> QtGui.QEnterEvent
        :return:
        '''
        pos = event.pos()  # QPoint():マウスカーソルの位置(受け取るwidgetでの相対位置)
        self.put(int(pos.x()/100), int(pos.y()/100))  # OかXをカーソル位置に置く
        self.judge()
        self.update()  # 更新
        super(Ox, self).mousePressEvent(event)

    def boundingRect(self):
        return QRectF(0, 0, 300, 300)

    def judge(self):
        '''
        mousePressEvent発火毎に 実行
        :param board: 3x3盤面状態[[-1,-1,-1],
                                [-1,-1,-1],
                                [-1,-1,-1]]
        :winner: 勝者 o:0, x:1, 未確定:-1
        '''
        board = self.board
        winner_item = ""

        if board[0][0] == board[0][1] == board[0][2]:
            # 一番上の行:000 or 111:
            winner = board[0][0]
        elif board[0][0] == board[1][0] == board[2][0]:
            # 一番左の列:000 or 111
            winner = board[0][0]
        elif board[0][0] == board[1][1] == board[2][2]:
            # 左上から右下への斜め:000 or 111
            winner = board[0][0]
        elif board[1][0] == board[1][1] == board[1][2]:
            # 真ん中の行(左→右):000 or 111
            winner = board[1][0]
        elif board[2][0] == board[2][1] == board[2][2]:
            # 一番下の行(左→右):000 or 111
            winner = board[2][0]
        elif board[2][0] == board[1][1] == board[0][2]:
            # 左下から右上への斜め:000 or 111
            winner = board[2][0]
        elif board[0][1] == board[1][1] == board[2][1]:
            # 真ん中の列:000 or 111
            winner = board[0][1]
        elif board[0][2] == board[1][2] == board[2][2]:
            # 一番右の列:000 or 111
            winner = board[0][2]

        if winner == -1:
            return 
        elif winner == 0:
            winner_item = "○"
        elif winner == 1:
            winner_item = "✕"
        QMessageBox.information(None, "勝敗判定", "{}の勝ちです！".format(winner_item), QMessageBox.Yes)  # 通知MsgBox ボタン:はい(Y)





class MainWindow(QGraphicsView):
    '''
    メインウィンドウ
    '''
    def __init__(self):
        super(MainWindow, self).__init__()
        scene = QGraphicsScene(self)
        self.ox = Ox()  # インスタンス生成
        scene.addItem(self.ox)
        scene.setSceneRect(0, 0, 300, 300)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setWindowTitle("三目並べ○✕")

    def keyPressEvent(self, event):
        # キー入力で [R]ESET(再プレイ)
        key = event.key()  # キーボードからの入力を読み取る
        if key == Qt.Key_R:
            # キーボードのRキーが押されたら:
            self.ox.replay()  # ゲームを再スタート
        super(MainWindow, self).keyPressEvent(event)








if __name__ == '__main__':
    # main()
    app = QApplication(sys.argv)
    mainWindow = MainWindow()  # メインウィンドウ インスタンス生成

    mainWindow.show()  # メインウィンドウ 表示
    sys.exit(app.exec_())  # 終了時処理