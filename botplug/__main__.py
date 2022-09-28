import re

from pathlib import Path
import importlib
from botplug.bot import bot, BotPlug
from botplug.config import Config

from botplug.hook import commands, regex_commands, on_start_hooks

bot.set(BotPlug(Config(None)))

def safe_resolve(path_obj: Path) -> Path:
    """Resolve the parts of a path that exist, allowing a non-existant path
    to be resolved to allow resolution of its parents

    :param path_obj: The `Path` object to resolve
    :return: The safely resolved `Path`
    """
    unresolved = []
    while not path_obj.exists():
        unresolved.append(path_obj.name)
        path_obj = path_obj.parent

    path_obj = path_obj.resolve()

    for part in reversed(unresolved):
        path_obj /= part

    return path_obj


plugin_dir = Path("plugins/")
path_list = plugin_dir.rglob("[!_]*.py")

for path in path_list:
    path = Path(path)
    file_path = safe_resolve(path)
    plugin_path = file_path.relative_to(Path(__file__).parent.parent)
    title = ".".join(plugin_path.parts[1:]).rsplit(".", 1)[0]
    module_name = "plugins.{}".format(title)
    print(module_name)
    plugin_module = importlib.import_module(module_name)

def mainloop():
    while True:
        try:
            text = input(">> ")
        except KeyboardInterrupt:
            break
        command, args = text.split(" ", 1)
        try:
            for cmd in commands:
                if command in cmd.commands:
                    print(cmd.hook(text=args, reply=print))
                    break
            else:
                print("Command not found\n")
        except Exception as e:
            print(e)

mainloop()
