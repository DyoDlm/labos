#!/bin/bash

arg=$(echo $1 | wc -w)

if (( $arg != 1 )) ; then
	exit
fi

pdflatex $1

mkdir -p tex_aux
mkdir -p pdfs

mv *.aux *.log *.out tex_aux

mv *.pdf pdfs 
