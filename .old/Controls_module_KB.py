import keyboard

pressed_keys_set = set()
API_calls_set = set()
transform_EDIT = {
    'haut': 'up',
    'z': 'up',
    'gauche': 'left',
    'q': 'left',
    'bas': 'down',
    's': 'down',
    'droite': 'right',
    'd': 'right',
    'space': 'change',
    'enter': 'change_mode',
    'esc': 'quit'}
transform_RUN = {
    "ctrl": "autorun",
    'space': 'step',
    'enter': 'change_mode',
    'esc': 'quit'}


def keys_to_API(mode):
    transform(mode)
    return API_calls_set


def transform(mode):
    global API_calls_set
    API_calls_set = set()
    used_transformation = eval(f"transform_{mode}")
    for key in pressed_keys_set:
        if key in used_transformation:
            API_calls_set.add(used_transformation[key])


def keypress_callback(key: keyboard.KeyboardEvent):
    string_key = key.name
    string_event = str(key).split(' ')[-1].removesuffix(')')
    if string_event == 'up' and string_key in pressed_keys_set:
        pressed_keys_set.discard(string_key)
    elif string_event == 'down' and string_key not in pressed_keys_set:
        pressed_keys_set.add(string_key)


keyboard.hook(keypress_callback)

if __name__ == '__main__':
    while True:
        print(keys_to_API("EDIT"))
