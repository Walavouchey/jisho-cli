#!/usr/bin/env python3

import requests as req
import sys
import os
import platform
import ctypes
import optparse
from urllib.parse import quote
from colors import color
import json

def strongColor(string):
    return color(string, fg="red")

def neutralColor(string):
    return color(string, fg=245)

def tagColor(string):
    return color(string, fg=130)

def linkColor(string):
    return color(string, fg="cyan")

if not sys.stdout.isatty():
    def cancel(string, *args, **kwargs):
        return string
    color = cancel
elif platform.system() == "Windows":
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    del kernel32

def checkCount(option, opt_str, value, parser):
    if value <= 0:
        raise optparse.OptionValueError(f"option {opt_str}: expected an integer > 0, got {value}")
    parser.values.count = value
usage = "Usage: jisho [options] <word or kanji>"
parser = optparse.OptionParser(usage=usage)
parser.add_option("-c", "--count", type="int", dest="count", metavar="COUNT", action="callback", callback=checkCount, help="number of results to display")
parser.add_option("-n", "--no-cache", action="store_false", dest="cache", default=True, help="don't use cache")
(options, args) = parser.parse_args()
if len(args) <= 0:
    print(usage)
    sys.exit(1)

searchTerm = args[0]
r = ""
def getDataAndCache(url, searchTerm):
    r = ""
    cacheFolder = ""
    appdata = os.getenv("localappdata")
    home = os.getenv("HOME")
    if appdata:
        cacheFolder = os.path.join(appdata, "jisho-cli")
    elif home:
        cacheFolder = os.path.join(home, ".cache", "jisho-cli")
    if not os.path.exists(cacheFolder) and (appdata or home):
        try:
            os.system(f"mkdir {cacheFolder}")
        except Exception:
            pass
    try:
        with open(os.path.join(cacheFolder, searchTerm), "r", encoding="utf-8") as file:
            r = json.loads(file.read())
    except Exception:
        r = req.get(url % searchTerm).json()
        try:
            with open(os.path.join(cacheFolder, searchTerm), "w", encoding="utf-8") as file:
                file.write(json.dumps(r))
        except Exception:
            pass
    return r

if options.cache:
    r = getDataAndCache("https://jisho.org/api/v1/search/words?keyword=%s", searchTerm)
else:
    r = req.get("https://jisho.org/api/v1/search/words?keyword=%s" % searchTerm).json()

count = min(len(r["data"]), options.count) if options.count is not None else len(r["data"])
print(
    "\n\n".join(
        [
            " - ".join(
                [
                    strongColor(t) if i == 0 else neutralColor(t) for i, t in enumerate(w["japanese"][0].values())
                ]
            )
            + (", " + tagColor("common") if w["is_common"] else "") 
            + ((", " + ", ".join([tagColor(t) for t in w["jlpt"]])) if w["jlpt"] else "")
            + ((", " + ", ".join([tagColor(t) for t in w["tags"]])) if w["tags"] else "")
            + "\n\t" + "\n\t".join(
                [
                    neutralColor(f"{i + 1}. ")
                    + (neutralColor("(%s) " % ", ".join(s["parts_of_speech"])) if s["parts_of_speech"] else "")
                    + "; ".join(
                        s["english_definitions"]
                    )
                    + (
                        (
                            (neutralColor(" (") + "%s" + neutralColor(")"))
                            % (
                                neutralColor(", ".join(s["tags"]))
                                + neutralColor((", see also " if s["tags"] else "see also ") if s["see_also"] else "")
                                + neutralColor(", ").join(
                                    [
                                        " - ".join(
                                            [
                                                strongColor(k) if l == 0 else neutralColor(k) for l, k in enumerate(j.split(" "))
                                            ]
                                        ) for j in s["see_also"]
                                    ]
                                )
                                + (neutralColor(", " + ", ".join(s["info"])) if s["info"] else "")
                            )
                        ) if s["tags"] or s["see_also"] else ""
                    )
                    + (
                        (
                            "\n\t" + "\n\t".join(
                                [
                                    neutralColor(l["text"] + ": ") + linkColor(l["url"]) for l in s["links"]
                                ]
                            )
                        ) if s["links"] else ""
                    )
                    for i, s in enumerate(w["senses"])
                ]
            ) 
            + (
                (
                    neutralColor("\n\tother forms: ") + ", ".join(
                        [
                            " - ".join(
                                [
                                    strongColor(t) if i == 0 else neutralColor(t) for i, t in enumerate(jp.values())
                                ]
                            ) for jp in w["japanese"][1:]
                        ]
                    )
                ) if len(w["japanese"]) > 1 else ""
            )
            for w in r["data"][0:count]
        ]
    )
    + f"\n\nShowing {count}{'/' + str(len(r['data'])) if options.count else ''} result{'' if count == 1 else 's'} for \"{strongColor(searchTerm)}\". Link: {linkColor('https://jisho.org/search/' + quote(searchTerm))}"
)
