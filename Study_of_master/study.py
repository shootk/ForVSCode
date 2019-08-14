import wx
import cv2
# import time
import numpy as np
from guide_module import guide
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

        # main ui
        self.Title = "webcam"

        # カメラ
        self.camera = cv2.VideoCapture(0)
        return_value, frame = self.camera.read()

        # カメラパネル
        self.webcampanel = WebcamPanel(self, frame)

        # キャリブレーションボタン配置，キャリブレーション設定
        self.calibration_button = wx.Button(self, wx.ID_ANY, '範囲設定')
        self.do_calibrate = False
        self.calibrate_points = np.float32(
            [[0, 0], [640, 0], [0, 480], [640, 480]])
        # メインウィンドウのサイズ感決定，パネル，ボタン配置
        main_window_sizer = wx.BoxSizer(wx.VERTICAL)
        main_window_sizer.Add(self.webcampanel, 7,
                              wx.CENTER | wx.BOTTOM | wx.EXPAND, 1)
        main_window_sizer.SetItemMinSize(self.webcampanel, (640, 480))
        main_window_sizer.Add(self.calibration_button, 1,
                              wx.CENTER | wx.BOTTOM | wx.EXPAND)
        # サイズを合わせる
        main_window_sizer.Fit(self)
        self.SetSizer(main_window_sizer)

        # カメラの画像を再描画する関数を呼び出す間隔を設定
        self.timer = wx.Timer(self)
        self.timer.Start(1000. / 10)

        self.Bind(wx.EVT_TIMER, self.WebcamPanelNextFrame)
        self.Bind(wx.EVT_BUTTON, self.Calibration)

        # ガイドを表示するウィンドウを作成，表示
        guide_window = guideWindow(self)
        guide_window.Show()

    def WebcamPanelNextFrame(self, e):  # カメラ画像書き換え
        return_value, frame = self.camera.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.webcampanel.bmp.CopyFromBuffer(frame)
        self.webcampanel.Refresh()

    def Calibration(self, e):  # キャリブレーション状態切替
        self.do_calibrate = not self.do_calibrate
        if self.do_calibrate:
            self.calibration_button.SetBackgroundColour('#6fbbee')
        else:
            self.calibration_button.SetBackgroundColour('#ffffff')

    def MouseDown(self, e):
        if self.do_calibrate:
            self.src_pt = [e.X, e.Y]

    def MouseUp(self, e):
        if self.do_calibrate:
            self.dst_pt = [e.X, e.Y]
            self.calibrate()

    def calibrate(self):
        src_pts = np.float32(
            [self.src_pt, self.src_pt, self.src_pt, self.src_pt])
        check_array = self.calibrate_points - src_pts
        distance = np.sum(np.square(check_array), axis=1)
        min_index = np.argmin(distance)
        self.calibrate_points[min_index] = self.dst_pt
        print(self.calibrate_points)
        cv2.line()


class guidePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure_guide = guide.FigureGuide()
        self.guide_image = np.zeros((640, 480), dtype=np.uint8)

    def set_guide(self, line):
        self.figure_guide.set_line(line.start, line.end)

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
