import os

class Caminhos():
    def __init__(self) -> None:
        self.registro_alunos = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dados/registro_alunos.json"))
        self.acervo = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dados/acervo.json"))

    # método para verificar se as variáveis do objeto estão recebendo os caminhos corretos
    def imprimir_caminhos(self):
        print(self.registro_alunos + "\n" + self.acervo)

    # método para verificar se os arquivos apontados nos caminhos existem ou não
    def verificar_caminhos(self):
        print(f"registro_alunos: {os.path.isfile(self.registro_alunos)}")
        print(f"acervo: {os.path.isfile(self.acervo)}")