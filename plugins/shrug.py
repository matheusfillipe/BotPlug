from botplug import hook


@hook.command("shrug", autohelp=False)
def shrug():
    r"""- shrugs

    >>> shrug()
    '¯\\_(ツ)_/¯'
    """
    return r"¯\_(ツ)_/¯"
