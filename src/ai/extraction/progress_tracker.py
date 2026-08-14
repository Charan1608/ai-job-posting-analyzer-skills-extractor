"""
=========================================================
PROGRESS TRACKER
=========================================================
"""

import time

START = time.time()


def show_progress(current, total):

    elapsed = time.time() - START

    percent = current / total * 100

    print(
        f"[{current}/{total}] "
        f"{percent:.1f}% "
        f"Elapsed: {elapsed:.1f}s"
    )