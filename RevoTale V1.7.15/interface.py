import math
import random

import pygame

from config import (
    ESCALA_BARRA_VIDA,
    ESCALA_BARRA_STAMINA,
    STAMINA_MAXIMA
)
from colisao import eh_parede


class Interface:

    def __init__(
        self,
        vida_maxima
    ):

        self.vida = vida_maxima

        self.vida_maxima = vida_maxima

        self.stamina = STAMINA_MAXIMA
        self.stamina_maxima = STAMINA_MAXIMA

        self.fonte_vida = pygame.font.Font(
            None,
            32
        )

        self.sprite_icone = pygame.image.load(
            "assets/BarraVida/Icone.png"
        ).convert_alpha()

        self.sprite_borda = pygame.image.load(
            "assets/BarraVida/borda.png"
        ).convert_alpha()

        self.sprite_meio = pygame.image.load(
            "assets/BarraVida/meio.png"
        ).convert_alpha()

        self.sprite_icone_stamina = pygame.image.load(
            "assets/BarraStamina/Icone.png"
        ).convert_alpha()

        self.sprite_borda_stamina = pygame.image.load(
            "assets/BarraStamina/borda.png"
        ).convert_alpha()

        self.sprite_meio_stamina = pygame.image.load(
            "assets/BarraStamina/meio.png"
        ).convert_alpha()

        self.sprite_sangue3 = pygame.image.load(
            "assets/particulas/sangue3.png"
        ).convert_alpha()
        self.sangue_no_chao = []
        self.game_over_inicio = None
        self.morta = False
        self.invencibilidade_secreta = False

        self.som_morte = pygame.mixer.Sound(
            "sfx/morte.wav"
        )

        self.sprite_icone = self._preparar_sprite(
            self.sprite_icone
        )

        self.sprite_borda = self._preparar_sprite(
            self.sprite_borda
        )

        self.sprite_meio = self._preparar_sprite(
            self.sprite_meio
        )

        self.sprite_icone_stamina = self._preparar_sprite(
            self.sprite_icone_stamina,
            ESCALA_BARRA_STAMINA
        )

        self.sprite_borda_stamina = self._preparar_sprite(
            self.sprite_borda_stamina,
            ESCALA_BARRA_STAMINA
        )

        self.sprite_meio_stamina = self._preparar_sprite(
            self.sprite_meio_stamina,
            ESCALA_BARRA_STAMINA
        )

        self.inicio_barra = 10 * ESCALA_BARRA_VIDA
        self.fim_barra = 44 * ESCALA_BARRA_VIDA
        self.espaco_icone = 2 * ESCALA_BARRA_VIDA
        self.largura_barra = (
            (self.vida_maxima - 1)
            * self.sprite_meio.get_width()
            +
            2
        )
        self.altura_barra = 4 * ESCALA_BARRA_VIDA
        self.limite_rotacao_particula = 18
        self.velocidade_rotacao_particula = 12
        self.tempo_invencibilidade_ms = 500
        self.invencivel_ate_ms = 0

    def receber_dano(
        self,
        dano,
        origem=None,
        direcao_ataque=None,
        velocidade_ataque=None
    ):
        agora = pygame.time.get_ticks()

        if dano <= 0 or self.morta or self.invencibilidade_secreta:
            return

        if agora < self.invencivel_ate_ms:
            return

        self.invencivel_ate_ms = agora + self.tempo_invencibilidade_ms
        self.vida = max(0, self.vida - dano)

        if self.vida == 0:
            self.game_over_inicio = pygame.time.get_ticks()
            self._criar_sangue(
                origem,
                direcao_ataque,
                dano,
                velocidade_ataque,
                game_over=True
            )
            self.morta = True
            self.som_morte.play()
            return

        self._criar_sangue(
            origem,
            direcao_ataque,
            dano,
            velocidade_ataque
        )

    def _criar_sangue(
        self,
        origem,
        direcao_ataque,
        dano,
        velocidade_ataque,
        game_over=False
    ):
        sprite = getattr(origem, "pegar_sprite", lambda: None)()

        if sprite is not None:
            limite = sprite.get_bounding_rect()
            centro_x = origem.x + limite.centerx
            chao_y = origem.y + limite.bottom
        elif origem is not None:
            centro_x, chao_y = origem
        else:
            centro_x, chao_y = self.obter_origem_particulas()

        direcao = pygame.Vector2(direcao_ataque or (0, -1))
        if direcao.length_squared() == 0:
            direcao = pygame.Vector2(0, -1)
        else:
            direcao.normalize_ip()

        if velocidade_ataque is None:
            velocidade_impacto = 7.0
        else:
            velocidade_impacto = pygame.Vector2(
                velocidade_ataque
            ).length()
        fator_velocidade = velocidade_impacto / 7.0
        if game_over:
            quantidade = max(720, dano * 720)
            velocidade_minima = 2.0
            velocidade_maxima = 5.5
            distancia_maxima = None
        else:
            quantidade = max(120, dano * 120)
            velocidade_minima = 4.0 * fator_velocidade
            velocidade_maxima = 7.0 * fator_velocidade
            distancia_maxima = 100

        area_sangue = self.sprite_sangue3.get_bounding_rect()
        sprite_sangue = self.sprite_sangue3.subsurface(
            area_sangue
        ).copy()
        sprite = pygame.transform.scale(
            sprite_sangue,
            (5, 5)
        )
        inicio = pygame.time.get_ticks()
        duracao = 8000 if game_over else random.randint(10000, 20000)
        for indice in range(quantidade):
            if game_over:
                angulo = random.uniform(0, math.tau)
                vetor = pygame.Vector2(
                    math.cos(angulo),
                    math.sin(angulo)
                )
            else:
                lado = 1 if indice % 2 == 0 else -1
                angulo = random.uniform(-0.14, 0.14)
                vetor = direcao.rotate_rad(angulo) * lado
            particula_lenta = random.random() < 0.08
            if particula_lenta:
                velocidade = random.uniform(0.12, 0.32) * (
                    fator_velocidade if not game_over else 1
                )
                aceleracao = random.uniform(0.008, 0.025) * fator_velocidade
                quadros_aceleracao = random.randint(4, 8)
            else:
                velocidade = random.uniform(
                    velocidade_minima,
                    velocidade_maxima
                )
                aceleracao = 0
                quadros_aceleracao = 0
            vetor *= velocidade

            sorteio = random.random()
            if game_over:
                if sorteio < 0.85:
                    distancia_inicial = random.uniform(0, 6)
                elif sorteio < 0.99:
                    distancia_inicial = random.uniform(6, 14)
                else:
                    distancia_inicial = random.uniform(14, 20)
            elif sorteio < 0.70:
                distancia_inicial = random.uniform(0, 8)
            elif sorteio < 0.95:
                distancia_inicial = random.uniform(8, 22)
            else:
                distancia_inicial = random.uniform(22, 35)

            angulo_inicial = random.uniform(0, math.tau)
            deslocamento_inicial = pygame.Vector2(
                math.cos(angulo_inicial),
                math.sin(angulo_inicial)
            ) * distancia_inicial

            self.sangue_no_chao.append({
                "sprite": sprite,
                "x": centro_x - 2.5 + deslocamento_inicial.x,
                "y": chao_y - 5 + deslocamento_inicial.y,
                "chao_y": chao_y + random.uniform(-2, 5),
                "velocidade_x": vetor.x,
                "velocidade_y": vetor.y,
                "aceleracao_x": vetor.normalize().x * aceleracao,
                "aceleracao_y": vetor.normalize().y * aceleracao,
                "quadros_aceleracao": quadros_aceleracao,
                "distancia_percorrida": distancia_inicial,
                "distancia_maxima": distancia_maxima,
                "margem_parede": random.uniform(2, 5),
                "frenagem": 0.94 if game_over else 0.84,
                "altura": random.uniform(0.2, 0.7),
                "velocidade_altura": random.uniform(0.12, 0.28),
                "assentado": False,
                "inicio": inicio,
                "duracao": duracao,
                "game_over": game_over,
                "alpha_inicial": 255,
                "alpha": 255
            })

    def obter_origem_particulas(self):
        x = 20
        y = 20
        x_barra = x + self.sprite_icone.get_width()
        x_barra += self.espaco_icone
        x_barra -= 5
        x_sprites = x_barra - 10
        x_borda = (
            x_sprites
            + (self.vida_maxima - 1) * self.sprite_meio.get_width()
            + 2
        )
        y_meio = y + (
            self.sprite_icone.get_height()
            - self.sprite_meio.get_height()
        ) // 2
        return (
            x_borda + self.sprite_borda.get_width(),
            y_meio + self.sprite_meio.get_height() // 2
        )

    @staticmethod
    def _encostou_na_parede(x, y, sprite):
        largura = sprite.get_width()
        altura = sprite.get_height()
        pontos = (
            (x, y),
            (x + largura - 1, y),
            (x, y + altura - 1),
            (x + largura - 1, y + altura - 1),
            (x + largura / 2, y + altura / 2)
        )

        return any(
            eh_parede(px, py)
            for px, py in pontos
        )

    def atualizar_particulas(self):
        agora = pygame.time.get_ticks()
        sangue_ativo = []
        for sangue in self.sangue_no_chao:
            tempo_decorrido = agora - sangue["inicio"]

            if tempo_decorrido >= sangue["duracao"]:
                continue

            if not sangue["assentado"]:
                if sangue["quadros_aceleracao"] > 0:
                    sangue["velocidade_x"] += sangue["aceleracao_x"]
                    sangue["velocidade_y"] += sangue["aceleracao_y"]
                    sangue["quadros_aceleracao"] -= 1
                novo_x = sangue["x"] + sangue["velocidade_x"]
                novo_y = sangue["y"] + sangue["velocidade_y"]

                if (
                    not sangue["game_over"]
                    and self._encostou_na_parede(
                        novo_x,
                        novo_y,
                        sangue["sprite"]
                    )
                ):
                    movimento = pygame.Vector2(
                        sangue["velocidade_x"],
                        sangue["velocidade_y"]
                    )
                    if movimento.length_squared() > 0:
                        movimento.scale_to_length(
                            sangue["margem_parede"]
                        )
                        sangue["x"] += movimento.x
                        sangue["y"] += movimento.y
                        sangue["distancia_percorrida"] += (
                            sangue["margem_parede"]
                        )
                    sangue["velocidade_x"] = 0
                    sangue["velocidade_y"] = 0
                    sangue["velocidade_altura"] = 0
                    sangue["altura"] = 0
                    sangue["assentado"] = True
                    sangue_ativo.append(sangue)
                    continue

                sangue["x"] = novo_x
                sangue["y"] = novo_y
                sangue["distancia_percorrida"] += math.hypot(
                    sangue["velocidade_x"],
                    sangue["velocidade_y"]
                )
                sangue["velocidade_x"] *= sangue["frenagem"]
                sangue["velocidade_y"] *= sangue["frenagem"]
                sangue["altura"] += sangue["velocidade_altura"]
                sangue["velocidade_altura"] -= 0.045

                if sangue["altura"] <= 0:
                    sangue["altura"] = 0
                    sangue["velocidade_altura"] = 0

                if (
                    (
                        sangue["distancia_maxima"] is not None
                        and sangue["distancia_percorrida"]
                        >= sangue["distancia_maxima"]
                    )
                    or (
                        sangue["altura"] == 0
                        and abs(sangue["velocidade_x"]) < 0.12
                        and abs(sangue["velocidade_y"]) < 0.12
                    )
                ):
                    sangue["velocidade_x"] = 0
                    sangue["velocidade_y"] = 0
                    sangue["assentado"] = True

            if sangue.get("game_over", False):
                tempo_game_over = agora - self.game_over_inicio
                if tempo_game_over >= 8000:
                    continue
                fade = max(
                    0,
                    (tempo_game_over - 5000) / 3000
                )
            else:
                fade = tempo_decorrido / sangue["duracao"]
            sangue["alpha"] = int(
                sangue["alpha_inicial"] * (1 - fade)
            )
            sangue_ativo.append(sangue)

        self.sangue_no_chao = sangue_ativo

    def obter_alpha_game_over(self):
        if self.game_over_inicio is None:
            return 255

        tempo_decorrido = pygame.time.get_ticks() - self.game_over_inicio

        if tempo_decorrido <= 5000:
            return 255

        return max(
            0,
            int(255 * (1 - (tempo_decorrido - 5000) / 3000))
        )

    def desenhar_gore(self, tela):
        for sangue in self.sangue_no_chao:
            sprite = sangue["sprite"].copy()
            sprite.set_alpha(sangue["alpha"])
            tela.blit(
                sprite,
                (
                    int(sangue["x"]),
                    int(sangue["y"] - sangue["altura"])
                )
            )

    @staticmethod
    def _preparar_sprite(sprite, escala=ESCALA_BARRA_VIDA):

        area = sprite.get_bounding_rect()
        sprite = sprite.subsurface(area).copy()

        return pygame.transform.scale(
            sprite,
            (
                sprite.get_width() * escala,
                sprite.get_height() * escala
            )
        )

    # ==========================================
    # DESENHAR VIDA
    # ==========================================

    @staticmethod
    def _desenhar_preenchimento_vida(
        tela,
        x,
        y,
        largura,
        altura,
        raio,
        cor
    ):

        pygame.draw.rect(
            tela,
            cor,
            (
                x,
                y,
                largura,
                altura
            ),
            border_radius=raio
        )

    def desenhar_vida(
        self,
        tela
    ):

        x = 20
        y = 20
        x_icone = x
        x_barra = x_icone + self.sprite_icone.get_width()
        x_barra += self.espaco_icone
        x_barra -= 5
        x_sprites = x_barra - 5
        x_sprites -= 10
        y_meio = y + (
            self.sprite_icone.get_height()
            -
            self.sprite_meio.get_height()
        ) // 2
        y_meio += 2
        y_barra = y_meio + 3
        y_borda = y + (
            self.sprite_icone.get_height()
            -
            self.sprite_borda.get_height()
        ) // 2
        y_borda += 2

        raio = self.altura_barra // 2
        x_borda = (
            x_sprites
            + (
                self.vida_maxima - 1
            ) * self.sprite_meio.get_width()
            + 2
        )
        largura_barra_desenhada = (
            x_borda
            -
            x_sprites
            +
            4
        )

        pygame.draw.rect(
            tela,
            (128, 128, 128),
            (
                x_sprites,
                y_barra,
                largura_barra_desenhada,
                self.altura_barra
            ),
            border_radius=raio
        )

        largura_vermelha = (
            self.vida
            * self.sprite_meio.get_width()
        )

        if self.vida == self.vida_maxima:
            largura_vermelha = largura_barra_desenhada

        if largura_vermelha > 0:

            percentual_vida = (
                self.vida
                /
                self.vida_maxima
            )
            intensidade_vermelha = int(
                210
                +
                20 * (1 - percentual_vida)
            )

            self._desenhar_preenchimento_vida(
                tela,
                x_sprites,
                y_barra,
                largura_vermelha,
                self.altura_barra,
                raio,
                (
                    intensidade_vermelha,
                    0,
                    0
                )
            )

        for indice in range(self.vida_maxima):

            largura_meio = self.sprite_meio.get_width()

            if indice == self.vida_maxima - 1:
                largura_meio = 2

            x_meio = (
                x_sprites
                + indice * self.sprite_meio.get_width()
            )

            tela.blit(
                self.sprite_meio,
                (
                    x_sprites
                    + indice * self.sprite_meio.get_width(),
                    y_meio
                ),
                pygame.Rect(
                    0,
                    0,
                    largura_meio,
                    self.sprite_meio.get_height()
                )
            )

        tela.blit(
            self.sprite_icone,
            (
                x_icone,
                y
            )
        )

        tela.blit(
            self.sprite_borda,
            (
                x_borda,
                y_borda
            )
        )

        texto = (
            f"HP: "
            f"{self.vida}/"
            f"{self.vida_maxima}"
        )

        imagem_texto = (
            self.fonte_vida.render(
                texto,
                True,
                (0, 0, 0)
            )
        )

        tela.blit(
            imagem_texto,
            (
                20,
                y + self.sprite_icone.get_height() + 8
            )
        )

    def desenhar_stamina(self, tela):
        x = 20
        y = 20 + self.sprite_icone.get_height() + 38
        x_icone = x
        x_barra = x_icone + self.sprite_icone_stamina.get_width()
        x_barra += self.espaco_icone
        x_barra -= 5
        x_sprites = x_barra - 5
        x_sprites -= 10
        y_meio = y + (
            self.sprite_icone_stamina.get_height()
            - self.sprite_meio_stamina.get_height()
        ) // 2
        y_meio += 2
        y_barra = y_meio + 3
        y_borda = y + (
            self.sprite_icone_stamina.get_height()
            - self.sprite_borda_stamina.get_height()
        ) // 2
        y_borda += 2
        segmentos = self.vida_maxima
        largura_segmento = self.sprite_meio_stamina.get_width()
        x_borda_vida = (
            x
            + self.sprite_icone.get_width()
            + self.espaco_icone
            - 5
            - 5
            - 10
            + (self.vida_maxima - 1) * self.sprite_meio.get_width()
            + 2
        )
        x_sprites = (
            x_borda_vida
            - (segmentos - 1) * largura_segmento
            - 2
        )
        x_borda = x_borda_vida
        largura_total = x_borda - x_sprites + 4
        raio = self.altura_barra // 2

        pygame.draw.rect(
            tela,
            (128, 128, 128),
            (x_sprites, y_barra, largura_total, self.altura_barra),
            border_radius=raio
        )

        largura_preenchida = int(
            largura_total
            * self.stamina
            /
            self.stamina_maxima
        )

        if largura_preenchida > 0:
            self._desenhar_preenchimento_vida(
                tela,
                x_sprites,
                y_barra,
                largura_preenchida,
                self.altura_barra,
                raio,
                (222, 211, 8)
            )

        for indice in range(segmentos):
            largura_meio = largura_segmento
            if indice == segmentos - 1:
                largura_meio = 2
            tela.blit(
                self.sprite_meio_stamina,
                (
                    x_sprites + indice * largura_segmento,
                    y_meio
                ),
                pygame.Rect(
                    0,
                    0,
                    largura_meio,
                    self.sprite_meio_stamina.get_height()
                )
            )

        tela.blit(self.sprite_icone_stamina, (x_icone, y))
        tela.blit(self.sprite_borda_stamina, (x_borda, y_borda))

        texto = (
            f"ST: "
            f"{int(self.stamina)}/"
            f"{self.stamina_maxima}"
        )
        imagem_texto = self.fonte_vida.render(
            texto,
            True,
            (0, 0, 0)
        )
        tela.blit(
            imagem_texto,
            (
                20,
                y + self.sprite_icone_stamina.get_height() + 8
            )
        )
