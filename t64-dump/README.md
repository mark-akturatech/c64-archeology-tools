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
python t64-dump archon.zip -l

t64-dump
========

Tape description:
C64S tape file
Demo tape......

User description:
DEMO TAPE               

Number of directory entries: 1

Filename                File Type       Start Addr      End Addr
MANUAL                  PRG             $0801           $212c
ARCHON                  PRG             $0801           $9f0a
(end)
```

Extract all files from the archive to the current directory:
```bash
python t64-dump archon.zip -x

t64-dump
========

Extracting file MANUAL to ./manual.prg(0801-212c)
Extracting file ARCHON to ./archon.prg(0801-9f0a)
(end)
```

Extract only the archon file in the archive to a given directory:
```bash
python t64-dump archon.zip -x archon -d ./output/

t64-dump
========

Skipping file MANUAL
Extracting file ARCHON to ./output/archon.prg(0801-9f0a)
(end)

```

## References

See [VICE manual](https://vice-emu.sourceforge.io/vice_16.html) and [T64 Format spec](https://ist.uwaterloo.ca/~schepers/formats/T64.TXT)
for T64 file image format.
