# lnk_parser

A basic _Shell Link (.LNK) Binary File_ parser.

_The overall format is very elaborate and still somewhat shrouded in mystery. Only the structures I have needed are supported. Very much a hobby project._

## Usage

```
$ ./lnk_parser.py --help
usage: lnk_parser.py [-h] lnk_file [lnk_file ...]

positional arguments:
  lnk_file

optional arguments:
  -h, --help  show this help message and exit
```


### Example

```
$ ./lnk_parser.py ~/code/py/lnk_parser/lnk_files/2017_ham_11.lnk
```

**Output:**
```
/home/vph/code/py/lnk_parser/lnk_files/2017_ham_11.lnk
======================================================
General
-------
            Link target: C:\Windows\system32\cmd.exe
              Arguments: /c start wscript /e:VBScript.Encode Manuel.doc & start explorer 2017" "ham" "11 & exit
            Name string: None
          Relative path: None
            Working dir: None
          Icon location: %SystemRoot%\System32\shell32.dll
Header
------
             Link flags: <LinkFlags.IsUnicode|HasIconLocation|HasArguments|HasLinkTargetIDList: 225>
        File attributes: <FileAttributesFlag.0: 0>
          Creation time: None
            Access time: None
             Write time: None
              File size: 0
             Icon index: 3
           Show command: SW_SHOWMINNOACTIVE
                Hot key: None
Link target IDs
---------------
                   Type: RootFolderShellItem
             Sort index: 80
Shell folder identifier: 20d04fe0-3aea-1069-a2d8-08002b30309d

                   Type: VolumeShellItem
                   Name: C:\
                  Flags: <VolumeShellItemFlags.UNKNOWN_2|UNKNOWN_1|HAS_NAME: 7>

                   Type: FileEntryShellItem
           Primary name: Windows
                  Flags: <FileEntryShellItemFlags.IS_DIRECTORY: 1>
              File size: None
        File attributes: <FileAttributesFlag.FILE_ATTRIBUTE_DIRECTORY: 16>
          Last modified: None

                   Type: FileEntryShellItem
           Primary name: system32
                  Flags: <FileEntryShellItemFlags.IS_DIRECTORY: 1>
              File size: None
        File attributes: <FileAttributesFlag.FILE_ATTRIBUTE_DIRECTORY: 16>
          Last modified: None

                   Type: FileEntryShellItem
           Primary name: cmd.exe
                  Flags: <FileEntryShellItemFlags.IS_FILE: 2>
              File size: None
        File attributes: <FileAttributesFlag.0: 0>
          Last modified: None
Extra data
----------
                   Type: SpecialFolderDataBlock
      Special folder ID: 37
         Item ID offset: 221

                   Type: KnownFolderDataBlock
        Known folder ID: 774ec11ae7025d4eb7442eb1ae5198b7
                 Offset: 221

                   Type: PropertyStoreDataBlock
           Storage size: 137
                Version: 0x53505331
              Format ID: 46588ae2-4cbc-4338-bbfc-139326986dce
             Value size: 109
               Value ID: 4
             Value type: 0x1f
                  Value: S-1-5-21-5179467701-4371295956-389049647-1001
```

:thumbsup:

## Implementation references

- [[MS-SHLLINK]: Shell Link (.LNK) Binary File Format | Microsoft Docs](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/16cb4ca1-9339-4d0c-a68d-bf1d6cc0f943)
- [libfwsi/Windows Shell Item format.asciidoc at master · libyal/libfwsi](https://github.com/libyal/libfwsi/blob/master/documentation/Windows%20Shell%20Item%20format.asciidoc)
