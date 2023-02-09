from tkinter import Tk, Listbox, Label, StringVar, Button, Frame, Checkbutton, IntVar, LEFT
from random import sample
from datetime import datetime

from scripts.locale import Locale
from scripts.listvar import ListVar

PLAYER_FILE_PATH = "./players.txt"
LOCALE_FILE_PATH = "./locales/en-gb.csv"


class Window:
    def __init__(self, tk: Tk, player_file_path: str, locale: Locale):
        self.root = tk
        self.player_file_path = player_file_path
        self.loc = locale

        # Window config
        self.root.title(self.loc.g('Title'))
        self.root.config(pady=5)
        self.root.resizable(False, False)

        self.widgets = {}
        self.int_vars = {}
        self.string_vars = {}
        self.list_vars = {}
        self.roles_selected = {"Tank": IntVar(self.root),
                               "DPS_1": IntVar(self.root), "DPS_2": IntVar(self.root),
                               "Support_1": IntVar(self.root), "Support_2": IntVar(self.root)}

        # Keybindings
        self.root.bind("1", lambda _: toggle_bool_int_var(self.roles_selected["Tank"]))
        self.root.bind("2", lambda _: toggle_bool_int_var(self.roles_selected["DPS_1"]))
        self.root.bind("3", lambda _: toggle_bool_int_var(self.roles_selected["DPS_2"]))
        self.root.bind("4", lambda _: toggle_bool_int_var(self.roles_selected["Support_1"]))
        self.root.bind("5", lambda _: toggle_bool_int_var(self.roles_selected["Support_2"]))
        self.root.bind("<Right>", lambda _: self.add_player_to_selected())
        self.root.bind("d", lambda _: self.add_player_to_selected())
        self.root.bind("<Control_L>", lambda _: self.toggle_selected_listbox())
        self.root.bind("<Control_R>", lambda _: self.toggle_selected_listbox())
        self.root.bind("<Left>", lambda _: self.removed_player_from_selected())
        self.root.bind("a", lambda _: self.removed_player_from_selected())
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
            self.string_vars["error"].set(self.loc.g("player_file_error"))
        return players

    def toggle_selected_listbox(self):
        if self.root.focus_get() is self.widgets["available_list_box"]:
            self.widgets["selected_list_box"].focus()
        else:
            self.widgets["available_list_box"].focus()

    def main_window(self):
        self.list_vars["available"] = ListVar(self.root)
        self.widgets["available_list_box"] = Listbox(self.root, width=20, height=10,
                                                     listvariable=self.list_vars["available"])
        self.list_vars["selected"] = ListVar(self.root)
        self.widgets["selected_list_box"] = Listbox(self.root, width=20, height=10,
                                                    listvariable=self.list_vars["selected"])
        self.string_vars["output"] = StringVar(self.root)
        self.string_vars["last_roll"] = StringVar(self.root)
        self.string_vars["last_roll"].set(f"{self.loc.g('last_roll')} -")
        self.string_vars["output"].set(f"{self.loc.g('Tank')}: -\n{self.loc.g('DPS')}:"
                                       f" -\n{self.loc.g('DPS')}: -\n{self.loc.g('Support')}:"
                                       f" -\n{self.loc.g('Support')}: -")
        self.roles_selected["DPS_1"].set(1)
        self.roles_selected["DPS_2"].set(1)
        self.widgets["roll_frame"] = Frame(self.root)
        self.widgets["last_roll_label"] = Label(self.widgets["roll_frame"],
                                                textvariable=self.string_vars["last_roll"])
        self.string_vars["error"] = StringVar()

        players = self.load_players()

        self.list_vars["available"].set(players)
        self.widgets["available_label"] = Label(self.root, text=self.loc.g("available_label"))
        self.widgets["button_frame"] = Frame(self.root)
        self.widgets["add_button"] = Button(self.widgets["button_frame"], text=">>",
                                            command=self.add_player_to_selected)
        self.widgets["remove_button"] = Button(self.widgets["button_frame"], text="<<",
                                               command=self.removed_player_from_selected)
        self.widgets["selected_label"] = Label(self.root, text=self.loc.g("selected_label"))
        self.widgets["output_frame"] = Frame(self.root)
        self.widgets["next_roles_label"] = Label(self.widgets["output_frame"],
                                                 textvariable=self.string_vars["output"],
                                                 anchor="w", justify=LEFT)
        self.widgets["roll_button"] = Button(self.widgets["roll_frame"], text=self.loc.g("roll_button"), width=10,
                                             command=self.roll)
        self.widgets["role_options_frame"] = Frame(self.root)
        self.widgets["roles_label"] = Label(self.root, text=self.loc.g("roles_label"))
        self.widgets["tank_checkbutton"] = Checkbutton(self.widgets["role_options_frame"], text=self.loc.g('Tank'),
                                                       variable=self.roles_selected["Tank"], offvalue=0, onvalue=1)
        self.widgets["dps_1_checkbutton"] = Checkbutton(self.widgets["role_options_frame"], text=self.loc.g('DPS'),
                                                        variable=self.roles_selected["DPS_1"], offvalue=0, onvalue=1, )
        self.widgets["dps_2_checkbutton"] = Checkbutton(self.widgets["role_options_frame"], text=self.loc.g('DPS'),
                                                        variable=self.roles_selected["DPS_2"], offvalue=0, onvalue=1)
        self.widgets["support_1_checkbutton"] = Checkbutton(self.widgets["role_options_frame"],
                                                            text=self.loc.g('Support'),
                                                            variable=self.roles_selected["Support_1"],
                                                            offvalue=0, onvalue=1)
        self.widgets["support_2_checkbutton"] = Checkbutton(self.widgets["role_options_frame"],
                                                            text=self.loc.g('Support'),
                                                            variable=self.roles_selected["Support_2"],
                                                            offvalue=0, onvalue=1)
        self.widgets["error_label"] = Label(self.root, textvariable=self.string_vars["error"],
                                            fg="#AA0000", bg="#CCCCCC")

        self.widgets["available_label"].grid(column=0, row=0, padx=5, sticky="w")
        self.widgets["available_list_box"].grid(column=0, row=1, padx=5)
        self.widgets["button_frame"].grid(column=1, row=1)
        self.widgets["add_button"].grid(column=0, row=0, padx=5, pady=10)
        self.widgets["remove_button"].grid(column=0, row=1, padx=5, pady=10)
        self.widgets["selected_label"].grid(column=2, row=0, padx=5, sticky="w")
        self.widgets["selected_list_box"].grid(column=2, row=1, padx=5)
        self.widgets["output_frame"].grid(column=2, row=2, columnspan=2, pady=5, padx=5, sticky="w")
        self.widgets["roll_frame"].grid(column=0, row=2, pady=5, padx=5)
        self.widgets["roll_button"].grid(column=0, row=0, sticky="sn")
        self.widgets["last_roll_label"].grid(column=0, row=1)
        self.widgets["next_roles_label"].grid(column=0, row=0, sticky="w")
        self.widgets["role_options_frame"].grid(column=3, row=1)
        self.widgets["roles_label"].grid(column=3, row=0, sticky="w")
        self.widgets["tank_checkbutton"].grid(column=0, row=0, sticky="w", padx=5)
        self.widgets["dps_1_checkbutton"].grid(column=0, row=1, sticky="w", padx=5)
        self.widgets["dps_2_checkbutton"].grid(column=0, row=2, sticky="w", padx=5)
        self.widgets["support_1_checkbutton"].grid(column=0, row=3, sticky="w", padx=5)
        self.widgets["support_2_checkbutton"].grid(column=0, row=4, sticky="w", padx=5)
        self.widgets["error_label"].grid(column=0, row=3, columnspan=5, sticky="we")

        self.root.update()
        dimensions = self.root.grid_bbox()
        self.root.geometry(f"{dimensions[2]}x{dimensions[3]}")

    def add_player_to_selected(self):
        selected = self.widgets["available_list_box"].curselection()
        if len(selected) == 1:
            index = selected[0]
            self.list_vars["selected"].append(self.list_vars["available"].select(index))
            self.list_vars["available"].remove(index)
            self.sort_list_boxes()

    def removed_player_from_selected(self):
        selected = self.widgets["selected_list_box"].curselection()
        if len(selected) == 1:
            index = selected[0]
            self.list_vars["available"].append(self.list_vars["selected"].select(index))
            self.list_vars["selected"].remove(index)
            self.sort_list_boxes()

    def sort_list_boxes(self):
        self.list_vars["selected"].sort()
        self.list_vars["available"].sort()

    def start(self):
        self.main_window()
        self.root.mainloop()

    def roll(self):
        selected = self.list_vars["selected"].get()
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
                output_string += f"{self.loc.g('DPS')}: {result[index]}\n"
                index += 1
            else:
                output_string += f"{self.loc.g('DPS')}: -\n"

            if self.roles_selected["DPS_2"].get():
                output_string += f"{self.loc.g('DPS')}: {result[index]}\n"
                index += 1
            else:
                output_string += f"{self.loc.g('DPS')}: -\n"

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

            self.string_vars["error"].set("")
            if index > 0:
                self.string_vars["last_roll"].set(f"{self.loc.g('last_roll')} "
                                                  f"{datetime.today().time().strftime('%H:%M:%S')}")
            else:
                self.string_vars["error"].set(self.loc.g('role_count_error'))
            self.string_vars["output"].set(output_string)

        else:
            required_count = roll_count - len(selected)
            self.string_vars["error"].set(f"{self.loc.g('player_count_error')}" % required_count)

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
