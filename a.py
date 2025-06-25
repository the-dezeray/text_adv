class a:
    def __init__(self):

        self.b = 9
        self.__post_init__()
    def __post_init__(self):
        self.b = 10

class ted(a):
    def __post_init__(self):
        self.b  =3234

gd =ted()

print(gd.b)