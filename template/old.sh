#!/bin/bash

COMPILER="pdflatex"
SRC_DIR="./srcs"
LOG_DIR="tex_aux"
MAIN="./main.tex"
PDF="./report.pdf"
AUXS=" \
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


info() {
	echo -e "\033[36m$1\033[0m"
}
error() {
	echo -e "\033[31m$1\033[0m"
}
success() {
	echo -e "\033[32m$1\033[0m"
}
warning() {
	echo -e "\033[33m$1\033[0m"
}

watch() {
	STATE_A=""
	PROG_PID=""

	while [[ true ]]
	do
		STATE_B=$(get_state)
		if [[ $STATE_A != $STATE_B ]]; then
			STATE_A=$STATE_B
			clear
			info "───────── $(date) ─────────"
			rm -f "$PDF"
			compile
			if [ ! -f "$PDF" ]; then
				error "COMPILATION\ERROR"
                # grep some shit into debug
			else
				success "COMPILATION\tOK\n"
				info "───────────────────────────────────────────────────\n"
			    echo "OPENING $PDF"
                open $PDF
            fi
            info "────────────────────── WAITING A MODIFICATION ─────────────────────────"
        fi
		sleep 0.1
	done
}

get_state() {
	if [[ $(uname) == "Linux" ]];  then
		MD5="md5sum"
	else
		MD5="md5"
	fi
	SRC_STATE=$(find -L $SRC_DIR -type f -name "*.[ch]" -exec $MD5 {} \;)
	#TEST_STATE=$(find -L ./test -type f -name "*.sh" -exec $MD5 {} \;)
	echo "$SRC_STATE $TEST_STATE"
}

compile() { 
    info "FIRST COMPILATION"
    echo Q | $COMPILER $MAIN >> dbug
    echo "" >> dbug.log
    echo "SECOND COMPILATION" >> dbug
    echo Q | $COMPILER $MAIN
    mkdir -p $LOG_DIR
    for FORMAT in $AUXS
    do
        if [ -f "$FORMAT" ] ; then
            mv $FORMAT $LOG_DIR
        fi
    done
    mv dbug $LOG_DIR
}


#compile
watch "$@"
