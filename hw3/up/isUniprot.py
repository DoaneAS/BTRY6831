import re
import sys

idt = sys.argv[1]



def isUni(idx):
    id_type = ["Uniprot", "Isoform", "Unknown"]
    uniprot = re.compile(
    r"""
    ^

    # Uniprot ID
    (
    \b[OPQ][0-9][A-Z0-9]{3}[0-9]$\b
    |
    \b^[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}\b
    )

    """, re.VERBOSE)

    u = uniprot.match(idx)
    if u:
        if u.group() == idx:
            return (id_type[0])

    isoform = re.compile(
    r"""
    ^
    #isoform
    (
    \b^[OPQ]
    [0-9]
    [A-Z0-9]{3}
    [0-9]
    \-[0-9]+
    \b
    |
    \b^[A-NR-Z]
    [0-9]
    ([A-Z][A-Z0-9]{2}[0-9]){1,2}
    \-[0-9]+\b
    )


    """, re.VERBOSE)
    iso = isoform.match(idx)
    if iso:
        if iso.group() == idx:
            return (id_type[1])
    return (id_type[2])

print isUni(idt)