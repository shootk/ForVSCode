import wx
import cv2
import time
import numpy as np
import random
from guidemodule import guide
from detectormodule import linedetector
import concurrent.futures


class MyThread(concurrent.futures.ProcessPoolExecutor):
    def __init__(self):
        super(MyThread, self).__init__()


class WebcamPanel(wx.Panel):
    def __init__(self, parent, frame):
        '''
        Paramaters
        ----------
        parent : wd.Frame
        frame : Mat
        '''
        # Webカメラの入力画像を移すパネルの初期設定をオーバーライド
        wx.Panel.__init__(self, parent)
        # 入力画像の高さ,幅を取得
        height, width = frame.shape[:2]
        # 入力画像をRGBの並びに変換、ビットマップ化する
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp = wx.BitmapFromBuffer(width, height, frame)
        # 入力画像の高さ、幅に合わせる
        self.SetSize((width, height))

        #
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, parent.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, parent.MouseLeftUp)
        self.Bind(wx.EVT_RIGHT_UP, parent.MouseRightUp)

    def OnPaint(self, e):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)


class MainWindow(wx.Frame):
    def __init__(self):
        # 継承
        wx.Frame.__init__(self, None)
        self.Title = "webcam"

        # ガイドを表示するウィンドウを作成，表示
        self.guide_window = guideWindow(self)
        self.guide_window.Show()
        self.line_detector = linedetector.LineDitector()
        # カメラ
        self.camera = cv2.VideoCapture(0)

        return_value, frame = self.camera.read()
        height, width = frame.shape[:2]
        # カメラパネル
        self.webcampanel = WebcamPanel(self, frame)

        # ボタン配置，キャリブレーション設定
        self.calibration_button = wx.Button(self, wx.ID_ANY, '範囲設定')
        self.do_calibrate = False
        self.calibrate_points = np.float32(
            [(0, 0), (0, height - 1), (width - 1, height - 1), (width - 1, 0)])
        self.calibration_button.Bind(wx.EVT_BUTTON, self.CalibStateChange)
        self.calibration_button.SetBackgroundColour('#ffffff')

        self.color_set_button = wx.Button(self, wx.ID_ANY, 'チョーク色取得')
        self.do_color_set = False
        self.choke_color = (255, 255, 255)
        self.color_set_button.Bind(wx.EVT_BUTTON, self.SetColorStateChange)
        self.color_set_button.SetBackgroundColour('#ffffff')

        self.cancel_button = wx.Button(self, wx.ID_ANY, 'CANCEL')
        self.cancel_button.SetBackgroundColour('#ffffff')
        self.cancel_button.Disable()
        self.cancel_button.Bind(wx.EVT_BUTTON, self.SelectChange)

        self.ok_button = wx.Button(self, wx.ID_ANY, 'OK')
        self.ok_button.SetBackgroundColour('#ffffff')
        self.ok_button.Bind(wx.EVT_BUTTON, self.SelectChange)

        self.selection = False

        self.do = True

        button_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_box_sizer.Add(self.cancel_button, 1, wx.EXPAND)
        button_box_sizer.Add(self.calibration_button,
                             2, wx.BOTTOM | wx.EXPAND)
        button_box_sizer.Add(self.color_set_button,
                             2, wx.BOTTOM | wx.EXPAND)
        button_box_sizer.Add(self.ok_button, 1, wx.EXPAND)

        # メインウィンドウのサイズ感決定，パネル，ボタン配置
        main_window_sizer = wx.BoxSizer(wx.VERTICAL)
        main_window_sizer.Add(self.webcampanel, 7,
                              wx.CENTER | wx.BOTTOM | wx.EXPAND, 1)
        main_window_sizer.SetItemMinSize(self.webcampanel, (640, 480))
        main_window_sizer.Add(button_box_sizer, 1, wx.BOTTOM | wx.EXPAND)
        # サイズを合わせる
        main_window_sizer.Fit(self)
        self.SetSizer(main_window_sizer)

        # カメラの画像を再描画する関数を呼び出す間隔を設定
        self.timer = wx.Timer(self)
        self.timer.Start(1000. / 15)
        self.Bind(wx.EVT_TIMER, self.WebcamPanelNextFrame)

    def WebcamPanelNextFrame(self, e):  # カメラ画像書き換え
        return_value, frame = self.camera.read()
        if return_value:
            for i in range(len(self.calibrate_points)):
                cv2.line(
                    frame, tuple(self.calibrate_points[i % 4]), tuple(self.calibrate_points[(i + 1) % 4]), (187, 111, 0))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.webcampanel.bmp.CopyFromBuffer(frame)
        self.webcampanel.Refresh()

    def CalibStateChange(self, e):  # キャリブレーション状態切替
        self.do_calibrate = not self.do_calibrate
        self.do_color_set = False
        self.color_set_button.SetBackgroundColour('#ffffff')
        if self.do_calibrate:
            self.calibration_button.SetBackgroundColour('#6fbbee')
            self.guide_window.guide_panel.color = True
            self.guide_window.guide_panel.Refresh()
        else:
            self.calibration_button.SetBackgroundColour('#ffffff')

    def SetColorStateChange(self, e):  # チョーク色取得状態切替
        self.do_color_set = not self.do_color_set
        self.do_calibrate = False
        self.calibration_button.SetBackgroundColour('#ffffff')
        if self.do_color_set:
            self.color_set_button.SetBackgroundColour('#afbea5')
            self.guide_window.guide_panel.color = False
            self.guide_window.guide_panel.Refresh()
        else:
            self.color_set_button.SetBackgroundColour('#ffffff')

    def SelectChange(self, e):
        self.selection = not self.selection
        if self.selection:
            self.ok_button.SetBackgroundColour('#74e69d')
            self.calibration_button.SetBackgroundColour('#ffffff')
            self.do_calibrate = False
            self.color_set_button.SetBackgroundColour('#ffffff')
            self.do_color_set = False

            self.ok_button.Disable()
            self.color_set_button.Disable()
            self.calibration_button.Disable()
            self.cancel_button.Enable()
            self.line_detector.SetColor(self.choke_color)
            return_value, frame = self.camera.read()
            guide_display = wx.Display(self.guide_window.display_index)
            _, _, w, h = guide_display.GetGeometry()
            src_pts = np.array(
                [[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]], dtype=np.float32)
            dst_pts = self.calibrate_points
            mat = cv2.getPerspectiveTransform(dst_pts, src_pts)
            self.guide_window.guide_panel.color = False
            self.guide_window.guide_panel.Refresh()
            self.warp_frame = cv2.warpPerspective(frame, mat, (w, h))
            self.line_detector.SetSrcImage(img=self.warp_frame)

        else:
            self.ok_button.SetBackgroundColour('#ffffff')
            self.ok_button.Enable()
            self.color_set_button.Enable()
            self.calibration_button.Enable()
            self.cancel_button.Disable()

    def MouseDown(self, e):  # マウスが押されたらその地点の座標を取得
        if self.do_calibrate:
            self.src_pt = (e.X, e.Y)

    def MouseLeftUp(self, e):  # マウスが離されたらその座標を取得
        if self.do_calibrate:
            self.dst_pt = (e.X, e.Y)
            self.calibrate()

        elif self.do_color_set:
            return_value, frame = self.camera.read()
            hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if return_value:
                self.choke_color = hsvframe[e.Y, e.X]
                self.line_detector.SetColor(self.choke_color)
                self.color_set_button.SetBackgroundColour(
                    tuple(frame[e.Y, e.X]))

        elif self.selection:
            return_value, frame = self.camera.read()
            guide_display = wx.Display(self.guide_window.display_index)
            _, _, w, h = guide_display.GetGeometry()
            src_pts = np.array(
                [[0, 0], [0, h - 1],
                 [w - 1, h - 1], [w - 1, 0]], dtype=np.float32)
            dst_pts = self.calibrate_points
            mat = cv2.getPerspectiveTransform(dst_pts, src_pts)
            self.warp_frame = cv2.warpPerspective(frame, mat, (w, h))
            self.line_detector.SetSrcImage(img=self.warp_frame)

    def MouseRightUp(self, e):
        if self.selection:
            return_value, frame = self.camera.read()
            guide_display = wx.Display(self.guide_window.display_index)
            _, _, w, h = guide_display.GetGeometry()
            src_pts = np.array(
                [[0, 0], [0, h - 1],
                 [w - 1, h - 1], [w - 1, 0]], dtype=np.float32)
            dst_pts = self.calibrate_points
            mat = cv2.getPerspectiveTransform(dst_pts, src_pts)
            self.warp_frame = cv2.warpPerspective(frame, mat, (w, h))
            self.line_detector.SetDstImage(img=self.warp_frame)
            self.line_ditecting()

    def calibrate(self):
        # マウスが押された点を要素とする長さ4の配列
        src_pts = np.float32(
            [self.src_pt, self.src_pt, self.src_pt, self.src_pt])
        # 現在の検出範囲4点のx,y座標とマウスが押されたx,y座標との差
        check_array = self.calibrate_points - src_pts
        # chack_arrayで求めたx,y座標からマウスが押された点と検出範囲の4角との距離を計算
        distance = np.sum(np.square(check_array), axis=1)
        # 一番短い距離となった配列番号を取得
        min_index = np.argmin(distance)
        # 上で求めた配列番号の点をマウスが離された点に変更
        self.calibrate_points[min_index] = self.dst_pt

    def line_ditecting(self):
        detected_line = self.line_detector.DoDetecting()
        if detected_line is not None:
            self.guide_window.guide_panel.line = detected_line
            self.guide_window.guide_panel.line_detect = True


class guidePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        guide_display = wx.Display(parent.display_index)
        _, _, width, height = guide_display.GetGeometry()
        self.line = guide.Line()
        self.line_detect = False
        self.color = False
        self.image_list = [
            wx.Bitmap('src/chara/arare.png'),
            wx.Bitmap('src/chara/ayamin.png'),
            wx.Bitmap('src/chara/chee.png'),
            wx.Bitmap('src/chara/gitex.png'),
            wx.Bitmap('src/chara/haru.png'),
            wx.Bitmap('src/chara/kazoo.png'),
            wx.Bitmap('src/chara/pakche.png'),
            wx.Bitmap('src/chara/shiro.png'),
            wx.Bitmap('src/chara/shoot.png'),
            wx.Bitmap('src/chara/tak.png'),
            wx.Bitmap('src/chara/tuna.png')
        ]
        self.SetSize(width, height)
        self.bmp = wx.EmptyBitmap(width, height, -1)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.place = [0, 0]
        self.chara = None

    def OnPaint(self, e):
        dc = wx.BufferedPaintDC(self)
        if self.color:
            dc.SetBackground(wx.Brush('white'))
        else:
            dc.SetBackground(wx.Brush('black'))

        dc.Clear()
        if self.line_detect:
            image = self.image_list[random.randint(0, len(self.image_list))]
            x1, y1 = 0, 0
            x2, y2 = 100, 100
            # x1, y1 = self.line.start.X, self.line.start.Y
            # x2, y2 = self.line.end.X, self.line.end.Y
            a = 1
            if (x1 < x2):
                x, y = x1, y1
                a = (y1 - y2) / (x1 - x2)
            elif(x2 < x1):
                x, y = x2, y2
                a = (y1 - y2) / (x1 - x2)
            dc.DrawBitmap(image, x, y)
        else:


class Chara():
    def __init__(self, line=guide.Line(), image):
        self.x1 = line.start.X
        self.y1 = line.start.Y
        self.x2 = line.end.X
        self.y2 = line.end.Y
        self.image = image
        if (x1 < x2):
            self.x, self.y = self.x1, self.y1
            self.a = (self.y1 - self.y2) / (self.x1 - self.x2)
        elif(x2 < x1):
            self.x, self.y = self.x2, self.y2
            self.a = (self.y1 - self.y2) / (self.x1 - self.x2)

    def step(self, r):
        self.x += r
        self.y += r * self.a
        return (x <= x2)


class guideWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.Maximize(True)
        self.display_index = 0
        self.switch_window(parent)
        self.guide_panel = guidePanel(self)
        self.guide_panel.Refresh()

        main_window_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_window_sizer.Add(self.guide_panel, 7,
                              wx.CENTER | wx.BOTTOM | wx.EXPAND, 1)
        main_window_sizer.SetItemMinSize(self.guide_panel, (1200, 1024))
        # サイズを合わせる
        main_window_sizer.Fit(self)
        self.timer = wx.Timer(self)
        self.timer.Start(1000. / 15)
        self.Bind(wx.EVT_TIMER, self.guide_panel.OnPaint)
        self.SetSizer(main_window_sizer)
        self.ShowFullScreen(True)

    def switch_window(self, parent):
        if wx.Display.GetCount() == 2:
            self.parent_display_index = wx.Display.GetFromWindow(parent)
            self.display_index = (self.parent_display_index + 1) % 2

            self.parent_display = wx.Display(self.parent_display_index)
            _, _, parent_display_w, parent_display_h = self.parent_display.GetGeometry()
            self.guide_display = wx.Display(self.display_index)
            _, _, self.guide_display_w, self.guide_display_h = self.guide_display.GetGeometry()

            parent_position_x, parent_position_y = parent.GetPosition()

            if parent_display_w > parent_position_x:
                self.SetPosition(
                    (int(parent_display_w + (self.guide_display_w / 2)), int(self.guide_display_h / 2)))
            else:
                self.SetPosition(
                    (int(self.guide_display_w / 2), int(self.guide_display_h / 2)))


def main():
    app = wx.App()
    main_window = MainWindow()
    main_window.Show()
    app.MainLoop()


# main関数呼び出し
if __name__ == "__main__":
    main()
