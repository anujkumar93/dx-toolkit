#!/usr/bin/env python

import dxpy
import argparse
import sys

parser = argparse.ArgumentParser(description="Export Mappings gtable to a FASTQ/FASTA file")
parser.add_argument("mappings_id", help="Mappings table id to read from")
parser.add_argument("--output", dest="file_name", default=None, help="Name of file to write FASTQ to.  If not given data will be printed to stdout.")


def writeFastq( row, fh ):
    if 'name' in row:
        fh.write("".join(["@", row['name'], "\n"]))
    else:
        fh.write("@\n")

    fh.write(row['sequence']+"\n")
    fh.write("+\n")
    fh.write(row['quality']+"\n")

def writeFasta( row, fh ):
    if 'name' in row:
        fh.write("".join([">", row['name'],"\n"]))
    else:
        fh.write(">\n")
    
    fh.write(row['sequence']+"\n")


def main(**kwargs):
    if len(kwargs) == 0:
        opts = parser.parse_args(sys.argv[1:])
    else:
        opts = parser.parse_args(kwargs)

    if opts.mappings_id == None:
        parser.print_help()
        sys.exit(1)
    
    mappingsTable = dxpy.DXGTable(opts.mappings_id)

    if opts.file_name != None:
        fh = open(opts.file_name, "w")
    else:
        fh = sys.stdout

    if 'quality' in mappingsTable.get_col_names():
        outputFastq = True
    else:
        outputFastq = False

    for row in mappingsTable.iterate_rows(want_dict=True):
        if outputFastq:
            writeFastq( row, fh )
        else:
            writeFasta( row, fh )

    
