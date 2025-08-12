import mysql.connector
from tkinter import *
from tkinter import ttk

root = Tk()
class funcs():
    def limpar_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
class aplicacao(funcs):

    def __init__(self):
        self.root = root
        self.tela()
        self.frame_tela()
        self.widgets_frame1()
        self.lista_frame2()
        root.mainloop()

    def tela(self):

        self.root.title('Cadastro de cliente')
        self.root.configure(background='#1e3743')
        self.root.geometry('700x500')
        self.root.resizable(True,True)
        self.root.wm_maxsize(1280, 1080)
        self.root.wm_minsize(520, 380)

    def frame_tela(self):
        
        self.frame_1 = Frame(self.root , bd=4 , bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
        self.frame_1.place(relx=0.02 , rely=0.02 , relwidth=0.96 , relheight=0.46)

        self.frame_2 = Frame(self.root , bd=4 , bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02 , rely=0.5 , relwidth=0.96 , relheight=0.46)

    def widgets_frame1(self):
        
        #limpar#
        self.bt_limpar = Button(self.frame_1, text='Limpar', bd=3, bg='#107db2',fg='white', command= self.limpar_tela )
        self.bt_limpar.place(relx=0.2, rely=0.1,relwidth=0.09 , relheight=0.13)
        #buscar#
        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=3, bg='#107db2',fg='white')
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.09, relheight=0.13)
        #novo#
        self.bt_novo = Button(self.frame_1, text="Novo", bd=3, bg='#107db2',fg='white')
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.09, relheight=0.13)
        #alterar#
        self.bt_alterar = Button(self.frame_1, text="Alterar", bd=3, bg='#107db2',fg='white')
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.09, relheight=0.13)
        #apagar#
        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=3, bg='#107db2',fg='white')
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.09, relheight=0.13)

        # Label código
        self.lb_codigo = Label(self.frame_1, text='Código', bg= '#dfe3ee')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry= Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05,rely=0.15, relwidth=0.08)

        #Label nome
        self.lb_nome = Label(self.frame_1, text='Nome', bg= '#dfe3ee')
        self.lb_nome.place(relx=0.05, rely=0.35)

        self.nome_entry= Entry(self.frame_1)
        self.nome_entry.place(relx=0.05,rely=0.45, relwidth=0.5)

        #Label telefone
        self.lb_telefone = Label(self.frame_1, text='Telefone', bg= '#dfe3ee')
        self.lb_telefone.place(relx=0.05, rely=0.6)

        self.telefone_entry= Entry(self.frame_1)
        self.telefone_entry.place(relx=0.05,rely=0.7, relwidth=0.4)

        #Label cidade
        self.lb_cidade = Label(self.frame_1, text='Cidade', bg= '#dfe3ee')
        self.lb_cidade.place(relx=0.5, rely=0.6)

        self.cidade_entry= Entry(self.frame_1)
        self.cidade_entry.place(relx=0.5,rely=0.7, relwidth=0.4)
    def lista_frame2(self):
        self.listaCL= ttk.Treeview(self.frame_2, height=3, columns= ('colun1', 'colun2','colun3','colun4'))
        self.listaCL.heading('#0',text='')
        self.listaCL.heading('#1',text='Código')
        self.listaCL.heading('#2',text='Nome')
        self.listaCL.heading('#3',text='Telefone')
        self.listaCL.heading('#4',text='Cidade')

        self.listaCL.column('#0', width=1)
        self.listaCL.column('#1', width=50)
        self.listaCL.column('#2', width=200)
        self.listaCL.column('#3', width=125)
        self.listaCL.column('#4', width=125)

        self.listaCL.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scrolLis = Scrollbar(self.frame_2, orient='vertical')
        self.listaCL.configure(yscroll=self.scrolLis.set)
        self.scrolLis.place(relx=0.96, rely=0.1, relwidth=0.02, relheight=0.85)

aplicacao()