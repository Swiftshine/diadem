#!/usr/bin/env python3

import os
import sys
import tarfile
import urllib.request

MUSL_VERSION = "musl-1.2.5"
LLVM_VERSION = "19.1.7"
CLANG_VERSION = "19.1.7"

ARCH = "arm"
PLATFORM = "NX"

ARCHIVE = (
    f"stdlib_{MUSL_VERSION}_"
    f"llvm-{LLVM_VERSION}_"
    f"clang-{CLANG_VERSION}_"
    f"{ARCH}_{PLATFORM}.tar.xz"
)

URL = (
    f"https://codeberg.org/fruityloops1/LibHakkun/"
    f"releases/download/stdlib-{LLVM_VERSION}/{ARCHIVE}"
)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STD_DIR = os.path.join(ROOT_DIR, "lib", "std")
ARCHIVE_PATH = os.path.join(ROOT_DIR, ARCHIVE)


def download():
    print(f"Downloading standard library:\n{URL}")

    urllib.request.urlretrieve(URL, ARCHIVE_PATH)

    print("Download complete.")


def extract():
    print("Extracting standard library...")

    os.makedirs(STD_DIR, exist_ok=True)

    with tarfile.open(ARCHIVE_PATH, "r:xz") as archive:
        archive.extractall(ROOT_DIR, filter="data")

    print("Extraction complete.")


def cleanup():
    if os.path.exists(ARCHIVE_PATH):
        os.remove(ARCHIVE_PATH)


def is_installed():
    required = [
        "libc.a",
        "libc++.a",
        "libc++abi.a",
        "libm.a",
        "libunwind.a",
        "libclang_rt.builtins-arm.a",
        "llvm-project/build/include/c++/v1",
        "musl/include",
    ]

    return all(
        os.path.exists(os.path.join(STD_DIR, item))
        for item in required
    )


def main():
    if is_installed():
        return

    try:
        download()
        extract()

        if not is_installed():
            raise RuntimeError(
                "Standard library installation is incomplete. "
                "Check the archive contents."
            )

        print("Standard library installed successfully!")

    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    finally:
        cleanup()


if __name__ == "__main__":
    main()
