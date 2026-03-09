/*
Copyright 2019 @foostan
Copyright 2020 Drashna Jaelre <@drashna>
Copyright 2021 Elliot Powell <@e11i0t23>
Copyright 2021 Matt Gemmell <@mattgemmell>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include QMK_KEYBOARD_H
//#include "oneshot.h"
//#include "swapper.h"

#define KC_MAC_UNDO LGUI(KC_Z)
#define KC_MAC_REDO LSFT(LGUI(KC_Z))
#define KC_MAC_CUT LGUI(KC_X)
#define KC_MAC_COPY LGUI(KC_C)
#define KC_MAC_PASTE LGUI(KC_V)
#define KC_MAC_LOCK_SCRN LCTL(LGUI(KC_Q))
//#define KC_MAC_SCRN_SHOT LGUI(LSFT(KC_3))
//#define KC_MAC_SCRN_MRKP LGUI(LSFT(KC_4))
//#define KC_MAC_HOME LGUI(KC_UP)
//#define KC_MAC_END LGUI(KC_DOWN)
#define KC_MAC_PREV_TAB LGUI(LSFT(KC_LBRC))
#define KC_MAC_NEXT_TAB LGUI(LSFT(KC_RBRC))
#define KC_MAC_SPOTLIGHT LGUI(KC_SPC)
#define KC_EN_DASH LALT(KC_MINUS)
#define KC_EM_DASH LSFT(LALT(KC_MINUS))
#define KC_BACK_MG LGUI(KC_LBRC)
#define KC_FWD_MG LGUI(KC_RBRC)

#define HRM_A_LSFT LSFT_T(KC_A)
#define HRM_S_LCTL LCTL_T(KC_S)
#define HRM_D_LALT LALT_T(KC_D)
#define HRM_F_LGUI LGUI_T(KC_F)
#define HRM_J_RGUI RGUI_T(KC_J)
#define HRM_K_RALT RALT_T(KC_K)
#define HRM_L_RCTL RCTL_T(KC_L)
#define HRM_QUOT_RSFT RSFT_T(KC_QUOT)

#ifdef RGB_MATRIX_ENABLE
    #define ___off___	{0,0,0}
    #define MG__WHITE	{255,255,255}
    #define	MG____RED	{255,0,0}
    #define MG__GREEN	{32,159,33}
    #define MG___BLUE	{0,181,213}
    #define MG_YELLOW	{255,208,0}
    #define MG_ORANGE	{255,85,0}
    #define MG___PINK	{208,0,255}
    #define MG_PURPLE	{50,0,232}
#endif

enum my_layers {
    _BASE,
    _NAV,
    _NUM,
    _ADJUST,
};
/*
enum my_keycodes {
    // Callum oneshot mod implementation with no timers.
    OS_SHFT = SAFE_RANGE,
    OS_CTRL,
    OS_ALT,
    OS_CMD,
    OS_CAPS, // for use as Globe on iPadOS, via remapping in Settings.app

    APP_SWITCH_FRWD, // cmd-tab but holds cmd between invocations
};
*/
//#define NAV MO(_NAV)
//#define NUM MO(_NUM)
//#define ENT_SHFT RSFT_T(KC_ENT)
//#define B_NUM LT(_NUM, KC_B)
#define SPC_NAV LT(_NAV, KC_SPC)
#define ENT_NUM LT(_NUM, KC_ENT)

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
  [_BASE] = LAYOUT_split_3x6_3(
       XXXXXXX, KC_Q, KC_W, KC_E,    KC_R, KC_T,         KC_Y,   KC_U, KC_I,    KC_O,   KC_P,    XXXXXXX,
       XXXXXXX, HRM_A_LSFT, HRM_S_LCTL, HRM_D_LALT,    HRM_F_LGUI, KC_G,         KC_H,   HRM_J_RGUI, HRM_K_RALT,    HRM_L_RCTL,   HRM_QUOT_RSFT, XXXXXXX,
       XXXXXXX, KC_Z, KC_X, KC_C,    KC_V, KC_B,         KC_N, KC_M, KC_COMM, KC_DOT, KC_SLSH, XXXXXXX,
                            XXXXXXX, ENT_NUM, XXXXXXX,      XXXXXXX, SPC_NAV,  XXXXXXX
  ),

  [_NAV] = LAYOUT_split_3x6_3(
      _______, KC_ESC,      XXXXXXX,    XXXXXXX,  XXXXXXX,  XXXXXXX,            KC_PGUP,   KC_MAC_PREV_TAB,  KC_UP,           KC_MAC_NEXT_TAB, KC_BSPC, _______,
      _______, _______,      _______,    _______,            _______,            XXXXXXX,            KC_PGDN, KC_LEFT,          KC_DOWN,         KC_RIGHT,        KC_SCLN, _______,
      _______, KC_MAC_UNDO, KC_MAC_CUT, KC_MAC_COPY,       KC_MAC_PASTE,      KC_MAC_REDO,        XXXXXXX,   KC_MAC_SPOTLIGHT, KC_BACK_MG, KC_FWD_MG,         KC_ENT,  _______,
                                                         _______, _______, _______,             _______, _______, _______
  ),

  [_NUM] = LAYOUT_split_3x6_3(
     _______, KC_TAB,     KC_GRAVE,    KC_LPRN,     KC_RPRN,     KC_BSLS,          KC_SLSH, KC_7, KC_8, KC_9, KC_EQUAL,   _______,
     _______, _______,     _______,    _______,      _______,      XXXXXXX,            KC_COMM, KC_4, KC_5, KC_6, KC_MINUS,   _______,
     _______, KC_EN_DASH, XXXXXXX, KC_LBRC, KC_RBRC, KC_EM_DASH,           KC_0, KC_1, KC_2, KC_3, KC_DOT,     _______,
                                           _______, _______, _______,            _______, _______, _______
  ),

  [_ADJUST] = LAYOUT_split_3x6_3(
      _______, XXXXXXX, KC_AUDIO_VOL_DOWN,   KC_AUDIO_MUTE,       KC_AUDIO_VOL_UP,     XXXXXXX,            MS_WHLD,    MS_BTN1, MS_UP,   MS_BTN2,  KC_MAC_LOCK_SCRN,   _______,
      _______, _______, _______,             _______,              _______,              XXXXXXX,            MS_WHLU,      MS_LEFT, MS_DOWN, MS_RGHT, XXXXXXX,   _______,
      _______, XXXXXXX, KC_MEDIA_PREV_TRACK, KC_MEDIA_PLAY_PAUSE, KC_MEDIA_NEXT_TRACK, XXXXXXX,            XXXXXXX,          XXXXXXX,    XXXXXXX,    XXXXXXX,     XXXXXXX, _______,
                                                                         _______, _______, _______,             _______, _______, _______
  )
};

#ifdef RGB_MATRIX_ENABLE

const uint8_t PROGMEM ledmap[][42][3] = {
/* Starts at layer 1; we don't apply lights to Base (layer 0). */
[_NAV] = {
MG_ORANGE, MG____RED, ___off___, ___off___, ___off___, ___off___, 				MG_ORANGE, MG___PINK, MG__WHITE, MG___PINK, MG____RED, MG_ORANGE,
MG_ORANGE, MG___BLUE, MG___BLUE, MG___BLUE, MG___BLUE, ___off___, 				MG_ORANGE, MG__WHITE, MG__WHITE, MG__WHITE, MG_ORANGE, MG_ORANGE,
MG_ORANGE, MG___PINK, ___off___, MG__GREEN, ___off___, ___off___, 				___off___, MG_YELLOW, MG___PINK, MG___PINK, MG___BLUE, MG_ORANGE,
								 ___off___, ___off___, ___off___, 				___off___, MG_ORANGE, ___off___
			},
[_NUM] = {
MG__GREEN, MG_ORANGE, ___off___, MG_YELLOW, MG_YELLOW, MG___PINK, 				MG___PINK, MG__GREEN, MG__GREEN, MG__GREEN, MG__GREEN, MG__GREEN,
MG__GREEN, MG___BLUE, MG___BLUE, MG___BLUE, MG___BLUE, ___off___, 				___off___, MG__GREEN, MG__GREEN, MG__GREEN, MG____RED, MG__GREEN,
MG__GREEN, ___off___, ___off___, MG_ORANGE, MG_ORANGE, MG_PURPLE, 				MG__GREEN, MG__GREEN, MG__GREEN, MG__GREEN, ___off___, MG__GREEN,
						   		 ___off___, MG__GREEN, ___off___, 				___off___, ___off___, ___off___
			},
[_ADJUST] = {
MG_PURPLE, ___off___, MG_PURPLE, MG____RED, MG_PURPLE, ___off___, 				MG_ORANGE, MG___BLUE, MG__WHITE, MG___BLUE, MG____RED, MG_PURPLE,
MG_PURPLE, MG___BLUE, MG___BLUE, MG___BLUE, MG___BLUE, ___off___, 				MG_ORANGE, MG__WHITE, MG__WHITE, MG__WHITE, ___off___, MG_PURPLE,
MG_PURPLE, ___off___, MG_YELLOW, MG_YELLOW, MG_YELLOW, ___off___, 				___off___, ___off___, ___off___, ___off___, ___off___, MG_PURPLE,
						   		 ___off___, MG_PURPLE, ___off___, 				___off___, MG_PURPLE, ___off___
			},
};

extern bool g_suspend_state;
extern rgb_config_t rgb_matrix_config;

void keyboard_post_init_user(void) {
    rgb_matrix_enable();
    rgb_matrix_sethsv_noeeprom(0, 0, 0); // (180, 255, 231) is purple
    rgb_matrix_mode_noeeprom(1);
}

// ====================================================
// RGB matrix
// ====================================================

uint8_t ledIndexForKeymapIndex(uint8_t keyIndex) {
	// Turn keyIndex into a row and column within g_led_config.
	// Reference: https://github.com/qmk/qmk_firmware/blob/master/keyboards/crkbd/r2g/r2g.c
	uint8_t row = 0;
	uint8_t col = 0;
	uint8_t keysPerRow = 12; // Specific to crkdb!
	uint8_t keysPerHalf = keysPerRow / 2; // Assumes equal split!

	row = keyIndex / keysPerRow;
	col = keyIndex % keysPerRow;
	if (row == 3) { // Specific to crkbd!
		col += 3; // Compensate for leading three NO_LED entries in g_led_config.
	}

	bool mirror = (col >= keysPerHalf);
	if (mirror) {
		// Normalise row and col per g_led_config structure.
		row += 4;
		col -= keysPerHalf;
		// Mirror column position.
		col = (keysPerHalf - 1) - col;
	}

	return g_led_config.matrix_co[row][col];
}

bool rgb_matrix_indicators_advanced_user(uint8_t led_min, uint8_t led_max) {

    uint8_t layerNum = get_highest_layer(layer_state);
    if (layerNum == 0) {
        rgb_matrix_set_color_all(0, 0, 0);
        return false;
    }

    // Per-key indicators
    uint8_t ledIndex = 0;
    uint8_t r, g, b;
    for (uint8_t keyIndex = 0; keyIndex < 42; keyIndex++) { // 0 to 42
        ledIndex = ledIndexForKeymapIndex(keyIndex);

        if (ledIndex >= led_min && ledIndex <= led_max) {
            r = pgm_read_byte(&ledmap[layerNum][keyIndex][0]);
            g = pgm_read_byte(&ledmap[layerNum][keyIndex][1]);
            b = pgm_read_byte(&ledmap[layerNum][keyIndex][2]);

            if (!r && !g && !b) {
                RGB_MATRIX_INDICATOR_SET_COLOR(ledIndex, 0, 0, 0);
            } else {
                RGB_MATRIX_INDICATOR_SET_COLOR(ledIndex, r, g, b);
            }
        }
    }
    /*
    // Underglow layer indicators
    uint8_t keyIndex = 36; // layer-switch key
    r = pgm_read_byte(&ledmap[layerNum][keyIndex][0]);
    g = pgm_read_byte(&ledmap[layerNum][keyIndex][1]);
    b = pgm_read_byte(&ledmap[layerNum][keyIndex][2]);
    for (uint8_t  i = 0; i < 12; i++) {
        ledIndex = (i < 6) ? i : i + 21;
        RGB_MATRIX_INDICATOR_SET_COLOR(ledIndex, r, g, b);
    }
    */

    return false;
}

#endif

// ====================================================
// Callum One-Shot Modifiers
// ====================================================
/*
bool is_oneshot_cancel_key(uint16_t keycode) {
    switch (keycode) {
    case NAV:
    case NUM:
    //case B_NUM:
    //case SPC_NAV:
    //case KC_ESC:
        return true;
    default:
        return false;
    }
}

bool is_oneshot_ignored_key(uint16_t keycode) {
    switch (keycode) {
    case NAV:
    case NUM:
    //case B_NUM:
    //case SPC_NAV:
    case KC_LSFT:
    case OS_SHFT:
    case OS_CTRL:
    case OS_ALT:
    case OS_CMD:
    case OS_CAPS:
        return true;
    default:
        return false;
    }
}

oneshot_state os_shft_state = os_up_unqueued;
oneshot_state os_ctrl_state = os_up_unqueued;
oneshot_state os_alt_state = os_up_unqueued;
oneshot_state os_cmd_state = os_up_unqueued;
oneshot_state os_caps_state = os_up_unqueued;

bool app_switch_frwd_active = false;

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    update_swapper(
        &app_switch_frwd_active, KC_LGUI, KC_TAB, APP_SWITCH_FRWD,
        keycode, record
    );

    update_oneshot(
        &os_shft_state, KC_LSFT, OS_SHFT,
        keycode, record
    );
    update_oneshot(
        &os_ctrl_state, KC_LCTL, OS_CTRL,
        keycode, record
    );
    update_oneshot(
        &os_alt_state, KC_LALT, OS_ALT,
        keycode, record
    );
    update_oneshot(
        &os_cmd_state, KC_LCMD, OS_CMD,
        keycode, record
    );
    update_oneshot(
        &os_caps_state, KC_CAPS, OS_CAPS,
        keycode, record
    );

    return true;
}
*/

layer_state_t layer_state_set_user(layer_state_t state) {
    return update_tri_layer_state(state, _NAV, _NUM, _ADJUST);
}
