from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
#from mesa import Mesa

from pyexpat.errors import messages

from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from dog.start_status import StartStatus
class PlayerInterface(DogPlayerInterface):
    def __init__(self,mesa):
        self.main_window = Tk()
        self.fill_main_window()
        self.__mesa = mesa
        self.__descarte = "desc"
        self.__status = StartStatus
        self.create_menubar()
        self.create_table()
        self.create_baralho()
        self.create_placar()
        self.create_mao()
        self.create_descarte()
        # preenchimento da janela

        player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        self.dog_server_interface= DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)

        self.main_window.mainloop()

    def fill_main_window(self):
        # Título, dimensionamento e fundo da janela
        self.main_window.title("Cubirds")
        #self.main_window.iconbitmap("images/icon.ico")
        self.main_window.geometry("1280x840")
        self.main_window.resizable(False, False)
        self.main_window["bg"] = "lightgray"
        #configuracao do grid main window
        self.main_window.columnconfigure(0, weight=0)
        self.main_window.columnconfigure(1, weight=1)
        self.main_window.columnconfigure(2, weight=0)
        self.main_window.rowconfigure(0, weight=0)
        self.main_window.rowconfigure(1, weight=0)
        self.main_window.rowconfigure(2, weight=1)

        #cria os frames que serao usados
        self.table_frame = Frame(self.main_window,width= 1280,height= 480,bg="lightgray")
        self.table_frame.grid(row=1,column=1)
        self.mao_frame = Frame(self.main_window, width=1280, height=120, bg="lightgray")
        self.mao_frame.grid(row=2, column=1)

        #imagens usadas ate o momento
        self.an_image = PhotoImage(file="images/carta1.png")
        self.add_image = PhotoImage(file="images/add.png")

        #variaveis usadas para aprensentar valores na tela (serao trocadas no futuro)
        self.n_pontos_player1 = '1'
        self.n_pontos_player2 = '4'
        self.n_cartas_baralho= '43'
        self.n_cartas_mesa= 3
        self.n_cartas_mao = 7

        # imagem vazia para tudo ficar centralizado (nao sei se tem um jeito melhor de fazer isso)
    def create_descarte(self):
        descarte = Label(self.main_window, bg="lightgray", text=self.__descarte, font="arial 30",image=self.an_image, compound='center')
        descarte.bind("<Button-1>", lambda event: self.descarte())
        descarte.grid(row=0, column=2)
    #cria o placar
    def create_placar(self):
        placar= Label(self.main_window, bg="lightgray", text=self.n_pontos_player1+' VS '+self.n_pontos_player2, font="arial 30")
        placar.bind("<Button-1>", lambda event: self.placar())
        placar.grid(row=0, column=1)
    #cria o baralho
    def create_baralho(self):
        baralho = Label(self.main_window, bg="lightgray", text=self.n_cartas_baralho, font="arial 40",image=self.an_image, compound='center')
        baralho.bind("<Button-1>", lambda event: self.baralho())
        baralho.grid(row=0, column=0)

    #preenche o grid da mesa
    def create_table(self):
        #adiciona os botoes add no inicio de cada linha
        for x in range(4):
            aLabel = Label(self.table_frame, bd=0, image=self.add_image)
            aLabel.grid(row=x, column=0)
            aLabel.bind("<Button-1>", lambda event,a_line=x, a_column=0: self.add( a_line, a_column))
        #adiciona as cartas
        for y in range(1,self.n_cartas_mesa+1):
            for x in range(4):
                aLabel = Label(self.table_frame, bd=0, image=self.an_image)
                aLabel.grid(row=x, column=y)
                aLabel.bind("<Button-1>", lambda event, a_line=x, a_column=y: self.click_mesa(a_line, a_column))
        # adiciona os botoes add no final de cada linha
        for x in range(4):
            aLabel = Label(self.table_frame, bd=0, image=self.add_image)
            aLabel.grid(row=x, column=self.n_cartas_mesa+2)
            aLabel.bind("<Button-1>", lambda event,a_line=x, a_column=self.n_cartas_mesa+1: self.add(a_line, a_column))
    #preenche o grid da mao
    def create_mao(self):
        for x in range(self.n_cartas_mao):
            carta_mao = Label(self.mao_frame, bd=0, image=self.an_image)
            carta_mao.grid(row=0, column=x)
            carta_mao.bind("<Button-1>", lambda event,a_column=x: self.click_carta_mao(a_column))
    #cria o menu e seus botoes
    def create_menubar(self):
        self.menubar = Menu(self.main_window)
        self.menubar.option_add('*tearOff', FALSE)
        self.main_window['menu'] = self.menubar

        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')

        self.menu_file.add_command(label='Iniciar jogo', command=self.start_match)
        self.menu_file.add_command(label='restaurar estado inicial', command=self.start_game)

        self.menubar.option_add('*tearOff', FALSE)

    #metodos de cada tipo de botao
    def start_match(self):
        start_status= self.dog_server_interface.start_match(2)
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        if message == "Partida iniciada":
            self.__mesa.inicia_partida()
    def pega_id(self):
        return self.__status.get_local_id()
    def start_game(self):
        print('precionou restaurar estado inicial')
    def click_mesa(self, a_line, a_column):
        print('precionou botão na posicao '+str(a_line)+" "+ str(a_column) )
    def add(self, a_line, a_column):
        print('precionou botão add na posicao ' + str(a_line) + " " + str(a_column))
    def placar(self):
        print('precionou placar')
    def baralho(self):
        print('precionou baralho')
    def descarte(self):
        print('precionou descarte')
    def click_carta_mao(self,a_column):
        print('precionou botão carta da mao na posicao '+str(a_column))

    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)

    def receive_move(self, a_move):
        self.__mesa.recebe_jogada(a_move)
    def enviar_turno(self,dicionario):
        self.dog_server_interface.send_move(dicionario)
    def receive_withdrawal_notification(self):
        message = "o outro jogador abandonou a partida"
        messagebox.showinfo(message=message)
        self.__mesa.finaliza_partida()

    def att_baralho(self,quantidade):
        self.__descarte = "desc " + str(quantidade)
        self.create_descarte()
    def att_descarte(self,quantidade):
        self.__baralho = str(quantidade)
        self.create_descarte()
    def att_mao(self,mao):
        pass
    def att_mesa(self,mesa):
        pass
