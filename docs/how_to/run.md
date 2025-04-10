# How to Run

<!-- toc -->
## Contents

  * [Mac and Linux](#mac-and-linux)
  * [Windows](#windows)
    * [Get Python](#get-python)
    * [Running](#running)<!-- endToc -->

## Mac and Linux

Mac and Linux typically have Python 3 installed on the path as `python3`,
so you can just double-click the file or run it from the command line with.
Any one of the following will work:

```commandline
./.approval_tests_temp/approve_all.py
```

```commandline
python3 .approval_tests_temp/approve_all.py
```

**Note**: the script works regardless of the current working directory

## Windows

### Get Python

Check if Python is installed:

```commandline
python --version
```

If not, install from one of:

- Chocolatey: `choco install python`
- WinGet: `winget install -e --id Python.Python.3.12`
- Python: [Website](https://www.python.org/downloads/)

### Running

```commandline
python .approval_tests_temp/approve_all.py
```

