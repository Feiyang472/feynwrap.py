import os
from feynwrap import vert

vert('q').br().bl(r'\bar{q}',True).ppgt(r'\gamma', 'boson').br('l',True).ar('anti fermion',r'\bar{l}', True)

vert.saveas('./examples/demo.tex')

os.system("cd examples; pdflatex --interaction=batchmode -jobname=demo1 tikz-feyn.tex; rm *.log *.aux")
