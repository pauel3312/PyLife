import keyboard

pressed_keys_set = set()


# TODO: transform method for the set to meet the API command spec
def keys_to_API(mode):
    print(mode)


def keypress_callback(key):
    string_key, string_event = str(key).split('(')[1].strip(')').split(' ')
    if string_event == 'up' and string_key in pressed_keys_set:
        pressed_keys_set.discard(string_key)
    elif string_event == 'down' and string_key not in pressed_keys_set:
        pressed_keys_set.add(string_key)


keyboard.hook(keypress_callback)

if __name__ == '__main__':
    while True:
        print(pressed_keys_set)
