# PicPay Challenge - QA Engineer

Este projeto foi criado para atender o desafio da vaga de QA Engineer do Picpay. A descrição do desafio consiste em:

```
Utilizando a Collection do Postman abaixo:
https://www.getpostman.com/collections/77cfd2465c5d146503d0

Fazer os seguintes cenários de automação utilizando o framework de sua preferência:
- Usar o endpoint de 'Criar um Usuario' para criar um usuário válido, e então validar se o mesmo foi criado no endpoint 'Listar todos Usuarios';
- Alterar o nome deste usuário criado com o endpoint 'Alterar dados do Usuario' e então validar as alterações no endpoint 'Listar um unico Usuario';
- Deletar o usuário criado no endpoint 'Deletar Usuario' e validar se o mesmo foi removido no endpoint 'Listar todos Usuarios'';
```

## Cenários Automatizados
Foram identificados cenários além dos propostos no desafio que achei interessante automatizar. A lista completa de cenários automatizados é:

- Teste de criação de usuário e validação se o mesmo existe no endpoint Listar todos os Usuários
- Teste de alteração do nome de um usuário e a validação das alterações no endpoint Listar um unico Usuario
- Teste de deleção de um usuário através do endpoint Deletar Usuario e verificação se o mesmo foi deletado de fato no endpoint Listar todos Usuarios e Listar um Unico Usuario
- Teste de validação de campos obrigatórios no endpoint de criação de usuário
- Teste de validação de campos inválidos no endpoint de criação de usuário
- Teste de validação de tentativa de deleção de um usuário não existente
- Teste de validação de tentativa de alteração de dados de um usuário não existente
- Teste de validação de credenciais na criação de usuário
- Teste de validação de credenciais na deleção de usuário
- Teste de validação de credenciais na alteração dos dados do usuário

## Framework escolhido

O framework escolhido para a implementação dos testes foi o pytest (Python)

## Pré-requisitos

Para instalar e executar o projeto, basta ter a versão 3.6 ou maior do python instalada na máquina

## Instalação

1. **Realize o clone do repositório:**

 ```sh
 git clone https://github.com/joaolucasfernandes/pp-challenge.git`
```

***
2. **Entre na pasta do projeto(pp-challenge) e rode o seguinte comando:**

```sh
pip install -r requirements.txt`
```

***

## Rodando os testes

**Após instalar o projeto e suas dependências, dentro da pasta raiz do projeto (pp-challenge), execute:**

 `pytest -v -n 15 --reruns 5 --reruns-delay 1`

## Estrutura do Projeto
```
|api-test [1]  
├──resources [2]  
│  └──clients [3] 
│  └───utils [4] 
└───tests [5]
```
1. `api-test` - Pasta raiz dos testes de api do projeto
2. `resources` - Pasta que agrega diretórios com recursos a serem usados no projeto pelos testes, como clients, helpers, classes base, utils, etc...
3. `utils` - Pasta que contém utilitários a serem usados pelos testes
4. `clients` - Pasta que contém os clients usados no projeto pelos testes (Clients são classes que encapsulam algumas funcionalidades de determinadas entidades no contexto da Api (Métodos put, get, delete, post, etc))
5. `tests` - Pasta que contém os arquivos onde os testes estão de fato implementados 

### Observações adicionais
Durante os testes, encontrei alguns bugs  e comportamentos cuja a implementação na aplicação poderia ser discutida com o time de negócios:

1. Não enviar valores relacionados aos campos no Json, causa um erro 500. Tratar isso seria legal. (Retornando um 400, talvez?)
2. Quando você coloca um número no campo nome no payload de cadastro do usuário, a API aceita. Talvez uma validação aceitando só Strings valeria a pena, já que nomes geralmente não são compostos por números.
3. O status da maioria dos requests feitos, retorna sempre 200, e o código de fato relacionado a resposta, fica dentro do payload da mesma, no campo code (Um request com um token inválido retorna 200 no status code, e 401 no campo code, na resposta por exemplo). Já vi muitas implementações de api, e esse é apenas um modo de se fazer. Mas acredito que seria melhor retornar o código correto já no status code. Isso faz com que os clientes da api não precisem escrever códigos que olhem para além do status code para validar respostas de erro ou validação, como um 401, por exemplo. 
5. O timezone usado pela api é um timezone diferente do Brasil. Seria bom verificar com o time de negócios se isso não causaria problemas em algum nível.
6. Os erros relacionados a não existência de um registro na api(404) estão tendo precedência sob erros de autenticação. Ou seja, se eu enviar um request para deletar um usuário com um id que não existe e com o token de autenticação inválido, o erro que me é retornado é o 404, antes do 401. Acredito que seria melhor fazer a verificação do token antes de realizar qualquer outra operação no sistema(neste caso, a consulta pra ver se o usuário existe ou não antes de deletar). Tanto em termos de eficiência quanto de segurança.