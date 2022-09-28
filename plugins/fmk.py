import random
from typing import List

from botplug import hook
from botplug.bot import BotPlug

fmklist: List[str] = []


@hook.on_start()
def load_fmk(bot: BotPlug) -> None:
    fmklist.clear()
    with open(bot.data_path / "fmk.txt", encoding="utf-8") as f:
        fmklist.extend(
            line.strip() for line in f.readlines() if not line.startswith("//")
        )


@hook.command("fmk", autohelp=False)
def fmk(text, message):
    """[nick] - Fuck, Marry, Kill"""
    message(
        " {} FMK - {}, {}, {}".format(
            (text.strip() if text.strip() else ""),
            random.choice(fmklist),
            random.choice(fmklist),
            random.choice(fmklist),
        )
    )
