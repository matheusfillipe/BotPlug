import socket

from mcstatus import MinecraftServer
from mcstatus.pinger import PingResponse

from botplug import hook
from botplug.util import colors

DEFAULT_SERVER = "minecraft.dot.org.es"

mc_colors = [
    ("\xa7f", "\x0300"),
    ("\xa70", "\x0301"),
    ("\xa71", "\x0302"),
    ("\xa72", "\x0303"),
    ("\xa7c", "\x0304"),
    ("\xa74", "\x0305"),
    ("\xa75", "\x0306"),
    ("\xa76", "\x0307"),
    ("\xa7e", "\x0308"),
    ("\xa7a", "\x0309"),
    ("\xa73", "\x0310"),
    ("\xa7b", "\x0311"),
    ("\xa71", "\x0312"),
    ("\xa7d", "\x0313"),
    ("\xa78", "\x0314"),
    ("\xa77", "\x0315"),
    ("\xa7l", "\x02"),
    ("\xa79", "\x0310"),
    ("\xa7o", ""),
    ("\xa7m", "\x13"),
    ("\xa7r", "\x0f"),
    ("\xa7n", "\x15"),
]


def format_colors(description):
    for original, replacement in mc_colors:
        description = description.replace(original, replacement)
    return description.replace("\xa7k", "")


def mcping(text):
    try:
        server = MinecraftServer.lookup(text)
    except (IOError, ValueError) as e:
        return str(e)

    try:
        s = server.status()  # type: PingResponse
    except socket.gaierror:
        return "Invalid hostname"
    except socket.timeout:
        return "Request timed out"
    except ConnectionRefusedError:
        return "Connection refused"
    except ConnectionError:
        return "Connection error"
    except (IOError, ValueError) as e:
        return "Error pinging server: {}".format(e)

    if isinstance(s.description, dict):
        description = format_colors(" ".join(s.description["text"].split()))
    else:
        description = format_colors(" ".join(s.description.split()))

    output_format = colors.parse(
        "{}$(clear) - $(bold){}$(clear) - $(bold){:.1f}ms$(clear) - $(bold){}/{}$(clear) players"
    )

    return output_format.format(
        description, s.version.name, s.latency, s.players.online, s.players.max
    ).replace("\n", colors.parse("$(clear) - "))


@hook.command("mc", autohelp=False)
def d_mcp():
    "Information about our minecraft server"
    return mcping(DEFAULT_SERVER)

@hook.command("mcping", "mcp")
def a_mcp(text):
    """<server[:port]> - gets info about the Minecraft server at <server[:port]>"""
    return mcping(text)
