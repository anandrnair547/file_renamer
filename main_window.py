import wx
from file_manager import FileManager


class MainWindow(wx.Frame):

    folder_path = None
    files_in_folder = []
    search_string = "TamilRocker"

    def __init__(self):
        super().__init__(parent=None, title='Twiinix File Renamer')
        panel = wx.Panel(self)
        my_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        my_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # self.text_ctrl = wx.TextCtrl(panel)
        self.selected_folder_label = wx.StaticText(panel, label="Select Folder", style=wx.ALIGN_LEFT)
        my_horizontal_sizer.Add(self.selected_folder_label, 0, wx.EXPAND, 2)
        choose_dir_button = wx.Button(panel, label="Select Folder")
        choose_dir_button.Bind(wx.EVT_BUTTON, self.show_select_dir_dialog)
        my_horizontal_sizer.AddStretchSpacer(1)
        my_horizontal_sizer.Add(choose_dir_button, 0, wx.ALIGN_RIGHT, 0)
        my_vertical_sizer.Add(my_horizontal_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.list_view = MainWindow.create_files_list_view(panel)
        my_vertical_sizer.Add(self.list_view, 5, wx.EXPAND)

        rename_button = wx.Button(panel, label="Rename files")
        rename_button.Bind(wx.EVT_BUTTON, self.rename_files)
        my_vertical_sizer.Add(rename_button, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(my_vertical_sizer)
        # self.text_ctrl.Bind(wx.EVT_SET_FOCUS, self.toggle1)
        # self.text_ctrl.Bind(wx.EVT_KILL_FOCUS, self.toggle2)
        panel.Fit()
        self.Centre()
        self.Show()

    # def toggle1(self, evt):
    #     if self.text_ctrl.GetValue() == "Select Folder":
    #         self.text_ctrl.SetValue("")
    #     evt.Skip()
    #
    # def toggle2(self, evt):
    #     if self.text_ctrl.GetValue() == "":
    #         self.text_ctrl.SetValue("Select Folder")
    #     evt.Skip()


    @staticmethod
    def create_files_list_view(panel):

        list = FileListCtrl(panel, -1, style=wx.LC_VIRTUAL | wx.LC_REPORT)
        list.InsertColumn(0, 'File Name')
        list.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)

        return list

    def show_select_dir_dialog(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           # | wx.DD_DIR_MUST_EXIST
                           # | wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            print("You chose" + dlg.GetPath())
            self.folder_path = dlg.GetPath()
            self.selected_folder_label.SetLabel("Folder:" + self.folder_path)
            self.files_in_folder = FileManager.list_files(self.folder_path, self.search_string)
            self.refresh_list_view()
            print(FileManager.find_urls_in_list(self.files_in_folder))

        dlg.Destroy()

    def refresh_list_view(self):
        self.list_view.files_list = self.files_in_folder
        self.list_view.SetItemCount(len(self.files_in_folder))
        self.list_view.Refresh()
        # self.list_view.SetColumnWidth(0, wx.LIST_AUTOSIZE)


    def rename_files(self, event):
        # self.folder_path = "/Volumes/Backup Drive/Movies"
        if self.folder_path is None:
            print("Please chose a folder to rename files")
            return
        FileManager.rename_files_by_replacing_string(self.folder_path, self.files_in_folder,
                                                     "www.TamilRockers.ws - ", "***###***")
        print("Rename files pressed")


class FileListCtrl (wx.ListCtrl):
    files_list = []

    def OnGetItemText(self, item, column):
        return self.files_list[item]
