#----------------------------------------------------------------------
# panelOne.py
#
#
# Author: Nguyen Huy Hieu - nguyen.huy.hieu292@gmail.com
#
#----------------------------------------------------------------------

import wx
import wx.grid as gridlib
import kMeans
from numpy import *

class TabPanel(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        grid = gridlib.Grid(self)
        grid.CreateGrid(100,25)
        newkmean = kMeans.kmean()
        dataset = mat(newkmean.loadDataSet("dataset.txt"))
        for row in range(shape(dataset)[0]):
            for col in range(shape(dataset)[1]):
                grid.SetCellValue(row, col,str(dataset[row,col]))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid,1,wx.EXPAND,5)
        self.SetSizer(sizer)
          



