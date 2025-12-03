#!/usr/bin/env python3
"""
Main program for Assignment 5.

Queries tissue expression data for given gene and species 
from Unigene database.
"""
import os
import sys
import re
import argparse
from assignment5 import config
import io_utils


def update_host_name(host):
    """
    Converts common host names to scientific names and validates them.

    Args:
        host (str): Host name provided by user

    Returns:
        str: Scientific name of the host
    """
    host_lower = host.lower().strip()
    host_keywords = config.get_keywords_for_hosts()

    if host_lower in host_keywords:
        return host_keywords[host_lower]

    _print_directories_for_hosts()
    sys.exit(1)


def _print_directories_for_hosts():
    """
    Prints available host directories to stderr and exits program.
    """
    host_keywords = config.get_keywords_for_hosts()

    scientific_names = sorted(set(host_keywords.values()))
    common_names = sorted(set(host_keywords.keys()))

    error_msg = (
        "\nEither the Host Name you are searching for is not in the database\n"
        "or If you are trying to use the scientific name please put the name\n"
        "in double quotes:\n\n\"Scientific name\"\n"
    )
    print(error_msg, file=sys.stderr)

    print("Here is a (non-case sensitive) list of available "
          "Hosts by scientific name\n", file=sys.stderr)

    for i, name in enumerate(scientific_names, 1):
        print(f"{i}. {name}", file=sys.stderr)

    print("\nHere is a (non-case sensitive) list of available "
          "Hosts by common name\n", file=sys.stderr)

    for i, name in enumerate(common_names, 1):
        print(f"{i}. {name}", file=sys.stderr)


def get_data_for_gene_file(gene_file):
    """
    Extracts tissue expression data from gene file.

    Args:
        gene_file (str): Path to the gene file

    Returns:
        list: Sorted list of tissues where gene is expressed
    """
    tissues = []

    try:
        with io_utils.get_filehandle(gene_file, 'r') as fh:
            for line in fh:
                line = line.strip()
                match = re.search(r'EXPRESS\s+(.+)', line)
                if match:
                    tissue_string = match.group(1)
                    raw_tissues = tissue_string.split('|')
                    for tissue in raw_tissues:
                        tissue_clean = tissue.strip()
                        if tissue_clean:
                            tissue_capped = (tissue_clean[0].upper() +
                                           tissue_clean[1:].lower())
                            tissues.append(tissue_capped)
                    break

    except (OSError, IOError) as e:
        print(f"Error reading file {gene_file}: {e}", file=sys.stderr)
        sys.exit(1)

    return sorted(tissues)


def print_host_to_gene_name_output(host, gene, tissues):
    """
    Prints the tissue expression data in the required format.

    Args:
        host (str): Host name
        gene (str): Gene name
        tissues (list): List of tissues where gene is expressed
    """
    print(f"Found Gene {gene} for {host}")
    print(f"In {host}, There are {len(tissues)} tissues that "
          f"{gene} is expressed in:\n")

    for i, tissue in enumerate(tissues, 1):
        print(f"{i}. {tissue}")


def main():
    """Main function that orchestrates the program execution."""
    parser = argparse.ArgumentParser(description='Give the Host and Gene name')
    parser.add_argument('--host', default='Human', help='Name of Host')
    parser.add_argument('-g', '--gene', default='TGM1', help='Name of Gene')

    args = parser.parse_args()

    scientific_host = update_host_name(args.host)

    data_dir = config.get_directory_for_unigene()
    file_extension = config.get_extension_for_unigene()
    gene_file = os.path.join(data_dir, scientific_host,
                           f"{args.gene}.{file_extension}")

    if not io_utils.is_gene_file_valid(gene_file):
        error_msg = (f"Gene {args.gene} does not exist for "
                     f"{scientific_host}. exiting now...")
        print(error_msg, file=sys.stderr)
        sys.exit(1)

    print(f"\nFound Gene {args.gene} for {scientific_host}")

    tissues = get_data_for_gene_file(gene_file)

    print_host_to_gene_name_output(scientific_host, args.gene, tissues)


if __name__ == '__main__':
    main()
