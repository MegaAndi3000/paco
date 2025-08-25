# paco

**P**ython **A**uto **Co**py is a small python program, which can be used to automatically copy specific files and folders to a given directory (e.g. backups).

## Installation

1. Clone this repository or download the source code of a given [release](https://github.com/MegaAndi3000/paco/releases).
2. If you want an executable (and have `make` and `pyinstaller` installed): simply run `make` in the cloned repository.
3. Done!

## Usage

In order to start the copy process, you simply have to run the `main.py` file or a given executable with an appropriate configuration file.

### config.json

By default paco uses './config.json' as a configuration file. You can however specify another path via '-c'.

The config consists of 3 arguments:

| Argument | Description |
| --- | --- |
| destination_path | Path to directory, in which the destination folder will be created. |
| shortcuts | JSON-object, whose keys will be replaced in source_list origin paths by their respective value. |
| source_list      | JSON-object, where the key specifies the name of the destination subdirectory and the value is a list of source files/folders. If the key is "root", no subdirectory is created. |
| ignore_list      | List of file/folder names, which are to be ignored when copying. |


### Example

**file tree:**
```
input
├── A
│   ├── A1
│   │   ├── file
│   │   ├── file_2
│   │   └── file_3
│   ├── A2
│   │   ├── file
│   │   ├── file_2
│   │   └── file_3
│   ├── file_a
│   └── file_a_2
├── B
│   ├── file_b
│   └── file_b_2
└── C
    ├── file_c
    └── file_c_2
```

**config.json:**
```json
{
   "destination_path": "path/",
   "shortcuts": {"my_dir": "/path/to/input"},
   "source_list": {"root": ["my_dir/A/A1",
                            "my_dir/A/file_a",
                            "my_dir/A/file_a_2",
                            "my_dir/B"],
                   "C": ["path/input/C/file_c_2"]},
   "ignore_list": []
}
```

**output (with `-n output`):**
```
input
├── ...
output
├── A1
│   ├── file
│   ├── file_2
│   └── file_3
├── B
│   ├── file_b
│   └── file_b_2
├── C
│   └── file_c_2
├── file_a
└── file_a_2
```
