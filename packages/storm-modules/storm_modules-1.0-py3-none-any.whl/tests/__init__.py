import os

from tests.common import clean, OUTPUT_TEST_DIR

if os.getenv("RUN_ENV") == "CI":
    clean(OUTPUT_TEST_DIR)
