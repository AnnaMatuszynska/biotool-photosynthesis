#!/bin/bash

cd locales
./split_allversion_po.py
cd ..

msgfmt -o locales//4bio/pl/LC_MESSAGES/main.mo locales//4bio/pl/LC_MESSAGES/main
msgfmt -o locales//4bio/de/LC_MESSAGES/main.mo locales//4bio/de/LC_MESSAGES/main.po
msgfmt -o locales//4bio/fr/LC_MESSAGES/main.mo locales//4bio/fr/LC_MESSAGES/main.po
msgfmt -o locales//4bio/es/LC_MESSAGES/main.mo locales//4bio/es/LC_MESSAGES/main.po
msgfmt -o locales//4bio/en/LC_MESSAGES/main.mo locales//4bio/en/LC_MESSAGES/main.po
msgfmt -o locales//4math/pl/LC_MESSAGES/main.mo locales//4math/pl/LC_MESSAGES/main.po
msgfmt -o locales//4math/de/LC_MESSAGES/main.mo locales//4math/de/LC_MESSAGES/main.po
msgfmt -o locales//4math/fr/LC_MESSAGES/main.mo locales//4math/fr/LC_MESSAGES/main.po
msgfmt -o locales//4math/es/LC_MESSAGES/main.mo locales//4math/es/LC_MESSAGES/main.po
msgfmt -o locales//4math/en/LC_MESSAGES/main.mo locales//4math/en/LC_MESSAGES/main.po
