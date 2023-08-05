[![PyPI](https://img.shields.io/pypi/v/horimotemce.svg)](https://pypi.python.org/pypi/horimotemce/)

# Horimote MCE

Listen for MCE remote button presses detected by [InputLIRC](https://packages.debian.org/buster/inputlirc) and send them to [horimote](https://github.com/benleb/horimote).

It is used to detect IR keypresses generated from a Windows MCE compatible remote (or a suitably configured Logitech Harmony Hub) and send them to a Samsung SMT-G7400/G7401 box, commonly branded as the Virgin Media/upc/Unitymedia Horizon box used by several European cable operators. This allows commands that cannot be sent via IR (eg. DVD and Guide buttons) to be emulated via the SMT-G7400/G7401 IP interface.

## Installation

This package should run on most Linux installations (including Raspbian/Rasperry Pi OS) and requires the following:

- an MCE IR receiver that is supported by inputlirc.
- `inputlirc` package installed and configured on the underlying operating system to read and process input from the MCE IR receiver

Install the module via PyPi:
```yaml
pip install horimotemce
```

Run the daemon using `horimotemce`.

## Options

| **Option** | **Default** | **Description**
| -- | -- | --
| <nobr>`-v` \| `--verbose`</nobr> | none | Set logging verbosity (repeat to increase)
| <nobr>`-V` \| `--version`</nobr> | | Show currently installed version

