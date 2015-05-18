#----------------------------------------------------------------------
# panelTwo.py
#
#
# Author: Nguyen Huy Hieu - nguyen.huy.hieu292@gmail.com
#
#----------------------------------------------------------------------

import wx
import kMeans
from numpy import *

class TabPanel(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        self.newkmean = kMeans.kmean()
        self.oncompute = 0
        self.oncheck = 0
        # self.num_cluster
        # self.calculate
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        sampleList = ['2', '3','4','5','6','7','8','9','10']

        
        txt1 = wx.StaticText(self, -1, label = "Select Number of Clusters (less than 10 and default is 3) :", pos = (20,10))
        self.combo = wx.ComboBox(self, -1, "3", (15, 30), wx.DefaultSize,sampleList, wx.CB_DROPDOWN)
        cbtn = wx.Button(self, label='K-Means Compute', pos=(20, 30))
        txt2 = wx.StaticText(self, -1, label = "Number of recalculate Centroids:", pos = (20,10))
        self.lable_num_cluster = wx.StaticText(self, label="lable_num_cluster")
        txt3 = wx.StaticText(self, -1, label = "Select Position of Centroid (less than above) :", pos = (20,10))
        self.txtOne = wx.TextCtrl(self, wx.ID_ANY, "")
        check = wx.Button(self, label='Check', pos=(20, 30))
        show_2d = wx.Button(self, label='Show 2D', pos=(20, 30))
        show_3d = wx.Button(self, label='Show 3D', pos=(20, 30))
        txt4 = wx.StaticText(self, -1, label = "Final Result :", pos = (20,10))
        show_2d_final = wx.Button(self, label='Show 2D', pos=(20, 30))
        show_3d_final = wx.Button(self, label='Show 3D', pos=(20, 30))
        show_error = wx.Button(self, label='Show Error Chart', pos=(20, 30))
        save_file = wx.Button(self, label='Export file', pos=(20, 30))
         
        self.combo.Bind(wx.EVT_COMBOBOX, self.onCombo)
        cbtn.Bind(wx.EVT_BUTTON, self.OnCompute)
        check.Bind(wx.EVT_BUTTON, self.OnCheck)
        show_2d.Bind(wx.EVT_BUTTON, self.OnShow_2d)
        show_3d.Bind(wx.EVT_BUTTON, self.OnShow_3d)
        show_2d_final.Bind(wx.EVT_BUTTON, self.OnShow_2d_final)
        show_3d_final.Bind(wx.EVT_BUTTON, self.OnShow_3d_final)
        show_error.Bind(wx.EVT_BUTTON, self.OnShowError)
        save_file.Bind(wx.EVT_BUTTON, self.OnSave)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(txt1, 0, wx.ALL, 5)
        sizer.Add(self.combo, 0, wx.ALL, 5)
        sizer.Add(cbtn, 0, wx.ALL, 5)
        sizer.Add(txt2, 0, wx.ALL, 5)
        sizer.Add(self.lable_num_cluster, 0, wx.ALL, 5)
        sizer.Add(txt3, 0, wx.ALL, 5)
        sizer.Add(self.txtOne, 0, wx.ALL, 5)
        sizer.Add(check, 0, wx.ALL, 5)
        sizer.Add(show_2d, 0, wx.ALL, 5)
        sizer.Add(show_3d, 0, wx.ALL, 5)
        sizer.Add(txt4, 0, wx.ALL, 5)
        sizer.Add(show_2d_final, 0, wx.ALL, 5)
        sizer.Add(show_3d_final, 0, wx.ALL, 5)
        sizer.Add(show_error, 0, wx.ALL, 5)
        sizer.Add(save_file, 0, wx.ALL, 5)
        
        self.SetSizer(sizer)
        
    def OnCompute(self, e):
        self.oncompute = 1
        a = self.combo.GetValue()
        self.num_cluster=int(a)
        self.newkmean.set_num_cluster(self.num_cluster)
        self.newkmean.run1()
        self.calculate = self.newkmean.calculate
        b = str(self.calculate)
        self.lable_num_cluster.SetLabel(b)
            
    def onCombo(self, event):
        a = self.combo.GetValue()
        self.num_cluster=int(a)
    def OnCheck(self,event):
        self.oncheck = 1
        if self.oncompute ==1:
            a =  self.txtOne.GetValue()
            try:
                b=int(a)
            except:
                dlg = wx.MessageDialog(None, "You should take number and not alphabet please !!!",'You Got an Error',wx.OK | wx.ICON_INFORMATION)
                retCode = dlg.ShowModal()
            if b<1 or b>self.calculate:
                war = wx.MessageDialog(None, "You should take number less then Number of recalculate Centroids above and more than one!!! ",'You Got an Error',wx.OK | wx.ICON_INFORMATION)
                retCode = war.ShowModal()
            else:
                self.newkmean.run2(b)
        else:
            war2 = wx.MessageDialog(None, "You must click button K-Means Compute to do this!!! ",'You Got an Error',wx.OK | wx.ICON_INFORMATION)
            retCode = war2.ShowModal()
    def OnShow_2d(self,event):
        if self.oncompute == 1 and self.oncheck == 1:
            self.newkmean.run3()
        else:
            war2 = wx.MessageDialog(None, "You must click button K-Means Compute and Check to do this!!! ",'You Got an Error',wx.OK | wx.ICON_INFORMATION)
            retCode = war2.ShowModal()
    def OnShow_3d(self,event):
        if self.oncompute == 1 and self.oncheck == 1:
            self.newkmean.run4()
        else:
            war2 = wx.MessageDialog(None, "You must click button K-Means Compute and Check to do this!!! ",'You Got an Error',wx.OK | wx.ICON_INFORMATION)
            retCode = war2.ShowModal()
    def OnShow_2d_final(self,event):
        if self.oncompute ==1:
            self.newkmean.run5()
        else:
            war2 = wx.MessageDialog(None, "You must click button K-Means Compute to do this!!! ",'You Got an Error',wx.OK | wx.ICON_INFORMATION)
            retCode = war2.ShowModal()
    def OnShow_3d_final(self,event):
        if self.oncompute ==1:
            self.newkmean.run6()
        else:
            war2 = wx.MessageDialog(None, "You must click button K-Means Compute to do this!!! ",'You Got an Error',wx.OK | wx.ICON_INFORMATION)
            retCode = war2.ShowModal()
    def OnShowError(self,event):
        if self.oncompute ==1:
            self.newkmean.run7()
        else:
            war2 = wx.MessageDialog(None, "You must click button K-Means Compute to do this!!! ",'You Got an Error',wx.OK | wx.ICON_INFORMATION)
            retCode = war2.ShowModal()
    def OnSave(self,event):
        if self.oncompute ==1:
            self.newkmean.save_file()
        else:
            war2 = wx.MessageDialog(None, "You must click button K-Means Compute to do this!!! ",'You Got an Error',wx.OK | wx.ICON_INFORMATION)
            retCode = war2.ShowModal()
          
         


