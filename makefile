.PHONY: Psionics.pdf all clean scripts copy

all: Psionics.pdf

Psionics.pdf: Psionics.tex
				lualatex Psionics.tex -synctex=1 -interaction=nonstopmode -file-line-error -pdf %DOC%
				open -a Skim.app Psionics.pdf

clean:
				latexmk -CA

# need to copy powers from root dir to _data dir for github pages
# since symlink does not seem to be working
copy:
				cp powers_final.yml docs/_data/powers_final.yml

scripts:
				python Scripts/pwrs_to_tex.py
				python Scripts/create_subclass_tables.py