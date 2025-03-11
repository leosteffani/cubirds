class Placar():
    def __init__(self):
        self.__pontos_local = 0
        self.__pontos_externo = 0
        self.__pontuacao_final = 8
    def atualiza(self,valor):
        self.__pontos_local += valor
    def att_externo(self,valor):
        self.__pontos_externo = valor
    def detecta_final(self):
        if self.__pontos_local >= self.__pontuacao_final:
            return 1
        elif self.__pontos_externo >= self.__pontuacao_final:
            return 2
        else:
            return 0
    def get_pontos_local(self):
        return self.__pontos_local
    def get_pontos_externo(self):
        return self.__pontos_externo