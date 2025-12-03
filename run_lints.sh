#!/bin/bash
# Linting script for Assignment 5

echo "Running pylint on Python files..."
echo "=================================="

# Run pylint with all fixes
pylint \
    get_gene_level_information.py \
    assignment5/config.py \
    assignment5/io_utils.py \
    --max-line-length=79 \
    --good-names="e,ex,exc,fd,fh,fn,i,j,k,v,x,y,z" \
    --disable=W0613,W0719,C0103,R0903,R0913,R0914 \
    --fail-under=10.0 \
    --exit-zero

echo "=================================="
echo "Linting complete!"

