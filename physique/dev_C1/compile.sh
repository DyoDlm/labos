#!/bin/bash

aux="*.log *.aux *.toc *.out"

echo Q | pdflatex main.tex

echo Q | pdflatex main.tex

rm $aux
