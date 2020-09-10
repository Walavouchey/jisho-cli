# jisho-cli

A simple cli interface for the [jisho](https://jisho.org) search api.

## Dependencies

- requests
- ansicolors

Using pip:

```
pip install requests ansicolors
```

## Running

Make sure to have python 3 and pip installed. Using pyinstaller is recommended - just add the executable to the PATH environment variable.

```
pip install pyinstaller
git clone https://www.github.com/Walavouchey/jisho-cli.git
cd jisho-cli
pyinstaller jisho-cli
```

The executable will be at `dist/jisho/jisho.exe`.

## Usage

```
jisho <word or kanji>
```

Full search options are documented at the [jisho docs](https://jisho.org/docs). Note that the api may not support all features of the website.

Make sure your terminal can handle japanese characters.

## Licence

jisho-cli is licensed under the [MIT licence](https://opensource.org/licenses/mit).
