[Matt Gemmell][]'s ever-evolving keymap for the Corne split keyboard, designed for use with Apple devices. I've written about its various iterations [on my blog][].

![](keymap_diagram.svg)

## Features

- 5x3 + 1 thumb key per hand, for 32 keys in total.
- QWERTY with Home Row Mods in an Apple-suitable style: A-F = Shift, Ctrl, Alt/Opt, Cmd/GUI, and the symmetrical arrangement on the right half.
- No animations, OLED, tap-dance, or combos.
- 4 layers in the usual Planck-style momentary setup.
- Mostly for writing (what I do). In particular, the semicolon key is moved to a layer in favour of the more useful quote key on the base.
- Includes numpad, inverted-T cursors, mouse and scroll-wheel, media keys, and system shortcuts.
- Optional per-key, per-layer RGB LED colours, configured intuitively in the same layout as the keymap.
- Small firmware size; easily fits on a Pro Micro.

## Usage

Change to the qmk_firmware folder and do: `qmk compile -kb crkbd -km mattgemmell`.

The resulting `crkbd_rev1_mattgemmell.hex` should be flashed onto each half of the Corne keyboard, using `qmk flash` or the QMK Toolbox app. Flash each half of the device separately, leaving the TRRS cable fully connected to both halves at all times. To put each half of the keyboard into bootloader mode for flashing, hold down the key corresponding to the usual qwerty Q or P (depending on the half; will be top row and second-outermost key on 6x3 Cornes) when powering it on by connecting the USB cable, or press the recessed reset button on the bottom of each half.

To update the keymap diagram, change to the keymap directory (`qmk_firmware/keyboards/crkbd/keymaps/mattgemmell`) and do: `python update-keymap-diagram.py`.


[Talk to me about it][] if you like.

[Matt Gemmell]: https://mattgemmell.scot
[on my blog]: https://mattgemmell.scot/category/tech/
[Talk to me about it]: https://mattgemmell.scot/contact
