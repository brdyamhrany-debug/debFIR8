#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'

echo -e "${RED}"
echo "       mm            mm                           "
echo "       ##            ##                           "
echo "  m###m##   m####m   ##m###m             ##m###m  "
echo " ##\"  \"##  ##mmmm##  ##\"  \"##            ##\"  \"## "
echo " ##    ##  ##\"\"\"\"\"\"  ##    ##            ##    ## "
echo " \"##mm###  \"##mmmm#  ###mm##\"     ##     ###mm##\" "
echo "   \"\"\" \"\"    \"\"\"\"\"   \"\" \"\"\"       \"\"     ## \"\"\"   "
echo "                                         ##        "
echo -e "${NC}"

read -p "name target: " chars
read -p "Min length: " min
read -p "Max length: " max
read -p "Output filename: " filename

python3 -c "
import itertools
chars = '$chars'
min_l = $min
max_l = $max
with open('$filename', 'w') as f:
    for length in range(min_l, max_l + 1):
        for combo in itertools.product(chars, repeat=length):
            f.write(''.join(combo) + '\n')
"
