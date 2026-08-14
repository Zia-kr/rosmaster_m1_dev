from pynput.keyboard import Listener, Key

def on_press(key):
    print("PRESS:", key)

def on_release(key):
    print("RELEASE:", key)

with Listener(on_press=on_press, on_release=on_release) as l:
    l.join()