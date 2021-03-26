"""
formatter
"""
from ctypes import c_int32 as Int

I_PARTICLE = 0
I_POSITION = 1
I_ENDING_VERTEX = 2
I_LABEL = 3

def feyn_arg_sort(args):
    sorted_args = ['fermion', 'right', False, None, None]

    switcher = {}
    switcher.update(dict.fromkeys(['boson',
                                   'fermion',
                                   'anti fermion',
                                   'gluon'], I_PARTICLE) )

    switcher.update(dict.fromkeys(['above left',
                                   'above right',
                                   'below left',
                                   'below right'], I_POSITION) )

    switcher.update(dict.fromkeys([True,
                                   False], I_ENDING_VERTEX))

    for arg in args:
        i_arg = switcher.get(arg, I_LABEL)
        if i_arg == I_LABEL:
            print('created label ' + arg)
        sorted_args[i_arg] = arg

    return sorted_args

def propagate_format(line, this_vi, next_vi, edge):
    edge_format = '' if not edge else '[edge label = \\({}\\)]'.format(edge)
    return '\n\\propag [{}] (v{}) to {}(v{});'.format(line, this_vi, edge_format, next_vi)


def wrap_tikz(content):
    return ("\\begin{{tikzpicture}}"
            "\n\\begin{{feynhand}}\n{}\n\\end{{feynhand}}"
            "\n\\end{{tikzpicture}}\n").format(content)
    
headfoot = """
\\documentclass{{article}} 
\\usepackage{{tikz}}
\\usepackage[compat=1.1.0]{{tikz-feynhand}}

\\usepackage[active,tightpage]{{preview}}
\\PreviewEnvironment{{tikzpicture}} 

\\begin{{document}}

{}

\\end{{document}}
"""

