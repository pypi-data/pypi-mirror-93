from dict_tools import data


async def start(hub, name):
    """
    Called only after the named run has compiled low data. If no low data
    is present an exception will be raised
    """
    if not hub.idem.RUNS[name].get("low"):
        raise ValueError()
    ctx = data.NamespaceDict({"run_name": name, "test": hub.idem.RUNS[name]["test"]})
    rtime = hub.idem.RUNS[name]["runtime"]
    low = hub.idem.RUNS[name].get("low")
    ref = f"idem.run.{rtime}.runtime"
    old_seq = {}
    old_seq_len = -1
    needs_post_low = True
    while True:
        # TODO: make the errors float up
        seq = hub.idem.req.seq.init.seq(low, hub.idem.RUNS[name]["running"])
        if seq == old_seq:
            raise Exception()
        await getattr(hub, ref)(name, ctx, seq, low, hub.idem.RUNS[name]["running"])
        await hub.idem.resolve.render(name)
        await hub.idem.state.compile(name)
        low = hub.idem.RUNS[name].get("low")
        if len(low) <= len(hub.idem.RUNS[name]["running"]):
            if hub.idem.RUNS[name]["post_low"] and needs_post_low:
                hub.idem.RUNS[name]["low"].extend(hub.idem.RUNS[name]["post_low"])
                needs_post_low = False
                continue
            else:
                break
        if len(seq) == old_seq_len:
            # We made no progress! Recursive requisite!
            raise Exception()
        old_seq = seq
        old_seq_len = len(seq)
        # Check for any new, available blocks to render
