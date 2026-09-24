import math

import pygame
import sys


# ==========================================
# CONFIGURAÇÕES
# ==========================================

from config import (
    LARGURA,
    ALTURA,
    FPS,
    TITULO,
    VIDA_MAXIMA,
    ESCALA
)


# ==========================================
# TELA INICIAL
# ==========================================

from tela_inicial import tela_inicial


# ==========================================
# CENAS
# ==========================================

from cenas import mostrar_cenas


# ==========================================
# RECURSOS
# ==========================================

from recursos import (
    carregar_chao,
    carregar_parede,
    carregar_personagem,
    carregar_coracao,
    carregar_eren,
    carregar_pbrr,
    carregar_boss,
    carregar_boss6,
    carregar_boss7,
    carregar_arma
)


# ==========================================
# JOGADOR
# ==========================================

from jogador import Jogador


# ==========================================
# EREN
# ==========================================

from eren import Eren


# ==========================================
# CORAÇÃO
# ==========================================

from coracao import Coracao


# ==========================================
# PBRR
# ==========================================

from PBRR import PBRR


# ==========================================
# BOSSES
# ==========================================

from bosses import GerenciadorBosses


# ==========================================
# INTERFACE
# ==========================================

from interface import Interface


# ==========================================
# MAPA
# ==========================================

from mapa import (
    desenhar_chao,
    desenhar_paredes
)


# ==========================================
# CAIXA DE DIÁLOGO
# ==========================================

from caixa_dialogo import CaixaDialogo


# ==========================================
# SOMBRAS
# ==========================================

from sombra import SistemaSombras


# ==========================================
# INICIAR PYGAME
# ==========================================

pygame.init()


# ==========================================
# JANELA
# ==========================================

tela = pygame.display.set_mode(
    (
        0,
        0
    ),
    pygame.FULLSCREEN
)

fullscreen = True


# ==========================================
# TELA INTERNA DO JOGO
# ==========================================

tela_jogo = pygame.Surface(
    (
        LARGURA,
        ALTURA
    )
)


# ==========================================
# TÍTULO
# ==========================================

pygame.display.set_caption(
    TITULO
)


# ==========================================
# FUNÇÃO FULLSCREEN
# ==========================================

def alternar_fullscreen():

    global tela
    global fullscreen

    fullscreen = not fullscreen

    if fullscreen:

        tela = pygame.display.set_mode(
            (
                0,
                0
            ),
            pygame.FULLSCREEN
        )

    else:

        tela = pygame.display.set_mode(
            (
                LARGURA,
                ALTURA
            ),
            pygame.RESIZABLE
        )


# ==========================================
# APRESENTAR TELA
# ==========================================

def apresentar_tela():

    largura_tela = tela.get_width()
    altura_tela = tela.get_height()

    escala = min(
        largura_tela / LARGURA,
        altura_tela / ALTURA
    )

    novo_tamanho = (
        int(LARGURA * escala),
        int(ALTURA * escala)
    )

    tela_escalada = pygame.transform.scale(
        tela_jogo,
        novo_tamanho
    )

    tela.fill(
        (
            0,
            0,
            0
        )
    )

    tela.blit(
        tela_escalada,
        (
            (largura_tela - novo_tamanho[0]) // 2,
            (altura_tela - novo_tamanho[1]) // 2
        )
    )


# ==========================================
# CLOCK
# ==========================================

clock = pygame.time.Clock()


# ==========================================
# TELA INICIAL
# ==========================================

if not tela_inicial(tela):

    pygame.quit()
    sys.exit()


# ==========================================
# CENAS
# ==========================================

if not mostrar_cenas(tela):

    pygame.quit()
    sys.exit()


# ==========================================
# CARREGAR CHÃO
# ==========================================

chao = carregar_chao()


# ==========================================
# CARREGAR PAREDE
# ==========================================

parede = carregar_parede()


# ==========================================
# CARREGAR SPRITES DO JOGADOR
# ==========================================

(
    baixo,
    cima,
    esquerda,
    direita
) = carregar_personagem()


# ==========================================
# CARREGAR SPRITES DO EREN
# ==========================================

sprites_eren = carregar_eren()


# ==========================================
# CARREGAR CORAÇÃO
# ==========================================

sprites_coracao = carregar_coracao()


# ==========================================
# CARREGAR SPRITES DO PBRR
# ==========================================

(
    pbrr_frente,
    pbrr_costas,
    pbrr_esquerda,
    pbrr_direita
) = carregar_pbrr()


# ==========================================
# CRIAR PBRR
# ==========================================

pbrr = PBRR(
    pbrr_frente,
    pbrr_costas,
    pbrr_esquerda,
    pbrr_direita,
    LARGURA // 2,
    ALTURA // 2
)


# ==========================================
# CRIAR OUTROS BOSSES
# ==========================================

bosses = {
    "pbrr": pbrr
}

for identificador, pasta in (
    ("boss2", "boss2"),
    ("boss3", "boss3"),
    ("boss4", "boss4")
):
    bosses[identificador] = PBRR(
        *carregar_boss(pasta),
        LARGURA // 2,
        ALTURA // 2
    )

    if identificador == "boss4":
        sprite_ataque_boss4 = pygame.image.load(
            "assets/ataques/ataque4.png"
        ).convert_alpha()
        bosses[identificador].sprite_ataque_4 = pygame.transform.scale(
            sprite_ataque_boss4,
            (
                sprite_ataque_boss4.get_width() * ESCALA,
                sprite_ataque_boss4.get_height() * ESCALA
            )
        )
        bosses[identificador].sprite_ataque_4_seq = [
            bosses[identificador].sprite_ataque_4
        ]

bosses["boss2"].configurar_padrao_ataque("boss2")
bosses["boss3"].configurar_padrao_ataque("boss3")
bosses["boss4"].configurar_padrao_ataque("boss4")

(
    sprite_boss6_caindo,
    sprites_boss6_entrada,
    sprites_boss6_frente
) = carregar_boss6()
bosses["boss6"] = PBRR(
    sprites_boss6_frente,
    sprites_boss6_frente,
    sprites_boss6_frente,
    sprites_boss6_frente,
    LARGURA // 2,
    ALTURA // 2
)
bosses["boss6"].configurar_animacao_boss6(
    sprite_boss6_caindo,
    sprites_boss6_entrada,
    sprites_boss6_frente
)
bosses["boss6"].configurar_padrao_ataque("boss6")

bosses["boss7"] = PBRR(
    *carregar_boss7(),
    LARGURA // 2,
    ALTURA // 2
)
bosses["boss7"].configurar_padrao_ataque("boss6")

# ==========================================
# CRIAR JOGADOR
# ==========================================

jogador = Jogador(
    baixo,
    cima,
    esquerda,
    direita,
    largura_tela=LARGURA,
    altura_tela=ALTURA
)


# ==========================================
# CRIAR ARMA NO CHÃO
# ==========================================

arma_base = carregar_arma()
arma = pygame.transform.scale(
    arma_base,
    (
        arma_base.get_width() * 4,
        arma_base.get_height() * 4
    )
)
arma_rect = arma.get_rect(
    center=(
        LARGURA // 2,
        ALTURA // 2 - 120
    )
)
arma_angulo = 0
arma_coletada = False


def atualizar_arma():
    global arma_angulo

    if arma_coletada:
        sprite_jogador = jogador.pegar_sprite()
        centro = pygame.Vector2(
            jogador.x + sprite_jogador.get_width() / 2,
            jogador.y + sprite_jogador.get_height() / 2
        )
        direcao = jogador.direcao_mira.copy()
        if direcao.length_squared() == 0:
            direcao = pygame.Vector2(0, 1)
        direcao = direcao.normalize()

        # O sprite da arma foi desenhado apontando para a direita.
        # Então o ângulo deve seguir a convenção do sprite:
        # cima=0°, cima-direita=45°, direita=90°, baixo-direita=135°,
        # baixo=180°, esquerda-baixo=-135°, esquerda=-90°, esquerda-cima=-45°.
        # Quando a mira vira para a esquerda, o sprite precisa ser espelhado
        # para manter a orientação real da arma.
        arma_angulo = math.degrees(math.atan2(direcao.x, -direcao.y))

        offset_x = 10 if direcao.x > 0 else -10 if direcao.x < 0 else 0
        offset_y = 0 if direcao.y >= 0 else 14

        deslocamento = direcao * (sprite_jogador.get_width() * 0.45)
        arma_rect.center = centro + deslocamento + \
            pygame.Vector2(offset_x, offset_y)
        return

    tempo = pygame.time.get_ticks() / 1000
    arma_angulo = math.sin(tempo * 1.8) * 7
    arma_rect.centerx = LARGURA // 2 + math.sin(tempo * 1.3) * 8
    arma_rect.centery = ALTURA // 2 - 120 + math.sin(tempo * 1.9) * 6


# ==========================================
# GERENCIADOR DE BOSSES
# ==========================================

gerenciador_bosses = GerenciadorBosses(
    bosses,
    jogador
)


# ==========================================
# CRIAR EREN
# ==========================================

eren = Eren(
    *sprites_eren,
    jogador
)


# ==========================================
# CRIAR CORAÇÃO
# ==========================================

coracao = Coracao(
    sprites_coracao,
    LARGURA,
    ALTURA
)

jogador.definir_coracao(coracao)


# ==========================================
# CRIAR INTERFACE
# ==========================================

interface = Interface(
    VIDA_MAXIMA
)


# ==========================================
# CRIAR CAIXA DE DIÁLOGO
# ==========================================

caixa_dialogo = CaixaDialogo(
    LARGURA,
    ALTURA
)


# ==========================================
# SISTEMA DE SOMBRAS
# ==========================================

sistema_sombras = SistemaSombras(
    posicao_luz=(120, -180),
    cor=(10, 13, 24),
    intensidade=0.62
)


# ==========================================
# INICIAR PRIMEIRO DIÁLOGO
# ==========================================

caixa_dialogo.iniciar(
    0
)


# ==========================================
# LOOP PRINCIPAL
# ==========================================

rodando = True


while rodando:

    # ======================================
    # EVENTOS
    # ======================================

    for evento in pygame.event.get():

        # ----------------------------------
        # FECHAR JOGO
        # ----------------------------------

        if evento.type == pygame.QUIT:

            rodando = False

        # ----------------------------------
        # TECLAS
        # ----------------------------------

        if evento.type == pygame.KEYDOWN:

            if evento.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                interface.invencibilidade_secreta = not (
                    interface.invencibilidade_secreta
                )

            # ==================================
            # F11
            # ==================================

            if evento.key == pygame.K_F11:

                alternar_fullscreen()

            # ==================================
            # DIÁLOGO
            # ==================================

            caixa_dialogo.processar_evento(
                evento
            )

    # ======================================
    # ATUALIZAR CAIXA DE DIÁLOGO
    # ======================================

    caixa_dialogo.atualizar()

    # ======================================
    # ATUALIZAR ARMA
    # ======================================

    atualizar_arma()

    # ======================================
    # ATUALIZAR JOGO
    # ======================================

    if not interface.morta and caixa_dialogo.pode_mover():

        gerenciador_bosses.atualizar(interface)
        gerenciador_bosses.atualizar_documentos(jogador)

        if not gerenciador_bosses.documento_ativo:
            identificador_dialogo = (
                gerenciador_bosses.consumir_dialogo_pendente()
            )
            if identificador_dialogo is not None:
                caixa_dialogo.iniciar_boss(identificador_dialogo)

            # ==================================
            # ATUALIZAR JOGADOR
            # ==================================

            jogador.atualizar()

            if (
                not arma_coletada
                and jogador.obter_rect().colliderect(arma_rect)
            ):
                arma_coletada = True
                gerenciador_bosses.iniciar()

            coracao.ativo = jogador.usando_coracao

            # ==================================
            # ATUALIZAR EREN
            # ==================================

            eren.atualizar()

            # ==================================
            # ATUALIZAR CORAÇÃO
            # ==================================

            coracao.atualizar()

    interface.atualizar_particulas()

    # ======================================
    # LIMPAR TELA
    # ======================================

    tela_jogo.fill(
        (
            0,
            0,
            0
        )
    )

    if interface.morta:
        interface.desenhar_gore(
            tela_jogo
        )
        jogador.desenhar(
            tela_jogo,
            interface.obter_alpha_game_over()
        )
    else:
        # ======================================
        # DESENHAR MAPA
        # ======================================

        desenhar_chao(
            tela_jogo,
            chao
        )

        bosses_ativos = gerenciador_bosses.obter_bosses()
        personagens = [
            (eren.obter_rect().bottom, eren),
            (jogador.obter_rect().bottom, jogador)
        ]
        for boss in bosses_ativos:
            personagens.append((boss.obter_rect().bottom, boss))
        personagens.sort(key=lambda personagem: personagem[0])

        objetos_sombra = [personagem for _, personagem in personagens]

        sistema_sombras.desenhar(
            tela_jogo,
            objetos_sombra
        )

        desenhar_paredes(
            tela_jogo,
            parede
        )

        for boss in bosses_ativos:
            boss.desenhar_ataques(tela_jogo)

        gerenciador_bosses.desenhar_balas(
            tela_jogo
        )

        for _, personagem in personagens:
            if (
                personagem in bosses_ativos
                and gerenciador_bosses.efeito_derrota is not None
            ):
                deslocamento = gerenciador_bosses.efeito_derrota
                sprite = deslocamento.get(
                    "sprite_final") or personagem.pegar_sprite()
                sprite = sprite.copy()
                brilho = deslocamento.get("brilho", 1.0)
                if brilho > 1.0 and deslocamento.get("aplicar_brilho", False):
                    brilho_surface = sprite.copy()
                    for y in range(brilho_surface.get_height()):
                        for x in range(brilho_surface.get_width()):
                            r, g, b, a = brilho_surface.get_at((x, y))
                            if a <= 0:
                                continue
                            intensidade = min(255, int((r + g + b) / 3))
                            fator = min(1.0, (brilho - 1.0) * 0.85)
                            novo_r = int(r + (255 - r) * fator)
                            novo_g = int(g + (255 - g) * fator)
                            novo_b = int(b + (255 - b) * fator)
                            brilho_surface.set_at(
                                (x, y),
                                (novo_r, novo_g, novo_b, a)
                            )
                    sprite = brilho_surface
                tela_jogo.blit(
                    sprite,
                    (
                        personagem.x + deslocamento["offset_x"],
                        personagem.y + deslocamento["offset_y"]
                    )
                )
            else:
                personagem.desenhar(tela_jogo)

        if not arma_coletada:
            sprite_arma = pygame.transform.rotate(arma, arma_angulo - 90)
            rect_arma = sprite_arma.get_rect(center=arma_rect.center)
            tela_jogo.blit(sprite_arma, rect_arma)
        else:
            sprite_base = arma
            if jogador.direcao_mira.x < 0:
                sprite_base = pygame.transform.flip(arma, True, False)

            sprite_arma = pygame.transform.rotate(
                sprite_base, arma_angulo - 90)
            rect_arma = sprite_arma.get_rect(center=arma_rect.center)
            tela_jogo.blit(sprite_arma, rect_arma)

        interface.desenhar_gore(
            tela_jogo
        )

        # ======================================
        # DESENHAR CORAÇÃO
        # ======================================

        coracao.desenhar(
            tela_jogo,
            jogador
        )

        # ======================================
        # DESENHAR VIDA
        # ======================================

        interface.desenhar_vida(
            tela_jogo
        )

        interface.stamina = jogador.stamina
        interface.desenhar_stamina(
            tela_jogo
        )

        gerenciador_bosses.desenhar_interface(
            tela_jogo
        )

    if not interface.morta:
        # ======================================
        # DESENHAR CAIXA DE DIÁLOGO
        # ======================================

        caixa_dialogo.desenhar(
            tela_jogo
        )

    gerenciador_bosses.desenhar_documentos(tela_jogo)

    # ======================================
    # APRESENTAR TELA
    # ======================================

    apresentar_tela()

    # ======================================
    # ATUALIZAR DISPLAY
    # ======================================

    pygame.display.flip()

    # ======================================
    # FPS
    # ======================================

    clock.tick(FPS)


# ==========================================
# ENCERRAR PYGAME
# ==========================================

pygame.quit()

sys.exit()
