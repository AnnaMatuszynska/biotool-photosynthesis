#!/usr/bin/env python3

import numpy as np
import re
from pathlib import Path
from warnings import warn

default_header = """
# PHOTOSYNTHESIS IN SILICO.
# Copyright (C) 2023 Computational Life Science RWTH Aachen
# Sarah Philipps et al., 2023.
#
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"POT-Creation-Date: 2022-12-02 17:21+0100\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: pygettext.py 1.5\n"
"""


def _get_header_and_version(po):
    # Extract the header
    header_end = np.where(np.array([bool(re.match("# TEXT VERSIONS\n", x)) for x in po]))[0][0]
    header = po[0:header_end]
    po = po[header_end:]

    # Extract the versions
    version_end = np.where(np.invert([bool(re.match("^#", x)) for x in po]))[0][0]
    versions = [x.removeprefix("# ").removesuffix("\n") for x in po[1:version_end]]
    po = po[version_end:]
    return header, versions, po


def split_allversion_po(file):
    with open(file, "r") as f:
        po = f.readlines()

        # Extract header and versions
        header, versions, po = _get_header_and_version(po)

        # Split the different version texts
        texts = {}
        ns = {}
        for version in versions:
            _po = np.array(po, dtype=str)
            ns[version] = np.sum([bool(re.search(f"^{version}\s+msgstr", x)) for x in _po])
            _po = np.array([re.sub(f"^{version}\s+msgstr", "msgstr", x) for x in _po])

            # Get the lines that should be deleted
            # Lines may be broken and extended by "\"
            others = np.array([bool(re.search(f"(?<!{version})\s+msgstr", x)) for x in _po])
            breaks = np.array([bool(re.search("\\\\\s*\n$|\\\\n\s*['\"]\s*$", x)) for x in _po])
            extended = np.logical_and(others, breaks)

            if any(extended):
                for i in np.where(extended)[0]:
                    for j in range(i, len(_po)):
                        if breaks[j]:
                            others[j + 1] = True
                        else:
                            break

            texts[version] = header + list(_po[np.invert(others)])
    ns_val = np.array(list(ns.values()))
    if np.any(ns_val < ns_val.max()):
        warn(f"fewer replacements in version(s) {np.array(list(ns.keys()))[ns_val < ns_val.max()]}")

    return texts


def save_split_po(pos, locales_dir="."):
    for nam, text in pos.items():
        vers, lang = nam.split("-")
        path = Path(locales_dir) / vers / lang / "LC_MESSAGES" / "main.po"
        with open(path, "w") as f:
            f.writelines(text)


if __name__ == "__main__":
    DIRPATH = Path(__file__).parent.resolve()
    pos = split_allversion_po(DIRPATH / "allversion.po")
    save_split_po(pos, locales_dir=DIRPATH)
