import math
import pygame

from config import VELOCIDADE
from colisao import pode_andar


class Eren:

    def __init__(
        self,
        baixo,
        cima,
        esquerda,
        direita,
        jogador
    ):

        # ==========================================
        # SPRITES
        # ==========================================

        self.baixo = baixo
        self.cima = cima
        self.esquerda = esquerda
        self.direita = direita

        # ==========================================
        # JOGADOR
        # ==========================================

        self.jogador = jogador

        # ==========================================
        # DIREÇÃO INICIAL
        # ==========================================

        self.direcao = "baixo"

        # ==========================================
        # ANIMAÇÃO
        # ==========================================

        self.frame = 0
        self.contador_animacao = 0
        self.velocidade_animacao = 8

        # ==========================================
        # DISTÂNCIA DO JOGADOR
        # ==========================================

        self.distancia = 40

        # ==========================================
        # VELOCIDADE
        # ==========================================

        self.velocidade = VELOCIDADE * 0.99

        # ==========================================
        # POSIÇÃO INICIAL
        # ==========================================

        sprite = self.baixo[0]

        self.x = (
            self.jogador.x
            - sprite.get_width()
        )

        self.y = self.jogador.y

        # ==========================================
        # MEMÓRIA DE MOVIMENTO
        # ==========================================

        self.direcao_bloqueada = None
        self.tempo_bloqueado = 0

    # ==================================================
    # PEGAR SPRITE
    # ==================================================

    def pegar_sprite(self):

        sprites = {
            "baixo": self.baixo,
            "cima": self.cima,
            "esquerda": self.esquerda,
            "direita": self.direita
        }[self.direcao]

        return sprites[
            self.frame % len(sprites)
        ]

    # ==================================================
    # TESTAR MOVIMENTO
    # ==================================================

    def pode_mover(
        self,
        x,
        y,
        sprite
    ):

        return pode_andar(
            x,
            y,
            sprite
        )

    # ==================================================
    # DEFINIR DIREÇÃO
    # ==================================================

    def definir_direcao(
        self,
        movimento_x,
        movimento_y
    ):

        # Movimento horizontal maior
        if abs(movimento_x) > abs(movimento_y):

            if movimento_x > 0:

                self.direcao = "direita"

            elif movimento_x < 0:

                self.direcao = "esquerda"

        # Movimento vertical
        elif movimento_y > 0:

            self.direcao = "baixo"

        elif movimento_y < 0:

            self.direcao = "cima"

    # ==================================================
    # ATUALIZAR
    # ==================================================

    def atualizar(self):

        # ==========================================
        # DISTÂNCIA ATÉ O JOGADOR
        # ==========================================

        distancia_x = (
            self.jogador.x
            - self.x
        )

        distancia_y = (
            self.jogador.y
            - self.y
        )

        distancia_total = math.hypot(
            distancia_x,
            distancia_y
        )

        # ==========================================
        # JÁ ESTÁ PERTO
        # ==========================================

        if distancia_total <= self.distancia:

            self.frame = 0
            self.contador_animacao = 0

            return

        # ==========================================
        # SPRITE ATUAL
        # ==========================================

        sprite = self.pegar_sprite()

        # ==========================================
        # NORMALIZAR DIREÇÃO
        # ==========================================

        if distancia_total != 0:

            direcao_x = (
                distancia_x
                /
                distancia_total
            )

            direcao_y = (
                distancia_y
                /
                distancia_total
            )

        else:

            direcao_x = 0
            direcao_y = 0

        # ==========================================
        # MOVIMENTO
        # ==========================================

        movimento_x = (
            direcao_x
            *
            self.velocidade
        )

        movimento_y = (
            direcao_y
            *
            self.velocidade
        )

        # ==========================================
        # NOVA POSIÇÃO
        # ==========================================

        novo_x = (
            self.x
            +
            movimento_x
        )

        novo_y = (
            self.y
            +
            movimento_y
        )

        # ==========================================
        # TESTAR COLISÃO
        # ==========================================

        conseguiu_x = self.pode_mover(
            novo_x,
            self.y,
            sprite
        )

        conseguiu_y = self.pode_mover(
            self.x,
            novo_y,
            sprite
        )

        # ==========================================
        # MOVIMENTO PRINCIPAL
        # ==========================================

        moveu = False

        if conseguiu_x:

            self.x = novo_x

            moveu = True

        if conseguiu_y:

            self.y = novo_y

            moveu = True

        # ==========================================
        # VERIFICAR BLOQUEIO
        # ==========================================

        if (
            not conseguiu_x
            or
            not conseguiu_y
        ):

            self.tempo_bloqueado += 1

        else:

            self.tempo_bloqueado = 0

        # ==========================================
        # CONTORNAR PAREDE
        # ==========================================

        if (
            not conseguiu_x
            and
            not conseguiu_y
        ):

            tentativas = []

            # --------------------------------------
            # ALVO MAIS À DIREITA / ESQUERDA
            # --------------------------------------

            if abs(distancia_x) > abs(distancia_y):

                if distancia_x > 0:

                    tentativas = [
                        (0, self.velocidade),
                        (0, -self.velocidade),
                        (-self.velocidade, 0)
                    ]

                else:

                    tentativas = [
                        (0, self.velocidade),
                        (0, -self.velocidade),
                        (self.velocidade, 0)
                    ]

            # --------------------------------------
            # ALVO MAIS ACIMA / ABAIXO
            # --------------------------------------

            else:

                if distancia_y > 0:

                    tentativas = [
                        (self.velocidade, 0),
                        (-self.velocidade, 0),
                        (0, -self.velocidade)
                    ]

                else:

                    tentativas = [
                        (self.velocidade, 0),
                        (-self.velocidade, 0),
                        (0, self.velocidade)
                    ]

            # ======================================
            # TENTAR CADA DIREÇÃO
            # ======================================

            for tentativa_x, tentativa_y in tentativas:

                teste_x = (
                    self.x
                    +
                    tentativa_x
                )

                teste_y = (
                    self.y
                    +
                    tentativa_y
                )

                if self.pode_mover(
                    teste_x,
                    teste_y,
                    sprite
                ):

                    self.x = teste_x
                    self.y = teste_y

                    movimento_x = tentativa_x
                    movimento_y = tentativa_y

                    moveu = True

                    break

        # ==========================================
        # SEGURANÇA CONTRA TRAVAMENTO
        # ==========================================

        if (
            not moveu
            and
            self.tempo_bloqueado > 20
        ):

            alternativas = [
                (self.velocidade, 0),
                (-self.velocidade, 0),
                (0, self.velocidade),
                (0, -self.velocidade)
            ]

            for dx, dy in alternativas:

                teste_x = self.x + dx
                teste_y = self.y + dy

                if self.pode_mover(
                    teste_x,
                    teste_y,
                    sprite
                ):

                    self.x = teste_x
                    self.y = teste_y

                    movimento_x = dx
                    movimento_y = dy

                    self.tempo_bloqueado = 0

                    moveu = True

                    break

        # ==========================================
        # ATUALIZAR DIREÇÃO
        # ==========================================

        if moveu:

            self.definir_direcao(
                movimento_x,
                movimento_y
            )

        # ==========================================
        # ANIMAÇÃO
        # ==========================================

        if moveu:

            self.contador_animacao += 1

            if (
                self.contador_animacao
                >=
                self.velocidade_animacao
            ):

                self.contador_animacao = 0

                self.frame += 1

                sprites = {
                    "baixo": self.baixo,
                    "cima": self.cima,
                    "esquerda": self.esquerda,
                    "direita": self.direita
                }[self.direcao]

                if self.frame >= len(sprites):

                    self.frame = 0

        else:

            self.frame = 0
            self.contador_animacao = 0

    # ==================================================
    # DESENHAR
    # ==================================================

    def desenhar(self, tela):

        sprite = self.pegar_sprite()

        tela.blit(
            sprite,
            (
                self.x,
                self.y
            )
        )

    # ==================================================
    # OBTER HITBOX DOS PÉS
    # ==================================================

    def obter_rect(self):

        sprite = self.pegar_sprite()
        sprite_rect = sprite.get_rect(
            topleft=(self.x, self.y)
        )

        hitbox = pygame.Rect(
            0,
            0,
            sprite.get_width(),
            int(sprite.get_height() * 0.20)
        )

        hitbox.midbottom = sprite_rect.midbottom

        return hitbox
