from tkinter import Tk, Listbox, Label, StringVar, Button, Frame, Checkbutton, IntVar, LEFT, Scrollbar
from json import loads
from random import sample
from datetime import datetime

PLAYER_FILE_PATH = "./players.txt"
LOCALE_FILE_PATH = "./locales/en-gb.csv"


class ListVar(StringVar):
    def __init__(self, *args):
        super().__init__(*args)

    def set(self, lst: list):
        super().set(tuple(lst))

    def get(self) -> list:
        result = list(super().get())
        if len(result) == 0:
            return list()
        result[0] = "["
        result[len(result) - 1] = "]"
        result = list(map(lambda x: x.replace("\'", "\""), result))
        result = "".join(result)
        if result.endswith(",]"):
            result = result[:-2]
            result += "]"
        decoded = loads(result)
        return decoded

    def append(self, item):
        tmp = self.get()
        tmp.append(item)
        self.set(tmp)

    def remove(self, index: int):
        tmp = self.get()
        tmp.pop(index)
        self.set(tmp)

    def select(self, index: int):
        return self.get()[index]

    def sort(self):
        tmp = self.get()
        tmp.sort()
        self.set(tmp)


class Locale:
    def __init__(self, locale_file_path: str):
        self.locale_file_path = locale_file_path
        self.lookup_dict = {}
        self.load_locale()

    def load_locale(self):
        try:
            with open(self.locale_file_path) as f:
                line = f.readline()
                while line:
                    try:
                        key, value = line.rstrip().split(",")
                    except ValueError:
                        pass
                    self.lookup_dict[key] = value
                    line = f.readline()
        except FileNotFoundError:
            pass

    def g(self, key: str) -> str:
        try:
            return self.lookup_dict[key]
        except KeyError:
            return "???"


class Window:
    def __init__(self, tk: Tk, player_file_path: str, locale: Locale):
        self.root = tk
        self.player_file_path = player_file_path
        self.loc = locale
        self.root.title(self.loc.g('Title'))
        self.root.config(pady=5)
        self.root.resizable(False, False)

        self.available_list_var = ListVar(self.root)
        self.available_list_box = Listbox(self.root, width=20, height=10, listvariable=self.available_list_var)
        self.selected_list_var = ListVar(self.root)
        self.selected_list_box = Listbox(self.root, width=20, height=10, listvariable=self.selected_list_var)
        self.output_text_var = StringVar(self.root)
        self.last_roll_text_var = StringVar(self.root)
        self.last_roll_text_var.set(f"{self.loc.g('last_roll')} -")
        self.output_text_var.set(f"{self.loc.g('Tank')}: -\n{self.loc.g('DPS')}: -\n{self.loc.g('Tank')}: -\n"
                                 f"{self.loc.g('Support')}: -\n{self.loc.g('Support')}: -")

        self.roles_selected = {"Tank": IntVar(self.root),
                               "DPS_1": IntVar(self.root), "DPS_2": IntVar(self.root),
                               "Support_1": IntVar(self.root), "Support_2": IntVar(self.root)}
        self.roles_selected["DPS_1"].set(1)
        self.roles_selected["DPS_2"].set(1)
        self.roll_frame = Frame(self.root)
        self.last_roll_label = Label(self.roll_frame, textvariable=self.last_roll_text_var)
        self.error_text_var = StringVar()

        self.root.bind("1", lambda _: toggle_bool_int_var(self.roles_selected["Tank"]))
        self.root.bind("2", lambda _: toggle_bool_int_var(self.roles_selected["DPS_1"]))
        self.root.bind("3", lambda _: toggle_bool_int_var(self.roles_selected["DPS_2"]))
        self.root.bind("4", lambda _: toggle_bool_int_var(self.roles_selected["Support_1"]))
        self.root.bind("5", lambda _: toggle_bool_int_var(self.roles_selected["Support_2"]))
        self.root.bind("<Right>", lambda _: self.add_player_to_selected())
        self.root.bind("<Control_L>", lambda _: self.toggle_selected_listbox())
        self.root.bind("<Control_R>", lambda _: self.toggle_selected_listbox())
        self.root.bind("<Left>", lambda _: self.removed_player_from_selected())
        self.root.bind("<space>", lambda _: self.roll())
        self.root.bind("<Return>", lambda _: self.roll())
        self.root.bind("<Escape>", lambda _: exit(0))

    def load_players(self) -> list:
        players = []
        try:
            with open(self.player_file_path) as f:
                line = f.readline()
                while line:
                    players.append(line.rstrip())
                    line = f.readline()
        except FileNotFoundError:
            self.error_text_var.set(self.loc.g("player_file_error"))
        return players

    def toggle_selected_listbox(self):
        if self.root.focus_get() is self.available_list_box:
            self.selected_list_box.focus()
        else:
            self.available_list_box.focus()

    def main_window(self):
        players = self.load_players()
        self.available_list_var.set(players)
        available_label = Label(self.root, text=self.loc.g("available_label"))
        button_frame = Frame(self.root)
        add_button = Button(button_frame, text=">>", command=self.add_player_to_selected)
        remove_button = Button(button_frame, text="<<", command=self.removed_player_from_selected)
        selected_label = Label(self.root, text=self.loc.g("selected_label"))
        output_frame = Frame(self.root)
        next_roles_label = Label(output_frame, textvariable=self.output_text_var, anchor="w", justify=LEFT)
        roll_button = Button(self.roll_frame, text=self.loc.g("roll_button"), width=10, command=self.roll)
        role_options_frame = Frame(self.root)
        roles_label = Label(self.root, text=self.loc.g("roles_label"))
        tank_checkbutton = Checkbutton(role_options_frame, text=self.loc.g('Tank'),
                                       variable=self.roles_selected["Tank"], offvalue=0, onvalue=1)
        dps_1_checkbutton = Checkbutton(role_options_frame, text=self.loc.g('DPS'),
                                        variable=self.roles_selected["DPS_1"], offvalue=0, onvalue=1, )
        dps_2_checkbutton = Checkbutton(role_options_frame, text=self.loc.g('DPS'),
                                        variable=self.roles_selected["DPS_2"], offvalue=0, onvalue=1)
        support_1_checkbutton = Checkbutton(role_options_frame, text=self.loc.g('Support'),
                                            variable=self.roles_selected["Support_1"], offvalue=0, onvalue=1)
        support_2_checkbutton = Checkbutton(role_options_frame, text=self.loc.g('Support'),
                                            variable=self.roles_selected["Support_2"], offvalue=0, onvalue=1)
        error_label = Label(self.root, textvariable=self.error_text_var, fg="#AA0000", bg="#CCCCCC")

        available_label.grid(column=0, row=0, padx=5, sticky="w")
        self.available_list_box.grid(column=0, row=1, padx=5)
        button_frame.grid(column=1, row=1)
        add_button.grid(column=0, row=0, padx=5, pady=10)
        remove_button.grid(column=0, row=1, padx=5, pady=10)
        selected_label.grid(column=2, row=0, padx=5, sticky="w")
        self.selected_list_box.grid(column=2, row=1, padx=5)
        output_frame.grid(column=2, row=2, columnspan=2, pady=5, padx=5, sticky="w")
        self.roll_frame.grid(column=0, row=2, pady=5, padx=5)
        roll_button.grid(column=0, row=0, sticky="sn")
        self.last_roll_label.grid(column=0, row=1)
        next_roles_label.grid(column=0, row=0, sticky="w")
        role_options_frame.grid(column=3, row=1)
        roles_label.grid(column=3, row=0, sticky="w")
        tank_checkbutton.grid(column=0, row=0, sticky="w", padx=5)
        dps_1_checkbutton.grid(column=0, row=1, sticky="w", padx=5)
        dps_2_checkbutton.grid(column=0, row=2, sticky="w", padx=5)
        support_1_checkbutton.grid(column=0, row=3, sticky="w", padx=5)
        support_2_checkbutton.grid(column=0, row=4, sticky="w", padx=5)
        error_label.grid(column=0, row=3, columnspan=5, sticky="we")

        self.root.update()
        dimensions = self.root.grid_bbox()
        self.root.geometry(f"{dimensions[2]}x{dimensions[3]}")

    def add_player_to_selected(self):
        selected = self.available_list_box.curselection()
        if len(selected) == 1:
            index = selected[0]
            self.selected_list_var.append(self.available_list_var.select(index))
            self.available_list_var.remove(index)
            self.sort_list_boxes()

    def removed_player_from_selected(self):
        selected = self.selected_list_box.curselection()
        if len(selected) == 1:
            index = selected[0]
            self.available_list_var.append(self.selected_list_var.select(index))
            self.selected_list_var.remove(index)
            self.sort_list_boxes()

    def sort_list_boxes(self):
        self.selected_list_var.sort()
        self.available_list_var.sort()

    def start(self):
        self.main_window()
        self.root.mainloop()

    def roll(self):
        selected = self.selected_list_var.get()
        roll_count = self.get_roll_selected_count()
        if len(selected) >= roll_count:
            index = 0
            output_string = ""
            result = sample(selected, roll_count)

            if self.roles_selected["Tank"].get():
                output_string += f"{self.loc.g('Tank')}: {result[index]}\n"
                index += 1
            else:
                output_string += f"{self.loc.g('Tank')}: -\n"

            if self.roles_selected["DPS_1"].get():
                output_string += f"{self.loc.g('Tank')}: {result[index]}\n"
                index += 1
            else:
                output_string += f"{self.loc.g('Tank')}: -\n"

            if self.roles_selected["DPS_2"].get():
                output_string += f"{self.loc.g('Tank')}: {result[index]}\n"
                index += 1
            else:
                output_string += f"{self.loc.g('Tank')}: -\n"

            if self.roles_selected["Support_1"].get():
                output_string += f"{self.loc.g('Support')}: {result[index]}\n"
                index += 1
            else:
                output_string += f"{self.loc.g('Support')}: -\n"

            if self.roles_selected["Support_2"].get():
                output_string += f"{self.loc.g('Support')}: {result[index]}"
                index += 1
            else:
                output_string += f"{self.loc.g('Support')}: -"

            self.error_text_var.set("")
            if index > 0:
                self.last_roll_text_var.set(f"{self.loc.g('last_roll')} "
                                            f"{datetime.today().time().strftime('%H:%M:%S')}")
            else:
                self.error_text_var.set(self.loc.g('role_count_error'))
            self.output_text_var.set(output_string)

        else:
            required_count = roll_count - len(selected)
            self.error_text_var.set(f"{self.loc.g('player_count_error')}" % required_count)

    def get_roll_selected_count(self) -> int:
        count = 0
        for roll in self.roles_selected.values():
            count += roll.get()
        return count


def toggle_bool_int_var(int_var: IntVar):
    int_var.set(not int_var.get())


if __name__ == '__main__':
    tk_root = Tk()
    main = Window(tk_root, PLAYER_FILE_PATH, Locale(LOCALE_FILE_PATH))
    main.start()
