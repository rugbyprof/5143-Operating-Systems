from rich import print


class Register:
    def __init__(self):
        self.r = None

    def write(self, x):
        self.r = x

    def read(
        self,
    ):
        return self.r

    def __str__(self):

        return f"[{self.r}]"

    def __repr__(self):
        return self.__str__()


class Registers:
    def __init__(self, num=2):
        self.registers = []
        for i in range(num):
            self.registers.append(Register())

    def __getitem__(self, item):
        return self.registers[item]

    def __str__(self):
        s = ""
        for r in self.registers:
            s += str(r)
        return s

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    reg = Registers(2)

    reg[0].write(5)
    reg[1].write(5)

    print(reg)
