#!/bin/bash

aux="*.log *.aux *.toc *.out srcs/*.log srcs/*.aux srcs/*.out srcs/*.toc"

echo FIRST COMPILATION : > dbug.log

echo Q | pdflatex main.tex >> dbug

echo "" >> dbug.log

echo "SECOND COMPILATION : " >> dbug.log

echo Q | pdflatex main.tex >> dbug

if [ -f "main.pdf" ] ; then
	mv main.pdf rendu.pdf 
fi

#rm $aux

clear && echo "Rapport compiled"

if [ -f "rendu.pdf" ] ; then
	open rendu.pdf
else
	echo "Something went wrong"
	cat dbug | grep error
fi

mkdir -p tex_aux

mv $aux tex_aux

mv dbug tex_aux

