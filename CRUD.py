import mysql.connector
from tkinter import *
from tkinter import ttk
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

root = Tk()
class funcs():
    def conecta_bd(self):
        self.conexao = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
        )
        self.cursor = self.conexao.cursor()

    def desconecta_bd(self):
        self.cursor.close()
        self.conexao.close()
    
    def add_livro(self):
        self.codigo = self.codigo_entry.get()
        self.Titulos = self.nome_entry.get()
        self.Genero = self.genero_entry.get()
        self.Autor = self.autor_entry.get()
        self.Dt_publi = self.publi_entry.get()
        # Conversão da data
        try:
            data_mysql = datetime.strptime(self.Dt_publi, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            try:
                data_mysql = datetime.strptime(self.Dt_publi, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                data_mysql = self.Dt_publi 
        
        self.conecta_bd()
        self.cursor.execute(f'INSERT INTO livros (Titulos, Genero, Autor, Dt_publi) VALUES("{self.Titulos}","{self.Genero}", "{self.Autor}", "{data_mysql}")')
        self.conexao.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()

    def select_lista(self):
        self.listaCL.delete(*self.listaCL.get_children())
        self.conecta_bd()
        self.cursor.execute('SELECT IDLivros, Titulos, Genero, Autor, Dt_publi FROM livros ORDER BY Titulos ASC;')
        lista = self.cursor.fetchall()
        for i in lista:
            self.listaCL.insert("", END, values=i)
        self.desconecta_bd

    def buscar_livros(self):
        self.conecta_bd()
        self.cursor.execute("SELECT * FROM livros")
        resultados = self.cursor.fetchall()

        self.desconecta_bd()
        return resultados
    def double_click(self):
        self.limpar_tela()
        
    def limpar_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.genero_entry.delete(0, END)
        self.autor_entry.delete(0, END)
        self.publi_entry.delete(0,END)
class aplicacao(funcs):

    def __init__(self):
        self.root = root
        self.tela()
        self.frame_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.select_lista()
        root.mainloop()

    def tela(self):

        self.root.title('Biblioteca digital')
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
        self.bt_novo = Button(self.frame_1, text="Novo", bd=3, bg='#107db2',fg='white', command=self.add_livro)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.09, relheight=0.13)
        #alterar#
        self.bt_alterar = Button(self.frame_1, text="Alterar", bd=3, bg='#107db2',fg='white')
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.09, relheight=0.13)
        #apagar#
        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=3, bg='#107db2',fg='white')
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.09, relheight=0.13)

        # Label código
        self.lb_codigo = Label(self.frame_1, text='ID', bg= '#dfe3ee')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry= Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05,rely=0.15, relwidth=0.08)

        #Label nome
        self.lb_nome = Label(self.frame_1, text='Título', bg= '#dfe3ee')
        self.lb_nome.place(relx=0.05, rely=0.35)

        self.nome_entry= Entry(self.frame_1)
        self.nome_entry.place(relx=0.05,rely=0.45, relwidth=0.65)

        #Label gênero
        self.lb_genero = Label(self.frame_1, text='Gênero', bg= '#dfe3ee')
        self.lb_genero.place(relx=0.05, rely=0.6)

        self.genero_entry= Entry(self.frame_1)
        self.genero_entry.place(relx=0.05,rely=0.7, relwidth=0.25)

        #Label autor
        self.lb_autor = Label(self.frame_1, text='Autor', bg= '#dfe3ee')
        self.lb_autor.place(relx=0.35, rely=0.6)

        self.autor_entry= Entry(self.frame_1)
        self.autor_entry.place(relx=0.35,rely=0.7, relwidth=0.4)

        #Label publicação
        self.lb_publi = Label(self.frame_1, text='Data de publicação', bg= '#dfe3ee')
        self.lb_publi.place(relx=0.78, rely=0.6)

        self.publi_entry= Entry(self.frame_1)
        self.publi_entry.place(relx=0.78,rely=0.7, relwidth=0.16)
    def lista_frame2(self):
        self.listaCL= ttk.Treeview(self.frame_2, height=3, columns= ('colun1', 'colun2','colun3','colun4','colun5'))
        self.listaCL.heading('#0',text='')
        self.listaCL.heading('#1',text='ID')
        self.listaCL.heading('#2',text='Título')
        self.listaCL.heading('#3',text='Gênero')
        self.listaCL.heading('#4',text='Autor')
        self.listaCL.heading('#5',text='Dt.publi')

        self.listaCL.column('#0', width=1)
        self.listaCL.column('#1', width=50)
        self.listaCL.column('#2', width=200)
        self.listaCL.column('#3', width=100)
        self.listaCL.column('#4', width=100)
        self.listaCL.column('#5', width=50)

        self.listaCL.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scrolLis = Scrollbar(self.frame_2, orient='vertical')
        self.listaCL.configure(yscroll=self.scrolLis.set)
        self.scrolLis.place(relx=0.96, rely=0.1, relwidth=0.02, relheight=0.85)

aplicacao()