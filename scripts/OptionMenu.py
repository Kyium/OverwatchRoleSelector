from tkinter import Menu, Tk, StringVar, Button
from typing import List
from functools import partial
from typing import Callable


class OptionMenu:
    def __init__(self, master_menu: Menu, options: List[str], default_option: str, variable: StringVar, name: str,
                 callback: Callable = None, callback_args: tuple = ()):
        self.master_menu = master_menu
        self.options = options
        self.selected_option = default_option
        self.previous_option = ""
        self.variable = variable
        self.name = name
        self.callback = callback
        self.callback_args = callback_args

        self.loaded = False

        self.menu = Menu(self.master_menu, tearoff=0)
        self.reload()
        self.variable.set(self.selected_option)

    def reload(self):
        if self.loaded:
            self.master_menu.delete(self.name)
            self.menu = Menu(self.master_menu, tearoff=0)
        self.master_menu.add_cascade(menu=self.menu, label=self.name)
        for option in self.options:
            self.menu.add_command(label=f"{option} {'✓' if option == self.selected_option else ''}",
                                  command=partial(self.__option_press, option))
        self.loaded = True

    def get_menu(self):
        return self.menu

    def __option_press(self, option: str):
        if option != self.selected_option:
            self.previous_option = self.selected_option
            self.selected_option = option
            self.variable.set(self.selected_option)
            self.reload()
            if self.callback is not None:
                partial(self.callback, *self.callback_args)()


if __name__ == '__main__':
    tk = Tk()
    main = Menu(tk)
    var = StringVar()
    test = OptionMenu(main, ["1", "2", "3"], "1", var, "test")
    tk.config(menu=main)
    Button(tk, text="Reload", command=test.reload).pack()
    tk.mainloop()
