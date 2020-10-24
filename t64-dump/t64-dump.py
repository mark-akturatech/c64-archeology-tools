# t64-dump.py
# by Mark Beljaars

# importing required modules
from zipfile import ZipFile
import argparse
import os
import sys

# global constants
VERSION = '0.1'

# tape archive image format constants
TAPE_RECORD_DESCRIPTION_START = 0
TAPE_RECORD_DESCRIPTION_LENGTH = 32
TAPE_RECORD_USER_DESCRIPTION_START = 40
TAPE_RECORD_USER_DESCRIPTION_LENGTH = 24
TAPE_RECORD_DIRECTORY_ENTRIES_START = 36
FILE_RECORD_START = 64
FILE_RECORD_LENGTH = 32
FILE_RECORD_OFFSET_ENTRY_TYPE = 0
FILE_RECORD_OFFSET_FILE_TYPE = 1
FILE_RECORD_OFFSET_START_ADDR = 2
FILE_RECORD_OFFSET_END_ADDR = 4
FILE_RECORD_OFFSET_CONTENT_START = 8
FILE_RECORD_OFFSET_FILE_NAME_START = 16
FILE_RECORD_OFFSET_FILE_NAME_LENGTH = 16

# c64 file types
FILE_TYPES = {
    0x80: "DEL",
    0x81: "SEQ",
    0x82: "PRG",
    0x83: "USR",
    0x84: "REL",
}


def main():
    # application arguments
    parser = argparse.ArgumentParser(
        prog='t64-dump',
        description='Dump each file in a T64 archive to individual hex dumps.')
    parser.add_argument(
        'input', help='the T64 or zip source file containing the files to dump')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', '-l', default=False,
                       action='store_true', help='lists the files in the input')
    group.add_argument('--extract', '-x', nargs='*',
                       help='extracts files from the input, provide a list of files to extract or leave empty for all')
    parser.add_argument(
        '--dest', '-d', default='./', help='the destination directory of the dumped files')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(VERSION))
    args = parser.parse_args()

    # header
    print("t64-dump")
    print("========\n")

    # load file in to memory
    try:
        if args.input.endswith('.zip'):
            with ZipFile(args.input, 'r') as zip_archive:
                for item in zip_archive.filelist:
                    data = zip_archive.read(item.filename)
                    process_data(data, args)
        else:
            with open(args.input, 'rb') as reader:
                data = reader.read()
                process_data(data, args)
    except(FileNotFoundError):
        print("File not found error")

    # footer
    print("(end)")


def process_data(data, args):
    # read archive header information
    desc = data[TAPE_RECORD_DESCRIPTION_START:TAPE_RECORD_DESCRIPTION_START +
                TAPE_RECORD_DESCRIPTION_LENGTH].decode()
    user_desc = data[TAPE_RECORD_USER_DESCRIPTION_START:TAPE_RECORD_USER_DESCRIPTION_START +
                     TAPE_RECORD_USER_DESCRIPTION_LENGTH].decode()
    entries = data[TAPE_RECORD_DIRECTORY_ENTRIES_START +
                   1] << 8 | data[TAPE_RECORD_DIRECTORY_ENTRIES_START]

    if (args.list):
        print("Tape description:\n{}".format(desc))
        print("\nUser description:\n{}".format(user_desc))
        print("\nNumber of directory entries: {}".format(entries))
        if (entries > 0):
            print("\nFilename\t\tFile Type\tStart Addr\tEnd Addr")

    # loop through each file in the directory
    recordOffset = FILE_RECORD_START
    for rec in range(entries):
        # read record information
        entry_type = data[recordOffset + FILE_RECORD_OFFSET_ENTRY_TYPE]
        file_type_id = data[recordOffset + FILE_RECORD_OFFSET_FILE_TYPE]
        file_type = FILE_TYPES[file_type_id] if file_type_id in FILE_TYPES else "UNK"
        start_addr_lo = data[recordOffset + FILE_RECORD_OFFSET_START_ADDR]
        start_addr_hi = data[recordOffset + FILE_RECORD_OFFSET_START_ADDR + 1]
        start_addr = start_addr_hi << 8 | start_addr_lo
        end_addr = data[recordOffset + FILE_RECORD_OFFSET_END_ADDR +
                        1] << 8 | data[recordOffset + FILE_RECORD_OFFSET_END_ADDR]
        content_start = data[recordOffset + FILE_RECORD_OFFSET_CONTENT_START +
                             3] << 24 | data[recordOffset + FILE_RECORD_OFFSET_CONTENT_START +
                                             2] << 16 | data[recordOffset + FILE_RECORD_OFFSET_CONTENT_START +
                                                             1] << 8 | data[recordOffset + FILE_RECORD_OFFSET_CONTENT_START]
        content_end = content_start + (end_addr - start_addr)
        file_name = data[recordOffset + FILE_RECORD_OFFSET_FILE_NAME_START:recordOffset + FILE_RECORD_OFFSET_FILE_NAME_START +
                         FILE_RECORD_OFFSET_FILE_NAME_LENGTH].decode()

        if (args.list):
            print("{}\t{}\t\t${}\t\t${}".format(
                file_name, file_type, format(start_addr, '04x'), format(end_addr, '04x')))
        elif(args.extract and not file_name.strip().lower() in args.extract):
            print("Skipping file {}".format(file_name.strip()))
        else:
            dest_dir = ("{}" if args.dest.endswith(
                "/") else "{}/").format(args.dest)
            output_file_name = "{}{}({}-{}).{}".format(dest_dir,
                                                       file_name.strip().lower(), format(start_addr, '04x'), format(end_addr, '04x'), file_type.lower())
            print("Extracting file {} to {}".format(
                file_name.strip(), output_file_name))

            
            content = bytes([start_addr_lo, start_addr_hi]) + data[content_start:content_end]

            # save the file
            try:
                if not os.path.isdir(dest_dir):
                    os.makedirs(dest_dir)
                try:
                    with open(output_file_name, "wb") as output:
                        output.write(content)
                except:
                    print("** Error saving file:", sys.exc_info()[0])
            except:
                print("** Could not create destination directory:",
                      sys.exc_info()[0])

        recordOffset += FILE_RECORD_LENGTH


# bootstrap
if __name__ == "__main__":
    main()
