import wx
import pandas as pd


class OrderMaker():
    def __init__(self, file_path):
        status_sheet = pd.read_excel(str(file_path), sheet_name=0)
        self.team_num = int(status_sheet.loc[0, '班数'])
        self.team_names = []
        for i in range(self.team_num):
            self.team_names.append(
                status_sheet.at[i, '班名'])
        start_schedule = list(str(status_sheet.loc[0, '開始']))[1]
        end_day = list(str(status_sheet.loc[0, '終了']))[0]
        end_schedule = list(str(status_sheet.loc[0, '終了']))[1]
        print('sucsess')

    def game_caluculation(self, ):
        pass

    def input_Info(self,):
        pass

    def status_input(self,):
        pass


class StatusInputPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.init_ui(parent)

    def init_ui(self, parent):
        self.SetSize(parent.Size)
        self.text = wx.StaticText(
            parent=self, id=-1, label='合宿全体のステータスを入力', pos=(10, 10))
        self.text = wx.StaticText(
            parent=self, id=-1, label='班の数を入力', pos=(10, 30), size=(100, 20))
        self.input_box = wx.TextCtrl(
            parent=self, id=-1, pos=(10, 50), size=(50, 20))


class FileInputPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.init_ui(parent)

    def init_ui(self, parent):
        btn = wx.Button(self, -1, 'OMOM(Order Made Order Maker)', pos=(10, 40))
        btn.Bind(wx.EVT_BUTTON, self.clicked)

    def clicked(self, event):
        dialog = wx.FileDialog(None, u'オーダーファイルを選択してください', style=wx.FD_OPEN)
        dialog.ShowModal()
        input_file_path = dialog.GetPath()
        self.order_maker = OrderMaker(input_file_path)


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)
        self.init_ui()

    def init_ui(self):
        self.SetTitle('テキストボックス')
        self.SetSize((400, 300))
        self.status_input_panel = StatusInputPanel(self)
        self.file_input_panel = FileInputPanel(self)


if __name__ == '__main__':
    my_app = wx.App()
    main_window = MainWindow()
    main_window.Show()
    my_app.MainLoop()
