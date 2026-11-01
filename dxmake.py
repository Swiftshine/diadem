#!/usr/bin/env python3

import sys
import os
import shutil
import platform
import subprocess

main_addr       = 0x00004000
main_size       = 0x00CD1000
subsdk_addr     = main_addr + main_size
main_build_id   = 'AEE6DCCC06D9C05B42061E2019123A61'
out_dir         = 'out'
out_nso         = os.path.join(out_dir, 'subsdk0')
out_ips         = os.path.join(out_dir, main_build_id + '.ips')

def fatal(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

def run_proc(cmd):
    return subprocess.call(cmd, shell=True)

def command_available(cmd):
    return shutil.which(cmd) is not None

targets = {
    'syms':     ['syms'],
    'make':     ['syms', 'make'],
    'nso':      ['syms', 'make', 'nso'],
    'ips':      ['syms', 'make', 'ips'],
    'all':      ['syms', 'make', 'nso', 'ips'],
    'ftp':      ['syms', 'make', 'nso', 'ips', 'ftp'],
    'srv':      ['syms', 'make', 'nso', 'ips', 'ftp', 'srv'],
    'ftp-only': ['ftp'],
    'srv-only': ['srv'],
    'clean':    ['clean']
}

default_target = 'all'

def main(argc, argv):
    if sys.version_info.major < 3:
        fatal("Python 3 or newer is required!")

    required_commands = ['cmake', 'clang', 'clang++', 'llvm-objdump', 'arm-none-eabi-ld']

    for cmd in required_commands:
        if not command_available(cmd):
            fatal('Required command \"%s\" is not available!' % cmd)

    if argc > 2:
        fatal('Usage: %s [target]' % argv[0])

    target_name = default_target if argc == 1 else argv[1]

    try:
        commands = targets[target_name]
    except KeyError:
        fatal('Invalid target \"%s\"' % target_name)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    
    # Remove all build files
    if 'clean' in commands:
        if os.path.exists('build'):
            shutil.rmtree('build')
        
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)

        for p in ['linker/main.ld', 'compile_commands.json']:
            try:
                os.remove(p)
            except:
                pass
        print('Clean.')
    
    # Relocate main symbols to to subsdk0
    if 'syms' in commands:
        rc = run_proc(f"{sys.executable} tools/symbol_relocate.py main.sym {hex(main_addr)} {hex(main_addr+main_size)} linker/main.ld")
        if rc != 0:
            fatal('Relocating main symbols failed!')

    # Compile and link code to ELF
    if 'make' in commands:
        if not os.path.exists('build'):
            rc = run_proc('cmake -B build')
            if rc != 0:
                fatal('Configuring cmake failed!')

        rc = run_proc('cmake --build build')
        if rc != 0:
            fatal('Building with cmake failed!')

        if os.path.exists('build/subsdk0.sym'):
            shutil.copy('build/subsdk0.sym', os.path.join(out_dir, 'subsdk0.sym'))
        if os.path.exists('build/subsdk0.elf'):
            shutil.copy('build/subsdk0.elf', os.path.join(out_dir, 'subsdk0.elf'))

    # Create NSO from ELF
    if 'nso' in commands:
        rc = run_proc(f"{sys.executable} tools/elf2nso.py {out_nso}.elf {out_nso} -s -c")
        if rc != 0:
            fatal('Creating NSO failed!')

    # Create IPS from hooks
    if 'ips' in commands:
        rc = run_proc(f"{sys.executable} tools/hooks_to_ips.py hooks {out_nso}.sym {hex(subsdk_addr - main_addr)} {out_ips}")
        if rc != 0:
            fatal('Creating IPS failed!')
    
    # Upload NSO and IPS to switch
    if 'ftp' in commands:
        rc = run_proc(f"{sys.executable} tools/ftp_up.py ftp.cfg {out_nso} {out_ips}")
        if rc != 0:
            sys.exit(1)
    
    # Run log server
    if 'srv' in commands:
        try:
            run_proc(f"{sys.executable} tools/log_server.py -s")
        except KeyboardInterrupt:
            pass

    sys.exit(0)

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
