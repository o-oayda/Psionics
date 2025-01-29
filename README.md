# Psionics
This repository houses the psionics system, in which two classes are offered: the psion and the psi knight.

## Roadmap
- [x] Initial release
- [ ] Additional PD based on Wisdom modifier
- [x] Add spells interacting with psionics
    - [ ] Expand spells interacting with psionics
- [x] Hyperlinks/index for navigating powers
- [x] Fix formatting in psion discipline sublists
- [ ] Additional high level powers

## Accessing Psionics
The latest psionics release can be found at the [release page](https://github.com/o-oayda/Psionics/releases).

## Changelogs
The full changelogs are also available on the [release page](https://github.com/o-oayda/Psionics/releases).

## Compiling the PDF
If you wish to compile the latest PDF from scratch (instead of choosing an
appropriate release from above), follow these steps.
1. Ensure that you have a working local tex installation and have Python 3 installed.
2. `git clone` the [fork of the D&D LaTeX template](https://github.com/o-oayda/DND-5e-LaTeX-Template)
into your `TEXMFHOME` directory:
```sh
git clone https://github.com/o-oayda/DND-5e-LaTeX-Template.git "$(kpsewhich -var-value TEXMFHOME)/tex/latex/dnd"
```
3. `git clone` this repo somewhere and `cd` into it.
4. Make a python virtual environment with `python3 -m venv .venv` and activate it.
5. Install the Python requirements (`pip install -r requirements.txt`).
6. Now you should be good to go. Run `make` in the command line to build the PDF.