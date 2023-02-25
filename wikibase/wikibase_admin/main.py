import eel
import sys

# Set web files folder
eel.init('web')

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
eel.say_hello_js('Python World!')   # Call a Javascript function


def main(argv):
    if '-w' in argv or '--web' in argv:
        eel.start('index.html', mode='electron .')
    elif '-a' in argv or '--app' in argv:
        eel.start('hello.html', mode='custom', cmdline_args=['node_modules/electron/dist/electron.exe', '.'])
    else:
        print('Usage: main.py [-w|--web] [-a|--app]')
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
