"""
Objects in the PyDraw library

No hiding spots here (for semicolons)
"""
import turtle;
from pydraw import Screen;
from pydraw import Location;
from pydraw import Color;

PIXEL_RATIO = 20;

class Object:
    """
    A base object containing a location and screen. This ensures coordinates are
    done with the root at the top left corner, and not at the center.
    """

    def __init__(self, screen: Screen, x: float = 0, y: float = 0, location: Location = None):
        self.screen = screen;
        self.location = location if location is not None else Location(x, y);

        self.ref = turtle.Turtle();
        self.ref.hideturtle();
        self.ref.penup();

    def x(self, x: float = None) -> float:
        if x is not None:
            self.moveto(x, self.y());

        return self.location.x();

    def y(self, y: float = None) -> float:
        if y is not None:
            self.moveto(self.x(), y);

        return self.location.y();

    def move(self, dx: float, dy: float) -> None:
        self.location.move(dx, dy);
        self.update();

    def moveto(self, x: float, y: float) -> None:
        self.location.moveto(x, y);
        self.update();

    def update(self) -> None:
        real_x = self.x() + self.width() / 2 - (self.screen.width() / 2);
        real_y = -self.y() + self.screen.height() / 2 - self.height() / 2;

        self.ref.goto(real_x, real_y);


class Renderable(Object):
    """
    A base class storing most useful methods for 2D Renderable objects.
    """

    def __init__(self, screen: Screen, x: float = 0, y: float = 0, width: float = 10, height: float = 10,
                 color: Color = Color('black'),
                 border: Color = None,
                 fill: bool = True,
                 location: Location = None):
        super().__init__(screen, x, y, location);

        # TODO: check_parameters(x, y, width, height)

        self._width = width;
        self._height = height;

        self._angle = 0;  # default angle to zero degrees

        self.ref.shape('square');
        self.ref.shapesize(stretch_wid=height / PIXEL_RATIO, stretch_len=width / PIXEL_RATIO);

        self._color = color;
        self._border = border;
        self.ref.color(color.__value__());

        self._fill = fill;

        self.ref.showturtle();
        self.update();

    def width(self, width: float = None) -> float:
        """
        Get or set the width of the object.
        :param width: the width to set to in pixels, if any
        :return: the width of the object
        """

        if width is not None:
            self._width = width;
            self.update();

        return self._width;

    def height(self, height: float = None) -> float:
        """
        Get or set the height of the object
        :param height: the height to set to in pixels, if any
        :return: the height of the object
        """

        if height is not None:
            self._height = height;
            self.update();

        return self._height;

    def color(self, color: Color = None) -> Color:
        """
        Get or set the color of the object
        :param color: the color to set to, if any
        :return: the color of the object
        """

        if color is not None:
            self._color = color;
            self.update();

        return self._color;

    def rotation(self, angle: float = None) -> float:
        """
        Get or set the rotation of the object.
        :param angle: the angle to set the rotation to in degrees, if any
        :return: the angle of the object's rotation in degrees
        """

        if angle is not None:
            self._angle = angle;
            self.update();

        return self._angle;

    def rotate(self, angle_diff: float = 0) -> None:
        """
        Rotate the angle of the object by a difference, in degrees
        :param angle_diff: the angle difference to rotate by
        :return: None
        """

        self.rotation(self._angle - angle_diff);

    def border(self, color: Color = None, fill: bool = None) -> Color:
        """
        Add or get the border of the object
        :param color: the color to set the border too, set to None to remove border
        :param fill: whether or not to fill the polygon.
        :return: The Color of the border
        """

        update = False;

        if color is not None:
            self._border = color;
            update = True;
        if fill is not None:
            self._fill = fill;
            update = True;

        if update:
            self.update();

        # TODO: We can create a second object here to act as a "border", or we can see what tkinter has in store...
        return self._border;

    def distance(self, renderable) -> float:
        """
        Returns the distance between two objects in pixels
        :param renderable: the Renderable to check distance between
        :return: the distance between this object and the passed Renderable.
        """

        return self.ref.distance(renderable.ref) * PIXEL_RATIO;

    def overlaps(self, renderable) -> bool:
        """
        Returns if this object is overlapping with the passed object.
        :param renderable: another Renderable instance.
        :return: true if they are overlapping, false if not.
        """

        # This should work regardless of rotations, but keep an eye on this.
        # Average width and height for "oblong shapes" as to be as close as possible.

        min_ax = self.x();
        max_ax = self.x() + self.width();

        min_bx = renderable.x();
        max_bx = renderable.x() + renderable.width();

        min_ay = self.y();
        max_ay = self.y() + self.height();

        min_by = renderable.y();
        max_by = renderable.y() + renderable.height();

        a_left_b = max_ax < min_bx;
        a_right_b = min_ax > max_bx;
        a_above_b = min_ay > max_by;
        a_below_b = max_ay < min_by;

        if self._angle != 0:
            return self.ref.distance(renderable.ref) <= ((self.width + self.height) / 2) / 2;
        return not (a_left_b or a_right_b or a_above_b or a_below_b)

    def update(self) -> None:
        """
        Update the internal reference of the object.
        :return: None
        """

        # noinspection PyBroadException
        try:
            super().update();
            self.ref.shapesize(stretch_wid=self.height() / PIXEL_RATIO, stretch_len=self.width() / PIXEL_RATIO);
            self.ref.setheading(self._angle);

            if self._fill is True:
                if self._border is not None:
                    self.ref.color(self._border.__value__(), self._color.__value__());
                else:
                    self.ref.color(self._color.__value__());
            elif self._border is not None:
                self.ref.color(None);
                self.ref.color(self._border.__value__(), None);
            else:
                raise NameError('Fill was set to false but no border was passed.');

        except:
            pass;  # debug('Termination likely, but an internal error may have occurred');


class Rectangle(Renderable):
    def __init__(self, screen: Screen, x: float = 0, y: float = 0, width: float = 10, height: float = 10,
                 color: Color = Color('black'),
                 location: Location = None):
        super().__init__(screen, x, y, width, height, color, location);
        self.ref.shape('square');


class Oval(Renderable):
    def __init__(self, screen: Screen, x: float = 0, y: float = 0, width: float = 10, height: float = 10,
                 color: Color = Color('black'),
                 location: Location = None):
        super().__init__(screen, x, y, width, height, color, location);
        self.ref.shape('circle');


class Triangle(Renderable):
    def __init__(self, screen: Screen, x: float = 0, y: float = 0, width: float = 10, height: float = 10,
                 color: Color = Color('black'),
                 location: Location = None):
        super().__init__(screen, x, y, width, height, color, location);
        self.ref.shape('triangle');
