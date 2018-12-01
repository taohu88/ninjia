#!/usr/bin/env bash

shuf $1 | split -l $(( $(wc -l < $1) * 80 / 100 ))