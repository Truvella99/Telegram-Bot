class user():
    def __init__(self, name, abbonamenti):
        self.name = name
        self.abbonamenti = abbonamenti

    def get_name(self):
        return self.name

    def get_abbonamenti(self):
        return self.abbonamenti

    def add_abbonamenti(self, abbonamento):
        if abbonamento not in self.abbonamenti.keys():
            self.abbonamenti[abbonamento] = 0

    def remove_abbonamenti(self, abbonamento):
        if abbonamento in self.abbonamenti.keys():
            if self.abbonamenti[abbonamento] == 0:
                self.abbonamenti.pop(abbonamento)

    def add_soldi(self, abbonamento, amount):
        self.abbonamenti[abbonamento] += amount

    def remove_soldi(self,abbonamento, amount):
        if self.abbonamenti[abbonamento]>0:
            self.abbonamenti[abbonamento]-=amount

    def __str__(self):
        resto = ""
        for abb in self.abbonamenti:
            resto += abb + " "
        return self.name + resto