import cv2
import numpy
import wx
import os


class Main(wx.Frame):

    def __init__(self, parent, id, title):
        """ レイアウトの作成 """

        wx.Frame.__init__(self, parent, id, title, size=(300, 100))
        self.folder = os.path.dirname(os.path.abspath(__file__))
        panel = wx.Panel(self, wx.ID_ANY)

        choose_button = wx.Button(panel, wx.ID_ANY, "フォルダの選択")
        choose_button.Bind(wx.EVT_BUTTON, self.choose_folder)
        self.choose_text = wx.StaticText(panel, wx.ID_ANY, self.folder)

        v_layout = wx.BoxSizer(wx.VERTICAL)
        v_layout.Add(choose_button, proportion=0)
        v_layout.Add(self.choose_text, proportion=0, flag=wx.EXPAND)
        panel.SetSizer(v_layout)

        self.Centre()
        self.Show(True)

    def choose_folder(self, event):
        """ フォルダの選択ボタンを押すとここ。フォルダ選択ダイアログを開き、choose_textに反映 """

        folder = wx.DirDialog(self,
                              style=wx.DD_CHANGE_DIR,
                              message="保存先フォルダ")

        if folder.ShowModal() == wx.ID_OK:
            self.folder = folder.GetPath()
        folder.Destroy()
        self.choose_text.SetLabel(self.folder)


def main():
    app = wx.App(False)
    Main(None, wx.ID_ANY, "ファイル選択ダイアログ")
    app.MainLoop()


if __name__ == "__main__":
    main()
