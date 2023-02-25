import eel

eel.init('web')

@eel.expose
def say_hello():
    return "Hello from Python"

eel.start('index.html', size=(300, 200))
