"""
Feynman Diagram wrapper
"""
from os import system as bash
import feynwrap.feynformat as fmt

def shorthand_function(pose):
    return lambda self, *args: self.propagate(pose, *args)

class vert:
    declarations_all = None
    propagatations_all = ''
    vertlist = []
    path = '.'
    filename = None
    
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
    def wrap_env(cls):
        vert.declarations_all = ''
        for vert_item in vert.vertlist:
            vert.declarations_all += vert_item.declaration
        return fmt.wrap_tikz(vert.declarations_all + 
                             vert.propagatations_all )

    @classmethod
    def save_tex(cls, filename, path=None, mode='w'):
        if filename.endswith('.tex'):
            filename = filename[:-4]

        cls.filename = filename
        if path:
            cls.path = path
        texfile = open(path+filename+'.tex', mode=mode)
        texfile.write(fmt.headfoot.format(vert.wrap_env() ))
        texfile.close()
    
    @classmethod
    def compile_pdf(cls, clean = ['tex']):
        if cls.filename:
            cleaning = 'rm {}.log {}.aux'.format(cls.filename, cls.filename)
            for cleaned_suffix in clean:
                cleaning += ' {}.{}'.format(cls.filename, cleaned_suffix)
            bash("cd {}; pdflatex --interaction=batchmode {}; {}".format(cls.path, cls.filename, cleaning) )
        else:
            raise(FileNotFoundError('tex file not saved yet'))

    @classmethod
    def append(cls, filename):
        texfile = open(filename, mode="a")
        texfile.write(vert.wrap_env() )
        texfile.close()
