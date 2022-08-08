import random

class Fuzz:
    def fuzz(self, type):
        li_integer = [1, 2, 3]
        li_character = ['a', 'b', 'c']
        li_string = ["python", "java", "rust", "c++"]
        if type == "integer" or type == "int":
            return random.choice(li_integer)
        elif type == "character" or type == "char":
            return random.choice(li_character)
        elif type == "string":
            return random.choice(li_string)