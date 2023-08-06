```
INSTALLATION

    $ pip3 install wmtile

HELP

    $ wmtile -h

USAGE

    $ wmtile [-h] [-H] [-V] [-i] [-k] [-m] [-t] [-p] [-l] [-s] [-b] [-c]


window tiler for XFCE desktop environment

Always give to wmtile one and only one argument.

wmtile reshapes in 7 different ways all windows in the current workspace.

wmtile is a CLI program, but you should use it either by mouse (via wmtile -i)...

    $ wmtile -i
    installing 7 wmtile panel launchers
        panel launcher --> wmtile -m # Minimize
        panel launcher --> wmtile -t # reshape as Tiles
        panel launcher --> wmtile -p # reshape as Portraits
        panel launcher --> wmtile -l # reshape as Landscapes
        panel launcher --> wmtile -s # reshape as a Stack
        panel launcher --> wmtile -b # reshape as Big = maximize
        panel launcher --> wmtile -c # gracefully Close

...or by keyboard (via wmtile -k)

    $ wmtile -k
    installing 7 wmtile keyboard shortcuts
        Alt+Shift+M --> wmtile -m # Minimize
        Alt+Shift+T --> wmtile -t # reshape as Tiles
        Alt+Shift+P --> wmtile -p # reshape as Portraits
        Alt+Shift+L --> wmtile -l # reshape as Landscapes
        Alt+Shift+S --> wmtile -s # reshape as a Stack
        Alt+Shift+B --> wmtile -b # reshape as Big = maximize
        Alt+Shift+C --> wmtile -c # gracefully Close
    please reboot in order to make wmtile keyboard shortcuts effective

for further details, type:

    $ wmtile -H

OPTIONAL ARGUMENTS

  -h, --help        show this help message and exit
  -H, --user-guide  open User Guide in PDF format and exit
  -V, --version     show program's version number and exit
  -i, --launchers   Install 7 panel launchers (XFCE only)
  -k, --shortcuts   install 7 Keyboard shortcuts (XFCE only)
  -m, --minimize    Minimize
  -t, --tiles       reshape as Tiles
  -p, --portraits   reshape as Portraits
  -l, --landscapes  reshape as Landscapes
  -s, --stack       reshape as a Stack
  -b, --big         reshape as Big = maximize
  -c, --close       gracefully Close
```
