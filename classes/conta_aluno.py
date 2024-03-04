from classes.caminho_arquivos import Caminhos
import json


class Conta:
    def __init__(self, ra_aluno) -> None:
        self.ra_aluno = ra_aluno
        self.dados_aluno = self.obter_dados_aluno(ra_aluno)
        self.esta_alugando = False
        self.livro_em_aluguel = ""

    # método para obter e retornar os dados de um aluno se ele for encontrado em registro_alunos.json
    def obter_dados_aluno(self, ra_aluno):
        try:
            caminho = Caminhos()
            with open(caminho.registro_alunos, "r", encoding="utf-8") as reg_alunos_json:
                conteudo = reg_alunos_json.read()

                if conteudo:
                    reg_alunos = json.loads(conteudo)

                    if reg_alunos:
                        for aluno in reg_alunos:
                            if aluno == ra_aluno:
                                return reg_alunos[aluno]
            return None
        except Exception as e:
            print(f"ERRO: {e}")
            input("Pressione ENTER para continuar...")
            return 1
    
    # método para atualizar self.dados_aluno e o arquivo registro_alunos.json com as alterações
    def atualizar_dados_aluno(self):
        try:
            caminho = Caminhos()
            with open(caminho.registro_alunos, "r+", encoding="utf-8") as reg_alunos_json:
                conteudo = reg_alunos_json.read()

                if conteudo:
                    reg_alunos = json.loads(conteudo)

                    if reg_alunos:
                        for aluno in reg_alunos:
                            if aluno == self.ra_aluno:
                                reg_alunos[aluno]["esta_alugando"] = self.esta_alugando
                                reg_alunos[aluno]["livro_em_aluguel"] = self.livro_em_aluguel

                                reg_alunos_json.seek(0)
                                json.dump(reg_alunos, reg_alunos_json)
                                reg_alunos_json.truncate()

                                self.dados_aluno["esta_alugando"] = self.esta_alugando
                                self.dados_aluno["livro_em_aluguel"] = self.livro_em_aluguel
                                
                                return 0
            return 1
        except Exception as e:
            print(f"ERRO: {e}")
            input("Pressione ENTER para continuar...")
            return 1
        
    # método para registrar o aluguel de livros no acervo e no registro do aluno
    def alugar_livro(self):
        try:
            id_livro = input("Qual o ID do livro que deseja alugar?\n>")

            if id_livro.isdigit() and len(id_livro) == 3:
                caminho = Caminhos()
                with open(caminho.acervo, "r+", encoding="utf-8") as acervo_json:
                    conteudo = acervo_json.read()

                    if conteudo:
                        acervo = json.loads(conteudo)

                        if acervo:
                            if id_livro in acervo and acervo[id_livro]["disponibilidade"]["esta_alugado"] == False:
                                acervo[id_livro]["disponibilidade"]["esta_alugado"] = True
                                acervo[id_livro]["disponibilidade"]["ra_aluno"] = self.ra_aluno

                                acervo_json.seek(0)
                                json.dump(acervo, acervo_json)
                                acervo_json.truncate()

                                self.esta_alugando = True
                                self.livro_em_aluguel = id_livro

                                self.dados_aluno["esta_alugando"] = self.esta_alugando
                                self.dados_aluno["livro_em_aluguel"] = self.livro_em_aluguel


                                self.atualizar_dados_aluno()

                                print(f"Livro {acervo[id_livro]['titulo']} alugado com sucesso!")
                                input("Pressione ENTER para continuar...")
                                return 0
                            elif id_livro in acervo and acervo[id_livro]["disponibilidade"]["esta_alugado"] == True:
                                print("Este livro já está sendo alugado. Experimente o ID de outro livro que deseja alugar e tente novamente ou aguarde este livro ser devolvido!")
                                input("Pressione ENTER para continuar...")
                                return 1
                            else:
                                print("Livro não encontrado em nosso Acervo. Por favor, verifique o ID do livro e tente novamente!")
                                input("Pressione ENTER para continuar...")
                                return 1
            else:
                print("Os IDs dos livros são compostos por 3 caracteres numéricos entre 0 e 9. Por favor, tente novamente!")
                input("Pressione ENTER para continuar...")
                return 1
        except Exception as e:
            print(f"ERRO: {e}")
            input("Pressione ENTER para continuar...")
            return 1
        
    # método para registrar a devolução de livros no acervo e no registro do aluno
    def devolver_livro(self):
        try:
            id_livro = input("Qual o ID do livro que deseja devolver?\n>")

            if id_livro.isdigit() and len(id_livro) == 3:
                caminho = Caminhos()
                with open(caminho.acervo, "r+", encoding="utf-8") as acervo_json:
                    conteudo = acervo_json.read()

                    if conteudo:
                        acervo = json.loads(conteudo)

                        if acervo:
                            if id_livro in acervo and id_livro == self.dados_aluno["livro_em_aluguel"]:
                                acervo[id_livro]["disponibilidade"]["esta_alugado"] = False
                                acervo[id_livro]["disponibilidade"]["ra_aluno"] = ""

                                acervo_json.seek(0)
                                json.dump(acervo, acervo_json)
                                acervo_json.truncate()

                                self.esta_alugando = False
                                self.livro_em_aluguel = ""

                                self.dados_aluno["esta_alugando"] = self.esta_alugando
                                self.dados_aluno["livro_em_aluguel"] = self.livro_em_aluguel

                                self.atualizar_dados_aluno()

                                print(f"Livro {acervo[id_livro]['titulo']} devolvido com sucesso!")
                                input("Pressione ENTER para continuar...")
                                return 0
                            elif id_livro in acervo and id_livro != self.dados_aluno["livro_em_aluguel"]:
                                print("Você não está alugando este livro. Verifique o ID do livro que deseja devolver e tente novamente!")
                                input("Pressione ENTER para continuar...")
                                return 1
                            else:
                                print("Livro não encontrado em nosso Acervo. Por favor, verifique o ID do livro e tente novamente!")
                                input("Pressione ENTER para continuar...")
                                return 1
            else:
                print("Os IDs dos livros são compostos por 3 caracteres numéricos entre 0 e 9. Por favor, tente novamente!")
                input("Pressione ENTER para continuar...")
                return 1
        except Exception as e:
            print(f"ERRO: {e}")
            input("Pressione ENTER para continuar...")
            return 1
