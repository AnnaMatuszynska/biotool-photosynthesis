#!/usr/bin/env python3

import re
import numpy as np
from pathlib import Path
from warnings import warn

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
            breaks = np.array([bool(re.search("\\\\\s*\n$|\\\\n\s*[\'\"]$", x)) for x in _po])
            extended = np.logical_and(others, breaks)

            if any(extended):
                for i in np.where(extended)[0]:
                    for j in range(i, len(_po)):
                        if breaks[j]:
                            others[j+1] = True
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
    pos = split_allversion_po("allversion.po")
    save_split_po(pos, locales_dir="")



