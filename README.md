# jisho-cli

A simple cli interface for the [jisho](https://jisho.org) search api.

## Dependencies

- [requests](https://requests.readthedocs.io/en/master)
- [urllib3](https://pypi.org/project/urllib3)
- [ansicolors](https://pypi.org/project/ansicolors)

Using pip:

```
pip install requests urllib3 ansicolors
```

## Running

Make sure to have python and pip installed. Using pyinstaller is recommended for Windows users - just add the executable to the PATH environment variable.

```
pip install pyinstaller
git clone https://www.github.com/Walavouchey/jisho-cli.git
cd jisho-cli
pyinstaller jisho-cli
```

The executable will be at `dist/jisho/jisho.exe`. Searches are cached at `%APPDATA%/local/jishocache/` to save on repeated api calls.

## Usage

```
jisho <word or kanji>
```

Full search options are documented at the [jisho docs](https://jisho.org/docs). Note that the api may not support all features of the website.

Make sure your terminal can handle japanese characters. The colors are for readability, but they can be customised by changing the definitions at the top of the code. Refer to the [ansicolors documentation](https://pypi.org/project/ansicolors).

## Contributing

You're welcome.

## Licence

jisho-cli is licensed under the [MIT licence](https://opensource.org/licenses/mit).
