#!/bin/bash

auxs=" \
	"*.log"\
	"*.aux"\
	"*.toc"\
	"*.out"\
	"srcs/*.aux"\
        "srcs/*.toc"\
        "srcs/*.out"\
        "srcs/*.log"\
	"srcs/*/*.aux"\
	"srcs/*/*.toc"\
	"srcs/*/*.out"\
	"srcs/*/*.log"\
"

echo FIRST COMPILATION : > dbug.log

echo Q | pdflatex main.tex >> dbug

echo "" >> dbug.log

echo "SECOND COMPILATION : " >> dbug.log

echo Q | pdflatex main.tex >> dbug

if [ -f "main.pdf" ] ; then
	mv main.pdf rendu.pdf 
fi

clear && echo "Rapport compiled"

if [ -f "rendu.pdf" ] ; then
	open rendu.pdf
else
	echo "Something went wrong"
	cat dbug | grep error
fi

mkdir -p tex_aux

for format in $auxs
do
	if [ -f "$format" ] ; then
		mv $format tex_aux
	fi
done

mv dbug tex_aux

