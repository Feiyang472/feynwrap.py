from feynwrap import vert

vert('q').br().bl(r'\bar{q}',True).ppgt(r'\gamma', 'boson').br('l',True).ar('anti fermion',r'\bar{l}', True)

vert.save_tex('demo.tex', path='./examples/')

vert.compile_pdf()
