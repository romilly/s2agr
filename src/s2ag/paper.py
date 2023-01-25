import re

CC_RE = pattern = re.compile(r'(?<!^)(?=[A-Z])')


def snake(name: str) -> str:
    return CC_RE.sub('_', name).lower()


class Paper:
    def __init__(self, jason_dictionary: dict):
        self.jason_dictionary = jason_dictionary
        for key in self.jason_dictionary.keys():
            self.__setattr__(snake(key), self.jason_dictionary[key])
