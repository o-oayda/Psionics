.PHONY: Psionics.pdf all clean scripts copy docs

all: Psionics.pdf

Psionics.pdf: Psionics.tex
				make scripts
				lualatex Psionics.tex -synctex=1 -interaction=nonstopmode -file-line-error -pdf %DOC%
				open -a Skim.app Psionics.pdf

clean:
				latexmk -CA

# need to copy powers from root dir to _data dir for github pages
# since symlink does not seem to be working
# copy:
# cp powers_final.yml docs/_data/powers_final.yml

scripts:
				python Scripts/pwrs_to_tex.py
				python Scripts/create_subclass_tables.py
				python Scripts/items_to_tex.py
				python Scripts/spells_to_tex.py

docs:
				python Scripts/create_pages.py
				cd docs && bundle exec jekyll build && bundle exec jekyll serve