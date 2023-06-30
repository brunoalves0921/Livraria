from datetime import datetime as dt
import PySimpleGUI as sg
import json

class LivrariaException(Exception):
    pass
class Livraria():
    def __init__(self):
        sg.theme('reddit')
        self.layout = [
            [sg.Button('Cadastrar Livro', key='cadastrar', size=(60, 2))],
            [sg.Button('Comprar Livro', key='comprarlivro', size=(60, 2))],
            [sg.Button('Vender Livro', key='venderlivro', size=(60, 2))],
            [sg.Button('Consultar Dinheiro em Caixa', key='consultardinheiro', size=(60, 2))],
            [sg.Button('Consultar Histórico de Vendas', key='consultarhistorico', size=(60, 2))],
            [sg.Button('Consultar Estoque', key='consultarEstoque', size=(60, 2))],
        ]
        self.janela = sg.Window('Livraria Sr. Code', self.layout)
        self.historicoVendasArquivo = open("vendas.json", "a", encoding="utf-8")
        self.vendas = 0
        self.dinheiroCaixa = 1000
        self.estoque:dict[int, Livro] = dict()
        try:
            estoque = json.loads(open("estoque.json", "r", encoding="utf-8").read())
            for livro in estoque['livros']:
                self.estoque[livro["id"]] = Livro.fromJSON(livro)
            self.dinheiroCaixa = estoque['caixa']
        except FileNotFoundError:
            pass

    def venderLivro(self, idLivro, qtd):
        if idLivro not in self.estoque:
            raise LivrariaException("Livro não encontrado")

        livro = self.estoque[idLivro]
        if livro.qtdEstoque <= 0:
            raise LivrariaException("Livro sem estoque")

        if livro.qtdEstoque < qtd:
            raise LivrariaException("Quantidade de livros insuficiente")
        if qtd <= 0:
            raise LivrariaException("Quantidade inválida")


        livro.qtdEstoque -= qtd
        self.vendas += livro.valor * qtd
        self.dinheiroCaixa += livro.valor * qtd
        self.__salvarEstoque()
        self.historicoVendasArquivo.write(f"Livro: {livro.nome} - Valor Total: {livro.valor * qtd}R$ - Quantidade: {qtd} - Data: {dt.now().strftime('(%d/%m/%Y) %H:%M')}\n")
        self.historicoVendasArquivo.flush()
        return True

    def __salvarEstoque(self):
        livros = [livro.toJSON() for livro in self.estoque.values()]
        open("estoque.json", "w", encoding="utf-8").write(json.dumps(
            {'caixa': self.dinheiroCaixa, 'livros': livros},  indent=4, ensure_ascii=False
        ))

    def addLivro(self, livro):
        if livro.id in self.estoque:
            self.estoque[livro.id].qtdEstoque += livro.qtdEstoque
        else:
            self.estoque[livro.id] = livro
        self.__salvarEstoque()

    def comprarLivro(self, idLivro, qtd):
        if idLivro not in self.estoque:
            raise LivrariaException("Livro não encontrado")

        livro = self.estoque[idLivro]
        if livro.valor * 0.7 * qtd > self.dinheiroCaixa:
            raise LivrariaException("Dinheiro insuficiente")

        livro.qtdEstoque += qtd
        self.dinheiroCaixa -= livro.valor * 0.7 * qtd
        self.__salvarEstoque()
        return True
class Livro():
    __count = 0
    def __init__(self, nome:str, valor:float, tipo:str, qtdEstoque:int=0):
        self.__nome = nome
        self.__valor = valor
        self.__qtdEstoque = qtdEstoque
        self.__id = Livro.__count
        self.__tipo = tipo
        Livro.__count += 1

    @property
    def nome(self):
        return self.__nome
    @property
    def valor(self):
        return self.__valor
    @property
    def qtdEstoque(self):
        return self.__qtdEstoque
    @property
    def nome(self):
        return self.__nome
    @property
    def tipo(self):
        return self.__tipo
    @property
    def caracteristicas(self):
        match self.__tipo:
            case 'aventura':
                return 'ilustrações'
            case 'drama':
                return 'capa dura'
            case 'comedia':
                return 'capa tipo brochura'
    @property
    def id(self):
        return self.__id

    @qtdEstoque.setter
    def qtdEstoque(self, qtdEstoque):
        self.__qtdEstoque = qtdEstoque

    def toJSON(self):
        return {
            'id': self.__id,
            'nome': self.__nome,
            'valor': self.__valor,
            'tipo': self.__tipo,
            'qtdEstoque': self.__qtdEstoque
        }

    @staticmethod
    def fromJSON(json):
        livro = Livro(json['nome'], json['valor'], json['tipo'], json['qtdEstoque'])
        livro.__id = json['id']
        if livro.__id >= Livro.__count:
            Livro.__count = livro.__id + 1
        return livro

def iniciar():
    livraria = Livraria()
    while True:
        event, values = livraria.janela.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'comprarlivro':
            layout = [
                [sg.Listbox(values=[f"ID: {livro.id} - Nome: {livro.nome} - Valor de compra: {livro.valor * 0.7}R$ - Valor de revenda: {livro.valor}" for livro in livraria.estoque.values()], size=(90, 10), key='livros')],
                [sg.Text('Quantidade:'), sg.Input(key='qtd', size=(5, 1)), sg.Text('Saldo no caixa: ' + str(livraria.dinheiroCaixa) + 'R$', key='saldo')],
                [sg.Button('Comprar')]
            ]
            janela = sg.Window('Comprar Livro', layout)
            while True:
                event, values = janela.read()
                if event == sg.WINDOW_CLOSED:
                    break
                if event == 'Comprar':
                    try:
                        if not values['livros'] == []:
                            idLivro = int(values['livros'][0].split(' - ')[0].split(': ')[1])
                            qtd = int(values['qtd'])
                            if qtd <= 0:
                                raise LivrariaException("Quantidade inválida")
                            livraria.comprarLivro(idLivro, qtd)
                            sg.popup('Compra realizada com sucesso')
                            janela['saldo'].update('Saldo no caixa: ' + str(livraria.dinheiroCaixa) + 'R$')

                        else:
                            sg.popup('ID inválido, selecione um livro da lista')
                    except LivrariaException as e:
                        sg.popup(e)
                    except ValueError:
                        sg.popup('ID ou quantidade inválidos')
        if event == 'venderlivro':
            layout = [
                [sg.Listbox(values=[f"ID: {livro.id} - Nome: {livro.nome} - Valor: {livro.valor} - Quantidade em estoque: {livro.qtdEstoque}" for livro in livraria.estoque.values()], size=(80, 10), key='livros')],
                [sg.Text('Quantidade:'), sg.Input(key='qtd', size=(5, 1)), sg.Text('Saldo no caixa: ' + str(livraria.dinheiroCaixa) + 'R$', key='saldo')],
                [sg.Button('Vender')]
            ]
            janela = sg.Window('Vender Livro', layout)
            while True:
                event, values = janela.read()
                if event == sg.WINDOW_CLOSED:
                    break
                if event == 'Vender':
                    try:
                        if not values['livros'] == []:
                            idLivro = int(values['livros'][0].split(' - ')[0].split(': ')[1])
                            qtd = int(values['qtd'])
                            livraria.venderLivro(idLivro, qtd)
                            sg.popup('Venda realizada com sucesso')
                            janela['qtd'].update('')
                            janela['saldo'].update('Saldo no caixa: ' + str(livraria.dinheiroCaixa) + 'R$')
                            janela['livros'].update([f"ID: {livro.id} - Nome: {livro.nome} - Valor: {livro.valor} - Quantidade em estoque: {livro.qtdEstoque}" for livro in livraria.estoque.values()])
                        else:
                            sg.popup('ID inválido, selecione um livro da lista')
                    except LivrariaException as e:
                        sg.popup(e)
                    except ValueError:
                        sg.popup('ID ou quantidade inválidos')
        if event == 'cadastrar':
            layout = [
                [sg.Text('Nome do livro:')],
                [sg.Input(key='nome', size=(45, 2))],
                [sg.Text('Valor do livro:')],
                [sg.Input(key='valor', size=(45, 2))],
                [sg.Text('Escolha o tipo do livro:')],
                [sg.Radio('Aventura', 'tipo', key='aventura'), sg.Radio('Drama', 'tipo', key='drama'), sg.Radio('Comédia', 'tipo', key='comedia')],
                [sg.Button('Cadastrar')],
            ]
            janela = sg.Window('Cadastrar Livro na livraria ', layout)
            while True:
                event, values = janela.read()
                if event == sg.WINDOW_CLOSED:
                    break
                if event == 'Cadastrar':
                    try:
                        if values['aventura']:
                            tipo = 'aventura'
                        elif values['drama']:
                            tipo = 'drama'
                        elif values['comedia']:
                            tipo = 'comedia'
                        else:
                            raise LivrariaException('Tipo inválido')
                        if values['nome'] == '':
                            raise LivrariaException('Nome inválido')
                        if float(values['valor']) <= 0:
                            raise LivrariaException('Valor inválido')
                        livro = Livro(values['nome'], float(values['valor']), tipo)
                        livraria.addLivro(livro)
                        sg.popup('Livro cadastrado com sucesso')
                        janela.close()
                    except LivrariaException as e:
                        sg.popup(e)
                    except ValueError:
                        sg.popup('Valor inválido')
        if event == 'consultardinheiro':
            sg.popup(f'Você tem R${livraria.dinheiroCaixa:.2f} no caixa')
        if event == 'consultarhistorico':
            with open('vendas.json', 'r', encoding="utf-8") as historico:
                layout = [
                    [sg.Multiline(historico.read(), size=(90, 20), key='historico')],
                    [sg.Button('Voltar')]
                ]
            janela = sg.Window('Histórico de vendas', layout)
            while True:
                event, values = janela.read()
                if event == sg.WINDOW_CLOSED:
                    break
                if event == 'Voltar':
                    janela.close()
                    break
        if event == 'consultarEstoque':
            layout = [
                [sg.Listbox(values=[f"ID: {livro.id} - Quantidade em estoque: {livro.qtdEstoque}" for livro in livraria.estoque.values()], size=(80, 10), key='livros')],
                [sg.Button('Consultar')],
            ]
            janela = sg.Window('Consultar Estoque', layout)
            while True:
                event, values = janela.read()
                if event == sg.WINDOW_CLOSED:
                    break
                if event == 'Consultar':
                    try:
                        if not values['livros'] == []:
                            idLivro = int(values['livros'][0].split(' - ')[0].split(': ')[1])
                            livro = livraria.estoque[idLivro]
                            sg.popup(f"Nome: {livro.nome} \nValor: {livro.valor} \nTipo: {livro.tipo} \nCaracterísticas: {livro.caracteristicas}", title='Informações do livro')
                        else:
                            sg.popup('ID inválido, selecione um livro da lista')
                    except LivrariaException as e:
                        sg.popup(e)
                    except ValueError:
                        sg.popup('ID inválido')
iniciar()

