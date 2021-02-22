from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import pymysql


class AdminJanela():

    def __init__(self):
        self.root = Tk()
        self.root.title('admin')

        Button(self.root, text='Pedidos', width=20, bg='#AED9E0', fg='white',
               command=self.MostrarPedidos).grid(row=0, column=0, padx=10, pady=10)
        Button(self.root, text='Cadastros', width=20, bg='#AED9E0', fg='white',
               command=self.CadastrarProduto).grid(row=1, column=0, padx=10, pady=10)

        self.root.mainloop()

    def CadastrarProduto(self):
        self.cadastrar = Tk()
        self.cadastrar.title('Cadastro de Produto')
        self.cadastrar['bg'] = '#524f4f'

        Label(self.cadastrar, text='Cadastre os produtos', bg='#524f4f',
              fg='white').grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        Label(self.cadastrar, text='Nome', bg='#524f4f', fg='white').grid(
            row=1, column=0, columnspan=1, padx=5, pady=5)
        self.nome = Entry(self.cadastrar)
        self.nome.grid(row=1, column=1, columnspan=2, pady=5, padx=5)

        Label(self.cadastrar, text='Ingredientes', bg='#524f4f', fg='white').grid(
            row=2, column=0, columnspan=1, padx=5, pady=5)
        self.ingredientes = Entry(self.cadastrar)
        self.ingredientes.grid(row=2, column=1, columnspan=2, pady=5, padx=5)

        Label(self.cadastrar, text='Grupo', bg='#524f4f', fg='white').grid(
            row=3, column=0, columnspan=1, padx=5, pady=5)
        self.grupo = Entry(self.cadastrar)
        self.grupo.grid(row=3, column=1, columnspan=2, pady=5, padx=5)

        Label(self.cadastrar, text='Preço', bg='#524f4f', fg='white').grid(
            row=4, column=0, columnspan=1, padx=5, pady=5)
        self.preco = Entry(self.cadastrar)
        self.preco.grid(row=4, column=1, columnspan=2, pady=5, padx=5)

        Button(self.cadastrar, text='Cadastrar', width=15, bg='gray', relief='flat', highlightbackground='#524f4f',
               command=self.CadastrarProdutosBackEnd).grid(row=5, column=0, padx=5, pady=5)
        Button(self.cadastrar, text='Excluir', width=15, bg='gray', relief='flat', highlightbackground='#524f4f',
               command=self.RemoverCadastrosBackEnd).grid(row=5, column=1, padx=5, pady=5)
        Button(self.cadastrar, text='Atualizar', width=15, bg='gray', relief='flat', highlightbackground='#524f4f',
               command=self.CadastrarProdutosBackEnd).grid(row=6, column=0, padx=5, pady=5)
        Button(self.cadastrar, text='Limpar Produtos', width=15, bg='gray', relief='flat',
               highlightbackground='#524f4f', command=self.LimparCadastrosBackEnd).grid(row=6, column=1, padx=5, pady=5)

        self.tree = ttk.Treeview(self.cadastrar, selectmode='browse', column=(
            'column1', 'column2', 'column3', 'column4'), show='headings')

        self.tree.column('column1', width=200, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='Nome')
        self.tree.column('column2', width=400, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Ingredientes')
        self.tree.column('column3', width=200, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Grupo')
        self.tree.column('column4', width=60, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Preco')

        self.tree.grid(row=0, column=4, padx=10,
                       pady=10, columnspan=3, rowspan=6)

        self.MostrarProdutosBackEnd()

        self.cadastrar.mainloop()

    def MostrarProdutosBackEnd(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar ao banco de dados')

        try:
            with conn.cursor() as cursor:
                cursor.execute('select * from produtos')
                resultados = cursor.fetchall()
        except:
            print('Erro ao fazer consulta')

        self.tree.delete(*self.tree.get_children())

        linhaV = []

        for linha in resultados:
            linhaV.append(linha['nome'])
            linhaV.append(linha['ingredientes'])
            linhaV.append(linha['grupo'])
            linhaV.append(linha['preco'])

            self.tree.insert('', END, values=linhaV, iid=linha['id'], tag='1')
            linhaV.clear()

    def CadastrarProdutosBackEnd(self):
        nome = self.nome.get()
        ingrediente = self.ingredientes.get()
        grupo = self.grupo.get()
        preco = self.preco.get()

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar ao banco de dados')

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'insert into produtos (nome, ingredientes, grupo, preco) values (%s,%s,%s,%s)', (nome, ingrediente, grupo, preco))
                conn.commit()
        except:
            print('Erro ao cadastrar produto')

    def RemoverCadastrosBackEnd(self):
        idDeletar = int(self.tree.selection()[0])

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar ao banco de dados')

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'delete from produtos where id = %s', (idDeletar))
                conn.commit()
        except:
            print('Erro ao deletar produto')
        self.MostrarProdutosBackEnd()

    def LimparCadastrosBackEnd(self):
        if messagebox.askokcancel('Limpar dados CUIDADO!!!', 'DESEJA EXCLUIR TODOS OS DADOS DA TABELA? NÃO HÁ MAIS VOLTA!'):

            try:
                conn = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='',
                    db='erp',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
            except:
                print('Erro ao conectar ao banco de dados')

            try:
                with conn.cursor() as cursor:
                    cursor.execute('TRUNCATE produtos')
                    conn.commit()
            except:
                print('Erro ao deletar produtos')

            self.MostrarProdutosBackEnd()

    def MostrarPedidos(self):
        self.pedidos = Tk()
        self.pedidos.title('Pedidos')
        self.pedidos['bg'] = '#524f4f'

        Label(self.pedidos, text='Pedidos', bg='#524f4f', fg='white').grid(
            row=0, column=0, columnspan=4, padx=5, pady=5)

        # Label(self.pedidos, text='Nome', bg='#524f4f', fg='white').grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        # self.nome = Entry(self.pedidos)
        # self.nome.grid(row=1, column=1, columnspan=2, pady=5, padx=5)

        # Label(self.pedidos, text='Ingredientes', bg='#524f4f', fg='white').grid(row=2, column=0, columnspan=1, padx=5, pady=5)
        # self.ingredientes = Entry(self.pedidos)
        # self.ingredientes.grid(row=2, column=1, columnspan=2, pady=5, padx=5)

        # Label(self.pedidos, text='Grupo', bg='#524f4f', fg='white').grid(row=3, column=0, columnspan=1, padx=5, pady=5)
        # self.grupo = Entry(self.pedidos)
        # self.grupo.grid(row=3, column=1, columnspan=2, pady=5, padx=5)

        # Label(self.pedidos, text='Local de entrega', bg='#524f4f', fg='white').grid(row=4, column=0, columnspan=1, padx=5, pady=5)
        # self.lEntrega = Entry(self.pedidos)
        # self.lEntrega.grid(row=4, column=1, columnspan=2, pady=5, padx=5)

        # Label(self.pedidos, text='Observações', bg='#524f4f', fg='white').grid(row=5, column=0, columnspan=1, padx=5, pady=5)
        # self.observacoes = Entry(self.pedidos)
        # self.observacoes.grid(row=5, column=1, columnspan=2, pady=5, padx=5)

        Button(self.pedidos, text='Excluir', width=15, bg='gray', relief='flat', highlightbackground='#524f4f',
               command=self.RemoverPedidosBackEnd).grid(row=7, column=0, padx=5, pady=5)
        Button(self.pedidos, text='Atualizar', width=15, bg='gray', relief='flat', highlightbackground='#524f4f',
               command=self.MostrarPedidosBackEnd).grid(row=7, column=1, padx=5, pady=5)
        Button(self.pedidos, text='Limpar Produtos', width=15, bg='gray', relief='flat',
               highlightbackground='#524f4f', command=self.LimparPedidosBackEnd).grid(row=7, column=2, padx=5, pady=5)

        self.tree = ttk.Treeview(self.pedidos, selectmode='browse', column=(
            'column1', 'column2', 'column3', 'column4', 'column5'), show='headings')

        self.tree.column('column1', width=200, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='Nome')
        self.tree.column('column2', width=400, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Ingredientes')
        self.tree.column('column3', width=200, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Grupo')
        self.tree.column('column4', width=200, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Local de entrega')
        self.tree.column('column5', width=300, minwidth=500, stretch=NO)
        self.tree.heading('#5', text='Observações')

        self.tree.grid(row=1, column=0, padx=10,
                       pady=10, columnspan=3, rowspan=6)

        self.MostrarPedidosBackEnd()

        self.pedidos.mainloop()

    def MostrarPedidosBackEnd(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar ao banco de dados')

        try:
            with conn.cursor() as cursor:
                cursor.execute('select * from pedidos')
                resultados = cursor.fetchall()
        except:
            print('Erro ao fazer consulta')

        self.tree.delete(*self.tree.get_children())

        linhaV = []

        for linha in resultados:
            linhaV.append(linha['nome'])
            linhaV.append(linha['ingredientes'])
            linhaV.append(linha['grupo'])
            linhaV.append(linha['localEntrega'])
            linhaV.append(linha['observacoes'])

            self.tree.insert('', END, values=linhaV, iid=linha['id'], tag='1')
            linhaV.clear()

    def RemoverPedidosBackEnd(self):
        idDeletar = int(self.tree.selection()[0])

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar ao banco de dados')

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'delete from pedidos where id = %s', (idDeletar))
                conn.commit()
        except:
            print('Erro ao remover pedido')
        self.MostrarPedidosBackEnd()

    def LimparPedidosBackEnd(self):
        if messagebox.askokcancel('Limpar dados CUIDADO!!!', 'DESEJA EXCLUIR TODOS OS DADOS DA TABELA? NÃO HÁ MAIS VOLTA!'):

            try:
                conn = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='',
                    db='erp',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
            except:
                print('Erro ao conectar ao banco de dados')

            try:
                with conn.cursor() as cursor:
                    cursor.execute('TRUNCATE pedidos')
                    conn.commit()
            except:
                print('Erro ao deletar pedidos')

            self.MostrarPedidosBackEnd()


class JanelaLogin():

    def VerificaLogin(self):
        autenticado = False
        usuarioMaster = False
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar ao banco de dados')

        usuario = self.login.get()
        senha = self.senha.get()

        try:
            with conn.cursor() as cursor:
                cursor.execute('select * from cadastros')
                resultado = cursor.fetchall()
        except:
            print('Erro ao fazer consulta')

        for linha in resultado:
            if usuario == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False

        if not autenticado:
            messagebox.showinfo('login', 'Email ou senha inválido')
        if autenticado:
            self.root.destroy()
            if usuarioMaster:
                AdminJanela()

    def Cadastro(self):
        Label(self.root, text='Chave de segurança').grid(
            row=3, column=0, pady=5, padx=5)
        self.codigoSeguranca = Entry(self.root, show='*')
        self.codigoSeguranca.grid(row=3, column=1, pady=5, padx=10)

        Button(self.root, text='Confirmar cadastro', width=15, bg='blue1', fg='white',
               command=self.CadastroBackEnd).grid(row=4, column=0, columnspan=2, pady=5, padx=10)

    def CadastroBackEnd(self):
        codigoPadrao = '123@h'

        if self.codigoSeguranca.get() == codigoPadrao:
            if len(self.login.get()) <= 20:
                if len(self.senha.get()) <= 50:
                    nome = self.login.get()
                    senha = self.senha.get()

                    try:
                        conn = pymysql.connect(
                            host='localhost',
                            user='root',
                            password='',
                            db='erp',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor
                        )
                    except:
                        print('Erro ao conectar ao banco de dados')

                    try:
                        with conn.cursor() as cursor:
                            cursor.execute(
                                'insert into cadastros (nome, senha, nivel) values (%s,%s,%s)', (nome, senha, 1))
                            conn.commit()
                        messagebox.showinfo(
                            'Cadastro', 'Usuário cadastrado com sucesso')
                        self.root.destroy()
                    except:
                        print('Erro ao isnerir dados')
                else:
                    messagebox.showerror(
                        'Erro', 'Senha é maior que 50 caracteres. Por favor, insira uma senha com 50 ou menos caracteres')
            else:
                messagebox.showerror(
                    'Erro', 'Nome é maior que 20 caracteres. Por favor, insira um nome com 20 ou menos caracteres')
        else:
            print('Erro no código de segurança')

    def UpdateBackEnd(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar ao banco de dados')

        try:
            with conn.cursor() as cursor:
                cursor.execute('select * from cadastros')
                resultados = cursor.fetchall()
        except:
            print('Erro ao fazer consulta')

        self.tree.delete(*self.tree.get_children())

        linhaV = []

        for linha in resultados:
            linhaV.append(linha['id'])
            linhaV.append(linha['nome'])
            linhaV.append(linha['senha'])
            linhaV.append(linha['nivel'])

            self.tree.insert('', END, values=linhaV, iid=linha['id'], tag=1)
            linhaV.clear()

    def VisualizarCadastros(self):
        self.vc = Toplevel()
        self.vc.resizable(False, False)
        self.vc.title('Visualizar cadastros')

        self.tree = ttk.Treeview(self.vc, selectmode='browse', column=(
            'column1', 'column2', 'column3', 'column4'), show='headings')

        self.tree.column('column1', width=40, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='ID')
        self.tree.column('column2', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Usuário')
        self.tree.column('column3', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Senha')
        self.tree.column('column4', width=40, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Nível')

        self.tree.grid(row=0, column=0, padx=10, pady=10)
        self.UpdateBackEnd()
        self.vc.mainloop()

    def __init__(self):
        self.root = Tk()
        self.root.title('Login')
        Label(self.root, text='Faça o login').grid(
            row=0, column=0, columnspan=2)

        Label(self.root, text='Usuário').grid(row=1, column=0)

        self.login = Entry(self.root)
        self.login.grid(row=1, column=1, padx=5, pady=5)

        Label(self.root, text='Senha').grid(row=2, column=0)

        self.senha = Entry(self.root, show='*')
        self.senha.grid(row=2, column=1, padx=5, pady=5)

        Button(self.root, text='Login', bg='green3', command=self.VerificaLogin, width=10).grid(row=5, column=0,
                                                                                                padx=10, pady=5)

        Button(self.root, text='Cadastrar', bg='orange3',
               width=10, command=self.Cadastro).grid(row=5, column=1)

        Button(self.root, text='Visualizar cadastros', bg='white', command=self.VisualizarCadastros).grid(
            row=6, column=0, columnspan=2, padx=10, pady=5)

        self.root.mainloop()


JanelaLogin()
