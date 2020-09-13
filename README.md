# Jisho-cli

A simple cli interface for the [Jisho](https://jisho.org) search api.

## Dependencies

- [requests](https://requests.readthedocs.io/en/master)
- [urllib3](https://pypi.org/project/urllib3)
- [ansicolors](https://pypi.org/project/ansicolors)

Using pip:

```
pip install requests urllib3 ansicolors
```

## Running

Make sure to have python and pip installed. Using pyinstaller is recommended - just add the executable to the PATH environment variable.

```
pip install pyinstaller
git clone https://www.github.com/Walavouchey/jisho-cli.git
cd jisho-cli
pyinstaller jisho-cli
```

The executable will be at `./dist/jisho/jisho.exe`. Searches are cached at `%APPDATA%/local/jisho-cli/` or `$HOME/.cache/jisho-cli/` to save on repeated api calls.

## Usage

```
Usage: jisho [options] <word or kanji>

Options:
-h, --help            show this help message and exit
-c COUNT, --count=COUNT
                      number of results to display
-n, --no-cache        don't use cache
```

Full search term specifications are documented at the [Jisho docs](https://jisho.org/docs). Note that the api may not support all features of the website.

Make sure your terminal can handle japanese characters. The colors are for readability, but they can be customised by changing the definitions at the top of the code. Refer to the [ansicolors documentation](https://pypi.org/project/ansicolors).

## Contributing

You're welcome.

## Licence

Jisho-cli is licensed under the [MIT licence](https://opensource.org/licenses/mit).
