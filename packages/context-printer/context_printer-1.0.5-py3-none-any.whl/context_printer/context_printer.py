from typing import Union


class Color:
    """
    Color class regrouping the ANSI escape sequences to print with colors and effects in console.
    """

    NONE = ''
    END = '\033[0m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'

    BLACK = '\033[30m'
    DARK_GRAY = '\033[90m'
    GRAY = '\033[37m'
    WHITE = '\033[97m'

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'

    DARK_RED = '\033[31m'
    DARK_GREEN = '\033[32m'
    DARK_YELLOW = '\033[33m'
    DARK_BLUE = '\033[34m'
    DARK_PURPLE = '\033[35m'
    DARK_CYAN = '\033[36m'

    def __add__(self, other):
        return self + other

    @staticmethod
    def text_to_color(text: str):
        if not (text.startswith('\033[') or text == ''):
            return getattr(Color, text.upper())
        else:
            return text


class ContextPrinter:
    @staticmethod
    def check_init() -> None:
        """
        Verify that the OutputDecorator is correctly initialized.
        """
        try:
            ContextPrinter.self.is_init
        except AttributeError:
            ContextPrinter.reset()
            ContextPrinter.self.is_init = True

    @staticmethod
    def self() -> None:
        """
        Does nothing, only used to store static attributes.
        """
        pass

    @staticmethod
    def reset() -> None:
        """
        Reset the parameters of the decorator.
        """
        ContextPrinter.self.headers = []
        ContextPrinter.self.activated = True
        ContextPrinter.self.max_depth = None
        ContextPrinter.self.automatic_skip = False
        ContextPrinter.self.buffered_skiplines = 0

    @staticmethod
    def __add_header(header: str, color: Color) -> None:
        """
        Adds a header to print before the text.
        :param header: header string to print.
        :param color: color of the header to print.
        """
        ContextPrinter.self.headers.append(color + header + Color.END)

    @staticmethod
    def enter_section(title: str = None, color: Union[Color, str] = Color.NONE, header: str = '█ ') -> None:
        """
        Enter a new section with the corresponding color code and prints the corresponding title.
        :param title: name of the section.
        :param color: color to use for this section.
        :param header: string to use as header for the whole section.
        """
        ContextPrinter.check_init()

        if ContextPrinter.self.activated:
            color = Color.text_to_color(color)
            if title is not None:
                ContextPrinter.print(title, color=color, bold=True)
            ContextPrinter.__add_header(header, color)

    @staticmethod
    def exit_section() -> None:
        """
        Exit the last section added.
        """
        if ContextPrinter.self.automatic_skip:
            if ContextPrinter.self.max_depth is None or ContextPrinter.self.max_depth >= len(ContextPrinter.self.headers):
                ContextPrinter.self.buffered_skiplines += 1

        if ContextPrinter.self.activated:
            ContextPrinter.self.headers = ContextPrinter.self.headers[:-1]

    @staticmethod
    def __print_line(text: str = '', color: Color = Color.NONE, bold: bool = False, underline: bool = False, blink: bool = False,
                     print_headers: bool = True, rewrite: bool = False, end: str = '\n') -> None:
        """
        Print the sections' headers and the input text line.
        :param text: text to be printed. It should be in a single line (no \n character).
        :param color: color to give to the text.
        :param bold: if set to true, prints the text in boldface.
        :param underline: if set to true, prints the text underlined.
        :param blink: if set to true, the line will be blinking (not compatible with all consoles).
        :param print_headers: if set to true, all section headers will be printed before the text.
        :param rewrite: if set to true, rewrites over the current line instead of printing a new line.
        :param end: character to print at the end of the line.
        """
        if rewrite:
            print('\r', end='')

        if print_headers:
            for header in ContextPrinter.self.headers:
                print(header, end='')

        print(color + (Color.BOLD if bold else '') + (Color.UNDERLINE if underline else '') + (Color.BLINK if blink else '') +
              text + Color.END, end=end)

    @staticmethod
    def print(text: str = '', color: Union[Color, str] = Color.NONE, bold: bool = False, underline: bool = False, blink: bool = False,
              print_headers: bool = True, rewrite: bool = False, end: str = '\n') -> None:
        """
        Print the sections' headers and the input text
        :param text: text to be printed.
        :param color: color to give to the text.
        :param bold: if set to true, prints the text in boldface.
        :param underline: if set to true, prints the text underlined.
        :param blink: if set to true, the text will be blinking (not compatible with all consoles).
        :param print_headers: if set to true, all section headers will be printed before the text.
        :param rewrite: if set to true, rewrites over the current line instead of printing a new line.
        :param end: character to print at the end of the text.
        """
        ContextPrinter.check_init()
        if ContextPrinter.self.activated and (ContextPrinter.self.max_depth is None or
                                              ContextPrinter.self.max_depth >= len(ContextPrinter.self.headers)):
            color = Color.text_to_color(color)

            if ContextPrinter.self.automatic_skip:
                prefix = '\n' * ContextPrinter.self.buffered_skiplines
                ContextPrinter.self.buffered_skiplines = 0
            else:
                prefix = ''

            lines = (prefix + text).split('\n')
            for line in lines:
                ContextPrinter.__print_line(line, color=color, bold=bold, underline=underline, blink=blink,
                                            print_headers=print_headers, rewrite=rewrite, end=end)

    @staticmethod
    def activate():
        """
        Reactivate the printer so that it gets back to work after a call to deactivate.
        """
        ContextPrinter.check_init()
        ContextPrinter.self.activated = True

    @staticmethod
    def deactivate():
        """
        Deactivate the printer so that it does not do anything (printing, entering sections, exiting sections) until reactivation.
        """
        ContextPrinter.check_init()
        ContextPrinter.self.activated = False

    @staticmethod
    def set_max_depth(value: int):
        """
        Sets a maximum number of nested sections after which the printer will stop printing (it will still be able to enter or exit
        deeper sections but without printing their title or their header at all).
        :param value: value to set to the max depth parameter.
        """
        ContextPrinter.check_init()
        ContextPrinter.self.max_depth = value

    @staticmethod
    def set_automatic_skip(value: bool):
        """
        Sets on or off the automatic skip-line mode of the printer. When it's set to True, it will automatically skip an appropriate
        number of lines when exiting a section. When set to false it will not do anything special when exiting a section.
        :param value: value to set on or off the automatic skip-line mode.
        """
        ContextPrinter.check_init()
        ContextPrinter.self.automatic_skip = value


