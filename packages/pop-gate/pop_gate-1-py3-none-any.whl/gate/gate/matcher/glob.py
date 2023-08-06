# Import python libs
import fnmatch


def match(hub, ref: str) -> bool:
    """
    Check the desired ref to see if it matches a globular ref in the refs list
    """
    for pattern in hub.OPT.gate.refs:
        if hub.OPT.gate.prefix:
            pattern = f"{hub.OPT.gate.prefix}.{pattern}"
        if fnmatch.fnmatch(ref, pattern):
            return True
    else:
        return False
