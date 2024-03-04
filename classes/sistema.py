from classes.aluno import Aluno
from classes.conta_aluno import Conta
from classes.clear import clear
from classes.caminho_arquivos import Caminhos
import json


class Sistema:
    def __init__(self) -> None:
        self.sessao_ativa = True

    # método para limpar o terminal e printar um cabeçalho
    def cabecalho(self):
        clear()
        print("=== Biblioteca Virtual da Descomplica ===\n\n")

    # método para iniciar o loop do sistema
    def iniciar_sistema(self):
        while self.sessao_ativa:
            self.cabecalho()
            menu = input("Opções:\n1 - Login\n2 - Cadastrar\n3 - Sair\n>")

            # checar erros de entrada para as opções
            if not menu.isdigit() or (menu != "1" and menu != "2" and menu != "3"):
                print("Opção desconhecida.\nSelecione uma opção digitando apenas o seu número.\nPor exemplo: [1], [2] ou [3].")
                input("Pressione ENTER para continuar...")

            # ao selecionar a opção "1 - Login"
            elif menu == "1":
                self.login_aluno()

            # ao selecionar a opção "2 - Cadastrar"
            elif menu == "2":
                self.cadastrar_aluno()

            # ao selecionar a opção "3 - Sair"
            elif menu == "3":
                self.encerrar_sessao()

            # tratamento para demais opções desconhecidas/inválidas
            else:
                print("Opção desconhecida. Por favor, tente novamente!")
                input("Pressione ENTER para continuar...")

    # método para fazer login como aluno
    def login_aluno(self):
        self.cabecalho()

        login = input("Para começar, informe o seu RA do Aluno:\n>").lower()

        if login.isdigit() and len(login) == 7:
            conta = Conta(login)

            # verifica se conta.dados_aluno é igual a None, se for, significa que o aluno não foi encontrado
            if conta.dados_aluno == None:
                print("Aluno não encontrado. Verifique o RA do Aluno e tente novamente!")
                input("Pressione ENTER para continuar...")
                return 1
            
            self.menu_login(conta)
        else:
            print("Seu RA do Aluno é composto por 7 caracteres numéricos entre 0 e 9. Por favor, tente novamente!")
            input("Pressione ENTER para continuar...")
            return 1

    # método para mostrar o menu após o login como aluno
    def menu_login(self, conta):
        while True:
            self.cabecalho()
            print(f"Olá {conta.dados_aluno['nome']}!")

            opcao = input("O que deseja fazer?\n\n1 - Alugar Livro\n2 - Devolver Livro\n3 - Ver Acervo\n4 - Sair\n>")

            # checar erros de entrada para as opções
            if not opcao.isdigit() or (opcao != "1" and opcao != "2" and opcao != "3" and opcao != "4"):
                    print("Opção desconhecida.\nSelecione uma opção digitando apenas o seu número.\nPor exemplo: [1], [2] ou [3].")
                    input("Pressione ENTER para continuar...")

            # ao selecionar a opção "1 - Alugar Livro"
            elif opcao == "1":
                self.alugar(conta)

            # ao selecionar a opção "2 - Devolver Livro"
            elif opcao == "2":
                self.devolucao(conta)

            # ao selecionar a opção "3 - Ver Acervo"
            elif opcao == "3":
                self.ver_acervo()

            # ao selecionar a opção "4 - Sair"
            elif opcao == "4":
                return 0

            # tratamento para demais opções desconhecidas/inválidas
            else:
                print("Opção desconhecida. Por favor, tente novamente!")
                input("Pressione ENTER para continuar...")

    # método para cadastrar alunos
    def cadastrar_aluno(self):
        self.cabecalho()

        print("Boas-vindas à Biblioteca Virtual da Descomplica!\n")
        print("Bora começar o seu cadastro?\n")

        ra_aluno = input("Para começar, por favor, informe seu RA do Aluno:\n>")

        if ra_aluno.isdigit() and len(ra_aluno) == 7:
            if self.ra_aluno_ja_cadastrado(ra_aluno):
                print("Um aluno com este RA já foi cadastrado!")
                input("Pressione ENTER para continuar...")
                return 1
            else:
                nome_aluno = input("Perfeito, agora informe seu NOME COMPLETO:\n>").upper()
                if not nome_aluno.replace(' ','').isalpha() or len(nome_aluno.split(" ")) < 2:
                    print("Entrada inválida, por favor, certifique-se de digitar o seu NOME COMPLETO e utilizar somente caracteres alfabéticos!")
                    input("Pressione ENTER para continuar...")
                    return 1

                curso_aluno = input("Beleza, agora informe o curso de sua matrícula:\n>").upper()
                if not curso_aluno.replace(' ', '').isalpha() or len(curso_aluno.split(" ")) < 1 or len(curso_aluno) < 3:
                    print("Entrada inválida, por favor, certifique-se de digitar corretamente o nome do seu CURSO e utilizar somente caracteres alfabéticos!")
                    input("Pressione ENTER para continuar...")
                    return 1
                
                novo_cadastro = Aluno(ra_aluno, nome_aluno, curso_aluno)

                try:
                    caminho = Caminhos()
                    with open(caminho.registro_alunos, "r+", encoding="utf-8") as reg_alunos_json:
                        conteudo = reg_alunos_json.read()

                        reg_alunos = json.loads(conteudo)
                        reg_alunos[ra_aluno] = novo_cadastro.dados_aluno

                        reg_alunos_json.seek(0)
                        json.dump(reg_alunos, reg_alunos_json)
                        reg_alunos_json.truncate()

                    print("Cadastro realizado com sucesso!")
                    input("Pressione ENTER para continuar...")
                    return 0
                except Exception as e:
                    print(f"ERRO: {e}")
                    input("Pressione ENTER para continuar...")
                    return 1
        else:
            print("Seu RA do Aluno é composto por 7 caracteres numéricos entre 0 e 9. Por favor, tente novamente!")
            input("Pressione ENTER para continuar...")
            return 1

    # método para verificar se o ra do aluno já está cadastrado ou não
    def ra_aluno_ja_cadastrado(self, ra_aluno):
        caminho = Caminhos()
        try:
            with open(caminho.registro_alunos, "r", encoding="utf-8") as reg_alunos_json:
                conteudo = reg_alunos_json.read()

                if conteudo:
                    reg_alunos = json.loads(conteudo)

                    if reg_alunos:
                        for aluno in reg_alunos:
                            if aluno == ra_aluno:
                                return True
                return False
        except Exception as e:
            print(f"ERRO: {e}")
            input("Pressione ENTER para continuar...")
            return True
        
    # método para verificar se o livro encontra-se alugado ou não, retorna True para alugado e False para não alugado
    def livro_alugado(self, id_livro):
        try:
            caminho = Caminhos()
            with open(caminho.acervo, "r+", encoding="utf-8") as acervo_json:
                conteudo = acervo_json.read()

                if conteudo:
                    acervo = json.loads(conteudo)

                    if acervo:
                        if acervo[id_livro]["disponibilidade"]["esta_alugado"] == True:
                            print("Este Livro já está sendo alugado.")
                            input("Pressione ENTER para continuar...")
                            return True
                        else:
                            return False
                return False
        except Exception as e:
            print(f"ERRO: {e}")
            input("Pressione ENTER para continuar...")
            return True

    # método para alugar um livro
    def alugar(self, conta_aluno):
        if conta_aluno.dados_aluno["esta_alugando"] == True:
            print("Esta conta já está alugando um livro no momento.\nRealize a devolução para alugar outro livro.")
            input("Pressione ENTER para continuar...")
            return 1
        return conta_aluno.alugar_livro()

    # método para devolver um livro
    def devolucao(self, conta_aluno):
        if conta_aluno.dados_aluno["esta_alugando"] == False:
            print("Esta conta não está alugando nenhum livro no momento.")
            input("Pressione ENTER para continuar...")
            return 1
        return conta_aluno.devolver_livro()
    
    # método para visualizar o acervo da biblioteca
    def ver_acervo(self):
        caminho = Caminhos()
        with open(caminho.acervo, "r", encoding="utf-8") as acervo_json:
            conteudo = acervo_json.read()

            if conteudo:
                acervo = json.loads(conteudo)

                if acervo:
                    for id_livro in acervo:
                        print(
                            f"\nID: {id_livro}" +
                            f"\nTítulo: {acervo[id_livro]['titulo']}" +
                            f"\nResumo: {acervo[id_livro]['resumo']}"
                              )
                        if acervo[id_livro]["disponibilidade"]["esta_alugado"] == True:
                            with open(caminho.registro_alunos, "r", encoding="utf-8") as reg_alunos_json:
                                conteudo = reg_alunos_json.read()

                                if conteudo:
                                    reg_alunos = json.loads(conteudo)
                            print(f"Disponibilidade: Alugado por {reg_alunos[acervo[id_livro]['disponibilidade']['ra_aluno']]['nome']}" +
                                  f" RA: {reg_alunos[acervo[id_livro]['disponibilidade']['ra_aluno']]['ra_aluno']}.")
                        else:
                            print("Disponibilidade: Disponível para alugar")
                input("Pressione ENTER para continuar...")

    # método para encerrar o loop do sistema
    def encerrar_sessao(self):
        print("Encerrando...")
        self.sessao_ativa = False

    