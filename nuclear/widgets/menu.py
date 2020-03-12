import wx

def get_frame(win):
    s = [win]
    while s:
        e = s.pop(-1)
        if isinstance(e, wx.Frame):
            return e
        else:
            s.append(e.GetParent())
    
    return frame

def create_menu_bar(parent):
    menu_bar = wx.MenuBar()
    frame = get_frame(parent)
    frame.SetMenuBar(menu_bar)
    return menu_bar

def set_menu_label(menu, menu_bar, value):
    menu_bar.SetMenuLabel(menu.index, value)
    
def create_menu(parent):
    menu = wx.Menu()
    parent.Append(menu, '&default')
    
    if isinstance(parent, wx.MenuBar):
        menu.index = parent.GetMenuCount() - 1
        menu.SetTitle = lambda value: set_menu_label(menu, parent, value)
    
    return menu

def create_menu_item(parent):
    menu_item = parent.Append(wx.ITEM_NORMAL, 'Default', 'Default Description')
    return menu_item