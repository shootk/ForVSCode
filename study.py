import wx
import wx.lib.newevent
import threading
import cv2
import time
import numpy as np
import os
import serial
import serial.tools.list_ports

class Guide():
	def __init__():
		pass

class MyThread(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)


    def setTarget(self, target):
        self.target = target

    def run(self):
        for i in range(10):
            if i % 2 == 0:
                img = self.img
            else:
                img = 255 - self.img
            time.sleep(1)
            evt = self.target.__class__.Event(img = img, msg = 'hoge %d' % i)
            wx.PostEvent(self.target, evt)

class MyBluetooth():
	Event, EVT_GETSERIAL = wx.lib.newevent.NewEvent()
	def __init__(self, parent, setter, ID = wx.ID_ANY):
		self.setter = setter
		self.size = self.setter.size

		wx.Panel.__init__(self, parent, ID, size = self.size)
		self.stbmp = wx.StaticBitmap(self, bitmap = wx.EmptyBitmap(self.size[0], self.size[1]))

		setter.setTarget(self)
		self.Bind(ImageViewer.EVT_NEWIMAGE, self.newImageArrived)

	def start(self):
		self.setter.start()

	def stop(self):
		self.setter.stop()

	def redraw(self, img):
		assert(img.ndim == 3)
		assert(img.dtype == np.uint8)
		assert(img.shape[0] == self.size[1] and img.shape[1] == self.size[0])

		buf = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		bmp = wx.BitmapFromBuffer(img.shape[1], img.shape[0], buf)
		self.stbmp.SetBitmap(bmp)

	def newImageArrived(self, event):
		self.redraw(event.img)
		print(event.msg)

#カメラキャプチャ表示用パネル
class WebcamPanel(wx.Panel):
	def __init__(self, parent, camera, fps=10):#fps15くらいが目安

		wx.Panel.__init__(self, parent)

		self.camera = camera
		return_value, frame = self.camera.read()
		height, width = frame.shape[:2]

		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		self.bmp = wx.BitmapFromBuffer(width, height, frame)

		self.SetSize((width,height))

		self.timer = wx.Timer(self)
		self.timer.Start(1000./fps)

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
	def __init__(self, camera):

		#inheritence
		wx.Frame.__init__(self, None)
		self.Title = "webcam"

		#main ui
		self.webcampanel = WebcamPanel(self, camera)

		main_window_sizer = wx.BoxSizer(wx.VERTICAL)

		main_window_sizer.Add(self.webcampanel, 7, wx.CENTER | wx.BOTTOM | wx.EXPAND, 1)
		main_window_sizer.SetItemMinSize(self.webcampanel, (640,480))

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
                self.SetPosition((int(parent_display_w+(guide_display_w/2)),int(guide_display_h / 2)))
            else:
                self.SetPosition((int(guide_display_w / 2),int(guide_display_h / 2)))

def main():
    app = wx.App()

    camera = cv2.VideoCapture(0)
    main_window = MainWindow(camera)
    main_window.Show()
    app.MainLoop()

#main関数呼び出し
if __name__ == "__main__":
    main()