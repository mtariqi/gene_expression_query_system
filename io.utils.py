#!/usr/bin/env python3

"""
Input/output utilities for Assignment 5.

This module provides helper functions for safely opening files and
validating the existence of Unigene gene files.
"""

import os
from typing import TextIO


def get_filehandle(file_name: str, mode: str = "r",
                   encoding: str = "utf-8") -> TextIO:
    """
    Open a file and return a file handle.

    Parameters:
        file_name (str): Path to the file to open.
        mode (str): File open mode, e.g. 'r' for reading. Defaults to 'r'.
        encoding (str): Text encoding to use when opening in text mode.
            Defaults to 'utf-8'.

    Returns:
        TextIO: An open file handle.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If the file cannot be opened for any other reason.
    """
    if not os.path.exists(file_name):
        raise FileNotFoundError(
            f"Could not open the file: {file_name} for reading"
        )

    try:
        return open(file_name, mode, encoding=encoding)
    except OSError as exc:
        raise IOError(
            f"Could not open the file: {file_name} for mode: {mode}. "
            "Please check file path and permissions."
        ) from exc


def is_gene_file_valid(file_name: str) -> bool:
    """
    Check if a given gene file exists on disk.

    Parameters:
        file_name (str): Full path to the gene file to test.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_name)

