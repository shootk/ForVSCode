import wx
import wx.lib.newevent
import threading
import cv2
import time
import numpy as np
import os
import serial
import serial.tools.list_ports
import bluetooth
import concurrent.futures


class MyThread(concurrent.futures.ProcessPoolExecutor):
    def __init__(self):
        super(MyThread, self).__init__()


class WebcamPanel(wx.Panel):
    def __init__(self, parent, fps=10):  # fps15くらいが目安
        wx.Panel.__init__(self, parent)

        self.camera = cv2.VideoCapture(0)
        return_value, frame = self.camera.read()
        height, width = frame.shape[:2]

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp = wx.BitmapFromBuffer(width, height, frame)

        self.SetSize((width, height))

        self.timer = wx.Timer(self)
        self.timer.Start(1000. / fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)

    def OnPaint(self, e):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, e):
        return_value, frame = self.camera.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()


class MainWindow(wx.Frame):
    def __init__(self):

        # inheritence
        wx.Frame.__init__(self, None)
        self.Title = "webcam"

        # main ui
        self.webcampanel = WebcamPanel(self)

        main_window_sizer = wx.BoxSizer(wx.VERTICAL)

        main_window_sizer.Add(self.webcampanel, 7,
                              wx.CENTER | wx.BOTTOM | wx.EXPAND, 1)
        main_window_sizer.SetItemMinSize(self.webcampanel, (640, 480))

        self.SetSizer(main_window_sizer)
        main_window_sizer.Fit(self)
        guide_window = guideWindow(self)
        guide_window.Show()


class guidePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)


class guideWindow(wx.Frame):
    def __init__(self, parent):

        wx.Frame.__init__(self, parent)
        self.guide_panel = guidePanel(self)
        self.switch_window(parent)
        self.Maximize()

    def switch_window(self, parent):
        if wx.Display.GetCount() == 2:
            self.parent_display_index = wx.Display.GetFromWindow(parent)
            self.display_index = (self.parent_display_index + 1) % 2

            parent_display = wx.Display(self.parent_display_index)
            _, _, parent_display_w, parent_display_h = parent_display.GetGeometry()
            guide_display = wx.Display(self.display_index)
            _, _, guide_display_w, guide_display_h = guide_display.GetGeometry()

            parent_position_x, parent_position_y = parent.GetPosition()

            if parent_display_w < parent_position_x:
                self.SetPosition(
                    (int(parent_display_w + (guide_display_w / 2)), int(guide_display_h / 2)))
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
