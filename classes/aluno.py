class Aluno:
    def __init__(self, ra_aluno, nome, curso) -> None:
        self.ra_aluno = ra_aluno
        self.nome= nome
        self.curso = curso
        self.esta_alugando = False
        self.livro_em_aluguel = ""
        self.dados_aluno = {
            "ra_aluno": self.ra_aluno,
            "nome": self.nome,
            "curso": self.curso,
            "esta_alugando": self.esta_alugando,
            "livro_em_aluguel": self.livro_em_aluguel
        }
