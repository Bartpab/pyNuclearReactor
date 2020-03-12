import wx

class ComboBox(wx.ComboBox):
    def SetValue(self, elements):
        self.Clear()
        for el in elements:
            self.Append(el)