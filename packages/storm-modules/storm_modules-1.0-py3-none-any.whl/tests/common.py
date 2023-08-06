"""
Common functions used by tests.
"""
import os
import re
import shutil

from storm_modules import REPO_DIR

TEST_DATA_DIR = REPO_DIR / "test_data"
INPUT_TEST_DIR = TEST_DATA_DIR / "input"
OUTPUT_TEST_DIR = TEST_DATA_DIR / "output"
CONFIG_TEST_DIR = TEST_DATA_DIR / "config"
CACHE_TEST_DIR = INPUT_TEST_DIR / "mercure_cache"

TEST_YAML_LOCAL = "storm_test_local.yaml"
TEST_YAML_CI = "storm_test_ci.yaml"


def rmtree(dirpath):
    """
    Delete an entire directory tree.

    This is an attempt at a workaround for windows locking files/dirs.

    :param dirpath: Path to directory to delete.
    """
    success = False
    count = 0
    while not success:
        try:
            shutil.rmtree(dirpath)
            success = True
        except OSError:
            if count > 10:
                raise
            count += 1


def clean(dirpath: str):
    """
    Ensure the directory exists and is empty.

    :param dirpath: Directory to clean or create.
    """
    if os.path.exists(dirpath):
        try:
            rmtree(dirpath)
        except OSError:
            os.chdir("..")
            rmtree(dirpath)
    os.makedirs(dirpath)


def strip_args_of_output_test_dir(input_args: str) -> str:
    """
    If found, cut out OUTPUT_TEST_DIR from a string leaving only filenames instead full paths.

    :param input_args: string to find and cut out directory paths.
    """
    split_chars = r"[\\/]"
    return "_".join(
        [
            re.split(split_chars, arg)[-1] if any(char in arg for char in split_chars) else arg
            for arg in input_args
        ]
    )


def prepare_output_dir(test_name: str):
    """
    Create or (if exists) cleans output directory for a test.

    :param test_name: Name of the test.
    """
    clean(OUTPUT_TEST_DIR / test_name)
