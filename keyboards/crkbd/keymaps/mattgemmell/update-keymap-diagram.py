#!/usr/bin/env python

# ============================================
#   Creates an SVG keymap diagram by parsing
#   my qmk keymap.c file, including RGB LED
#   colours.
#
#   This is COMPLETELY SPECIFIC to my map!
#
#   by Matt Gemmell
#   Web:        https://mattgemmell.scot/
#   Mastodon:   https://mastodon.scot/@mattgemmell
#   GitHub:     https://github.com/mattgemmell
#
# ============================================


# ============================================
#   SETTINGS
# ============================================

# Files (in same dir as this script)
keymap_filename = "keymap.c"
svg_filename = "keymap_diagram.svg"
create_layer_diagrams = True # also create one diagram per layer, named "[svg_filename basename]_[layer_id lowercase].[svg_filename extension]"

# SVG Geometry
diagram_inset = 10 # horizontal and vertical, around entire diagram
layer_spacing = 30 # vertical spacing between each layer
layout_keys_per_row = 12 # last row (only) can have fewer keys
# Note: layout_keys_per_row is the actual, real number of keys per row in the keymap structure. It includes ignored edge keys.
layout_num_edge_keys_ignored = 1 # first and last x keys per row won't be displayed in diagram
ignored_keys_affects_final_row = False # whether the above layout_num_edge_keys_ignored setting also affects the final/lowest/thumb row
max_keys_to_output = 0 # physical keys, including ignored edge keys. Zero to output all.
key_width = 65
key_height = 55
key_radius = 6 # corner radius
key_spacing = 4 # horizontal and vertical, both between keys and around entire layer
last_row_pad = 0 # additional vertical spacing (added to key_spacing) for final row

# Split layout
layout_split = True # expects an equal number of keys per half, and thus an even number of keys per row
split_spacing = 40 # horizontal spacing between halves of a split layout (used instead of horizontal key_spacing if layout_split is True)

# RGB LED colours
show_led_colours = True # if True, sets "rgb" CSS class on the root <svg> element
led_colours_lightness = 0.85 # 0.0 to 1.0

# Layers
show_layer_titles = True # applies to single overall diagram
show_layer_titles_per_layer = False # applies to separate layer-specific diagrams
layer_title_height = 20 # text box height; set font attributes in CSS below
layer_title_spacing = 10 # vertical spacing between layer title and its layer diagram
held_css_class = "held" # CSS class applied to keys which are held down on a given layer, e.g. MO() or LT(); edit the actual CSS below.
keycode_blank = "XXXXXXX"
blank_css_class = "blank" # as above, applied to keys with no function (i.e. keycode_blank above).
keycode_transparent = "_______"
transparent_css_class = "transparent" # as above, applied to transparent keys (falling through to base layer; i.e. keycode_transparent above).
# Note: Transparent keys (on non-base layers) will be labelled identically to the corresponding key on the base layer.
annotation_keycodes = { # keycodes with annotations
    "layer": {"keycodes": ["NAV", "NUM", "B_NUM", "SPC_NAV", "ENT_NUM"],
              "label": "layer"},
    #"num": {"keycodes": ["NUM", "B_NUM"],
    #          "label": "num"},
    #"nav": {"keycodes": ["NAV", "SPC_NAV"],
    #          "label": "nav"},
    "one-shot": {"keycodes": ["OS_SHFT", "OS_CTRL", "OS_ALT", "OS_CMD", "OS_CAPS"],
                 "label": "one-shot"},
    "hrm-shift": {"keycodes": ["HRM_A_LSFT", "HRM_QUOT_RSFT"],
              "label": "shift"},
    "hrm-control": {"keycodes": ["HRM_S_LCTL", "HRM_L_RCTL"],
              "label": "control"},
    "hrm-option": {"keycodes": ["HRM_D_LALT", "HRM_K_RALT"],
              "label": "option"},
    "hrm-command": {"keycodes": ["HRM_F_LGUI", "HRM_J_RGUI"],
              "label": "command"},
    held_css_class: {"keycodes": [], # special case, to provide label for held layer keys
                     "label": "held"},
}
layer_held_keycodes = { # keycodes whose keys are implicitly held down on a given layer, gaining the held_css_class specified above. Key is the layer, value is an array of keys implicitly held on that layer.
  "_NAV": ["NAV", "SPC_NAV"],
  "_NUM": ["NUM", "B_NUM", "ENT_NUM"],
  "_ADJUST": ["NUM", "NAV", "SPC_NAV", "B_NUM", "ENT_NUM"]
}
layer_note_height = 0 # text box height; set font attributes in CSS below
layer_note_spacing = 0 # vertical spacing between layer diagram and its layer note
layer_notes = { # Notes to be displayed for a given layer
  #"_BASE": "B+N = Space",
}

# Advanced
apply_keycode_class = True # applies the lowercase keycode name as a class to the key's DIV, to allow CSS customisation; for example, the "A" key would have class "kc_a" applied.
apply_keycode_title = True # applies the keycode (as-is) as a "title" attribute to the key's DIV, allowing it to be shown in a tooltip upon hover etc.
apply_layer_class = True # applies the lowercase layer ID as a class to each key's DIV on that layer, e.g. each key on the _BASE layer would have the "_base" class applied.

# SVG template segments
svg_header = '''<svg width="100%" height="auto" viewBox="0 0 ${svg_width} ${svg_height}" xmlns="http://www.w3.org/2000/svg" class="${svg_classes}">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
    svg {
        font-family: -apple-system, "Helvetica Neue", sans-serif;
        font-size: 14px;
        text-rendering: optimizeLegibility;
        background-color: white;
    }

    text {
    	text-anchor: middle;
    	dominant-baseline: middle;
    }

    .text-container > div {
        cursor: default;
        box-sizing: border-box;
        background-color: #f0f0f0;
        text-align: center;
        width: ${key_width}px;
        height: ${key_height}px;
        border-radius: ${key_radius}px;
        display: flex;
        flex-direction: column;
		overflow: hidden;
    }

    .glyph {
        padding: 1px 2px;
        display: flex;
        justify-content: center;
        align-items: center;
        hyphens: auto;
        -webkit-hyphens: auto;
        -moz-hyphens: auto;
        -ms-hyphens: auto;
		flex: 1 0 auto;
		color: black;
    }

    .text-container > div:after {
        box-sizing: border-box;
        font-size: 11px;
    	font-weight: bold;
    	font-variant: small-caps;
		position: fixed;
		bottom: 0;
		padding-bottom: 1px;
		width: 100%;
		display: none;
    }

    .text-container > div.${held_css_class} > .glyph {
        background-color: #bbf;
    }

    .rgb .text-container > div.${held_css_class} > .glyph {
        background-color: initial;
        border: 3px solid #00e;
        border-bottom-width: 0;
        border-radius: ${key_radius}px ${key_radius}px 0 0;
    }

    .text-container > div.${blank_css_class} {
        background-color: #fff6;
    }

    .text-container > div.${transparent_css_class} > .glyph {
        color: #bbb;
    }

    .text-container > div.${held_css_class} > .glyph {
        color: black;
    }

    .text-container > div.${blank_css_class}.${transparent_css_class},
    .text-container > div.${blank_css_class}._base {
        display: none;
    }

    .layer_title {
		font-size: 17px;
		font-weight: bold;
		fill: #777;
    }

    .layer_note {
		font-size: 12px;
		font-weight: bold;
		fill: #09f;
    }

    .layer_bg {
        fill: #c0c0c0;
        width: ${layer_bg_width}px;
        height: ${layer_bg_height}px;
    }

    .kc_up, .kc_down, .kc_left, .kc_right,
    .kc_ent, .ent_shft, .kc_bspc, /*.os_caps,*/ .kc_esc,
    .kc_lsft, .os_shft, .os_ctrl, .os_alt, .os_cmd, .kc_lcmd, .kc_lalt,
    .kc_mac_spotlight, .kc_pgup, .kc_pgdn,
    .kc_mac_undo, .kc_mac_redo, .kc_tab,
    /*.kc_mac_cut,*/ .kc_spc, .kc_mac_lock_scrn,
    .kc_brightness_up, .kc_brightness_down/*,
    .kc_audio_vol_up, .kc_audio_vol_down, .kc_audio_mute,
    .kc_media_play_pause, .kc_media_prev_track, .kc_media_next_track*/ {
    	font-size: 18px;
    }

    .kc_bspc {
    	font-size: 22px;
    }

/*
    .os_caps {
    	font-size: 16px;
    	padding-top: 1px !important;
    }
*/
    .kc_mac_spotlight {
    	font-size: 40px;
    }

    .kc_mac_undo {
    	font-size: 34px;
    }

    .kc_mac_redo {
    	font-size: 34px;
    }
/*
    .kc_mac_cut {
    	font-size: 20px;
    }
*/
    .kc_spc {
    	font-size: 24px;
    }

    .kc_mac_lock_scrn {
    	font-size: 22px;
    }

    .kc_brightness_up {
    	font-size: 28px;
    }

    .kc_brightness_down {
    	font-size: 32px;
    }
/*
    .kc_audio_vol_down {
    	font-size: 22px;
    }

    .kc_audio_vol_up {
    	font-size: 22px;
    }

    .kc_audio_mute {
    	font-size: 22px;
    }

    .kc_media_play_pause {
    	font-size: 26px;
    }

    .kc_media_prev_track {
    	font-size: 26px;
    }

    .kc_media_next_track {
    	font-size: 26px;
    }
*/
    .annotation {
        box-sizing: border-box;
        font-size: 11px;
    	font-weight: bold;
    	font-variant: small-caps;
		padding-bottom: 2px;
		width: 100%;
        color: #f6f6f6;
		background-color: #666;
    }

    .${held_css_class} .annotation {
        background-color: #00e;
    }
${extra_css}
</style>
'''

svg_footer = '''
</svg>
'''

svg_layer_title = '''
<text x="${layer_title_x}" y="${layer_title_y}" class="layer_title">${layer_title}</text>
'''

svg_layer_bg = '''
<rect rx="${key_radius}" x="${layer_bg_x}" y="${layer_bg_y}" class="layer_bg" />
'''

svg_key = '''
<foreignObject x="${key_x}" y="${key_y}" width="${key_width}" height="${key_height}" class="text-container">
	<div xmlns="http://www.w3.org/1999/xhtml" lang="en" ${title_attr}class="${key_classes}"><div class="glyph">${key_label}</div>${annotation}</div>
</foreignObject>
'''

svg_layer_note = '''
<text x="${layer_note_x}" y="${layer_note_y}" class="layer_note">${layer_note}</text>
'''

# ============================================
#   END OF SETTINGS
# ============================================


# Read keymap C file
keymap_file = open(keymap_filename, "r")
keymap_contents = keymap_file.read()
keymap_raw = ""
ledmap_raw = ""

# Extract raw C keymap and ledmap
import re
map_regexp = re.compile(r"^[^]\r\n]+?[a-z]+\[\][^}]+?{$.*?};$", re.MULTILINE | re.DOTALL)
keymap_match = map_regexp.search(keymap_contents)
search_start = 0;
if keymap_match != None:
    keymap_raw = keymap_match.group()
    search_start += keymap_match.span()[1]

ledmap_match = map_regexp.search(keymap_contents[search_start:])
if ledmap_match != None:
    ledmap_raw = ledmap_match.group()

# Parse keys and LED colours into usable data
key_layers = {}
led_layers = {}
layer_order = []
row_regexp = re.compile(r"^\s*\[([^\]]+)\][^({]+[({]$([^)}]+)[)}]", re.MULTILINE)
key_row_matches = row_regexp.finditer(keymap_raw)
led_row_matches = row_regexp.finditer(ledmap_raw)
for key_row_match in key_row_matches:
    key_layers.update({key_row_match.group(1): [x.strip() for x in key_row_match.group(2).split(",")]});
    layer_order.append(key_row_match.group(1))
for led_row_match in led_row_matches:
    led_layers.update({led_row_match.group(1): [x.strip() for x in led_row_match.group(2).split(",")]});

# Create substitution mappings
layer_names = {
  "_BASE": "Base",
  "_NAV": "Navigation &amp; Shortcuts",
  "_NUM": "Numpad &amp; Symbols",
  "_ADJUST": "Mouse &amp; Media"
}

# We'll just strip the keycode_prefix if a keycode isn't found in key_names.
keycode_prefix = "KC_"
key_names = {
    "KC_MAC_UNDO": {"label": "&#10554;", "title": "Undo"},
    "KC_MAC_REDO": {"label": "&#10555;", "title": "Redo"},
    #"KC_MAC_CUT": {"label": "&#9986;", "title": "Cut"},
    "KC_MAC_CUT": {"label": "Cut", "title": "Cut"},
    "KC_MAC_COPY": {"label": "Copy", "title": "Copy"},
    "KC_MAC_PASTE": {"label": "Paste", "title": "Paste"},
    "KC_MAC_LOCK_SCRN": {"label": "&#9211;", "title": "Lock Screen"},
    "KC_MAC_SCRN_SHOT": {"label": "Screen Shot", "title": "Screenshot"},
    "KC_MAC_SCRN_MRKP": {"label": "Markup Screen", "title": "Markup Screen"},
    "KC_MAC_HOME": {"label": "Home", "title": "Home"},
    "KC_MAC_END": {"label": "End", "title": "End"},
    "KC_MAC_PREV_TAB": {"label": "Prev Tab", "title": "Previous Tab"},
    "KC_MAC_NEXT_TAB": {"label": "Next Tab", "title": "Next Tab"},
    "KC_MAC_SPOTLIGHT": {"label": "&#8981;", "title": "Spotlight"},
    "KC_EN_DASH": {"label": "En Dash", "title": "En Dash"},
    "KC_EM_DASH": {"label": "Em Dash", "title": "Em Dash"},
    "KC_BACK_MG": {"label": "Back", "title": "Back"},
    "KC_FWD_MG": {"label": "Forward", "title": "Forward"},
    "KC_LSFT": {"label": "&#8679;", "title": "Shift"},
    "OS_SHFT": {"label": "&#8679;", "title": "Shift — One-Shot"},
    "OS_CTRL": {"label": "&#94;", "title": "Control — One-Shot"},
    "OS_ALT": {"label": "&#8997;", "title": "Option — One-Shot"},
    "OS_CMD": {"label": "&#8984;", "title": "Command — One-Shot"},
    #"OS_CAPS": {"label": "&#127760;", "title": "Globe — One-Shot"},
    "OS_CAPS": {"label": "Globe", "title": "Globe — One-Shot"},
    "HRM_A_LSFT": {"label": "A", "title": "A (tap), Shift (held)"},
    "HRM_S_LCTL": {"label": "S", "title": "S (tap), Control (held)"},
    "HRM_D_LALT": {"label": "D", "title": "D (tap), Option (held)"},
    "HRM_F_LGUI": {"label": "F", "title": "F (tap), Command (held)"},
    "HRM_J_RGUI": {"label": "J", "title": "J (tap), Command (held)"},
    "HRM_K_RALT": {"label": "K", "title": "K (tap), Option (held)"},
    "HRM_L_RCTL": {"label": "L", "title": "L (tap), Control (held)"},
    "HRM_QUOT_RSFT": {"label": "'", "title": "Quote (tap), Shift (held)"},
    "KC_LCMD": {"label": "&#8984;", "title": "Command"},
    "KC_LALT": {"label": "&#8997;", "title": "Option"},
    "APP_SWITCH_FRWD": {"label": "Switch App", "title": "Next App"},
    "NAV": {"label": "Nav", "title": "Nav"},
    "NUM": {"label": "Num", "title": "Num"},
    "SPC_NAV": {"label": "&#9251;", "title": "Space"},
    "ENT_NUM": {"label": "&#9166;", "title": "Enter"},
    #"B_NUM": {"label": "B", "title": "B"},
    #"KC_AUDIO_VOL_DOWN": {"label": "&#128265;", "title": "Volume Down"},
    "KC_AUDIO_VOL_DOWN": {"label": "Volume Down", "title": "Volume Down"},
    #"KC_AUDIO_MUTE": {"label": "&#128263;", "title": "Mute"},
    "KC_AUDIO_MUTE": {"label": "Mute", "title": "Mute"},
    #"KC_AUDIO_VOL_UP": {"label": "&#128266;", "title": "Volume Up"},
    "KC_AUDIO_VOL_UP": {"label": "Volume Up", "title": "Volume Up"},
    "KC_MS_ACCEL2": {"label": "Mouse Accel 2", "title": "Mouse Acceleration 2"},
    "MS_WHLD": {"label": "Mouse Wheel Down", "title": "Mouse Wheel Down"},
    "MS_BTN1": {"label": "Left Click", "title": "Left Click"},
    "MS_UP": {"label": "Mouse &#9650;", "title": "Mouse Up"},
    "MS_BTN2": {"label": "Right Click", "title": "Right Click"},
    "KC_MS_ACCEL1": {"label": "Mouse Accel 1", "title": "Mouse Acceleration 1"},
    "MS_WHLU": {"label": "Mouse Wheel Up", "title": "Mouse Wheel Up"},
    "MS_LEFT": {"label": "Mouse &#9664;", "title": "Mouse Left"},
    "MS_DOWN": {"label": "Mouse &#9660;", "title": "Mouse Down"},
    "MS_RGHT": {"label": "Mouse &#9654;", "title": "Mouse Right"},
    "KC_BRIGHTNESS_UP": {"label": "&#9728;", "title": "Brightness Up"},
    #"KC_MEDIA_PREV_TRACK": {"label": "&#9198;", "title": "Previous Track"},
    "KC_MEDIA_PREV_TRACK": {"label": "Prev Track", "title": "Previous Track"},
    #"KC_MEDIA_PLAY_PAUSE": {"label": "&#9199;", "title": "Play/Pause"},
    "KC_MEDIA_PLAY_PAUSE": {"label": "Play Pause", "title": "Play/Pause"},
    #"KC_MEDIA_NEXT_TRACK": {"label": "&#9197;", "title": "Next Track"},
    "KC_MEDIA_NEXT_TRACK": {"label": "Next Track", "title": "Next Track"},
    "KC_MS_ACCEL0": {"label": "Mouse Accel 0", "title": "Mouse Acceleration 0"},
    "KC_BRIGHTNESS_DOWN": {"label": "&#9788;", "title": "Brightness Down"},
    "KC_QUOT": {"label": "'", "title": "Quote"},
    "KC_COMM": {"label": ",", "title": "Comma"},
    "KC_DOT": {"label": ".", "title": "Full Stop"},
    "KC_SLSH": {"label": "/", "title": "Forward Slash"},
    "KC_SPC": {"label": "&#9251;", "title": "Space"},
    "SPC_QSTN": {"label": "&#9251;", "title": "Space"},
    "KC_ESC": {"label": "&#9099;", "title": "Escape"},
    "KC_PGUP": {"label": "&#8670;", "title": "Page Up"},
    "KC_UP": {"label": "&#9650;", "title": "Up"},
    "KC_BSPC": {"label": "&#9003;", "title": "Backspace"},
    "KC_TAB": {"label": "&#8677;", "title": "Tab"},
    "KC_PGDN": {"label": "&#8671;", "title": "Page Down"},
    "KC_LEFT": {"label": "&#9664;", "title": "Left"},
    "KC_DOWN": {"label": "&#9660;", "title": "Down"},
    "KC_RIGHT": {"label": "&#9654;", "title": "Right"},
    "KC_ENT": {"label": "&#9166;", "title": "Enter"},
    "ENT_SHFT": {"label": "&#9166;", "title": "Enter"},
    "KC_SCLN": {"label": ";", "title": "Semicolon"},
    "KC_LPRN": {"label": "(", "title": "Left Parenthesis"},
    "KC_RPRN": {"label": ")", "title": "Right Parenthesis"},
    "KC_BSLS": {"label": "\\", "title": "Backslash"},
    "KC_MINUS": {"label": "-", "title": "Hyphen"},
    "KC_ASTR": {"label": "*", "title": "Asterisk"},
    "KC_EQUAL": {"label": "=", "title": "Equals"},
    "KC_LBRC": {"label": "[", "title": "Left Bracket"},
    "KC_RBRC": {"label": "]", "title": "Right Bracket"},
    "KC_GRAVE": {"label": "`", "title": "Backtick"},
    "KC_0": {"label": "0", "title": "0"},
    "KC_1": {"label": "1", "title": "1"},
    "KC_2": {"label": "2", "title": "2"},
    "KC_3": {"label": "3", "title": "3"},
    "KC_4": {"label": "4", "title": "4"},
    "KC_5": {"label": "5", "title": "5"},
    "KC_6": {"label": "6", "title": "6"},
    "KC_7": {"label": "7", "title": "7"},
    "KC_8": {"label": "8", "title": "8"},
    "KC_9": {"label": "9", "title": "9"},
    "KC_A": {"label": "A", "title": "A"},
    "KC_B": {"label": "B", "title": "B"},
    "KC_C": {"label": "C", "title": "C"},
    "KC_D": {"label": "D", "title": "D"},
    "KC_E": {"label": "E", "title": "E"},
    "KC_F": {"label": "F", "title": "F"},
    "KC_G": {"label": "G", "title": "G"},
    "KC_H": {"label": "H", "title": "H"},
    "KC_I": {"label": "I", "title": "I"},
    "KC_J": {"label": "J", "title": "J"},
    "KC_K": {"label": "K", "title": "K"},
    "KC_L": {"label": "L", "title": "L"},
    "KC_M": {"label": "M", "title": "M"},
    "KC_N": {"label": "N", "title": "N"},
    "KC_O": {"label": "O", "title": "O"},
    "KC_P": {"label": "P", "title": "P"},
    "KC_Q": {"label": "Q", "title": "Q"},
    "KC_R": {"label": "R", "title": "R"},
    "KC_S": {"label": "S", "title": "S"},
    "KC_T": {"label": "T", "title": "T"},
    "KC_U": {"label": "U", "title": "U"},
    "KC_V": {"label": "V", "title": "V"},
    "KC_W": {"label": "W", "title": "W"},
    "KC_X": {"label": "X", "title": "X"},
    "KC_Y": {"label": "Y", "title": "Y"},
    "KC_Z": {"label": "Z", "title": "Z"},
}

# Parse colour values and create mapping
led_colours = {}
colours_regexp = re.compile(r"#define\s+(\S+)\s+\{([^\}]+)\}", re.MULTILINE)
colours_matches = colours_regexp.finditer(keymap_contents)
colour_rgb = []
import colorsys
for colour_match in colours_matches:
    colour_rgb_str = [x.strip() for x in colour_match.group(2).split(",")]
    colour_rgb = []
    for component_rgb in colour_rgb_str:
        colour_rgb.append(float(component_rgb) / float(255))
    colour_hsl = colorsys.rgb_to_hsv(colour_rgb[0], colour_rgb[1], colour_rgb[2])
    lightness = colour_hsl[2]
    if not (colour_hsl[0] == 0 and colour_hsl[1] == 0):
        lightness = led_colours_lightness
    led_colours.update({colour_match.group(1): [colour_hsl[0], colour_hsl[1], lightness]});

# Ensure we have at least layout_keys_per_row keys on our base layer.
num_keys = len(key_layers[layer_order[0]])
if max_keys_to_output > 0 and num_keys > max_keys_to_output:
    num_keys = max_keys_to_output
if num_keys < layout_keys_per_row:
    layout_keys_per_row = num_keys

# Calculate overall viewbox dimensions, paying attention to layout_num_edge_keys_ignored.
import math
num_rows = int(math.ceil(float(num_keys) / float(layout_keys_per_row)))
num_real_cols = layout_keys_per_row
num_cols = num_real_cols
if layout_num_edge_keys_ignored > 0:
    num_cols -= (2 * layout_num_edge_keys_ignored)

layer_width = (num_cols * key_width) + (num_cols * key_spacing)
if layout_split:
    layer_width += split_spacing
else:
    layer_width += key_spacing
svg_width = (2 * diagram_inset) + layer_width

num_layers = len(layer_order)
layer_height = (num_rows * key_height) + ((num_rows + 1) * key_spacing) + last_row_pad
svg_height = (2 * diagram_inset) + (num_layers * layer_height) + ((num_layers - 1) * layer_spacing)
if show_layer_titles:
    svg_height += num_layers * (layer_title_height + layer_title_spacing)
if len(layer_notes) > 0:
    svg_height += num_layers * (layer_note_height + layer_note_spacing)

extra_css = ""
from string import Template

if show_led_colours:
    colour_css_template = Template('''
    .text-container > div.${colour_class} {
		background-color: hsl(${colour_hsl});
    }
''')
    for colour in led_colours:
        colour_class = colour.lower()
        colour_hsl_vals = led_colours[colour]
        if not (colour_hsl_vals[2] == 0):
            colour_hsl = "%f, %f%%, %f%%" % (colour_hsl_vals[0] * 360.0,
                                             colour_hsl_vals[1] * 100.0,
                                             colour_hsl_vals[2] * 100.0)
            extra_css += colour_css_template.substitute({'colour_class': colour_class,
                                                         'colour_hsl': colour_hsl})

# Generate output
svg_raw = ""
svg_layer_header = "" # for per-layer svg output
svg_layers = {} # for per-layer svg output

# Header
svg_classes = []
if show_led_colours:
    svg_classes.append("rgb")
header_template = Template(svg_header)
svg_raw += header_template.substitute({'svg_width': svg_width,
                                       'svg_height': svg_height,
                                       'svg_classes': " ".join(svg_classes),
                                       'key_width': key_width,
                                       'key_height': key_height,
                                       'key_radius': key_radius,
                                       'held_css_class': held_css_class,
                                       'blank_css_class': blank_css_class,
                                       'transparent_css_class': transparent_css_class,
                                       'layer_bg_width': layer_width,
                                       'layer_bg_height': layer_height,
                                       'extra_css': extra_css})
if create_layer_diagrams:
    layer_diagram_height = layer_height + (2 * diagram_inset)
    if show_layer_titles_per_layer:
        layer_diagram_height += (layer_title_height + layer_title_spacing)
    if len(layer_notes) > 0:
        layer_diagram_height += (layer_note_height + layer_note_spacing)
    svg_layer_header = header_template.substitute({'svg_width': svg_width,
                                                   'svg_height': layer_diagram_height,
                                                   'svg_classes': " ".join(svg_classes),
                                                   'key_width': key_width,
                                                   'key_height': key_height,
                                                   'key_radius': key_radius,
                                                   'held_css_class': held_css_class,
                                                   'blank_css_class': blank_css_class,
                                                   'transparent_css_class': transparent_css_class,
                                                   'layer_bg_width': layer_width,
                                                   'layer_bg_height': layer_height,
                                                   'extra_css': extra_css})

if show_layer_titles or show_layer_titles_per_layer:
    layer_title_template = Template(svg_layer_title)
    layer_title_x = float(svg_width) / 2.0; # SVG text boxes are positioned at their centre point

if len(layer_notes) > 0:
    layer_note_template = Template(svg_layer_note)
    layer_note_x = float(svg_width) / 2.0; # SVG text boxes are positioned at their centre point

layer_bg_template = Template(svg_layer_bg)
key_template = Template(svg_key)

cur_y = diagram_inset
layer_num = 0

def svg_for_layer(layer_id, start_y, show_title):
    svg_raw = ""
    cur_y = start_y
    row_num = 0
    col_num = 0
    cur_x = diagram_inset

    # Layer title
    if show_title:
        layer_title = layer_names[layer_id]
        layer_title_y = float(cur_y) + (float(layer_title_height) / 2.0)
        svg_raw += layer_title_template.substitute({'layer_title_x': layer_title_x,
                                                    'layer_title_y': layer_title_y,
                                                    'layer_title': layer_title})
        cur_y += (layer_title_height + layer_title_spacing)

    # Layer background
    svg_raw += layer_bg_template.substitute({'key_radius': key_radius,
                                             'layer_bg_x': cur_x,
                                             'layer_bg_y': cur_y})

    cur_x += key_spacing
    cur_y += key_spacing

    # Keys
    key_index = 0 # Zero-based
    key_classes = []
    key_label = ""
    layer_keys = key_layers[layer_id]
    for key in layer_keys:
        if max_keys_to_output > 0 and key_index >= max_keys_to_output:
            break

        key_label = key
        key_classes = []

        last_col_num = num_real_cols;
        is_last_row = (row_num == num_rows - 1)
        if is_last_row:
            # Last row may have fewer keys.
            last_col_num = num_keys % ((num_rows - 1) * num_real_cols)

        # Decide whether to output key
        output_key = True
        if layout_num_edge_keys_ignored > 0 and (not is_last_row or (is_last_row and ignored_keys_affects_final_row)):
            if col_num < layout_num_edge_keys_ignored or (last_col_num - col_num) <= layout_num_edge_keys_ignored:
                output_key = False

        if output_key:
            # Key's human-readable label
            key_is_transparent = False
            key_is_blank = False
            if key == keycode_transparent:
                key_is_transparent = True
                key_classes.append(transparent_css_class)
                if layer_id != layer_order[0]:
                    # Obtain transparent key's effective keycode from base layer
                    try:
                        key = key_layers[layer_order[0]][key_index]
                    except IndexError:
                        print(f"Error: Couldn't find base layer keycode for transparent key {key_index} in layer {layer_id}!")

            if key in key_names:
                key_label = key_names[key]["label"]
            elif key.startswith(keycode_prefix):
                key_label = key[len(keycode_prefix):]
            elif key == keycode_blank:
                key_is_blank = True
                key_classes.append(blank_css_class)
                key_label = ""

            # CSS classes to apply to the key container
            key_is_held = (layer_id in layer_held_keycodes and key in layer_held_keycodes[layer_id])
            if key_is_held:
                key_classes.append(held_css_class)
            if show_led_colours and layer_id in led_layers:
                key_classes.append(led_layers[layer_id][key_index].lower())
            if apply_keycode_class and key not in [keycode_blank, keycode_transparent]:
                key_classes.append(key.lower())
            if apply_layer_class:
                key_classes.append(layer_id.lower())

            # Title attribute
            title_attr = ""
            title_val = ""
            if key in key_names:
                title_val = key_names[key]["title"]
            # Check to see if this is a layer key
            layer_key = "_" + key
            if layer_key in layer_names:
                title_val = layer_names[layer_key] + " Layer"

            title_keycode = key
            if key_is_transparent:
                title_keycode = transparent_css_class.capitalize()
            elif key_is_blank:
                title_keycode = blank_css_class.capitalize()
            if title_val != "" and apply_keycode_title:
                title_attr = 'title="%s (%s)" ' % (title_val, title_keycode)
            elif title_val != "":
                title_attr = 'title="%s" ' % (title_val)
            elif apply_keycode_title:
                title_attr = 'title="%s" ' % (title_keycode)

            # Annotation
            annotation = ""
            for ann_class in annotation_keycodes:
                if key in annotation_keycodes[ann_class]["keycodes"]:
                    ann_content = annotation_keycodes[ann_class]["label"]
                    if key_is_held:
                        ann_content = annotation_keycodes[held_css_class]["label"]
                    annotation = '<div class="annotation %s">%s</div>' % (ann_class, ann_content)
                    break;
            # <div class="annotation one-shot">one-shot</div>

            # Process key template
            svg_raw += key_template.substitute({'key_radius': key_radius,
                                                'key_x': cur_x,
                                                'key_y': cur_y,
                                                'title_attr': title_attr,
                                                'key_classes': " ".join(key_classes),
                                                'key_width': key_width,
                                                'key_height': key_height,
                                                'key_label': key_label,
                                                'annotation': annotation})

        # Prep for next key
        key_index += 1
        if (key_index % num_real_cols == 0) or (key_index == num_keys):
            # Start of a new row
            cur_x = diagram_inset + key_spacing
            cur_y += (key_spacing + key_height)
            row_num += 1
            col_num = 0
            if row_num == num_rows - 1:
                # Last row
                cur_y += last_row_pad

                last_col_num = num_keys % ((num_rows - 1) * num_real_cols)
                if last_col_num < num_real_cols:
                    # Fewer keys in last row; indent them so they're still centred.
                    indent_units = (num_real_cols - last_col_num)
                    if not ignored_keys_affects_final_row:
                        indent_units -= (layout_num_edge_keys_ignored * 2)
                    cur_x += ((indent_units / 2) * (key_spacing + key_width))
        else:
            # Continue current row
            if output_key:
                cur_x += key_width
            col_num += 1
            if col_num == last_col_num / 2 and layout_split:
                cur_x += split_spacing
            elif output_key:
                cur_x += key_spacing

    # Layer note
    if len(layer_notes) > 0:
        cur_y += layer_note_spacing
    if layer_id in layer_notes:
        layer_note_text = layer_notes[layer_id]
        layer_note_y = float(cur_y) + (float(layer_note_height) / 2.0)
        svg_raw += layer_note_template.substitute({'layer_note_x': layer_note_x,
                                                    'layer_note_y': layer_note_y,
                                                    'layer_note': layer_note_text})
    cur_y += layer_note_height

    return {'svg': svg_raw, 'delta_y': cur_y - start_y}

for layer_id in layer_order:
    layer_svg_data = svg_for_layer(layer_id, cur_y, show_layer_titles)
    svg_raw += layer_svg_data['svg']

    # Prep for next layer
    layer_num += 1
    cur_y += layer_spacing + layer_svg_data['delta_y']

    if create_layer_diagrams:
        layer_svg_data = svg_for_layer(layer_id, diagram_inset, show_layer_titles_per_layer)
        svg_layers[layer_id] = svg_layer_header + layer_svg_data['svg'] + svg_footer

# Footer
svg_raw += svg_footer # no vars in this, so it can be included literally

# Write out SVG file.
svg_file = open(svg_filename, "w")
svg_file.write(svg_raw)
svg_file.close()
# Got to love Python.

if create_layer_diagrams:
    for layer_id in svg_layers:
        svg_filename_components = svg_filename.split(".")
        svg_filename_root = svg_filename_components[0]
        svg_filename_ext = svg_filename_components[1]
        layer_filename = svg_filename_root + "_" + layer_id.lstrip("_").lower() + "." + svg_filename_ext
        svg_file = open(layer_filename, "w")
        svg_file.write(svg_layers[layer_id])
        svg_file.close()
