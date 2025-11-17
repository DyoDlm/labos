#!/bin/bash

aux="*.log *.aux *.toc *.out"

echo Q | pdflatex main.tex

echo Q | pdflatex main.tex

if [ -f "main.pdf" ] ; then
	mv main.pdf rapport.pdf
fi

rm $aux

clear && echo "Rapport compiled"
