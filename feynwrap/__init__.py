"""
Feynman Diagram wrapper
"""
import feynwrap.feynformat as fmt

def shorthand_function(pose):
    return lambda self, *args: self.propagate(pose, *args)

class vert:
    declarations_all = None
    propagatations_all = ''
    vertlist = []
    
    def __init__(self, name = None, rel_pos=None):
        self.vi = len(vert.vertlist) + 1
        self.rel_pos = rel_pos
        self.name = name
        self.declaration = self.declare()
        vert.vertlist.append(self)

    def declare(self):
        arg_pos = '' if not self.rel_pos else ' [{} = of v{}]'.format(*self.rel_pos) 
        arg_vertlabel = '' if not self.name else ' {{\\({}\\)}}'.format(self.name)

        return '\\vertex (v{}){}{};\n'.format(self.vi, arg_pos, arg_vertlabel)

    def propagate(self, *args):
        sorted_args = fmt.feyn_arg_sort(args)
        
        line, pos, end = map(sorted_args.__getitem__, [fmt.I_PARTICLE, fmt.I_POSITION, fmt.I_ENDING_VERTEX])
        
        name, edge = [None]*2
        if end:
            name = sorted_args[fmt.I_LABEL]
        else:
            edge = sorted_args[fmt.I_LABEL]

        next_vertex = vert(name, rel_pos=(pos, self.vi))

        vert.propagatations_all += fmt.propagate_format(line,self.vi, next_vertex.vi, edge)
        return self if end else next_vertex
    
    ppgt = propagate
    
    common_positions = ['above left',
                        'above right',
                        'below left',
                        'below right',
                        ]
    
    al, ar, bl, br = [shorthand_function(position) for position in common_positions]
    

    @classmethod
    def toTikz(cls):
        vert.declarations_all = ''
        for vert_item in vert.vertlist:
            vert.declarations_all += vert_item.declaration
        return (vert.declarations_all +
                vert.propagatations_all)

    @classmethod
    def wrapTikz(cls):
        return ("\\begin{{tikzpicture}}"
                "\n\\begin{{feynhand}}\n{}\n\\end{{feynhand}}"
                "\n\\end{{tikzpicture}}\n").format(vert.toTikz() )

    @classmethod
    def saveas(cls, fname):
        texfile = open(fname, mode="w")
        texfile.write(vert.wrapTikz())
        texfile.close()

    @classmethod
    def append(cls, fname):
        texfile = open(fname, mode="a")
        texfile.write(vert.wrapTikz())
        texfile.close()
