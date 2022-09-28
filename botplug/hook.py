on_start_hooks = []
def on_start(param=None, **kwargs):
    """External on_start decorator. Can be used directly as a decorator, or with args to return a decorator"""

    def _on_start_hook(func):
        on_start_hooks.append(func)
        return func

    if callable(param):
        return _on_start_hook(param)

    return _on_start_hook



commands = []
def command(*args, **kwargs):
    """External command decorator. Can be used directly as a decorator, or with args to return a decorator."""

    def _command_hook(func, alias_param=None):
        commands.append(func)
        return func

    if len(args) == 1 and callable(args[0]):
        return _command_hook(args[0])

    # this decorator is being used indirectly, so return a decorator function
    return lambda func: _command_hook(func, alias_param=args)



regex_commands = []
def regex(regex_param, **kwargs):
    """External regex decorator. Must be used as a function to return a decorator."""

    def _regex_hook(func):
        regex_commands.append(func)
        return func

    if callable(regex_param):
        raise TypeError(
            "@regex() hook must be used as a function that returns a decorator"
        )

    return _regex_hook


onload = on_start
