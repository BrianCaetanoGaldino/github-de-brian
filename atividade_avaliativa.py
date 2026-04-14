jogadoresCadastrados = 0

print("qual ação você deseja executar?")
print("cadastro;")

acao = input(print("consulta;"))
if(acao == cadastro):
    ac2 = input(print("deseja cadastrar um jogador ou um time?;"))
    if(ac2 == jogador):
        j = []
    elif(ac2 == time):
        t = []            

class cadastro_equipes:
    def __init__(self):
        self.nome_equipe = ""
        self.jogo = ""

class consulta:
    def __init__(self):
        pass
