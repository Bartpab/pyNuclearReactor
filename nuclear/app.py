import nuclear
import wx

class App(wx.App):
    def OnInit(self):
        self.root = wx.Frame()
        self.SetTopWindow(self.root)
        self.root.Show(True)
        return True


def run(template, data, methods, computed):
    app = wx.App()
    
    window = wx.Frame(parent=None, title="Test")
    window.SetSizer(wx.BoxSizer(wx.VERTICAL))
    
    
    reactor = nuclear.Reactor(template=template, data=data({}), methods=methods, computed=computed, root=window)
    reactor.mount()
    
    window.Show()

    # We need to periodically update the reactor state
    timer = wx.Timer(app, 100)
    app.Bind(wx.EVT_TIMER, reactor.nexTick)
    timer.Start(16)
    
    app.MainLoop()
    
if __name__ == "__main__":
    run()