#!/bin/bash
cd "$(dirname "$0")"
run() { echo "== $1  [$2]"; s=$(date +%s); python3 gen.py $1 | ./spansearch | tail -3; echo "   time $(( $(date +%s) - s ))s"; }
run "5 4 3 8 1,1,0,0,1 0,0,1,0" "(x^4+xy^3+y^4)⊗u^2v, r=s=3 mod 5; Thm B/Prop C bound 9, test n=8"
run "5 4 3 9 1,1,0,0,1 0,0,1,0" "same, n=9 (is 9 attained over F_5?)"
run "7 3 3 7 0,0,1,0 0,0,1,0" "W3⊗W3 over F_7, R=8, test n=7"
run "11 2 3 5 0,1,0 0,0,1,0" "W2⊗W3 over F_11, R=6, test n=5"
run "5 4 4 11 3,0,2,1,0 0,0,0,1,0" "(x^3y+2x^2y^2+3y^4)⊗u^3v, r=s=3 mod 5; bound 12, test n=11"
