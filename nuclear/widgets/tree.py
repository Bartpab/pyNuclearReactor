import wx

class Tree(wx.TreeCtrl):
    @staticmethod
    def default_get_key(self, node):
        return str(node)
        
    @staticmethod
    def default_walker(self, node):
        if not hasattr(node, "items"):
            return []
        
        items = []
        
        for key, value in node.items():
            items.append(value)
        
        return items
        
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent)    
        self.walker = Tree.default_walker
        self.get_key = Tree.default_get_key
        self.s = []
    
    def SetWalker(self, walker):
        self.walker = walker
    
    def add(self, key, node, data, parent_node=None, level=0):
        if parent_node is None:
            cparent_node = self.AddRoot(key)
        else:
            cparent_node = self.AppendItem(parent_node, key, data=data)
        
        for ckey, cnode, cdata in self.walker(node, level + 1):
            self.add(ckey, cnode, cdata, cparent_node, level + 1)
      
    def patch_node(self, key, node, data, tree_node, level):
        data_children = self.walker(node, level + 1)
        first, cookie = self.GetFirstChild(tree_node)
        s = [first]
        tree_children = []
        while s:
            e = s.pop()
            if e.IsOk():
                tree_children.append(e)
                c = self.GetNextSibling(e)
                s.append(c)
        
        self.patch_children(data_children, tree_children, tree_node, level + 1)       
    
    def same(self, key, node, data, tree_node):
        stored_key = self.GetItemText(tree_node)
        return key == stored_key
    
    def patch(self, key, node, data, tree_node, level=0):  
        redo = False
        
        if not tree_node or not tree_node.IsOk():
            redo = True
        
        else:
            if not self.same(key, node, data, tree_node):
                redo = True
        
        if redo:
            if not tree_node:
                self.add(key, node, data, None, level)
            elif tree_node == self.GetRootItem():
                self.DeleteAllItems()
                self.add(key, node, data, None, level)
            else:
                p_node = self.GetItemParent(tree_node)

                if not p_node.IsOk():
                    p_node = None
                
                self.Delete(tree_node)
                self.add(key, node, data, p_node, level)
        else:
            self.patch_node(key, node, data, tree_node, level)

    
    def patch_children(self, data_children, tree_children, parent_el, level):
        s = tree_children[:]
        
        same = []
        found = []
        
        for d in data_children:
            key, node, data = d
            ft = None
            to_r = []
            
            for t in s:
                if self.same(key, node, data, t):
                    ft = t
                    break
                   
            if ft:
                s.remove(ft)
                same.append((d,t))
                found.append(d)
        
        to_remove = s
        to_add    = list(filter(lambda e: e not in found, data_children))
        
        for d, t in same:
            self.patch(*d, t, level + 1)
        
        for r in to_remove:
            self.Delete(r)
        
        for a in to_add:
            key, node, data = a
            self.add(key, node, data, parent_el, level)
        
    def SetTree(self, tree):
        root_node = self.GetRootItem()
        
        if not root_node.IsOk():
            root_node = None

        key, node, data = self.walker(tree, 0)[0]
        self.patch(key, node, data, root_node, level=0)