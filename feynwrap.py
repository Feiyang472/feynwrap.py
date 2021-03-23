def util_function(pose):
    return lambda self, *args, **kwargs: self.propag(pose, *args, **kwargs)

class node:
    declarations_all = None
    propagations_all = ''
    nodelist = []
    lines = {
        'f': 'fermion',
        'af': 'anti fermion',
        'b': 'boson',
        'g': 'gluon'
    }
    
    def __init__(self, vert = None, rel_pos=None):
        self.vi = len(node.nodelist) + 1
        self.name = 'v{}'.format(self.vi)
        self.rel_pos = rel_pos
        self.vert = vert
        self.declaration = self.declare()
        node.nodelist.append(self)
    
    def declare(self):
        arg_pos = '' if not self.rel_pos else '[{} = of {}]'.format(*self.rel_pos) 
        arg_vertlabel = '' if not self.vert else '{{\\({}\\)}}'.format(self.vert)
        
        return '\\vertex ({}) {} {};\n'.format(self.name, arg_pos, arg_vertlabel)
    
    def propag(self, pos='right', line='f', vert = None, edge = None, end=False):
        next_vertex = node( vert=vert, rel_pos=(pos,self.name) )
        
        if not edge:
            node.propagations_all += '\n\\propag [{}] ({}) to ({});'.format(node.lines.get(line), self.name, next_vertex.name) 
        else:
            node.propagations_all += '\n\\propag [{}] ({}) to [edge label = \\({}\\)] ({});'.format(node.lines.get(line), self.name, edge, next_vertex.name) 
        return self if end else next_vertex
    
    
    common_positions = ['above left',
                        'above right',
                        'below left',
                        'below right',
                        ]
    
    al, ar, bl, br = [util_function(position) for position in common_positions]
    

    @classmethod
    def toTikz(cls):
        node.declarations_all = ''
        for nodeItem in node.nodelist:
            node.declarations_all += nodeItem.declaration
        return (node.declarations_all+
              node.propagations_all)
        
    @classmethod
    def wrapTikz(cls):
        return ("\\begin{{tikzpicture}}"
                "\n\\begin{{feynhand}}\n{}\n\\end{{feynhand}}"
                "\n\\end{{tikzpicture}}\n").format(node.toTikz())
        
    @classmethod
    def save(cls, fname):
        texfile = open(fname, mode="w")
        texfile.write(node.wrapTikz())
        texfile.close()

