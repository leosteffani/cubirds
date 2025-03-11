import random
from carta import Carta
class Baralho():
    def __init__(self):
        self.__n_tipos = [7,10,10,13,13,17,20,20] #numero de cartas de cada tipo
        self.__cartas = []
        self.__string = []
        self.__descarte = []
        self.__string_descarte = []
        self.__cartas_atual = 110
    def cria_baralho(self):
        for tipo in range(len(self.__n_tipos)):
            for i in range(self.__n_tipos[tipo]):
                self.__string.append(str(tipo))
        random.shuffle(self.__string)
        for i in range(len(self.__string)):
            self.__cartas.append(Carta(int(self.__string[i])))
    def set_baralho(self,baralho):
        self.__string = list(baralho)
        for i in range(len(self.__string)):
            self.__cartas.append(Carta(int(self.__string[i])))
        self.__cartas_atual = len(baralho)
    def set_descarte(self,descarte):
        self.__string_descarte = list(descarte)
        for i in range(len(self.__string_descarte)):
            self.__descarte.append(Carta(int(self.__string_descarte[i])))
    def compra_carta(self,n_cartas):
        if n_cartas > len(self.__cartas):
            return 0
        cartas_novas = []
        for i in range(n_cartas):
            cartas_novas.append(self.__cartas.pop())
            self.__string.pop()
        return cartas_novas
    def descarta_cartas(self,cartas):
        n_cartas = len(cartas)
        for i in range(n_cartas):
            self.__descarte.append(cartas[i])
            self.__string_descarte.append(cartas[i].get_id())
        cartas_novas = self.compra_carta(n_cartas)
        return cartas_novas
    def remove_cartas(self,cartas):
        for i in range(len(cartas)):
            self.__descarte.append(cartas[i])
            self.__string_descarte.append(cartas[i].get_id())
    def get_quantidade(self):
        return len(self.__cartas)
    def get_string(self):
        string = "".join(self.__string)
        return string
    def get_string(self):
        string_descarte = "".join(self.__string_descarte)
        return string_descarte
    def get_quantidade(self):
        return self.__cartas_atual