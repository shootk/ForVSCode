import wx
import cv2
# import time
import numpy as np
from guidemodule import guide
import concurrent.futures


class MyThread(concurrent.futures.ProcessPoolExecutor):
    def __init__(self):
        super(MyThread, self).__init__()


class WebcamPanel(wx.Panel):
    def __init__(self, parent, frame):  # fps15くらいが目安
        wx.Panel.__init__(self, parent)

        height, width = frame.shape[:2]

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp = wx.BitmapFromBuffer(width, height, frame)

        self.SetSize((width, height))

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, parent.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, parent.MouseUp)

    def OnPaint(self, e):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)


class MainWindow(wx.Frame):
    def __init__(self):
        # 継承
        wx.Frame.__init__(self, None)
        self.Title = "webcam"

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
            [(0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1)])
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
        self.timer.Start(1000. / 10)
        self.Bind(wx.EVT_TIMER, self.WebcamPanelNextFrame)

        # ガイドを表示するウィンドウを作成，表示
        guide_window = guideWindow(self)
        guide_window.Show()

    def WebcamPanelNextFrame(self, e):  # カメラ画像書き換え
        return_value, frame = self.camera.read()
        if return_value:
            for i in range(len(self.calibrate_points)):
                cv2.line(
                    frame, tuple(self.calibrate_points[i % 4]), tuple(self.calibrate_points[(i + 1) % 4]), (0, 255, 0))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.webcampanel.bmp.CopyFromBuffer(frame)
        self.webcampanel.Refresh()

    def CalibStateChange(self, e):  # キャリブレーション状態切替
        self.do_calibrate = not self.do_calibrate
        self.do_color_set = False
        self.color_set_button.SetBackgroundColour('#ffffff')
        if self.do_calibrate:
            self.calibration_button.SetBackgroundColour('#6fbbee')
        else:
            self.calibration_button.SetBackgroundColour('#ffffff')

    def SetColorStateChange(self, e):  # チョーク色取得状態切替
        self.do_color_set = not self.do_color_set
        self.do_calibrate = False
        self.calibration_button.SetBackgroundColour('#ffffff')
        if self.do_color_set:
            self.color_set_button.SetBackgroundColour('#edc26a')
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

        else:
            self.ok_button.SetBackgroundColour('#ffffff')
            self.ok_button.Enable()
            self.color_set_button.Enable()
            self.calibration_button.Enable()
            self.cancel_button.Disable()

    def MouseDown(self, e):  # マウスが押されたらその地点の座標を取得
        if self.do_calibrate:
            self.src_pt = (e.X, e.Y)

    def MouseUp(self, e):  # マウスが離されたらその座標を取得
        if self.do_calibrate:
            self.dst_pt = (e.X, e.Y)
            self.calibrate()

        elif self.do_color_set:
            return_value, frame = self.camera.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if return_value:
                hsvframe = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
                self.choke_color = tuple(hsvframe[e.Y, e.X])
                self.color_set_button.SetBackgroundColour(
                    tuple(frame[e.Y, e.X]))

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


class guidePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure_guide = guide.FigureGuide()
        self.guide_image = np.zeros((640, 480), dtype=np.uint8)
        self.set_guide(guide.Line(guide.Point(50, 50), guide.Point(200, 200)))
        # self.redraw()

    def set_guide(self, line):
        self.figure_guide.set_line(line)

    def redraw(self):
        self.figure_guide.draw_guide(self.guide_image)


class guideWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.Maximize()
        self.guide_panel = guidePanel(self)
        self.switch_window(parent)

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
                    (int(parent_display_w - (self.guide_display_w / 2)), int(self.guide_display_h / 2)))
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
