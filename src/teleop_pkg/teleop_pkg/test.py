import sys
import termios
import tty

def get_key():
    # Get the file descriptor for standard input
    fd = sys.stdin.fileno()
    
    # Save original terminal settings to restore them later
    old_settings = termios.tcgetattr(fd)
    
    try:
        # Switch terminal to cbreak mode (disables line buffering and echo)
        tty.setcbreak(fd)
        
        # Read exactly 1 byte from standard input
        key = sys.stdin.read(1)
        if key == '\x1b' :
            key +=  sys.stdin.read(2)
        return key
        
    finally:
        # Always restore the terminal to its original "cooked" state
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# Example execution loop
print("Press any key (Press 'q' to quit):")
while True:
    char = get_key()
    print(f"\rYou pressed: {repr(char)}")
    if char == 'q':
        break
