from pyexpat.errors import messages

from interface import PlayerInterface
from carta import Carta
from baralho import Baralho
from placar import Placar
from jogador import Jogador
import random

class Mesa():
    def __init__(self):
        self.__baralho = Baralho()
        self.__jogador_local = Jogador()
        self.__placar = Placar()
        self.__turno = False
        self.__interface = PlayerInterface(self)
        self.__cartas_na_mesa = [[],[],[],[]]
        self.__codigo = self.__interface.pega_id()
        self.__partida_andamento = False

    def inicia_partida(self):
        dicionario = {}
        inicia = random.randint(0,1)
        self.__partida_andamento = True
        if inicia == 0:
            dicionario["match_status"] = "progress"
            self.__turno = True
        else:
            dicionario["match_status"] = "next"
        self.__baralho.cria_baralho()
        dicionario["player"] = self.__codigo  # achar como pegar isso
        dicionario["baralho"] = self.__baralho.get_string()
        self.__interface.enviar_turno(dicionario)
    def recebe_comeco(self,baralho):
        self.__baralho.set_baralho(baralho)
    def descarta_cartas(self,cartas_antigas):
        if not self.__turno:
            return False
        if len(cartas_antigas) == 0:
            return False
        cartas_antigas_obg = self.__jogador_local.remove_cartas(cartas_antigas)
        cartas_novas = self.__baralho.descarta_cartas(cartas_antigas_obg)
        self.__jogador_local.recebe_cartas(cartas_novas)
        return True

    def formar_bando(self,cartas):
        if not self.__turno:
            return False
        if len(cartas) == 0:
            return False
        cartas_obg = self.__jogador_local.remove_cartas(cartas)
        tipo = cartas_obg[0].get_tipo()
        bando_pequeno = cartas_obg[0].get_bando_pequeno()
        bando_grande = cartas_obg[0].get_bando_grande()
        for carta in range(1 , len(cartas_obg)):
            if cartas_obg[carta].get_tipo != tipo:
                self.__jogador_local.recebe_cartas(cartas_obg)
                return False
        cartas_bando = cartas_obg
        cartas_extras = []
        if len(cartas_obg) >= bando_grande:
            for temp in range(bando_grande,len(cartas_obg)):
                cartas_extras.append(cartas_bando.pop(temp))
            self.__baralho.remove_cartas(cartas_bando)
            self.__placar.atualiza(2)
        elif len(cartas_obg) >= bando_pequeno:
            for temp in range(bando_pequeno,len(cartas_obg)):
                cartas_extras.append(cartas_bando.pop(temp))
            self.__baralho.remove_cartas(cartas_bando)
            self.__placar.atualiza(1)
        else:
            self.__jogador_local.recebe_cartas(cartas_obg)
            return False
        self.__jogador_local.recebe_cartas(cartas_extras)
        return True

    def adiciona_carta_mesa(self,linha,esquerda,cartas,jogando_carta):
        loops = len(cartas)
        tipo = cartas[0].get_tipo
        cartas_add = []
        if jogando_carta:
            if esquerda:
                rodando = True
                while rodando:
                    if self.__cartas_na_mesa[linha][0].get_tipo() != tipo:
                        cartas_add.append(self.__cartas_na_mesa[linha].pop(0))
                    else:
                        rodando = False

            else:
                rodando = True
                while rodando:
                    if self.__cartas_na_mesa[linha][len(self.__cartas_na_mesa[linha])-1].get_tipo() != tipo:
                        cartas_add.append(self.__cartas_na_mesa[linha].pop())
                    else:
                        rodando = False
        for carta in range(loops):
            if esquerda:
                self.__cartas_na_mesa[linha].insert(0,cartas.pop())
            else:
                self.__cartas_na_mesa[linha].append(cartas.pop())
        tipo_teste =  self.__cartas_na_mesa[linha][0].get_tipo()
        volta = True
        for i in range(1,self.__cartas_na_mesa[linha]):
            if self.__cartas_na_mesa[linha][i].get_tipo() != tipo_teste:
                volta = False
        if volta:
            carta_nova = self.__baralho.compra_carta(1)
            self.adiciona_carta_mesa(linha,True,carta_nova,False)
        self.__interface.att_cartas_mesa(self.__cartas_na_mesa)
        return cartas_add

    def jogar_carta(self,cartas_selecionadas,linha,esquerda):
        if not self.__turno:
            return False
        if len(cartas_selecionadas) == 0:
            return False
        cartas_obg = self.__jogador_local.remove_cartas(cartas_selecionadas)
        tipo = cartas_obg[0].get_tipo()
        todas_cartas_removidas = self.__jogador_local.busca_tipo(tipo)
        if not todas_cartas_removidas:
            self.__jogador_local.recebe_cartas(cartas_obg)
            return False
        for carta in range(1, len(cartas_obg)):
            if cartas_obg[carta].get_tipo != tipo:
                self.__jogador_local.recebe_cartas(cartas_obg)
                return False
        sanduiche = self.adiciona_carta_mesa(linha,esquerda,cartas_obg,True)
        if len(sanduiche) != 0:
            self.__jogador_local.recebe_cartas(sanduiche)
        return True
    def passar_turno(self, cartas_selecionadas):
        if len(cartas_selecionadas) != 0:
            return False
        if not self.__turno:
            return False
        ganhador = self.__placar.detecta_final()
        dicionario = {}
        dicionario["baralho"] = self.__baralho.get_string()
        dicionario["descarte"] = self.__baralho.get_string_descarte()
        if ganhador == 0:
            dicionario["match_status"] = "next"
        else:
            dicionario["match_status"] = "finished"
        for linha in range(self.__cartas_na_mesa):
            for coluna in range(self.__cartas_na_mesa[linha]):
                endereco = str(linha)
                endereco += str(coluna)
                dicionario[endereco] = self.__cartas_na_mesa[linha][coluna].get_id()
        dicionario["pontos"] = self.__placar.get_pontos_local()
        dicionario["player"] = self.__codigo #achar como pegar isso
        self.__interface.enviar_turno(dicionario)
        self.__turno == False

    def receive_mesa(self,cartas):
        self.__cartas_na_mesa = [[],[],[],[]]
        for endereco in cartas:
            nova_carta = Carta(int(cartas[endereco]))
            self.__cartas_na_mesa[endereco[0]].append(nova_carta)

    def receive_baralho(self,string_estado):
        self.__baralho.att_externo(int(string_estado))

    def receive_descarte(self,string_estado):
        self.__baralho.att_externo_descarte(int(string_estado))
    def receive_placar(self,string_estado):
        self.__placar.att_placar_online(int(string_estado))

    def recebe_jogada(self,jogada):
        self.__id_externo = jogada.pop("player")
        self.receive_placar(jogada.pop("pontos"))
        self.receive_baralho(jogada.pop("baralho"))
        self.receive_descarte(jogada.pop("descarte"))
        status = jogada.pop("match_status")
        self.receive_mesa(jogada)
        if status == "next":
            self.__turno == True
        elif status == "finished":
            self.perdeu()
    def perdeu(self):
        self.__turno = False
        self.__partida_andamento = False
    def reset(self):
        self.__cartas_na_mesa = [[],[],[],[]]
        self.__baralho = Baralho()
        self.__placar = Placar()
        self.__turno = False
        self.__partida_andamento = False
    def gui_baralho(self,quantidade):
        self.__interface.att_baralho(quantidade)
    def gui_descarte(self,quantidade):
        self.__interface.att_descarte(quantidade)
    def gui_mao(self,mao):
        self.__interface.att_mao(mao)
    def gui_mesa(self):
        self.__interface.att_mesa(self.__cartas_na_mesa)
mesa = Mesa()