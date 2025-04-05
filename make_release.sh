#!/bin/bash
if [ -e release_notes/$1.md ]
then
    echo "$1 release notes exist, compiling pdf..."
    make clean
    make
    name="psionics_v$1"
    name="${name//./_}"
    name+=".pdf"
    echo "Making release with file: $name."
    mv Psionics.pdf $name
    gh release create v$1 -F release_notes/$1.md $name
else
    echo "release notes missing!"
fi