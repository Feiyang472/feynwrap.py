# feynwrap.py

Purpose: Writing tikz makes me sad, so I wrap a layer of python around it to allow continuous creation of vertices and edges in Feynman diagrams.

## Installation
```bash
git clone https://github.com/Feiyang472/feynwrap.py.git

cd feynwrap.py

pip3 install .
```

## Drell-Yan example
```python
from feynwrap import vert

vert('q').br().bl(r'\bar{q}',True).ppgt(r'\gamma', 'boson').br('l',True).ar('anti fermion',r'\bar{l}', True)

vert.save_tex('demo.tex', path='./examples/')

vert.compile_pdf()
```

Result

![Drell-Yan](tikz-feyn-1.png)

## Tutorial
The first method is always `vert`, which creates a vertex. We can give it a label, and/or specify its location with respect to another `vert` instance.
```python
a = vert('\lambda')
```
The label $\lambda$ will be put on this just created vertex. Now we can get a propagator from `a`, and retrieve the vertex where the propagator arrives. 
```python
b = a.ppgt()
b.ppgt('fermion')
b.ppgt('below right', 'boson').ppgt('below left', 'gluon' True).ppgt('e', 'below right')
```
The `propagate` method takes 0 to 4 arguments ***in any order***. It recognizes special strings specifying particle type (`'anti fermion', 'boson', 'gluon'` etc.) and relative locations (`'above left'` etc.), as well as a Boolean value which specifies whether the destination of this propagation is at ends of the diagram.

At ends of the diagram, propagator labels are put on vertices. Otherwise, they are put alongside the edges.

The program then allows us to save to a `.tex` file and build it to pdf. The associated `.aux` and `.log` files are always removed after build.
```python
vert.save_tex('demo.tex', path='./examples/')
# vert.save_tex('demo', path='./examples/') # is exactly the same

vert.compile_pdf() 
```
If you want to keep the `tex` file and make some edits, specify `clean=[]` in `compile_pdf`.

-------------------------
This is an example of the generated `.tex`.
```latex
\begin{tikzpicture}
\begin{feynhand}
\vertex (v1)  {\(q\)};
\vertex (v2) [below right = of v1] ;
\vertex (v3) [below left = of v2] {\(\bar{{q}}\)};
\vertex (v4) [right = of v2] ;
\vertex (v5) [below right = of v4] {\(l\)};
\vertex (v6) [above right = of v4] {\(\bar{{l}}\)};

\propag [fermion] (v1) to (v2);
\propag [fermion] (v2) to (v3);
\propag [boson] (v2) to [edge label = \(\gamma\)] (v4);
\propag [fermion] (v4) to (v5);
\propag [anti fermion] (v4) to (v6);
\end{feynhand}
\end{tikzpicture}
```