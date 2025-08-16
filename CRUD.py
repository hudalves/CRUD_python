import mysql.connector
import requests
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter.messagebox import showinfo
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
# Carrega as variáveis de ambiente do arquivo .env
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

root = Tk()
class validadores():
    # Validações de entrada

    def validar_dtpubli(self, text):
            import re

            if text == "":
                return True  # permite vazio (para apagar)

            # Verifica se contém apenas números, - ou / e até 10 caracteres
            if not re.fullmatch(r"[0-9/-]{0,10}", text):
                return False

            # Se for só número, checa se está no intervalo permitido
            if text.isdigit():
                valor = int(text)
                return 0 < valor < 100000000

            return True  # se tiver '-' ou '/', só valida o regex
class funcs():
    # Conexão com o banco de dados
    def conecta_bd(self):
        self.conexao = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
        )
        self.cursor = self.conexao.cursor()
    def desconecta_bd(self):
        # Fecha a conexão com o banco de dados
        self.cursor.close()
        self.conexao.close()
    def variaveis(self):
        # Variáveis para armazenar os dados do livro
        self.codigo = self.codigo_entry.get()
        self.Titulos = self.nome_entry.get()
        self.Genero = self.genvar.get()
        self.Autor = self.autor_entry.get()
        self.Dt_publi = self.publi_entry.get()
        # Validação simples:
        if not (self.Titulos and self.Genero and self.Autor and self.Dt_publi):
            from tkinter import messagebox
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return False
        return True
    def escolha(self):
        # Desabilita os botões de limpar, buscar, novo, alterar e apagar
        self.label()
        self.bt_buscar['state'] = DISABLED
        self.bt_novo['state'] = DISABLED
        self.bt_alterar['state'] = DISABLED
        self.bt_apagar['state'] = DISABLED
        # Verifica se os botões de salvar e cancelar já existem, se sim, destrói eles
        if hasattr(self, 'bt_salvar'):
            self.bt_salvar.destroy()
        if hasattr(self, 'bt_cancel'):
            self.bt_cancel.destroy()
        if hasattr(self, 'bt_procurar'):
            self.bt_procurar.destroy()
        # Cria os botões de salvar e cancelar
        self.bt_salvar = Button(self.frame_1, text='Salvar', bd=3, bg='#107db2',fg='white', command= self.save )
        self.bt_salvar.place(relx=0.7, rely=0.85,relwidth=0.09 , relheight=0.13)

        self.bt_cancel = Button(self.frame_1, text='Cancelar', bd=3, bg='#107db2',fg='white', command= self.cancelar )
        self.bt_cancel.place(relx=0.8, rely=0.85,relwidth=0.09 , relheight=0.13)
    def habilitar(self):
       # Habilita os botões de salvar e cancelar
        self.modo_operacao = "adicionar" 
        self.label()
        self.escolha()
    def habilitar_alterar(self):
       # Habilita os botões de salvar e cancelar
        self.modo_operacao = "alterar" 
        self.label()
        self.escolha()
    def habilitar_buscar(self):
        self.label()
        self.procurar()
    def confirm_delete(self):
        # Função para confirmar a exclusão de um livro
        answer = askyesno(title='confirmation', 
            message='Você tem certeza que deseja excluir o item selecionado?')
        if answer:
            self.deleta_livro()
            showinfo(title='Exclusão', 
            message='Livro excluído com sucesso!')
        else:
            showinfo(title='Exclusão', 
            message='Exclusão cancelada!')
    def add_livro(self):
        # Adiciona um novo livro ao banco de dados
        self.variaveis()
        self.escolha()
        
        # Conversão da data
        try:
            data_mysql = datetime.strptime(self.Dt_publi, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            try:
                data_mysql = datetime.strptime(self.Dt_publi, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                data_mysql = self.Dt_publi 
        # Conecta ao banco de dados e insere os dados do livro
        self.conecta_bd()
        self.cursor.execute(f'INSERT INTO livros (Titulos, Genero, Autor, Dt_publi) VALUES("{self.Titulos}","{self.Genero}", "{self.Autor}", "{data_mysql}")')
        self.conexao.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()
        

    def select_lista(self):
        # Seleciona todos os livros do banco de dados e os exibe na lista
        self.listaCL.delete(*self.listaCL.get_children())
        self.conecta_bd()
        self.cursor.execute('SELECT IDLivros, Titulos, Genero, Autor, Dt_publi FROM livros ORDER BY Titulos ASC;')
        # Obtém os resultados da consulta
        lista = self.cursor.fetchall()
        for i in lista:
            self.listaCL.insert("", END, values=i)
        self.desconecta_bd()
    
    def double_click(self, event): 
        # Evento de duplo clique na lista, preenche os campos com os dados do livro selecionado
        self.modo_operacao = "alterar"  
        self.label()
        self.limpar_tela()
        self.listaCL.selection()
        for n in self.listaCL.selection():
            colun1, colun2, colun3, colun4, colun5 = self.listaCL.item(n, 'values')
            self.codigo_entry.insert(END, colun1)
            self.nome_entry.insert(END, colun2)
            self.genvar.set(colun3)
            self.autor_entry.insert(END, colun4)
            self.publi_entry.insert(END, colun5)
    def deleta_livro(self):
        # Deleta o livro selecionado da lista
        if not self.codigo_entry.get():
            from tkinter import messagebox
            messagebox.showerror("Erro", "Selecione um livro para apagar!")
            return
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute('DELETE FROM livros WHERE IDLivros = %s',(self.codigo,))
        self.conexao.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_lista()
    def limpar_tela(self):
        # Limpa os campos de entrada
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.genvar.set("Genêro")
        self.autor_entry.delete(0, END)
        self.publi_entry.delete(0,END)
    def cancelar(self):
        # Cancela a operação atual, limpa os campos e reabilita os botões
        self.limpar_tela()
        self.bt_limpar['state'] = NORMAL
        self.bt_buscar['state'] = NORMAL
        self.bt_novo['state'] = NORMAL
        self.bt_alterar['state'] = NORMAL
        self.bt_apagar['state'] = NORMAL
        self.bt_salvar.destroy()
        self.bt_cancel.destroy()    
    def save(self):
        # Salva as alterações feitas no livro
        if not self.variaveis():
            self.bt_limpar['state'] = NORMAL
            self.bt_buscar['state'] = NORMAL
            self.bt_novo['state'] = NORMAL
            self.bt_alterar['state'] = NORMAL
            self.bt_apagar['state'] = NORMAL
            self.bt_salvar.destroy()
            self.bt_cancel.destroy()
            return
        
        if self.modo_operacao == "adicionar":
            self.add_livro()
        elif self.modo_operacao == "alterar":
            self.alterar_livro()
        self.limpar_tela()
        self.bt_limpar['state'] = NORMAL
        self.bt_buscar['state'] = NORMAL
        self.bt_novo['state'] = NORMAL
        self.bt_alterar['state'] = NORMAL
        self.bt_apagar['state'] = NORMAL
        self.bt_salvar.destroy()
        self.bt_cancel.destroy()

    def alterar_livro(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(
        'UPDATE livros SET Titulos = %s, Genero = %s, Autor = %s, Dt_publi = %s WHERE IDLivros = %s',
        (self.Titulos, self.Genero, self.Autor, self.Dt_publi, self.codigo)
        )
        self.conexao.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()
    def buscar_livros(self):
        self.conecta_bd()
        self.listaCL.delete(*self.listaCL.get_children())
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        query = '''SELECT IDLivros, Titulos, Genero, Autor, Dt_publi
               FROM livros
               WHERE Titulos LIKE %s
               ORDER BY Titulos ASC'''
        self.cursor.execute(query, ('%' + nome + '%',))
        buscanome= self.cursor.fetchall()
        for i in buscanome:
            self.listaCL.insert('','end', values= i)
        self.limpar_tela
        resultados = self.cursor.fetchall()

        self.desconecta_bd()
        return resultados
    def resumo(self):
        # Cria uma nova janela
        resumo_win = Toplevel(self.root)
        resumo_win.title("Resumo do Projeto")
        resumo_win.geometry("400x300")
        resumo_win.configure(background='#dfe3ee')

        # Texto do resumo
        texto = (
            "CRUD Biblioteca Digital\n\n"
            "Este projeto é um sistema de cadastro de livros usando Python, Tkinter e MySQL.\n\n"
            "Funcionalidades:\n"
            "- Adicionar, buscar, alterar e excluir livros\n"
            "- Interface gráfica \n"
            "- Armazenamento seguro dos dados\n\n"
            "Desenvolvido por Hudson"
        )

        # Label com o texto do resumo
        lbl = Label(resumo_win, text=texto, bg='#dfe3ee', justify=LEFT, wraplength=380, font=("Arial", 11))
        lbl.pack(padx=10, pady=10, fill=BOTH, expand=True)
    def procurar(self):
        if hasattr(self, 'bt_procurar'):
            self.bt_procurar.destroy()
        self.bt_procurar = Button(self.frame_1, text='Buscar', bd=3, bg='#107db2',fg='white', command= self.buscar_livros)
        self.bt_procurar.place(relx=0.7, rely=0.85,relwidth=0.09 , relheight=0.13)
class aplicacao(funcs, validadores):
    # Classe principal da aplicação
    def __init__(self):
        self.root = root
        self.modo_operacao = "adicionar"
        self.valida_ent()
        self.tela()
        self.frame_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.select_lista()
        self.menu()
        root.mainloop()
    def tela(self):
        # Configurações da janela principal
        self.root.title('Biblioteca digital')
        self.root.configure(background='#1e3743')
        self.root.geometry('700x500')
        self.root.resizable(True,True)
        self.root.wm_maxsize(1280, 1080)
        self.root.wm_minsize(520, 380)
    def frame_tela(self):
        # Criação dos frames para organizar os widgets
        self.frame_1 = Frame(self.root , bd=4 , bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
        self.frame_1.place(relx=0.02 , rely=0.02 , relwidth=0.96 , relheight=0.46)

        self.frame_2 = Frame(self.root , bd=4 , bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02 , rely=0.5 , relwidth=0.96 , relheight=0.46)
    def widgets_frame1(self):
        
        #limpar#
        self.bt_limpar = Button(self.frame_1, text='Limpar', bd=3, bg='#107db2',fg='white', command= self.limpar_tela )
        self.bt_limpar.place(relx=0.2, rely=0.1,relwidth=0.09 , relheight=0.13)

        #buscar#
        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=3, bg='#107db2',fg='white', command= self.habilitar_buscar)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.09, relheight=0.13)
        #novo#
        self.bt_novo = Button(self.frame_1, text="Novo", bd=3, bg='#107db2',fg='white', command=self.habilitar)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.09, relheight=0.13)
        #alterar#
        self.bt_alterar = Button(self.frame_1, text="Alterar", bd=3, bg='#107db2',fg='white', command= self.habilitar_alterar)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.09, relheight=0.13)
        #apagar#
        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=3, bg='#107db2',fg='white', command=self.confirm_delete)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.09, relheight=0.13)
    def label(self):
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

        #Label autor
        self.lb_autor = Label(self.frame_1, text='Autor', bg= '#dfe3ee')
        self.lb_autor.place(relx=0.35, rely=0.6)

        self.autor_entry= Entry(self.frame_1)
        self.autor_entry.place(relx=0.35,rely=0.7, relwidth=0.4)

        #Label publicação
        self.lb_publi = Label(self.frame_1, text='Data de publicação', bg= '#dfe3ee')
        self.lb_publi.place(relx=0.78, rely=0.6)

        self.publi_entry= Entry(self.frame_1,validate='key', validatecommand=self.vali_publi)
        self.publi_entry.place(relx=0.78,rely=0.7, relwidth=0.16)
        #Label gênero
        self.lb_genero = Label(self.frame_1, text='Gênero', bg= '#dfe3ee')
        self.lb_genero.place(relx=0.05, rely=0.6)

        # Dropdown para o campo de gênero
        self.genvar = StringVar()
        self.genv = ( "Romance",
    "Fantasia","Ficção científica","Aventura","Mistério / Suspense","Terror / Horror","Policial / Crime","Poesia","Drama / Teatro","Biografia",
    "Autobiografia","História","Ciência","Filosofia","Religião / Espiritualidade","Autoajuda","Negócios / Economia","Infantil","Young Adult (YA)","Quadrinhos / Mangá"
                     )
        self.genvar.set("Genêro")
        self.popupMenu = OptionMenu(self.frame_1, self.genvar, *self.genv)  
        self.popupMenu.place(relx=0.05,rely=0.7, relwidth=0.25)
        self.genero = self.genvar.get()
    def lista_frame2(self):
        # Criação da lista de livros
        self.listaCL= ttk.Treeview(self.frame_2, height=3, columns= ('colun1', 'colun2','colun3','colun4','colun5'))
        self.listaCL.heading('#0',text='')
        self.listaCL.heading('#1',text='ID')
        self.listaCL.heading('#2',text='Título')
        self.listaCL.heading('#3',text='Gênero')
        self.listaCL.heading('#4',text='Autor')
        self.listaCL.heading('#5',text='Dt.publi')

        self.listaCL.column('#0', width=1)
        self.listaCL.column('#1', width=30)
        self.listaCL.column('#2', width=220)
        self.listaCL.column('#3', width=100)
        self.listaCL.column('#4', width=100)
        self.listaCL.column('#5', width=50)

        self.listaCL.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scrolLis = Scrollbar(self.frame_2, orient='vertical')
        self.listaCL.configure(yscroll=self.scrolLis.set)
        self.scrolLis.place(relx=0.96, rely=0.1, relwidth=0.02, relheight=0.85)
        # Bind do evento de duplo clique na lista
        self.listaCL.bind('<Double-1>', self.double_click)
    def menu(self):
        # Criação do menu da aplicação
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        menu_1 = Menu(menubar, tearoff=0)
        menu_2 = Menu(menubar, tearoff=0)

        def quit(): self.root.destroy()

        menubar.add_cascade(label = 'Opções', menu= menu_1)
        menubar.add_cascade(label = 'Sobre', menu= menu_2)

        menu_1.add_command(label= 'Sair', command= quit)
        menu_2.add_command(label= 'Resumo', command= self.resumo)
    def valida_ent(self):
        self.vali_publi = (self.root.register(self.validar_dtpubli), '%P')
aplicacao()