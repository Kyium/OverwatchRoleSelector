from tkinter import Tk, Toplevel, Label, Entry, Button, Listbox, StringVar, Frame, OptionMenu
from string import punctuation
from os import listdir
from typing import Callable

from scripts.listvar import ListVar
from CreateDeafaultPlayerFile import create_default_player_file


PLAYER_FILE_DIR = "../../player_files/"


class PlayerFileManager:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Player File Manager")

        self.players_list_var = ListVar(self.root)
        self.new_player_string_var = StringVar(self.root)
        self.error_string_var = StringVar(self.root)
        self.selected_player_file = StringVar(self.root)

        self.selected_player_file.set("default.plr")

        self.new_file_name = ""

        self.player_files = []
        self.discover_player_files()

        self.player_label = Label(self.root, text="Players: ")
        self.player_listbox = Listbox(self.root, listvariable=self.players_list_var)

        player_files = self.player_files.copy()
        self.player_files.remove("default.plr")
        self.file_picker_frame = Frame(self.root)
        self.file_label = Label(self.file_picker_frame, text="File:")
        self.select_player_file_option_menu = OptionMenu(self.file_picker_frame, self.selected_player_file,
                                                         "default.plr", *player_files,
                                                         command=lambda _: self.file_changed())
        self.add_player_frame = Frame(self.root)
        self.new_player_entry = Entry(self.add_player_frame, textvariable=self.new_player_string_var)
        self.add_new_player_button = Button(self.add_player_frame, text="Add", command=self.add_new_player)
        self.button_frame = Frame(self.root)
        self.remove_player_button = Button(self.button_frame, text="Remove", command=self.remove_player)
        self.save_button = Button(self.button_frame, text="Save", command=self.save_file)

        self.error_label = Label(self.root, textvariable=self.error_string_var, fg="#AA0000", bg="#CCCCCC")

    def discover_player_files(self):
        dir_list = listdir(PLAYER_FILE_DIR)
        if "default.plr" not in dir_list:
            create_default_player_file()
        for file in dir_list:
            if file.endswith(".plr"):
                self.player_files.append(file)

    def main(self):
        self.file_picker_frame.grid(column=0, row=0, padx=5, pady=5)
        self.file_label.grid(column=0, row=0, padx=5)
        self.select_player_file_option_menu.grid(column=1, row=0)
        self.player_label.grid(column=1, row=0, sticky="w")
        self.player_listbox.grid(column=1, row=1, padx=5, sticky="w")
        self.add_player_frame.grid(column=0, row=2, pady=5)
        self.new_player_entry.grid(column=0, row=0, padx=5)
        self.add_new_player_button.grid(column=1, row=0)
        self.button_frame.grid(column=1, row=2)
        self.remove_player_button.grid(column=0, row=0, padx=5)
        self.save_button.grid(column=1, row=0, padx=5)
        self.error_label.grid(column=0, row=3, columnspan=10, sticky="we")

    def file_changed(self):
        pass

    def create_player_file(self):
        pass

    def add_new_player(self):
        errors = self.verify_player_name()
        if not errors:
            self.error_string_var.set("")
            self.players_list_var.append(self.new_player_string_var.get())
            self.players_list_var.sort()
        else:
            error_str = ""
            for error in errors:
                error_str += error + "\n"
            self.error_string_var.set(error_str)

    def remove_player(self):
        pass

    def save_file(self):
        pass

    def verify_player_name(self) -> list:
        character_limits = (2, 20)
        name = self.new_player_string_var.get()
        errors = []
        if len(name) > character_limits[1]:
            errors.append(f"Name length cannot be longer than {character_limits[1]} characters")
        elif len(name) < character_limits[0]:
            errors.append(f"Name length cannot be shorter than {character_limits[0]} characters")
        for char in name:
            if char in punctuation:
                errors.append(f"Name cannot contain character '{char}'")
        if name in self.players_list_var.get():
            errors.append("Name is already in list")
        return errors

    def start(self):
        self.main()
        self.root.mainloop()


class FileNamePopup:
    def __init__(self, callback: Callable):
        self.root = Tk()
        self.root.title("Add player file")

        self.callback = callback

        self.file_name = StringVar(self.root)
        self.errors = StringVar(self.root)

        self.name_entry = Entry(self.root, textvariable=self.file_name)
        self.add_button = Button(self.root, command=self.verify_file_name)
        self.error_label = Label()

    def verify_file_name(self):
        pass




if __name__ == '__main__':
    tk = Tk()
    test = PlayerFileManager(tk)
    test.start()
