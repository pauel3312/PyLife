import keyboard
from functools import partial

was_pressed = False


# TODO: Make a setup method for the API: one per mode that are called to set the `on_press_key`s and `on_release_key`s
def keys_to_API(mode):
    global was_pressed
    print(mode)
    was_pressed = True
    # TODO: return the global key presses set, converted to comply with the API spec.

# TODO: Callback method for the key presses, so they come to a global set object


keyboard.on_press_key('ctrl', keys_to_API)

while not was_pressed:
    None
