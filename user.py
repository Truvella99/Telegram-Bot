class user():
    def __init__(self, name, abbonamenti):
        self.__name = name
        self.__abbonamenti = abbonamenti

    def get_name(self):
        return self.__name

    def get_abbonamenti(self):
        return self.__abbonamenti

    def add_abbonamenti(self, abbonamento):
        if abbonamento not in self.__abbonamenti.keys():
            self.__abbonamenti[abbonamento] = 0

    def remove_abbonamenti(self, abbonamento):
        if abbonamento in self.__abbonamenti.keys():
            if self.__abbonamenti[abbonamento] == 0:
                self.__abbonamenti.pop(abbonamento)

    def empty_abbonamenti(self):
        return not self.__abbonamenti

    def add_amount(self, abbonamento, amount):
        self.__abbonamenti[abbonamento] += amount

    def remove_amount(self,abbonamento, amount):
        if self.abbonamenti[abbonamento] > 0 and self.abbonamenti[abbonamento]-amount >= 0:
            self.__abbonamenti[abbonamento] -= amount
        else:
            self.__abbonamenti[abbonamento] = 0

    def __str__(self):
        total = 0
        for amount in self.__abbonamenti.values():
            total += amount
        return self.__name + " " + "%0.2f" % total + " €\n"