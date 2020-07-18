# lnk_parser

A basic _Shell Link (.LNK) Binary File_ parser.

_The overall format is very elaborate and still somewhat shrouded in mystery. Only the structures I have needed are supported. Very much a hobby project._

## Usage

```
$ ./lnk_parser.py --help
usage: lnk_parser.py [-h] lnk_files [lnk_files ...]

positional arguments:
  lnk_files

optional arguments:
  -h, --help  show this help message and exit
```


### Example

```
$ ./lnk.parser.py 2017_ham_11.lnk
```

**Output:**
```
Link target: C:\Windows\system32\cmd.exe
Arguments: /c start wscript /e:VBScript.Encode Manuel.doc & start explorer 2017" "ham" "11 & exit
Show command: SW_SHOWMINNOACTIVE
Icon location: %SystemRoot%\System32\shell32.dll
```

:thumbsup:

## Implementation references

- [[MS-SHLLINK]: Shell Link (.LNK) Binary File Format | Microsoft Docs](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/16cb4ca1-9339-4d0c-a68d-bf1d6cc0f943)
- [libfwsi/Windows Shell Item format.asciidoc at master · libyal/libfwsi](https://github.com/libyal/libfwsi/blob/master/documentation/Windows%20Shell%20Item%20format.asciidoc)
