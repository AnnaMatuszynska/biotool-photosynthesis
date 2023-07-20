#!/usr/bin/env python3

import re
import numpy as np
from pathlib import Path
from warnings import warn
from collections import defaultdict
import glob

po_file_header = """# PHOTOSYNTHESIS IN SILICO.
# Copyright (C) 2023 Computational Life Science RWTH Aachen
# Sarah Philipps et al., 2023.
#
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"POT-Creation-Date: 2022-12-02 17:21+0100\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Generated-By: pygettext.py 1.5\\n"
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

def _default_entry():
    return {"header": None}

def read_single_po(file, version="", entries=None, add_header=False, verbose=False):
    if entries is None:
        entries = defaultdict(_default_entry)

    with open(file, "r") as f:
        po = f.readlines()

        # Get the msgids
        ids = np.where(np.array([bool(re.match(f"^msgid", x)) for x in po]))[0]

        for id in ids:
            # Get the msgid string
            nam = re.sub("^msgid\s*[\"\'](.*)[\"\']\s*\n", "\g<1>", po[id])
            if nam in ["","\n"]:
                continue
            else:
                if entries[nam]["header"] is None:
                    entries[nam]["header"] = [po[id-1]]
                elif po[id-1] in entries[nam]["header"]:
                    pass
                else:
                    if verbose:
                        warn(f"multiple headers for entry {nam}")
                    entries[nam]["header"] += [po[id-1]]

                # Check if the next line has the right structure
                if not re.search("^msgstr", po[id+1]):
                    raise ValueError(fr"the msgstr following msgid '{nam}' in line {id} has the wrong format")

                # Remove the prefix and, if it is not multiline, the suffix
                string = re.sub("^msgstr\s*[\"\']", "", po[id+1])
                if not re.search("\\\\n\s*[\'\"]$", po[id+1]):
                    string = re.sub("[\"\']?\s*\n$","", string)
                entries[nam][version] = string

                for i in range(1,len(po)-id):
                    if re.search("\\\\\s*\n$", po[id+i]):
                        if i == 1:
                            entries[nam][version] += "\n"
                        entries[nam][version] += re.sub('[\'\"][\s\n]*$',"", po[id+i+1])
                    elif re.search("\\\\n\s*[\'\"]$", po[id+i]):
                        string = po[id+i+1]
                        if not re.search("\\\\n\s*[\'\"]$", string):
                            string = re.sub('[\'\"][\s\n]*$',"", string)
                        entries[nam][version] += string
                    else:
                        break
        versions = entries.get("_versions_",[])
        if version not in versions:
            entries["_versions_"] = list(entries.get("_versions_",[]) + [version])
    return entries

def make_allversion_po(po, file_header = "\n", versions=None):
    if versions is None:
        versions = po["_versions_"]

    text = file_header + "\n# TEXT VERSIONS\n" + "# " + "\n# ".join(versions) + "\n\n"
    for nam, items in po.items():
        if nam in ["_versions_"]:
            continue
        else:
            text += "".join(items["header"]) + f'msgid "{nam}"\n'
            for vers in versions:
                text += f'{vers} msgstr "{items.get(vers, "")}"\n'
            text += "\n"
    return text

def write_allversion_po(po, path = Path("allversion.po"), file_header="\n", versions=None):
    text = make_allversion_po(po, file_header, versions)
    with open(path, "w") as f:
        f.write(text)

if __name__ == "__main__":
    # Find all main.po files and read them in
    pos = glob.glob("./*/*/LC_MESSAGES/main.po")
    versions = [re.sub("\./(\w+)/(\w+)/.*", "\g<1>-\g<2>", x) for x in pos]

    po = defaultdict(_default_entry)
    for file, version in zip(pos, versions):
        po = read_single_po(file, version, entries=po)
    write_allversion_po(po, file_header=po_file_header)


