import asyncio
from typing import Any, Dict


def __init__(hub):
    # A mapping of dyne_names/subs to a reference to a function on the hub that should run that function
    # If no reference is listed then a getattr(hub, ref) will be done and the reference will be called directly
    hub.gate.srv.RUNNER = {}


async def runner(hub, ref: str, params: Dict[str, Any]) -> Any:
    """
    Call a function based on runners defined before the program started
    """
    prefix = ref.split(".")[0]
    if prefix in hub.gate.srv.RUNNER:
        run = hub.gate.srv.RUNNER[prefix]
        if not hasattr(run, "__call__"):
            # If the prefix was a string then get it's reference on the hub
            run = hub[run]
        ret = run(ref, **params)
    else:
        ret = hub[ref](**params)

    if asyncio.iscoroutine(ret):
        ret = await ret

    return ret
