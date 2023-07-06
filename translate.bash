#!/bin/bash

find locales/ -name "*.po" | while read F; do
    msgfmt -o ${F::-3}.mo ${F::-3}
done
