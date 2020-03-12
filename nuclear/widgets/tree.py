import wx

class Tree(wx.TreeCtrl):
    @staticmethod
    def default_walker(self, node):
        if not hasattr(node, "items"):
            return []
        
        items = []
        
        for key, value in node.items():
            if not hasattr(value, "items"):
                items.append((key, value, False))
            else:
                items.append((key, value, True))
        
        return items
        
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent)    
        self.walker = Tree.default_walker
    
    def SetWalker(self, walker):
        self.walker = walker
    
    def rec_tree(self, node, tree_node=None):
        for key, value, is_node, data in self.walker(node, tree_node): 
            if tree_node is None:
                if not is_node:
                    ctree_node = self.AddRoot(key + ": " +value, data=data)
                else:
                    ctree_node = self.AddRoot(key)
                    self.rec_tree(value, ctree_node)
            else:
                if is_node:
                    ctree_node = self.AppendItem(tree_node, key, data=data)
                    self.rec_tree(value, ctree_node)
                else:
                    self.SetItemData(tree_node, value)
   
    def SetTree(self, tree):
        self.DeleteAllItems()
        self.bindings = {}
        self.rec_tree(tree)