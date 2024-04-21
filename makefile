.PHONY: Psionics.pdf all clean scripts

all: Psionics.pdf

Psionics.pdf: Psionics.tex
				lualatex Psionics.tex -synctex=1 -interaction=nonstopmode -file-line-error -pdf %DOC%
				open -a Skim.app Psionics.pdf

clean:
				latexmk -CA

scripts:
				python Scripts/pwrs_to_tex.py
				python Scripts/create_subclass_tables.py