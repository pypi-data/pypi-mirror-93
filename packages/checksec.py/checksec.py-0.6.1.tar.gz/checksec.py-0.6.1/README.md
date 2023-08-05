<h1 align="center">
  <br>checksec.py</br>
</h1>

<h3 align="center">
Checksec tool in Python, Rich output, based on LIEF
</h3>

<p align="center">
  <strong>
  <a href="https://asciinema.org/a/363216">
    Demo
  </a>
  </strong>
</p>

<p align="center">
  <a href="https://github.com/Wenzel/checksec.py/actions?query=workflow%3ACI">
    <img src="https://github.com/Wenzel/checksec.py/workflows/CI/badge.svg" alt="CI badge"/>
  </a>
  <a href="https://pypi.org/project/checksec.py/">
    <img src="https://img.shields.io/pypi/v/checksec.py?color=blue" alt="PyPI package badge"/>
  </a>
  <a href="https://pypi.org/project/checksec.py/">
    <img src="https://img.shields.io/pypi/pyversions/checksec.py" alt="Python version badge"/>
  </a>
  <a href="https://gitter.im/checksec-py/community?utm_source=share-link&utm_medium=link&utm_campaign=share-link">
    <img src="https://badges.gitter.im/checksec-py/community.svg" />
  </a>
</p>
<p align="center">
  <a href="https://pepy.tech/project/checksec.py">
    <img src="https://pepy.tech/badge/checksec-py" />  
  </a>
  <a href="https://pepy.tech/project/checksec.py">
    <img src="https://img.shields.io/pypi/dm/checksec.py?color=blue&label=downloads&style=flat-square" />
  </a>
</p>

<p align="center">
  <a href="https://asciinema.org/a/363216">
    <img src="https://user-images.githubusercontent.com/964610/94983280-9d007c80-0541-11eb-8462-3da5b7bce35b.png" />
  </a>
</p>

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Setup](#setup)
    - [Windows](#windows)
    - [Linux](#linux)
- [Usage](#usage)
- [FAQ](#faq)
- [References](#references)
- [License](#license)
- [Contributors](#contributors)

## Overview

A simple tool to verify the security properties of your binaries.

These properties can be enabled by your compiler to enforce the security of your executables, and mitigate exploits.
However it can be challenging to apply them on a whole system.

Check the level of security your Linux distro / Windows release is providing you !

Supported formats:

- [x] `ELF`
- [x] `PE`
- [ ] `Mach-O`

Based on:
- [Rich](https://github.com/willmcgugan/rich): Beautiful terminal output formatting
- [LIEF](https://github.com/lief-project/LIEF): Cross-platform library to parse, modify and abstract ELF, PE and Mach-O formats

## Requirements

![](https://img.shields.io/pypi/pyversions/checksec.py)

## Setup

### Windows

You find the `checksec.exe` on the latest Github releases:

<a href="https://github.com/Wenzel/checksec.py/releases/latest">
  <img src="https://img.shields.io/badge/Windows%20release-download-blue?style=for-the-badge"/>
</a>

### Linux

<a href="https://pypi.org/project/checksec.py/">
  <img src="https://img.shields.io/pypi/v/checksec.py?color=blue&label=PyPI%20package&style=for-the-badge" />
</a>

~~~
python3 -m venv venv
source venv/bin/activate
(venv) pip install checksec.py
~~~

## Usage

~~~
(venv) checkec <file_or_directory>...
~~~

Check `--help` for more options (_JSON output_, _recursive walk_, _workers count_)

## FAQ

1️⃣ What's the difference between [`checksec.py`](https://github.com/Wenzel/checksec.py) and [`checksec.sh`](https://github.com/slimm609/checksec.sh) ?

|                            | checksec.py | checksec.sh |
|----------------------------|:-----------:|:-----------:|
| Cross-Platform support      |     ✔       |     ❌      |
| Distributed workload        |     ✔       |     ❌      |
| Scan file                  |      ✔      |      ✔      |
| Scan directory             |      ✔      |      ✔      |
| Scan directory recursively |      ✔      |      ❌     |
| Specify libc path          |      ✔      |      ❌     |
| Scan process               |      ❌     |     ✔       |
| Scan process libs          |      ❌     |     ✔       |
| Scan kernel config         |      ❌     |     ✔       |
| Output Cli                 |      ✔      |      ✔      |
| Output JSON                |      ✔      |      ✔      |
| Output CSV                 |      ❌     |     ✔       |
| Output XML                 |      ❌     |     ✔       |
| ELF: Relro                 |     ✔       |     ✔       |
| ELF: Canary                |      ✔      |      ✔      |
| ELF: NX                    |      ✔      |      ✔      |
| ELF: PIE                   |      ✔      |      ✔      |
| ELF: RPATH                 |      ✔      |      ✔      |
| ELF: RUNPATH               |      ✔      |      ✔      |
| ELF: Symbols               |      ✔      |      ✔      |
| ELF: Fortify               |      ✔      |      ✔      |
| ELF: Fortified             |      ✔      |      ✔      |
| ELF: Fortifable            |      ✔      |      ✔      |
| ELF: Fortify Score         |      ✔      |      ❌       |


2️⃣ What's the difference between [`checksec.py`](https://github.com/Wenzel/checksec.py) and [`winchecksec`](https://github.com/trailofbits/winchecksec) ?

|                             | checksec.py | winchecksec |
|-----------------------------|:-----------:|:-----------:|
| Cross-Platform support      |     ✔       |     ✔      |
| Distributed workload        |     ✔       |     ❌       |
| Scan file                   |     ✔       |     ✔       |
| Scan directory              |     ✔       |     ❌      |
| Scan directory recursively  |     ✔       |     ❌      |
| Output CLI                  |     ✔       |    ✔        |
| Output JSON                 |     ✔       |    ✔        |
| PE: ASLR - DYNAMIC_BASE     |     ✔       |    ✔        |
| PE: ASLR - HIGHENTROPYVA    |     ✔       |    ✔        |
| PE: INTEGRITYCHECK          |     ✔       |    ✔        |
| PE: Authenticode signed     |     ✔       |    ✔        |
| PE: DEP                     |     ✔       |   ✔         |
| PE: Manifest Isolation      |     ✔       |    ✔        |
| PE: SEH                     |     ✔       |    ✔        |
| PE: SafeSEH                 |     ✔       |    ✔        |
| PE: Control Flow Guard      |     ✔       |    ✔        |
| PE: Return Flow Guard       |     ❌      |      ✔      |
| PE: Stack Cookie            |     ✔       |      ✔      |

3️⃣ `checksec` is slow on some huge binaries ! What's happening ?!

`checksec.py` relies on the [`LIEF`](https://github.com/lief-project/LIEF) library to parse `PE/ELF/MachO` formats.

➡️The library doesn't offer at this point _on-demand_ parsing, so it will parse and fetch unnecessary data.

➡️Retrieving symbols can be slow (ex: `pandoc`, `118M`, `+300 000` symbols, `+2m 20sec`). See this [issue](https://github.com/Wenzel/checksec.py/issues/52)

4️⃣ I sent a `CTRL-C` to cancel `checksec.py` processing, the app doesn't want to quit

`checksec.py` is working with multiple process workers to parallelize its execution and binary processing.
When a `CRTL-C` is received, `checksec.py` will [wait](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor.shutdown) for them to stop.

Sometimes, this is not working, and I don't know why at this point.
You can kill the remaining Python workers afterwards.

## References

- [@apogiatzis](https://github.com/apogiatzis) [Gist checksec.py](https://gist.github.com/apogiatzis/fb617cd118a9882749b5cb167dae0c5d)
- [checksec.sh](https://github.com/slimm609/checksec.sh)
- [winchecksec](https://github.com/trailofbits/winchecksec)

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Contributors

[![](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/images/0)](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/links/0)[![](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/images/1)](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/links/1)[![](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/images/2)](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/links/2)[![](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/images/3)](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/links/3)[![](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/images/4)](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/links/4)[![](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/images/5)](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/links/5)[![](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/images/6)](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/links/6)[![](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/images/7)](https://sourcerer.io/fame/Wenzel/Wenzel/checksec.py/links/7)
