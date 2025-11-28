#!/bin/bash

aux="*.log *.aux *.toc *.out srcs/*.log srcs/*.aux srcs/*.out srcs/*.toc"

echo Q | pdflatex main.tex

echo Q | pdflatex main.tex

if [ -f "main.pdf" ] ; then
	mv main.pdf rendu.pdf 
fi

rm $aux

clear && echo "Rapport compiled"
open rendu.pdf
