#!/bin/bash

MI2=164.8
SOLD2=207.6
LA2=220
LAD2=233
SI2=247.5
DO3=264
RE3=297
MI3=330
FA3=352
SOL3=392
LA3=440

function play {
	PITCH=$1
	DURATION=$2
	SLEEP_TIME=0

	if [ $# -ge 3 ]; then
		SLEEP_TIME=$3
	fi

	beep -f $PITCH -l $DURATION
	sleep $SLEEP_TIME
}

while true; do
	NB_LOOPS=$(( ( RANDOM % 20 ) + 1 ))
	MAX_I=$(( 4*NB_LOOPS ))
	for i in $(seq 1 ${MAX_I}); do
		play $LA2 150

		play $MI3 150
		play $LA3 150

		play $MI3 150
		play $LA3 150
		play $MI3 150
	done
	play $MI3 1000 0.5

	for i in {1..2}; do
		play $MI3 500
		play $FA3 750
		play $MI3 150 0.1
		play $MI3 150 0.1
		play $RE3 150 0.1
		play $RE3 150 0.1
		play $DO3 150 0.1
		play $MI3 750 0.1
		play $RE3 150 0.1
		play $DO3 400 0.1
		play $DO3 400 0.1
		play $RE3 400 0.3
		play $DO3 150 0.1
		play $DO3 150 0.1
		play $SI2 150 0.1
		play $SI2 150 0.1
		play $SOLD2 150 0.1
		play $LA2 500
	done
	for i in {1..2}; do
		play $MI3 500
		play $FA3 700 0.3
		play $SOL3 700 0.1
		play $FA3 250
		play $MI3 500 0.2
		play $RE3 150
		play $MI3 150
		play $RE3 400 0.1
		play $DO3 150 0.1
		play $MI3 150 0.1
		play $RE3 200 0.3
		play $DO3 150 0.1
		play $RE3 200 0.1
		play $SI2 150 0.1
		play $DO3 150 0.1
		play $SI2 150 0.1
		play $SOLD2 250
		play $LA2 500
	done
done
