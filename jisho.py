import requests as req
import sys
import os
import platform
import ctypes
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

searchTerm = sys.argv[1]
cacheFolder = os.getenv("localappdata") + "\\jishocache"
r = ""
if not os.path.exists(cacheFolder):
    try:
        os.system(f"mkdir e{cacheFolder}")
    except Exception:
        pass
try:
    with open(f"{cacheFolder}\\{searchTerm}", "r", encoding="utf-8") as file:
        r = json.loads(file.read())
except Exception:
    r = req.get(f"https://jisho.org/api/v1/search/words?keyword={searchTerm}").json();
    try:
        with open(f"{cacheFolder}\\{searchTerm}", "w", encoding="utf-8") as file:
            file.write(json.dumps(r));
    except Exception:
        pass

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
                        neutralColor(" (%s)" % (", ".join(s["tags"])
                        + ((", see also " if s["tags"] else "see also ") if s["see_also"] else "")
                        + ", ".join(s["see_also"]))) if s["tags"] or s["see_also"] else ""
                    )
                    + (("\n\t" + "\n\t".join(
                        [
                            neutralColor(l["text"] + ": ") + linkColor(l["url"]) for l in s["links"]
                        ]
                    )) if s["links"] else "")
                    for i, s in enumerate(w["senses"])
                ]
            ) 
            + ((neutralColor("\n\t other forms: ") + ", ".join(
                [
                    " - ".join(
                        [
                            strongColor(t) if i == 0 else neutralColor(t) for i, t in enumerate(jp.values())
                        ]
                    ) for jp in w["japanese"][1:]
                ]
            )) if len(w["japanese"]) > 1 else "")
            for w in r["data"]
        ]
    )
    + f"\n\nShowing results for \"{strongColor(searchTerm)}\". Link: {linkColor('https://jisho.org/search/' + quote(searchTerm))}"
)
