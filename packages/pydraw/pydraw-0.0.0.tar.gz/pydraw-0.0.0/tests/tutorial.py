# PyDraw Demonstration
# Noah Coetsee

# List:
# [x] Change color to take list of arguments and interpret type.
# - Border for filled/framed option is good. (see below)
# - Color alpha needs to be finished. ** = transparency isn't possible
# [1/2] Custom method / distance(object: Object) - Returns the distance between the centers of two objects.
# [1/2] .overlaps(object: Object) method
# - Mouseclick and Keypress.
# [x] 'shift_left', 'shift_right'
# [x] object.x(x: float) -> None | Change x coordinate directly (any object);
# [x] Change coordinate access in Location class to method
# [x] Ensure canvas sizing is correct.

from pydraw import Screen, Color, Location, Rectangle, Oval, Triangle;
import time;

screen = Screen(800, 600, 'Something Awesome!');
screen.color(Color('black'));

barry = Rectangle(screen, 600, 450, 75, 75, Color('red'));
barry.border(Color('yellow'), fill=False);

mustachio = Oval(screen, screen.width() - 20, screen.height() - 20, 20, 20);
mustachio.color(Color('red'));

print(f'Screen | Width: {screen.width()}, Height: {screen.height()}');

noah = Triangle(screen, 23, 45, 35, 60, Color('green'));
noah.rotation(90);
noah.rotate(-1);

# height = mustachio.width(135);
# width = mustachio.height(135);

print(f'Mustachio\'s Color: ' + str(mustachio.color()));

pos1 = Location(0, 0);
pos2 = Location(0, 0);
time_between = 0;


def mousedown(button, location):
    print('Mousedown detected', button, location);


def keydown(key):
    print('Keydown: ' + key);

    if key == 'Up':
        barry.move(0, -10);
    elif key == 'Down':
        barry.move(0, 10);
    elif key == 'Left':
        barry.move(-10, 0);
    elif key == 'Right':
        barry.move(10, 0);


def keyup(key):
    print('Keyup: ' + key);


# mousedown, mouseup, mousedrag, mouseclick, keydown, keyup, keypress
screen.listen();

running = True;
while running:
    screen.update();
    time.sleep(30 / 1000);

screen.exit();
