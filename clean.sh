#!/bin/sh
rm -rf tryed hacked
mv wordlists/wordlist.txt .
rm -rf wordlists
mkdir wordlists
mv wordlist.txt wordlists
mkdir tryed hacked
rm -rf __pycache__
