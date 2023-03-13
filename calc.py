import tkinter as tk

# colors
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"
WHITE = "#FFFFFF"
OFF_WHITE = "#F8FAFF"
LIGHT_BLUE = "#CCEDFF"

# font styles
SMALL_FONT_STYLE = ("Arial", 16)
LARGE_FONT_STYLE = ("Arial", 40, "bold")
DIGIT_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)


class Calculator:
    def __init__(self):
        # main window
        self.window = tk.Tk()

        # resolution
        self.window.geometry("375x667")

        # title bar
        self.window.title("Calculator")

        # disable resizing
        self.window.resizable(0, 0)

        # label for total expressions
        self.total_expression = ""

        # label for current expression
        self.current_expression = ""

        # frame for the display
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        # dictionary of all the possible digits and their position
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }

        # Dictionary of all the operations
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        # frame for buttons
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)

        # Fill the empty spaces
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        # call several methods
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    # take input from keyboard
    def bind_keys(self):
        # pressing the enter key is the same as pressing the equals button
        self.window.bind("<Return>", lambda event: self.evaluate())

        # loop through all the digits buttons
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        # loop through all the operators buttons
        for key in self.operations:
            self.window.bind(str(key), lambda event, operator=key: self.append_operator(operator))

    # add special buttons
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    # create labels for both total and current expressions
    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")
        return total_label, label

    # display method
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    # add the given value to the current expression
    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    # method to create the digits
    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGIT_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))

            # to place the buttons
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    # append operator symbols to the end of both current and total expression
    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression

        # clear current expression for the next entry
        self.current_expression = ""

        self.update_total_label()
        self.update_label()

    # Method to create button operators
    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            # place the buttons to the grid
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    # clear button method
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_total_label()
        self.update_label()

    # create clear button
    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        # place the buttons to the grid
        button.grid(row=0, column=1, sticky=tk.NSEW)

    # square button method
    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    # create square button
    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        # place the buttons to the grid
        button.grid(row=0, column=2, sticky=tk.NSEW)

    # square root button method
    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    # create square root button
    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        # place the buttons to the grid
        button.grid(row=0, column=3, sticky=tk.NSEW)

    # equals button method using eval()
    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()

        # handle exceptions
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""

        except Exception:
            self.current_expression = "Error"

        finally:
            self.update_label()

    # create equals button
    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        # place the buttons to the grid
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    # buttons method
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    # update the total label
    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    # update the current label
    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    # to start the app
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    # create an object of the class
    calc = Calculator()
    calc.run()
