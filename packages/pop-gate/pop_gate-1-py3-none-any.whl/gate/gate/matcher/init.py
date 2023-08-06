from typing import Dict


def match(hub, ref: str) -> bool:
    """
    Match the listed refs with the desired ref to see if the correct ref is
    being exposed.
    """
    return hub.gate.matcher[hub.OPT.gate.matcher].match(ref)
