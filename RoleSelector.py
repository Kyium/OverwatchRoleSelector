from tkinter import Tk, Listbox, Label, StringVar, Button, Frame, Checkbutton, IntVar, LEFT, Widget, Menu
from os import listdir
from random import sample
from datetime import datetime
from threading import Thread
from time import sleep
from typing import Dict
from json import load as json_load, dumps as json_dump_str, JSONDecodeError

from scripts.locale import Locale
from scripts.listvar import ListVar
from scripts.OptionMenu import OptionMenu

PLAYER_FILE_DIR = "./player_files/"
LOCALE_FILE_PATH = "./locales/en-gb.csv"
CONFIG_FILE_PATH = "./config.json"


class Window:
    def __init__(self, tk: Tk, player_file_dir: str, config_file_path: str, locale: Locale):
        self.root = tk
        self.player_file_dir = player_file_dir
        self.config_file_path = config_file_path
        self.loc = locale

        # config
        try:
            self.config = json_load(open(config_file_path, encoding="UTF-8"))
        except JSONDecodeError:
            self.create_config_file()
            self.config = json_load(open(config_file_path, encoding="UTF-8"))

        # Window config
        self.root.title(self.loc.g('Title'))
        self.root.config(pady=5)
        self.root.resizable(False, False)

        # clock thead
        self.__clock = Thread(target=self.__clock_thread, name="Clock thread", daemon=True)

        self.widgets: Dict[str: Widget] = {}
        self.string_vars: Dict[str: StringVar] = {}
        self.list_vars: Dict[str: ListVar] = {}
        self.int_vars: Dict[str: IntVar] = {"Tank": IntVar(self.root),
                                            "DPS_1": IntVar(self.root), "DPS_2": IntVar(self.root),
                                            "Support_1": IntVar(self.root), "Support_2": IntVar(self.root)}
        self.right_padding = 12
        self._available_player_files = []
        self.load_available_player_files()

        # Keybindings
        self.root.bind("1", lambda _: toggle_bool_int_var(self.int_vars["Tank"]))
        self.root.bind("2", lambda _: toggle_bool_int_var(self.int_vars["DPS_1"]))
        self.root.bind("3", lambda _: toggle_bool_int_var(self.int_vars["DPS_2"]))
        self.root.bind("4", lambda _: toggle_bool_int_var(self.int_vars["Support_1"]))
        self.root.bind("5", lambda _: toggle_bool_int_var(self.int_vars["Support_2"]))
        self.root.bind("<Right>", lambda _: self.add_player_to_selected())
        self.root.bind("d", lambda _: self.add_player_to_selected())
        self.root.bind("<Control_L>", lambda _: self.toggle_selected_listbox())
        self.root.bind("<Control_R>", lambda _: self.toggle_selected_listbox())
        self.root.bind("<Left>", lambda _: self.removed_player_from_selected())
        self.root.bind("a", lambda _: self.removed_player_from_selected())
        self.root.bind("<space>", lambda _: self.roll())
        self.root.bind("<Return>", lambda _: self.roll())
        self.root.bind("<Escape>", lambda _: exit(0))

    def load_available_player_files(self):
        for file in listdir(self.player_file_dir):
            if file.endswith(".plr"):
                self._available_player_files.append(file)

    def load_players(self, player_file) -> list:
        players = []
        try:
            with open(self.player_file_dir + player_file) as f:
                line = f.readline()
                while line:
                    players.append(line.rstrip())
                    line = f.readline()
        except FileNotFoundError:
            file_load_error = self.loc.g("player_file_error")
            file_load_error = file_load_error.replace("%s", player_file)
            self.string_vars["error"].set(file_load_error)
        return players

    def __clock_thread(self):
        while 1:
            self.string_vars["current_time"].set(f"{self.loc.g('current_time')} "
                                                 f"{datetime.today().time().strftime('%H:%M:%S')}")
            sleep(1)

    def toggle_selected_listbox(self):
        if self.root.focus_get() is self.widgets["available_list_box"]:
            self.widgets["selected_list_box"].focus()
            self.widgets["selected_list_box"].select_set(0)
        else:
            self.widgets["available_list_box"].focus()
            self.widgets["available_list_box"].select_set(0)

    def add_player_file_window(self):
        pass

    def remove_player_file_window(self):
        pass

    def main_window(self):
        players = self.load_players(self.config["selected_player_file"])

        # Define used variables
        self.list_vars["available"] = ListVar(self.root)
        self.list_vars["selected"] = ListVar(self.root)
        self.string_vars["output"] = StringVar(self.root)
        self.string_vars["last_roll"] = StringVar(self.root)
        self.string_vars["current_time"] = StringVar(self.root)
        self.string_vars["error"] = StringVar(self.root)
        self.string_vars["previous_output"] = StringVar(self.root)
        self.string_vars["selected_player_file"] = StringVar(self.root)

        # Assign variables values
        self.string_vars["current_time"].set(f"{self.loc.g('current_time')} -")
        self.string_vars["last_roll"].set(f"{self.loc.g('last_roll')} -")
        self.string_vars["output"].set(f"{self.loc.g('Tank')}: -\n{self.loc.g('DPS')}:"
                                       f" -\n{self.loc.g('DPS')}: -\n{self.loc.g('Support')}:"
                                       f" -\n{self.loc.g('Support')}: -")
        self.string_vars["selected_player_file"] = StringVar(self.root)
        self.string_vars["previous_output"].set(self.string_vars["output"].get())
        self.list_vars["available"].set(players)
        self.int_vars["DPS_1"].set(1)
        self.int_vars["DPS_2"].set(1)
        self.sort_list_boxes()

        # Menu
        self.widgets["menu"] = Menu(self.root)
        self.widgets["file_menu"] = Menu(self.widgets["menu"], tearoff=0)
        self.widgets["file_menu"].add_command(label="Add player file", command=self.add_player_file_window)
        self.widgets["file_menu"].add_command(label="Remove player file", command=self.remove_player_file_window)
        self.widgets["select_player_file_menu"] = OptionMenu(self.widgets["file_menu"], self._available_player_files,
                                                             "default.plr", self.string_vars["selected_player_file"],
                                                             "Select player file",
                                                             callback=self.change_selected_player_file)

        self.widgets["menu"].add_cascade(menu=self.widgets["file_menu"], label="File")
        # self.load_selectable_files_menu()

        # Define all widgets and frames
        self.widgets["available_list_box"]: Listbox = Listbox(self.root, width=20, height=10,
                                                              listvariable=self.list_vars["available"])
        self.widgets["selected_list_box"]: Listbox = Listbox(self.root, width=20, height=10,
                                                             listvariable=self.list_vars["selected"])
        self.widgets["roll_frame"] = Frame(self.root)
        self.widgets["last_roll_label"] = Label(self.widgets["roll_frame"],
                                                textvariable=self.string_vars["last_roll"])
        self.widgets["current_time_label"] = Label(self.widgets["roll_frame"],
                                                   textvariable=self.string_vars["current_time"])
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
        self.widgets["previous_rolls_label"] = Label(self.root, textvariable=self.string_vars["previous_output"],
                                                     anchor="w", justify=LEFT)
        self.widgets["separator"] = Label(self.root, text=" " * self.right_padding)
        self.widgets["current_label"] = Label(self.root, text=self.loc.g('current_roll'))
        self.widgets["previous_label"] = Label(self.root, text=self.loc.g('previous_roll'))
        self.widgets["roll_button"] = Button(self.widgets["roll_frame"], text=self.loc.g("roll_button"), width=10,
                                             command=self.roll)
        self.widgets["role_options_frame"] = Frame(self.root)
        self.widgets["roles_label"] = Label(self.root, text=self.loc.g("roles_label"))
        self.widgets["tank_checkbutton"] = Checkbutton(self.widgets["role_options_frame"], text=self.loc.g('Tank'),
                                                       variable=self.int_vars["Tank"], offvalue=0, onvalue=1)
        self.widgets["dps_1_checkbutton"] = Checkbutton(self.widgets["role_options_frame"], text=self.loc.g('DPS'),
                                                        variable=self.int_vars["DPS_1"], offvalue=0, onvalue=1, )
        self.widgets["dps_2_checkbutton"] = Checkbutton(self.widgets["role_options_frame"], text=self.loc.g('DPS'),
                                                        variable=self.int_vars["DPS_2"], offvalue=0, onvalue=1)
        self.widgets["support_1_checkbutton"] = Checkbutton(self.widgets["role_options_frame"],
                                                            text=self.loc.g('Support'),
                                                            variable=self.int_vars["Support_1"],
                                                            offvalue=0, onvalue=1)
        self.widgets["support_2_checkbutton"] = Checkbutton(self.widgets["role_options_frame"],
                                                            text=self.loc.g('Support'),
                                                            variable=self.int_vars["Support_2"],
                                                            offvalue=0, onvalue=1)
        self.widgets["error_label"] = Label(self.root, textvariable=self.string_vars["error"],
                                            fg="#AA0000", bg="#CCCCCC")

        # Display all widgets and frames
        self.widgets["available_label"].grid(column=0, row=0, padx=5, sticky="w")
        self.widgets["available_list_box"].grid(column=0, row=1, padx=5)
        self.widgets["button_frame"].grid(column=1, row=1)
        self.widgets["add_button"].grid(column=0, row=0, padx=5, pady=10)
        self.widgets["remove_button"].grid(column=0, row=1, padx=5, pady=10)
        self.widgets["selected_label"].grid(column=2, row=0, padx=5, sticky="w")
        self.widgets["selected_list_box"].grid(column=2, row=1, padx=5)
        self.widgets["separator"].grid(column=4, row=0)
        self.widgets["current_label"].grid(column=2, row=2, sticky="w", pady=5, padx=5)
        self.widgets["previous_label"].grid(column=3, row=2, sticky="w")
        self.widgets["output_frame"].grid(column=2, row=3, columnspan=2, pady=5, padx=5, sticky="w")
        self.widgets["roll_frame"].grid(column=0, row=3, pady=5, padx=5)
        self.widgets["roll_button"].grid(column=0, row=0, sticky="sn")
        self.widgets["last_roll_label"].grid(column=0, row=1)
        self.widgets["current_time_label"].grid(column=0, row=2)
        self.widgets["next_roles_label"].grid(column=0, row=0, sticky="w")
        self.widgets["previous_rolls_label"].grid(column=3, row=3, sticky="w")
        self.widgets["role_options_frame"].grid(column=3, row=1, sticky="w")
        self.widgets["roles_label"].grid(column=3, row=0, sticky="w", padx=10)
        self.widgets["tank_checkbutton"].grid(column=0, row=0, sticky="w", padx=5)
        self.widgets["dps_1_checkbutton"].grid(column=0, row=1, sticky="w", padx=5)
        self.widgets["dps_2_checkbutton"].grid(column=0, row=2, sticky="w", padx=5)
        self.widgets["support_1_checkbutton"].grid(column=0, row=3, sticky="w", padx=5)
        self.widgets["support_2_checkbutton"].grid(column=0, row=4, sticky="w", padx=5)
        self.widgets["error_label"].grid(column=0, row=4, columnspan=5, sticky="we")

        # Resize application to fit all elements
        self.root.config(menu=self.widgets["menu"])
        self.root.update()
        dimensions = self.root.grid_bbox()
        self.root.geometry(f"{dimensions[2]}x{dimensions[3]+5}")

    def create_config_file(self):
        config = {"selected_player_file": "default.plr"}
        config_data = json_dump_str(config)
        with open(self.config_file_path, "w") as f:
            f.write(config_data)

    def change_selected_player_file(self):
        self.config["selected_player_file"] = self.string_vars["selected_player_file"].get()
        self.list_vars["available"].set(self.load_players(self.config["selected_player_file"]))
        self.list_vars["selected"].set([])
        config_data = json_dump_str(self.config)
        with open(self.config_file_path, "w") as f:
            f.write(config_data)
        self.reset_ui()
        print("changed")

    def reset_ui(self):
        pass

    def load_selectable_files_menu(self):
        self.widgets["menu"].delete("File")
        self.widgets["menu"].add_cascade(menu=self.widgets["file_menu"], label="File")

    def add_player_to_selected(self):
        index = -1
        selected = self.widgets["available_list_box"].curselection()
        if len(selected) == 1:
            index = selected[0]
        elif len(self.list_vars["available"].get()) > 0:
            index = 0
        if index != -1:
            self.list_vars["selected"].append(self.list_vars["available"].select(index))
            self.list_vars["available"].remove(index)
            self.sort_list_boxes()

    def removed_player_from_selected(self):
        index = -1
        selected = self.widgets["selected_list_box"].curselection()
        if len(selected) == 1:
            index = selected[0]
        elif len(self.list_vars["selected"].get()) > 0:
            index = 0
        if index != -1:
            self.list_vars["available"].append(self.list_vars["selected"].select(index))
            self.list_vars["selected"].remove(index)
            self.sort_list_boxes()

    def sort_list_boxes(self):
        self.list_vars["selected"].sort()
        self.list_vars["available"].sort()

    def start(self):
        self.main_window()
        self.__clock.start()
        self.root.mainloop()

    def roll(self):
        selected = self.list_vars["selected"].get()
        roll_count = self.get_roll_selected_count()
        if len(selected) >= roll_count:
            index = 0
            output_string = ""
            result = sample(selected, roll_count)

            if self.int_vars["Tank"].get():
                output_string += f"{self.loc.g('Tank')}: {result[index]}\n"
                index += 1
            else:
                output_string += f"{self.loc.g('Tank')}: -\n"

            if self.int_vars["DPS_1"].get():
                output_string += f"{self.loc.g('DPS')}: {result[index]}\n"
                index += 1
            else:
                output_string += f"{self.loc.g('DPS')}: -\n"

            if self.int_vars["DPS_2"].get():
                output_string += f"{self.loc.g('DPS')}: {result[index]}\n"
                index += 1
            else:
                output_string += f"{self.loc.g('DPS')}: -\n"

            if self.int_vars["Support_1"].get():
                output_string += f"{self.loc.g('Support')}: {result[index]}\n"
                index += 1
            else:
                output_string += f"{self.loc.g('Support')}: -\n"

            if self.int_vars["Support_2"].get():
                output_string += f"{self.loc.g('Support')}: {result[index]}"
                index += 1
            else:
                output_string += f"{self.loc.g('Support')}: -"

            self.string_vars["error"].set("")
            if index > 0:
                self.string_vars["last_roll"].set(f"{self.loc.g('last_roll')} "
                                                  f"{datetime.today().time().strftime('%H:%M:%S')}")
                self.string_vars["current_time"].set(f"{self.loc.g('current_time')} "
                                                     f"{datetime.today().time().strftime('%H:%M:%S')}")
            else:
                self.string_vars["error"].set(self.loc.g('role_count_error'))
            self.string_vars["previous_output"].set(self.string_vars["output"].get())
            self.string_vars["output"].set(output_string)

        else:
            required_count = roll_count - len(selected)
            error_str = f"{self.loc.g('player_count_error')}"
            error_str = error_str.replace("%s", str(required_count))
            self.string_vars["error"].set(error_str)

    def get_roll_selected_count(self) -> int:
        count = 0
        for roll in self.int_vars.values():
            count += roll.get()
        return count


def toggle_bool_int_var(int_var: IntVar):
    int_var.set(not int_var.get())


if __name__ == '__main__':
    main = Window(Tk(), PLAYER_FILE_DIR, CONFIG_FILE_PATH, Locale(LOCALE_FILE_PATH))
    main.start()
