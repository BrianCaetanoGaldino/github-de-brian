import arcade
import random

# Configurações
ALTURA = 800
LARGURA = 600
TITULO = "Meu Joguinho"

# Ajustes de tamanho e gameplay
PLAYER_SCALE = 0.5
MOEDA_SCALE = 0.15
NUM_MOEDAS = 6
PLAYER_SPEED = 4

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("kachau.png", scale=PLAYER_SCALE)
        # textura para a direita usa kachauD.png conforme solicitado
        self.textura_direita = arcade.load_texture("kachauD.png")
        self.textura_esquerda = arcade.load_texture("kachau.png")
        # garante textura inicial
        self.texture = self.textura_esquerda

    def on_update(self, delta_time):
        pass

class Moeda(arcade.Sprite):

    def __init__(self):
        super().__init__("moeda.png", scale=MOEDA_SCALE)
        self.textura_direita = arcade.load_texture("moeda.png")
        self.textura_esquerda = arcade.load_texture("moeda.png")
        # Velocidade aleatória para movimento
        self.change_x = random.uniform(-2, 2)
        self.change_y = random.uniform(-2, 2)

    def on_update(self, delta_time):
        pass

class MeuJogo(arcade.Window):

    def __init__(self):
        super().__init__(LARGURA, ALTURA, TITULO)

        arcade.set_background_color((226, 237, 5))

        # Jogador
        self.personagem = Player()
        self.personagem.center_x = LARGURA // 2
        self.personagem.center_y = ALTURA // 2

        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.personagem)

        # Controle de movimento
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Moedas (várias)
        self.moedas = arcade.SpriteList()
        for _ in range(NUM_MOEDAS):
            m = self._criar_moeda_em_posicao_valida()
            self.moedas.append(m)

        # Placar
        self.score = 0

    def on_draw(self):
        self.clear()
        # Desenha moedas primeiro (atrás do jogador)
        self.moedas.draw()
        self.sprite_jogador.draw()

        # Desenha contador no canto superior esquerdo
        arcade.draw_text(f"Moedas: {self.score}", 10, self.height - 30, arcade.color.BLACK, 18)

    def on_update(self, delta_time):
        # Atualiza velocidade do personagem com base nas teclas
        dx = 0
        dy = 0
        if self.left_pressed:
            dx -= PLAYER_SPEED
        if self.right_pressed:
            dx += PLAYER_SPEED
        if self.up_pressed:
            dy += PLAYER_SPEED
        if self.down_pressed:
            dy -= PLAYER_SPEED

        self.personagem.change_x = dx
        self.personagem.change_y = dy

        # Ajusta textura do personagem conforme direção horizontal
        if dx > 0:
            self.personagem.texture = self.personagem.textura_direita
        elif dx < 0:
            self.personagem.texture = self.personagem.textura_esquerda

        # Atualiza posições
        self.sprite_jogador.update()
        self.moedas.update()

        # Move moedas aleatoriamente (com reflexão nas bordas)
        for moeda in self.moedas:
            moeda.center_x += moeda.change_x
            moeda.center_y += moeda.change_y
            # Reflexão nas bordas
            if moeda.center_x <= 20 or moeda.center_x >= self.width - 20:
                moeda.change_x = -moeda.change_x
            if moeda.center_y <= 20 or moeda.center_y >= self.height - 20:
                moeda.change_y = -moeda.change_y

        # Verifica colisões entre jogador e moedas
        colisoes = arcade.check_for_collision_with_list(self.personagem, self.moedas)
        for moeda in colisoes:
            moeda.kill()
            self.score += 1
            # cria uma nova moeda para manter múltiplas em cena
            nova = self._criar_moeda_em_posicao_valida()
            self.moedas.append(nova)

    def _criar_moeda_em_posicao_valida(self):
        m = Moeda()
        # Posiciona em lugar aleatório, longe do jogador
        min_dist = 0
        while True:
            m.center_x = random.randint(20, self.width - 20)
            m.center_y = random.randint(20, self.height - 20)
            dx = m.center_x - self.personagem.center_x
            dy = m.center_y - self.personagem.center_y
            if (dx * dx + dy * dy) >= (min_dist * min_dist):
                break
        return m

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False


def executar():
    tela = MeuJogo()
    arcade.run()


if __name__ == "__main__":
    executar()
