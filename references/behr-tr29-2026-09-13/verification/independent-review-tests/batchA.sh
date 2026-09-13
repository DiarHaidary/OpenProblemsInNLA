#!/bin/bash
cd "$(dirname "$0")"
run() { echo "== $1  [$2]"; s=$(date +%s); python3 gen.py $1 | ./spansearch | tail -3; echo "   time $(( $(date +%s) - s ))s"; }
run "5 3 4 9 0,0,1,0 0,0,0,1,0" "W3⊗W4 = x^2y⊗u^3v, claim R=10, test n=9"
run "5 3 4 8 0,0,1,0 0,0,1,0,0" "x^2y⊗u^2v^2, formula 9, test n=8"
run "5 4 4 11 0,0,0,1,0 0,0,0,1,0" "W4⊗W4 = x^3y⊗u^3v, claim R=12, test n=11"
run "5 4 4 11 0,0,0,1,0 0,0,1,0,0" "x^3y⊗u^2v^2, formula 12, test n=11"
run "5 4 4 11 0,0,0,1,0 0,0,0,1,0 11" "planted control: random 11-point combination, dim 25"
