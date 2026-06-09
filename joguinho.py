import arcade
import random
import math
import webbrowser

# Configurações gerais da janela do jogo
ALTURA = 800  # altura da janela em pixels
LARGURA = 600  # largura da janela em pixels
TITULO = "Meu Joguinho"  # título exibido na barra da janela

# Ajustes de escala e parâmetros de gameplay
PLAYER_SCALE = 0.3  # escala do sprite do jogador
MOEDA_SCALE = 0.3  # escala do sprite das moedas
NUM_MOEDAS = 7  # número total de moedas no jogo
PLAYER_SPEED = 960  # velocidade do jogador em pixels por segundo


class Player(arcade.Sprite):
    """Representa o personagem controlável pelo jogador."""

    def __init__(self):
        # Inicializa o sprite com a imagem padrão virada para a esquerda
        super().__init__("kachau.png", scale=PLAYER_SCALE)

        # Carrega duas texturas: uma para quando o jogador vai para a direita
        # e outra para quando ele vai para a esquerda. Isso dá mais realismo.
        self.textura_direita = arcade.load_texture("kachauD.png")
        self.textura_esquerda = arcade.load_texture("kachau.png")

        # Define a textura inicial como a versão virada para a esquerda
        self.texture = self.textura_esquerda

    def on_update(self, delta_time):
        # Método obrigatório em alguns padrões do Arcade, mas não usado aqui.
        pass


class Moeda(arcade.Sprite):
    """Representa uma moeda coletável no cenário."""

    def __init__(self, moving=False):
        # Inicializa o sprite da moeda usando a mesma imagem para todos os casos
        super().__init__("moeda.png", scale=MOEDA_SCALE)

        # Mantém texturas para consistência com outras sprites do jogo
        self.textura_direita = arcade.load_texture("moeda.png")
        self.textura_esquerda = arcade.load_texture("moeda.png")

        # Define o valor da moeda: 1 para estática, 10 para a moeda móvel
        self.valor = 10 if moving else 1

        if moving:
            # Se for a moeda móvel, dá um movimento inicial aleatório rápido
            self.change_x = random.uniform(-1200, 1200)
            self.change_y = random.uniform(-1200, 1200)
        else:
            # Moedas estáticas não se movem, apenas aguardam coleta
            self.change_x = 0
            self.change_y = 0

    def on_update(self, delta_time):
        # Método de atualização da sprite de moeda não utilizado explicitamente
        pass


class MeuJogo(arcade.Window):
    """Classe principal que controla a janela, lógica e desenho do jogo."""

    def __init__(self):
        super().__init__(LARGURA, ALTURA, TITULO)

        # Define cor de fundo clara para o jogo
        arcade.set_background_color((226, 237, 5))

        # Cria o jogador e o posiciona no centro da tela
        self.personagem = Player()
        self.personagem.center_x = LARGURA // 2
        self.personagem.center_y = ALTURA // 2

        # Define taxa de atualização para 120 frames por segundo
        self.set_update_rate(1 / 120)

        # Grupo de sprites do jogador (apenas um sprite neste caso)
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.personagem)

        # Variáveis de controle de entrada do teclado
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Variáveis para ativar movimento automático quando o jogador ficar inativo
        self.time_since_last_command = 0.0
        self.auto_move_active = False

        # Criar a lista de moedas: uma moeda móvel e várias estáticas
        self.moedas = arcade.SpriteList()
        moving_index = random.randrange(NUM_MOEDAS)
        for i in range(NUM_MOEDAS):
            m = self._criar_moeda_em_posicao_valida(moving=(i == moving_index))
            self.moedas.append(m)

        # Pontuação inicial
        self.score = 0

    def on_draw(self):
        # Limpa a tela e redesenha todos os elementos do jogo
        self.clear()

        # Desenha as moedas primeiro para que o jogador fique por cima delas
        self.moedas.draw()
        self.sprite_jogador.draw()

        # Mostra o placar no canto superior esquerdo
        arcade.draw_text(
            f"Moedas: {self.score}",
            10,
            self.height - 30,
            arcade.color.BLACK,
            18,
        )

    def on_update(self, delta_time):
        # Detecta se alguma tecla de movimento está pressionada
        command_active = (
            self.left_pressed
            or self.right_pressed
            or self.up_pressed
            or self.down_pressed
        )

        if command_active:
            # Se há entrada do jogador, reinicia o temporizador de inatividade
            self.time_since_last_command = 0.0
            self.auto_move_active = False
        else:
            # Se está inativo, acumula o tempo até acionar movimento automático
            self.time_since_last_command += delta_time
            if self.time_since_last_command >= 3.0:
                self.auto_move_active = True

        dx = 0
        dy = 0

        if command_active:
            # Ajusta direção a partir das teclas pressionadas
            if self.left_pressed:
                dx -= PLAYER_SPEED
            if self.right_pressed:
                dx += PLAYER_SPEED
            if self.up_pressed:
                dy += PLAYER_SPEED
            if self.down_pressed:
                dy -= PLAYER_SPEED
        elif self.auto_move_active:
            # Se inativo por tempo suficiente, move automaticamente em direção
            # à moeda mais próxima para dar dinâmica ao jogo.
            alvo = self._encontrar_moeda_mais_proxima()
            if alvo is not None:
                dx, dy = self._direcao_para_alvo(alvo)

        self.personagem.change_x = dx
        self.personagem.change_y = dy

        # Seleciona a textura correta dependendo da direção horizontal
        if dx > 0:
            self.personagem.texture = self.personagem.textura_direita
        elif dx < 0:
            self.personagem.texture = self.personagem.textura_esquerda

        # Move o jogador de forma independente do FPS usando delta_time
        self.personagem.center_x += self.personagem.change_x * delta_time
        self.personagem.center_y += self.personagem.change_y * delta_time

        # Atualiza as moedas móveis e reflete na borda da janela
        for moeda in self.moedas:
            moeda.center_x += moeda.change_x * delta_time
            moeda.center_y += moeda.change_y * delta_time

            # Se a moeda bate na borda, inverte sua direção para quicar
            if moeda.center_x <= 20 or moeda.center_x >= self.width - 20:
                moeda.change_x = -moeda.change_x
            if moeda.center_y <= 20 or moeda.center_y >= self.height - 20:
                moeda.change_y = -moeda.change_y

        # Detecta colisões entre o jogador e as moedas
        colisoes = arcade.check_for_collision_with_list(self.personagem, self.moedas)
        for moeda in colisoes:
            # Salva se a moeda coletada era a especial móvel
            moving = moeda.valor == 10
            moeda.kill()  # remove a moeda coletada da tela
            self.score += moeda.valor  # aumenta o placar

            # Garante que sempre haja uma quantidade constante de moedas
            nova = self._criar_moeda_em_posicao_valida(moving=moving)
            self.moedas.append(nova)

    def _criar_moeda_em_posicao_valida(self, moving=False):
        """Cria uma moeda em uma posição aleatória válida dentro da área de jogo."""
        m = Moeda(moving=moving)

        while True:
            # Posiciona a moeda com margem de 20 pixels das bordas
            m.center_x = random.randint(20, self.width - 20)
            m.center_y = random.randint(20, self.height - 20)

            dx = m.center_x - self.personagem.center_x
            dy = m.center_y - self.personagem.center_y

            # Garante que a posição seja suficientemente distante do jogador inicial
            if (dx * dx + dy * dy) >= 0:
                break

        return m

    def _encontrar_moeda_mais_proxima(self):
        """Retorna a moeda mais próxima do jogador, ou None se não houver moedas."""
        if len(self.moedas) == 0:
            return None

        return min(
            self.moedas,
            key=lambda moeda: (
                moeda.center_x - self.personagem.center_x
            )
            ** 2
            + (
                moeda.center_y - self.personagem.center_y
            )
            ** 2,
        )

    def _direcao_para_alvo(self, alvo):
        """Calcula a velocidade normalizada na direção de um alvo."""
        dx = alvo.center_x - self.personagem.center_x
        dy = alvo.center_y - self.personagem.center_y
        distancia = math.hypot(dx, dy)

        if distancia == 0:
            return 0, 0

        # Retorna um vetor de velocidade com magnitude PLAYER_SPEED
        return dx / distancia * PLAYER_SPEED, dy / distancia * PLAYER_SPEED

    def on_key_press(self, key, modifiers):
        """Tratamento de tecla pressionada para iniciar movimentos."""
        if key == arcade.key.ESCAPE:
            # Ao apertar ESC, abre o canal do Jazzghost e fecha o jogo
            webbrowser.open("https://www.youtube.com/@Jazzghost")
            self.close()
            return

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        else:
            return

        # Sempre que há entrada do jogador, resetamos o cronômetro de inatividade
        self.time_since_last_command = 0.0
        self.auto_move_active = False

    def on_key_release(self, key, modifiers):
        """Tratamento de tecla liberada para parar movimentos."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        else:
            return

        # Ao soltar a tecla, o jogador pode ficar inativo novamente
        self.time_since_last_command = 0.0
        self.auto_move_active = False


def executar():
    """Inicializa o jogo e inicia o loop principal do Arcade."""
    tela = MeuJogo()
    arcade.run()


if __name__ == "__main__":
    executar()
