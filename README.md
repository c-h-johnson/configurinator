# Configurinator

Makes it easy to reproduce configurations on different operating systems.

# About

Sets sensible settings than the defaults with an emphasis on speed, usability,
aesthetics, and reducing wear on the SSD. Installed programs are automatically
detected and configured by running `all.sh`. Any type of config file can be
modified with easy to use API. An advantage of managing the configs this way is
that only the modifications are stored and can be applied to any file no matter
what it already contains.

# Compatibility

## Operating system

Arch and Debian have first class support.
Alpine, Gentoo, NixOS, OpenSUSE, Red Hat, MacOS, Windows, and derivatives should
be usable also.

## Supported program configs

all configurations are listed in
[./configurinator/config/](configurinator/config/)

# Requirements

- python >= 3.10

# Usage

To configure everything automatically run `sh all.sh` .

To reuse a configuration on a different machine, copy over
`~/.config/configurinator/persist.json` then run it.