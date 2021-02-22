import pymysql.cursors
import matplotlib.pyplot as plt

conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='erp',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

autentico = False


def logarCadastrar():
    autenticado = False
    usuarioMaster = False
    if decisao == 1:
        nome = input("Digite o nome: ")
        senha = input("Digite sua senha: ")

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False
        if not autenticado:
            print('email ou senha errado')
    elif decisao == 2:
        print('Faça seu cadastro')
        nome = input("Digite o nome: ")
        senha = input("Digite sua senha: ")

        for linha in resultado:
            if nome == linha['nome']:
                print('Usuário existente')
            else:
                try:
                    with conexao.cursor() as cursor:
                        cursor.execute(
                            'insert into cadastros(nome, senha, nivel) values (%s,%s,%s)', (nome, senha, 1))
                        conexao.commit()
                        print('Usuário cadastrado com sucesso')
                except:
                    print('Erro ao inserir os dados')
    return autenticado, usuarioMaster


def cadastrarProdutos():
    nome = input('Digite o nome do produto: ')
    ingredientes = input('Digite os ingredientes do produto: ')
    grupo = input('Digite o grupo pertencente a esse produto: ')
    preco = float(input('Digite o preço do produto: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('insert into produtos (nome, ingredientes, grupo, preco) values (%s,%s,%s,%s)',
                           (nome, ingredientes, grupo, preco))
            conexao.commit()
            print('Produto cadastrado com sucesso!')
    except:
        print('Erro ao inserir os produtos no banco de dados.')


def listarProdutos():
    produtos = []

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtosCadastrados = cursor.fetchall()
    except:
        print('Erro ao conectar ao banco de dados')

    for i in produtosCadastrados:
        produtos.append(i)

    if len(produtos) != 0:
        print('ID     PODUTO')
        for i in range(0, len(produtos)):
            print(produtos[i]['id'], '    ', produtos[i]['nome'])
    else:
        print('Nenhum produto casastrado')


def excluirProdutos():
    idDeletar = int(
        input('Digite o id referente ao produto que deseja apagar: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('delete from produtos where id = %s', (idDeletar))
            conexao.commit()
            print('\nProduto excluido com sucesso\n')
    except:
        print('Erro ao excluir o produto.')


def listarPedidos():
    pedidos = []
    decision = 0

    while decision != 0:
        pedidos.clear()

        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from pedidos')
                listaPedidos = cursor.fetchall()
        except:
            print('Erro no banco de dados')

        for i in listaPedidos:
            pedidos.append(i)

        if len(pedidos) != 0:
            for i in range(0, len(pedidos)):
                print(pedidos[i])
        else:
            print('Nenhum pedido foi feito')

        decision = int(input('1 - Pedido entregue\n0 - Voltar\n-> '))

        if decision == 1:
            idDeletar = int(input('Digite o id do predido entregue: '))

            try:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        'delete from pedidos where id = %s', idDeletar)
                    print('Produto dado como entregue')
                    conexao.commit()
            except:
                print('Erro ao dar o pedido como entregue')


def gerarEstatistica():

    nomeProdutos = []
    nomeProdutos.clear()

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall()
    except:
        print('Erro no banco de dados')

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from estatisticaVendido')
            vendido = cursor.fetchall()
    except:
        print('Erro no banco de dados')

    estado = int(
        input('1 - Pesquisar por nome\n2 - Pesquisar por grupo\n0 - Sair\n-> '))

    if estado == 1:
        decisao3 = int(
            input('1 - Pesquisar por valor\n2 - Quantidade unitária\n-> '))
        if decisao3 == 1:
            for i in produtos:
                nomeProdutos.append(i['nome'])
                
            valores = []
            valores.clear()
            
            for h in range(0, len(nomeProdutos)):
                somaValor = -1
                for i in vendido:
                    if i['nome'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor+1)
    
            plt.plot(nomeProdutos, valores)
            plt.ylabel('Quantidade vendida em reais')
            plt.xlabel('Produtos')
            plt.show()
            
        if decisao3 == 2:
            grupoUnico = []
            grupoUnico.clear()
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('Erro no banco de dados')
                
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatisticaVendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('Erro no banco de dados')
            
            for i in grupo:
                grupoUnico.append(i['nome'])
                
            grupoUnico = sorted(set(grupoUnico))
            qtdFinal = []
            qtdFinal.clear()
            
            for h in range(0, len(grupoUnico)):
                qtdUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['nome']:
                        qtdUnitaria += 1
                qtdFinal.append(qtdUnitaria)
            
            plt.plot(grupoUnico, qtdFinal)
            plt.ylabel('Quantidade unitaria vendida')
            plt.xlabel('Produtos')
            plt.show()
            
    elif estado == 2:
        decisao3 = int(
            input('1 - Pesquisar por valor\n2 - Quantidade unitária\n-> '))
        if decisao3 == 1:
            for i in produtos:
                nomeProdutos.append(i['nome'])
                
            valores = []
            valores.clear()
            
            for h in range(0, len(nomeProdutos)):
                somaValor = -1
                for i in vendido:
                    if i['nome'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor+1)
    
            plt.plot(nomeProdutos, valores)
            plt.ylabel('Quantidade vendida em reais')
            plt.xlabel('Produtos')
            plt.show()
            
        if decisao3 == 2:
            grupoUnico = []
            grupoUnico.clear()
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('Erro no banco de dados')
                
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatisticaVendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('Erro no banco de dados')
            
            for i in grupo:
                grupoUnico.append(i['grupo'])
                
            grupoUnico = sorted(set(grupoUnico))
            qtdFinal = []
            qtdFinal.clear()
            
            for h in range(0, len(grupoUnico)):
                qtdUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['grupo']:
                        qtdUnitaria += 1
                qtdFinal.append(qtdUnitaria)
            
            plt.plot(grupoUnico, qtdFinal)
            plt.ylabel('Quantidade unitaria vendida')
            plt.xlabel('Produtos')
            plt.show()
            


while not autentico:
    decisao = int(input('Digite 1 para logar e 2 para cadastrar: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from cadastros')
            resultado = cursor.fetchall()
    except:
        print('Erro ao conectar')

    autentico, usuarioSupremo = logarCadastrar()

if autentico == True:
    print('Autenticado')
    if usuarioSupremo == True:
        decisaoUsuario = 1
        while decisaoUsuario != 0:
            decisaoUsuario = int(
                input('\nMenu ERP\n1 - Cadastrar produtos\n2 - Listar produtos cadastrados\n3 - Listar pedidos\n4 - Visualizar as estatisticas\n0 - Sair\n-> '))

            if decisaoUsuario == 1:
                cadastrarProdutos()
            elif decisaoUsuario == 2:
                listarProdutos()

                delete = int(input('\n1 - Excluir um produto\n0 - Sair\n-> '))
                if delete == 1:
                    excluirProdutos()
            elif decisaoUsuario == 3:
                listarPedidos()
                
            elif decisaoUsuario == 4:
                gerarEstatistica()
