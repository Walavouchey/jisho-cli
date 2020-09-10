import requests as req
import sys
import os
import platform
import ctypes
from urllib.parse import quote
from functools import partial
from colors import color
import json

if not sys.stdout.isatty():
    def cancel(string, *args, **kwargs):
        return string
    color = cancel

else:
    if platform.system() == "Windows":
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        del kernel32

cacheFile = os.getenv("localappdata") + "\\jishocache"
r = ""
searchTerm = sys.argv[1]
if not os.path.exists(cacheFile):
    os.system(f"mkdir {cacheFile}")
try:
    with open(f"{cacheFile}\\{searchTerm}", "r", encoding="utf-8") as file:
        r = json.loads(file.read())
except Exception:
    r = req.get(f"https://jisho.org/api/v1/search/words?keyword={searchTerm}").json();
    with open(f"{cacheFile}\\{searchTerm}", "w", encoding="utf-8") as file:
        file.write(json.dumps(r));

print(
    "\n\n".join(
        [
            ", ".join(
                [
                    " - ".join(
                        [
                            color(t, fg="red") if i is 0 else color(t, fg=245) for i, t in enumerate(jp.values())
                        ]
                    ) for jp in w["japanese"]
                ]
            )
            + (", " + color("common", fg=130) if w["is_common"] else "") 
            + ((", " + ", ".join([color(t, fg=130) for t in w["jlpt"]])) if w["jlpt"] else "")
            + ((", " + ", ".join([color(t, fg=130) for t in w["tags"]])) if w["tags"] else "")
            + "\n\t" + "\n\t".join(
                [
                    color(f"{i + 1}. ", fg=245)
                    + (color("(%s) " % ", ".join(s["parts_of_speech"]), fg=245) if s["parts_of_speech"] else "")
                    + "; ".join(
                        s["english_definitions"]
                    )
                    + (
                        color(" (%s)" % (", ".join(s["tags"])
                        + ((", see also " if s["tags"] else "see also ") if s["see_also"] else "")
                        + ", ".join(s["see_also"])), fg=245) if s["tags"] or s["see_also"] else ""
                    )
                    + (("\n\n\t" + "\n\t".join(
                        [
                            color(l["text"] + ": ", fg=245) + color(l["url"], fg="cyan") for l in s["links"]
                        ]
                    )) if s["links"] else "")
                    for i, s in enumerate(w["senses"])
                ]
            ) 
            + ((color("\n\t other forms: ", fg=245) + ", ".join(
                [
                    " - ".join(
                        [
                            color(t, fg="red") if i is 0 else color(t, fg=245) for i, t in enumerate(jp.values())
                        ]
                    ) for jp in w["japanese"][1:]
                ]
            )) if len(w["japanese"]) > 1 else "")
            for w in r["data"]
        ]
    )
    + f"\n\nShowing results for \"{color(searchTerm, fg='red')}\". Link: {color('https://jisho.org/search/' + quote(searchTerm), fg='cyan')}"
)
