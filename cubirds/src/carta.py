tipos = ["flamingo","coruja","tucano","pato","arara","andorinha","gaivota","periquito"]
bandos_pequenos = [2,3,3,4,4,5,6,6]
bandos_grandes = [3,4,4,6,6,7,9,9]
class Carta():
    def __init__(self,id):
        self.__id = id
        self.__tipo = tipos[id]
        self.__bando_pequeno = bandos_pequenos[id]
        self.__bando_grande = bandos_grandes[id]

    def get_tipo(self):
        return self.__tipo
    def get_bando_pequeno(self):
        return self.__bando_pequeno
    def get_bando_grande(self):
        return self.__bando_grande
    def get_id(self):
        return self.__id