import wx


class OrderMaker():
    def __init__(self, file):
        pass

    def game_caluculation(self, ):
        pass

    def input_Info(self,):
        pass

    def status_input(self,):
        pass


if __name__ == '__main__':
    my_app = wx.App()
    dialog = wx.FileDialog(None, u'オーダーファイルを選択してください', style=wx.FD_OPEN)
    dialog.ShowModal()
    input_file = dialog.GetPath()
