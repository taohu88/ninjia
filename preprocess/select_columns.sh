#!/usr/bin/env bash


awk -F";" 'BEGIN {OFS=","} {print $6,$5,$4,$3,$2}' infile.csv > outfile.csv