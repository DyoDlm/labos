MAIN = main

TEX_SRCS := $(MAIN).tex $(wildcard rapport/*.tex)
IMG_SRCS := $(wildcard Forcer/*.png Frainer/*.png)
CSV_SRCS := $(wildcard Forcer/*.csv Frainer/*.csv)

PDF = $(MAIN).pdf

LATEX = pdflatex -interaction=nonstopmode

all: $(PDF)

$(PDF): $(TEX_SRCS) $(IMG_SRCS) $(CSV_SRCS)
	$(LATEX) $(MAIN).tex
	$(LATEX) $(MAIN).tex   # 2x pour refs

clean:
	rm -f *.aux *.log *.toc *.out *.bbl *.blg

fclean: clean
	rm -f $(PDF)

re: fclean
	all

.PHONY: all clean fclean re

