If you are well-versed in LaTeX, you likely need to read no further than
quichem.pdf. If you are just starting out in LaTeX however, and wish to hack
on the quichem LaTeX support yourself, this README is for you.

On the LaTeX side, only two files are needed for quichem support: quichem.dtx
and quichem.ins. The quichem.pdf and quichem.sty files in the Git repository
were built from these two files. On the Python side, quichem must be
accessible as a module on the PYTHONPATH. As stated in quichem.pdf, you can
check that the Python side of quichem is set up correctly by ensuring that
"<python> -m quichem.tools.latex", where <python> is the Python 3 executable,
outputs "Congratulations! Your quichem installation is set up with LaTeX
support."

To build quichem.sty, the LaTeX package for quichem, run "latex quichem.ins".
The resulting quichem.sty file can then be placed into a directory searched
by TeX. For testing purposes, you can put quichem.sty into the current working
directory of a project rather than copying it to a TeX package installation
path.

To build quichem.pdf, the documentation for quichem.sty, run the following
commands:

    $ pdflatex -shell-escape quichem.dtx
    $ makeindex -s gind.ist quichem.idx
    $ makeindex -s gglo.ist -o quichem.gls quichem.glo
    $ pdflatex -shell-escape quichem.dtx

The first call to makeindex creates the code index and the second call to
makeindex creates the "Change History" section. The second run of pdflatex
ensures the "Change History" section is included at the end of the document.

quichem.pdf provides a good overview of the ways quichem can be used in LaTeX.
../SYNTAX.rst provides detailed documentation on the syntax of the quichem
input format.
