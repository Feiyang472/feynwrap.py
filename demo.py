import os  
from feynwrap import node

node(vert='q').br().bl(vert='\\bar{{q}}',end=True).propag(line='b',edge='\\gamma').br(vert='l',end=True).ar('af',vert='\\bar{{l}}')

node.save('demo.tex')

os.system("pdflatex --interaction=batchmode tikz-feyn.tex")