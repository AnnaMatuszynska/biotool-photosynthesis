#!/usr/bin/env python3

import re
import numpy as np
from pathlib import Path
from warnings import warn
from collections import defaultdict
import glob

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
                entries[nam][version] = re.sub("^msgstr\s*[\"\'](.*)[\"\']\s*\n", "\g<1>", po[id+1])
                for i in range(1,len(po)-id):
                    if re.search("\\\s*$", po[id+i]):
                        entries[nam][version] += po[id+i+1] + "\n"
                    else:
                        break
        versions = entries.get("_versions_",[])
        if version not in versions:
            entries["_versions_"] = list(entries.get("_versions_",[]) + [version])
    return entries

def make_allversion_po(po, versions=None):
    if versions is None:
        versions = po["_versions_"]

    text = "\n\n\n# TEXT VERSIONS\n" + "# " + "\n# ".join(versions) + "\n\n"
    for nam, items in po.items():
        if nam in ["_versions_"]:
            continue
        else:
            try:
                items["header"]
            except:
                print(nam)
            text += "".join(items["header"]) + f'msgid "{nam}"\n'
            for vers in versions:
                text += f'{vers} msgstr "{items.get(vers, "")}"\n'
            text += "\n"
    return text

def write_allversion_po(po, path = Path("allversion.po"), versions=None):
    text = make_allversion_po(po, versions)
    with open(path, "w") as f:
        f.write(text)

if __name__ == "__main__":
    # Find all main.po files and read them in
    pos = glob.glob("./*/*/LC_MESSAGES/main.po")
    versions = [re.sub("\./(\w+)/(\w+)/.*", "\g<1>-\g<2>", x) for x in pos]

    po = defaultdict(_default_entry)
    for file, version in zip(pos, versions):
        po = read_single_po(file, version, entries=po)
    write_allversion_po(po)

