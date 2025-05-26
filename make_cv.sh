#/bin/bash

mdFile=${1:?"missing arg 1 for markdown file"}
texFile="${mdFile%.md}.tex"
mkdir -p tmp
rm -f tmp/*
cp ${1} tmp/
python md_to_tex.py tmp/${1} french
pdflatex --output-directory tmp tmp/${texFile}
cp tmp/*.pdf .
