import random
from typing import List

from botplug import hook
from botplug.bot import BotPlug
from botplug.util import colors

responses: List[str] = []


@hook.on_start()
def load_responses(bot: BotPlug) -> None:
    path = bot.data_path / "8ball_responses.txt"
    responses.clear()
    with open(path, encoding="utf-8") as f:
        responses.extend(
            line.strip() for line in f.readlines() if not line.startswith("//")
        )


@hook.command("8ball", "8", "eightball")
async def eightball(action):
    """<question> - asks the all knowing magic electronic eight ball <question>"""
    magic = random.choice(responses)
    message = colors.parse("shakes the magic 8 ball... {}".format(magic))

    action(message)
