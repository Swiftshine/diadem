# diadem
Fork of [codedx](https://github.com/RicBent/codedx).

## Special Thanks
- [codedx](https://github.com/RicBent/codedx)
- [LibHakkun](https://codeberg.org/fruityloops1/LibHakkun) (precompiled stdlib)

## Requirements
- CMake
- `clang` and `clang++`
- `llvm-objdump`
  - If LLVM is installed but the program is just called `objdump`, you may want to create an alias/symlink.
- `arm-none-eabi-ld`
  - Install `arm-none-eabi-binutils`.
- Python 3
  - `pyelftools`
  - `lz4`
  - `itanium-demangle`

## Building
Run `dxmake.py`
