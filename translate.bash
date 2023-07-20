#!/bin/bash

cd locales
./split_allversion_po.py
cd ..

find locales/ -name "main.po" | while read F; do
    msgfmt -o ${F::-3}.mo ${F::-3}
done
