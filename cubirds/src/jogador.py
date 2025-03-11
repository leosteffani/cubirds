class Jogador():
    def __init__(self):
        self.__mao = []
    def recebe_cartas(self,cartas):
        for carta in range(len(cartas)):
            self.__mao.append(cartas[carta])
    def remove_cartas(self,cartas_string):
        cartas_removidas = []
        for i in range(len(cartas_string)):
            cartas_removidas.append(self.__mao.pop(cartas_string[i]-i))
        return cartas_removidas