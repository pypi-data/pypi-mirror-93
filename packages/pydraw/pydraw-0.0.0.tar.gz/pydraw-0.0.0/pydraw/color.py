import enum;


class Color:
    """
    An immutable class that contains a color values, usually by name or RGB
    """

    def __init__(self, *args):
        if len(args) == 0 or len(args) == 2:
            raise NameError('Invalid arguments passed to color!');

        # we should expect three-four arguments for rgb or rgba
        if len(args) >= 3:
            for arg in args:
                if type(arg) is not int:
                    raise NameError('Expected integer arguments, but found \'' + str(arg) + '\' instead.');

            self.r = args[0];
            self.g = args[1];
            self.b = args[2];
            self.a = None;  # TODO: figure out what to do

            self._mode = 0;
        elif len(args) == 1:
            if type(args[0]) is tuple:
                for arg in args[0]:
                    if type(arg) is not int:
                        raise NameError('Expected integer arguments, but found \'' + str(arg) + '\' instead.');

                self.r = args[0][0];
                self.g = args[0][1];
                self.b = args[0][2];

            if type(args[0]) is not str:
                raise NameError('Expected string but instead found: ' + str(args[0]));

            string = str(args[0]);
            if string.startswith('#'):
                self._hex_value = string;
                self._mode = 2;
            else:
                self._name = string;
                self._mode = 1;

    def __value__(self):
        """
        Retrieves the value to be interpreted internally by Turtle
        :return:
        """
        if self._mode == 0:
            return self.red, self.green, self.blue;
        elif self._mode == 1:
            return self._name;
        else:
            return self._hex_value;

    @property
    def red(self):
        """
        Get the red property.
        :return: r
        """
        return self.r;

    @property
    def green(self):
        """
        Get the green propety
        :return: g
        """
        return self.g;

    @property
    def blue(self):
        """
        Get the blue property
        :return: b
        """
        return self.b;

    @property
    def alpha(self):
        """
        Get the alpha property (def=1)
        :return: a
        """
        return self.a;

    @property
    def name(self):
        """
        Get the name of the color (only if defined)
        :return: color or None
        """
        return self._name;

    @property
    def hex(self):
        """
        Get the hex of the color (only if defined)
        :return: hex_value or None
        """
        return self._hex_value;

    def __str__(self):
        if self._mode == 0:
            string = f'({self.r, self.g, self.b})';
        elif self._mode == 1:
            string = self._name;
        else:
            string = self._hex_value;

        return string;

    def __repr__(self):
        return self.__str__();
