from tkinter import StringVar
from json import loads


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
