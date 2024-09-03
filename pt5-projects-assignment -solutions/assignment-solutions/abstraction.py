from abc import abstractmethod,ABC

class TouchScreenLaptop(ABC):
    @abstractmethod
    def scroll(self):
        pass
    @abstractmethod
    def click(self):
        pass

class Hp(TouchScreenLaptop):
    def scroll(self):
        print("In hp override scroll")
    @abstractmethod
    def click(self):
        pass


class Dell(TouchScreenLaptop):
    def scroll(self):
        print("In DELL override scroll")
    @abstractmethod
    def click(self):
        pass


class HpNotebook(Hp):
    def __init__(self):
        print("In hpnote")

    def scroll(self):
        super().scroll()
        print("In hp notebook scroll")

    def click(self):
        print("In hp notebook click")