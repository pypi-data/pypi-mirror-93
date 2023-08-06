def __init__(hub):
    hub.pop.sub.load_subdirs(hub.gate, recurse=True)


def cli(hub):
    hub.pop.config.load(["gate"], cli="gate")
    hub.pop.loop.create()
    hub.pop.Loop.run_until_complete(
        hub.gate.init.start(gate_server=hub.OPT.gate.server)
    )


async def test(hub, *args, **kwargs):
    """
    The test function for gate
    """
    return {"args": args, "kwargs": kwargs}


async def start(hub, gate_server: str):
    return await hub.gate.srv[gate_server].start()


async def stop(hub, gate_server: str):
    hub.log.debug("Shutting down gate server")
    return await hub.gate.srv[gate_server].stop()


async def join(hub, gate_server):
    return await hub.gate.srv[gate_server].join()
