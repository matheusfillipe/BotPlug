"""
Etymology plugin

Authors:
    - GhettoWizard
    - Scaevolus
    - linuxdaemon <linuxdaemon@snoonet.org>
"""
import re

import requests
from requests import HTTPError

from botplug import hook
from botplug.util import formatting, web
from botplug.util.http import parse_soup

import ety


@hook.command("etree")
def etymology_tree(nick, text, reply):
    """<word> - retrieves etymolocial tree of <word>"""
    # pager = CommandPager.from_multiline_string(str(ety.tree(text.strip())))
    for page in str(ety.tree(text.strip())).split("\n"):
        reply(page)


@hook.command("e", "etymology")
def etymology(text, reply):
    """<word> - retrieves the etymology of <word>"""

    url = "http://www.etymonline.com/index.php"

    response = requests.get(url, params={"term": text})

    try:
        response.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 404:
            return "No etymology found for {} :(".format(text)
        reply(
            "Error reaching etymonline.com: {}".format(e.response.status_code)
        )
        raise

    if response.status_code != requests.codes.ok:
        return "Error reaching etymonline.com: {}".format(response.status_code)

    soup = parse_soup(response.text)

    block = soup.find("div", class_=re.compile("word--.+"))

    etym = " ".join(e.text for e in block.div)

    etym = " ".join(etym.splitlines())

    etym = " ".join(etym.split())

    etym = formatting.truncate(etym, 200)

    etym += " Source: " + web.try_shorten(response.url)

    return etym
