import wx
import cv2
import time
import numpy as np
from guide_module import guide
import bluetooth
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

        # inheritence
        wx.Frame.__init__(self, None)
        self.Title = "webcam"
        # main ui
        self.camera = cv2.VideoCapture(0)
        return_value, frame = self.camera.read()

        self.webcampanel = WebcamPanel(self, frame)
        self.calibration_button = wx.Button(self, wx.ID_ANY, '範囲設定')
        main_window_sizer = wx.BoxSizer(wx.VERTICAL)
        self.do_calibrate = False

        main_window_sizer.Add(self.webcampanel, 7,
                              wx.CENTER | wx.BOTTOM | wx.EXPAND, 1)
        main_window_sizer.SetItemMinSize(self.webcampanel, (640, 480))
        main_window_sizer.Add(self.calibration_button, 1,
                              wx.CENTER | wx.BOTTOM | wx.EXPAND)

        self.SetSizer(main_window_sizer)
        main_window_sizer.Fit(self)

        self.timer = wx.Timer(self)
        self.timer.Start(1000. / 10)

        self.Bind(wx.EVT_TIMER, self.WebcamPanelNextFrame)
        self.Bind(wx.EVT_BUTTON, self.Calibration)

        guide_window = guideWindow(self)
        guide_window.Show()

    def WebcamPanelNextFrame(self, e):
        return_value, frame = self.camera.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.webcampanel.bmp.CopyFromBuffer(frame)
        self.webcampanel.Refresh()

    def Calibration(self, e):
        self.do_calibrate = not self.do_calibrate

    def MouseDown(self, e):
        if self.do_calibrate:
            self.src_pt = [e.X, e.Y]

    def MouseUp(self, e):
        if self.do_calibrate:
            self.dst_pt = [e.X, e.Y]


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

            parent_display = wx.Display(self.parent_display_index)
            _, _, parent_display_w, parent_display_h = parent_display.GetGeometry()
            guide_display = wx.Display(self.display_index)
            _, _, guide_display_w, guide_display_h = guide_display.GetGeometry()

            parent_position_x, parent_position_y = parent.GetPosition()

            if parent_display_w > parent_position_x:
                self.SetPosition(
                    (int(parent_display_w - (guide_display_w / 2)), int(guide_display_h / 2)))
            else:
                self.SetPosition(
                    (int(guide_display_w / 2), int(guide_display_h / 2)))


def main():
    app = wx.App()
    main_window = MainWindow()
    main_window.Show()
    app.MainLoop()


# main関数呼び出し
if __name__ == "__main__":
    main()
