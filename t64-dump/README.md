# t64-dump

t64-dump is a Python application used to extract files from T64 archives.

## Usage

```
usage: t64-dump [-h] (--list | --extract [EXTRACT [EXTRACT ...]]) [--dest DEST] [--version] input

Dump each file in a T64 archive to individual hex dumps.

positional arguments:
  input                 the T64 or zip source file containing the files to dump

optional arguments:
  -h, --help            show this help message and exit
  --list, -l            lists the files in the input
  --extract [EXTRACT [EXTRACT ...]], -x [EXTRACT [EXTRACT ...]]
                        extracts files from the input, provide a list of files to extract or leave empty for all
  --dest DEST, -d DEST  the destination directory of the dumped files
  --version             show program version number and exit
```

## Examples

List all files in the archive:
```bash
t64-dump archon.zip -l
```

Extract all files in the archive to the current directory:
```bash
t64-dump archon.zip -x
```

Extract only the archon file in the archive to a given directory:
```bash
t64-dump archon.zip -x archon -d ./output/
```

## References

See [VICE manual](https://vice-emu.sourceforge.io/vice_16.html) and [T64 Format spec](https://ist.uwaterloo.ca/~schepers/formats/T64.TXT)
for T64 file image format.
