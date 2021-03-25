# `feynwrap.py`

Purpose: Writing tikz makes me sad, so I wrap a layer of python around it to allow continuous creation of vertices and edges in Feynman diagrams.

## Installation
```bash
git clone https://github.com/Feiyang472/feynwrap.py.git

pip3 install .
```


## Getting started
The main class to create a vertex is `vert`.
```python
from feynwrap import node

quark = vert('q')
```
Once a vertex instance is created, one can call `propagate` or abbreviated `ppgt` from it.
```python
emVertex = quark.ppgt('below right')

# br, bl, al, ar are aliases for below right, below left, etc.
emVertex = emVertex.bl(r'\bar{q}',True)
```
`ppgt` takes arguments which are either strings or Booleans, in any order, without keywords. "Special" strings get recognized.
- `'fermion'`(default), `'boson'`, or `'gluon'` are  propagator specifiers
- `right`(default), `above left`, `below right`, etc. specify the position of the next vertex with respect to the calling instance.
- `True` or `False`(default) indicates whether the current vertex is a vertex at ends of the diagram. If `True`, the calling vertex is returned. Otherwise the destination vertex is returned.
- A string which isn't a propagator type or a location will be recognized as a label. The package will decide whether to put the label on the edge or the vertex

We can continue with the same example to do some more. Save to `tikz-feynman` format and compile to pdf.
```python
emVertex.ppgt(r'\gamma', 'boson').br('l',True).ar('anti fermion',r'\bar{l}', True)

node.save('./examples/demo.tex')

os.system("cd examples; pdflatex --interaction=batchmode -jobname=demo1 tikz-feyn.tex; rm *.log *.aux")
```

Result

![Drell-Yan](tikz-feyn-1.png)

The above example is the same as the following one liner
```python
vert('q').br().bl(r'\bar{q}',True).ppgt(r'\gamma', 'boson').br('l',True).ar('anti fermion',r'\bar{l}', True)
```

I wrote in python because programming in LaTeX is a pain.

-------------------------
This is the generated `demo.tex`.
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