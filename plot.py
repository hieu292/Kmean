#----------------------------------------------------------------------
# plot.py
#
#
# Author: Nguyen Huy Hieu - nguyen.huy.hieu292@gmail.com
#
#----------------------------------------------------------------------
import panelOne, panelTwo
import wx
import wx.lib.agw.aui as aui

ID_NotebookArtGloss = 0
ID_NotebookArtSimple = 1
ID_NotebookArtVC71 = 2
ID_NotebookArtFF2 = 3
ID_NotebookArtVC8 = 4
ID_NotebookArtChrome = 5
APP_OPEN =6
APP_EXP = 7
APP_EXIT = 8
APP_INF = 9
########################################################################
class AUIManager(aui.AuiManager):
    """
    AUI Manager class
    """

    #----------------------------------------------------------------------
    def __init__(self, managed_window):
        """Constructor"""
        aui.AuiManager.__init__(self)
        self.SetManagedWindow(managed_window)

########################################################################
class AUINotebook(aui.AuiNotebook):
    """
    AUI Notebook class
    """

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        aui.AuiNotebook.__init__(self, parent=parent)
        self.default_style = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
        self.SetWindowStyleFlag(self.default_style)

        # add some pages to the notebook
        pages = [panelOne, panelTwo]
        label = ["                          DataSet                           ","                      KMean Compute                        "]
        i = 0
        for page in pages:
            tab = page.TabPanel(self)
            self.AddPage(tab, label[i], False)
            i=i+1

########################################################################
class DemoFrame(wx.Frame):
    """
    wx.Frame class
    """
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        title = "K-Means Program"
        wx.Frame.__init__(self, None, wx.ID_ANY, 
                          title=title, size=(1024,687))
        self.themeDict = {"Glossy Theme (Default)":0,
                          "Simple Theme":1,
                          "VC71 Theme":2,
                          "Firefox 2 Theme":3,
                          "VC8 Theme":4,
                          "Chrome Theme":5,
                          }

        # create the AUI manager
        self.aui_mgr = AUIManager(self)

        # create the AUI Notebook
        self.notebook = AUINotebook(self)
        
        self._notebook_style = self.notebook.default_style
                
        # add notebook to AUI manager
        self.aui_mgr.AddPane(self.notebook, 
                             aui.AuiPaneInfo().Name("notebook_content").
                             CenterPane().PaneBorder(False)) 
        self.aui_mgr.Update()
        
        # create menu and tool bars
        self.createMenu()
        self.createTB()
        
    #----------------------------------------------------------------------
    def createMenu(self):
        menubar = wx.MenuBar()
        
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()
        
        omi = wx.MenuItem(fileMenu, APP_OPEN, '&Open\tCtrl+O')
        omi.SetBitmap(wx.Bitmap('Open.png'))
        fileMenu.AppendItem(omi)
        emi = wx.MenuItem(fileMenu, APP_EXP, '&Export\tCtrl+E')
        emi.SetBitmap(wx.Bitmap('Export.png'))
        fileMenu.AppendItem(emi)
        
        qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
        qmi.SetBitmap(wx.Bitmap('Exit.png'))
        fileMenu.AppendItem(qmi)

        hmi = wx.MenuItem(helpMenu, APP_INF, '&Info\tCtrl+I')
        hmi.SetBitmap(wx.Bitmap('Info.png'))
        helpMenu.AppendItem(hmi)

        self.Bind(wx.EVT_MENU, self.OnOpen, id=APP_OPEN)
        self.Bind(wx.EVT_MENU, self.OnExport, id=APP_EXP)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)
        self.Bind(wx.EVT_MENU, self.OnInfo, id=APP_INF)

        menubar.Append(fileMenu, '&File')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)
        
    #----------------------------------------------------------------------
    def createTB(self):
        """
        Create the toolbar
        """
        TBFLAGS = ( wx.TB_HORIZONTAL
                    | wx.NO_BORDER
                    | wx.TB_FLAT )
        tb = self.CreateToolBar(TBFLAGS)
        keys = self.themeDict.keys()
        keys.sort()
        choices = keys
        cb = wx.ComboBox(tb, wx.ID_ANY, "Glossy Theme (Default)", 
                         choices=choices,
                         size=wx.DefaultSize,
                         style=wx.CB_DROPDOWN)
        cb.Bind(wx.EVT_COMBOBOX, self.onChangeTheme)
        tb.AddControl(cb)
        tb.AddSeparator()
    
        
        tb.Realize()
        
    #----------------------------------------------------------------------
    def onChangeTabClose(self, event):
        """
        Change how the close button behaves on a tab
        
        Note: Based partially on the agw AUI demo
        """
        choice = event.GetString()        
        self._notebook_style &= ~(aui.AUI_NB_CLOSE_BUTTON |
                                 aui.AUI_NB_CLOSE_ON_ACTIVE_TAB |
                                 aui.AUI_NB_CLOSE_ON_ALL_TABS)
        
        # note that this close button doesn't work for some reason
        if choice == "Close Button At Right":
            self._notebook_style ^= aui.AUI_NB_CLOSE_BUTTON 
        elif choice == "Close Button On All Tabs":
            self._notebook_style ^= aui.AUI_NB_CLOSE_ON_ALL_TABS 
        elif choice == "Close Button On Active Tab":
            self._notebook_style ^= aui.AUI_NB_CLOSE_ON_ACTIVE_TAB
            
        self.notebook.SetWindowStyleFlag(self._notebook_style)
        self.notebook.Refresh()
        self.notebook.Update()
        
    #----------------------------------------------------------------------
    def onChangeTheme(self, event):
        """
        Changes the notebook's theme
        
        Note: Based partially on the agw AUI demo
        """
        evId = self.themeDict[event.GetString()]
        all_panes = self.aui_mgr.GetAllPanes()
        
        for pane in all_panes:

            if isinstance(pane.window, aui.AuiNotebook):
                nb = pane.window

                if evId == ID_NotebookArtGloss:
                
                    nb.SetArtProvider(aui.AuiDefaultTabArt())
                    
                elif evId == ID_NotebookArtSimple:
                    nb.SetArtProvider(aui.AuiSimpleTabArt())
                    
                elif evId == ID_NotebookArtVC71:
                    nb.SetArtProvider(aui.VC71TabArt())
                    
                elif evId == ID_NotebookArtFF2:
                    nb.SetArtProvider(aui.FF2TabArt())
                    
                elif evId == ID_NotebookArtVC8:
                    nb.SetArtProvider(aui.VC8TabArt())
                    
                elif evId == ID_NotebookArtChrome:
                    nb.SetArtProvider(aui.ChromeTabArt())
                    
                nb.Refresh()
                nb.Update()
                
    #----------------------------------------------------------------------
    def OnQuit(self, e):
        self.Close()
    def OnOpen(self, e):
        openFileDialog = wx.FileDialog(self, "Open", "", "", 
                                       "Dataset files (*.txt)|*.txt", 
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        self.get_path = openFileDialog.GetPath()
        #self.dataset = mat(self.newkmean.loadDataSet(self.get_path))
        #reload(panelOne)
        #panelOne.PanelOne(self.dataset)
        openFileDialog.Destroy()
    def OnExport(self, e):
        saveFileDialog = wx.FileDialog(self, "Save As", "", "", 
                                       "Export files (*.txt)|*.txt", 
                                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        saveFileDialog.ShowModal()
        saveFileDialog.GetPath()
        saveFileDialog.Destroy()
    def OnInfo(self,e):
        description = """K-Means Program is an meachine learning application to classify data
from real-world. It is eazy to use in your data. And it is free open source with education purpose.
"""

        licence = """K-Means Program is free software; you can redistribute 
it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation; either version 2 of the License, 
or (at your option) any later version.

K-Means Program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have 
received a copy of the GNU General Public License along with K-Means Program; 
if not, write to the Free Software Foundation, Inc., HUST (HANOI UNISERSITY OF SCIENCE TECHNOLOGY)"""


        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('kmean.PNG', wx.BITMAP_TYPE_PNG))
        info.SetName('K-Mean Program')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2014 Nguyen Huy Hieu')
        info.SetWebSite('https://www.facebook.com/profile.php?id=100005259373072')
        info.SetLicence(licence)
        info.AddDeveloper('Nguyen Huy Hieu')
        info.AddDocWriter('Nguyen Huy Hieu')

        wx.AboutBox(info)
        

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = DemoFrame()
    frame.Show()
    app.MainLoop()
    
    
