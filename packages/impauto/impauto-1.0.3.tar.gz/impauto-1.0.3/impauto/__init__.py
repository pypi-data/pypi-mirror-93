import builtins

author = "Edhyjox"
version = "1.0.3"


class Automated:

    def __init__(self, *args, show_message=True, forever=False, force_string=True, shuffle=False):
        """
        :param args: Every automated input
        :param show_message: will show the input message in the console
        :param forever: if set to True, the value will be yield forever
        :param force_string: if set to True, will try to converted any give value to strings
        :param shuffle: shuffle the input, works with forever
        """
        if shuffle:
            self.shuffle = __import__("random").shuffle

        self.values = self.__generate_values(args, forever, shuffle)
        self.show_message = show_message
        self.force_string = force_string

        builtins.input = self.__input__

    def __generate_values(self, values, forever, shuffle):
        if self.force_string:
            try:
                values = tuple(map(str, values))
            except ValueError:
                raise ValueError("Please use only str or values that can be converted to str.")

        once = True
        while forever or once:
            if once:
                once = False

            if shuffle:
                values = list(values)
                self.shuffle(values)

            for value in values:
                yield value

        raise StopIteration("No more input values given. Make sure to have enough values passed")

    def __input__(self, __prompt=None):
        value = next(self.values)
        if self.show_message:
            print(f"[Automated] {__prompt if __prompt else ''}{value}")
        return str(value)

