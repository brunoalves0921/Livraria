# Livraria Sr. Code

Este projeto consiste em uma aplicação de uma livraria chamada "Livraria Sr. Code", implementada em Python utilizando a biblioteca PySimpleGUI. A livraria possui funcionalidades como cadastrar livros, comprar livros, vender livros, consultar o dinheiro em caixa, consultar o histórico de vendas e consultar o estoque.

## Funcionalidades

### Cadastrar Livro
Ao selecionar a opção "Cadastrar Livro" no menu principal, é exibida uma janela onde o usuário pode inserir as informações do livro, como nome, valor e tipo. O livro é então cadastrado na livraria.

### Comprar Livro
Ao selecionar a opção "Comprar Livro" no menu principal, é exibida uma janela com uma lista de livros disponíveis no estoque. O usuário pode selecionar um livro e informar a quantidade desejada. Após a confirmação da compra, o livro é adicionado ao estoque da livraria e o valor da compra é deduzido do saldo em caixa.

### Vender Livro
Ao selecionar a opção "Vender Livro" no menu principal, é exibida uma janela com uma lista de livros disponíveis no estoque. O usuário pode selecionar um livro e informar a quantidade a ser vendida. Após a confirmação da venda, a quantidade de livros é deduzida do estoque da livraria, e o valor da venda é adicionado ao saldo em caixa.

### Consultar Dinheiro em Caixa
Ao selecionar a opção "Consultar Dinheiro em Caixa" no menu principal, uma janela exibe o saldo atual em caixa da livraria.

### Consultar Histórico de Vendas
Ao selecionar a opção "Consultar Histórico de Vendas" no menu principal, uma janela exibe o histórico de vendas da livraria, contendo informações como o nome do livro, valor total da venda, quantidade vendida e data da venda.

### Consultar Estoque
Ao selecionar a opção "Consultar Estoque" no menu principal, é exibida uma janela com uma lista de livros disponíveis no estoque. O usuário pode selecionar um livro e obter informações detalhadas sobre o livro, incluindo seu nome, valor, tipo e características específicas.

## Arquivos
A livraria utiliza dois arquivos para armazenar os dados: "estoque.json" e "vendas.json". O arquivo "estoque.json" contém as informações sobre o estoque de livros e o saldo em caixa da livraria, em formato JSON. O arquivo "vendas.json" armazena o histórico de vendas da livraria, também em formato JSON.

## Autor

Jorge Bruno Costa Alves

*Universidade Federal do Ceará - Campus Quixadá.*
