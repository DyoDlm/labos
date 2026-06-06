#!/bin/bash

COMPILER="pdflatex"
SRC_DIR="./srcs"
LOG_DIR="tex_aux"
MAIN="main.tex"
PDF="main.pdf" 

info()    { echo -e "\033[36m$1\033[0m"; }
error()   { echo -e "\033[31m$1\033[0m"; }
success() { echo -e "\033[32m$1\033[0m"; }
warning() { echo -e "\033[33m$1\033[0m"; }

get_state() {
	if [[ $(uname) == "Linux" ]]; then
		MD5="md5sum"
	else
		MD5="md5"
	fi
	SRC_STATE=$(find -L "$SRC_DIR" -type f -name "*.tex" -exec $MD5 {} \;)
	MAIN_STATE=$(find . -maxdepth 1 -name "main.tex" -exec $MD5 {} \;)
	echo "$SRC_STATE $MAIN_STATE"
}

compile() {
	mkdir -p "$LOG_DIR"

	info "FIRST COMPILATION"
	echo Q | $COMPILER "$MAIN" #>> "$LOG_DIR/dbug" 2>&1

	info "SECOND COMPILATION"
	echo Q | $COMPILER "$MAIN" #>> "$LOG_DIR/dbug" 2>&1

	#shopt -s nullglob
	for FORMAT in \
		*.log *.aux *.toc *.out \
		srcs/*.aux srcs/*.toc srcs/*.out srcs/*.log \
		srcs/*/*.aux srcs/*/*.toc srcs/*/*.out srcs/*/*.log
	do
		mv "$FORMAT" "$LOG_DIR/" 2>/dev/null
	done
	#shopt -u nullglob
}

watch() {
	STATE_A=""
	while true; do
		STATE_B=$(get_state)
		if [[ "$STATE_A" != "$STATE_B" ]]; then
			STATE_A="$STATE_B"
			clear
			info "───────── $(date) ─────────"
			rm -f "$PDF"
			compile
            sleep 0.5
			if [ ! -f "$PDF" ]; then
				error "\n\nCOMPILATION\tERROR\n\n"
				grep -i "error\|fatal" "$LOG_DIR/dbug" 2>/dev/null | head -20
			else
				success "\n\nCOMPILATION\tOK\n\n"
				info "───────────────────────────────────────────────────\n"
				xdg-open "$PDF" &>/dev/null &
			fi
			info "────────────────────── WAITING A MODIFICATION ─────────────────────────"
		fi
		sleep 0.1
	done
}

watch "$@"
