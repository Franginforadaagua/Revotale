import pygame
import math
import random


def tela_inicial(tela):

    clock = pygame.time.Clock()

    # ==================================================
    # INICIALIZAR ÁUDIO
    # ==================================================

    pygame.mixer.init()

    # Música da tela inicial
    pygame.mixer.music.load(
        "sfx/inicio.mp3"
    )

    pygame.mixer.music.play(
        -1
    )

    # Som ao apertar o botão
    som_start = pygame.mixer.Sound(
        "sfx/start.wav"
    )

    # ==================================================
    # LOGO
    # ==================================================

    logo_original = pygame.image.load(
        "assets/jogo/logo.png"
    ).convert_alpha()

    logo_largura = 1200

    proporcao = (
        logo_original.get_height()
        / logo_original.get_width()
    )

    logo_altura = int(
        logo_largura * proporcao
    )

    logo = pygame.transform.smoothscale(
        logo_original,
        (
            logo_largura,
            logo_altura
        )
    )

    # ==================================================
    # FONTE
    # ==================================================

    fonte = pygame.font.Font(
        None,
        32
    )

    # ==================================================
    # ANIMAÇÕES
    # ==================================================

    tempo = 0

    iniciando = False

    alpha_flash = 0

    velocidade_flash = 0.8

    # ==================================================
    # LOOP
    # ==================================================

    while True:

        # ==============================================
        # EVENTOS
        # ==============================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.mixer.music.stop()

                return False

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:

                    pygame.mixer.music.stop()

                    return False

                if not iniciando:

                    iniciando = True

                    alpha_flash = 0

                    # ==================================
                    # PARAR MÚSICA
                    # ==================================

                    pygame.mixer.music.stop()

                    # ==================================
                    # TOCAR SOM DE START
                    # ==================================

                    som_start.play()

        # ==============================================
        # TEMPO
        # ==============================================

        tempo += 0.05

        # ==============================================
        # FUNDO
        # ==============================================

        tela.fill(
            (
                0,
                0,
                0
            )
        )

        # ==============================================
        # MOVIMENTO SENOIDAL
        # ==============================================

        movimento_y = math.sin(
            tempo * 1.5
        ) * 8

        movimento_x = math.sin(
            tempo * 0.8
        ) * 3

        # ==============================================
        # ROTAÇÃO
        # ==============================================

        rotacao = math.sin(
            tempo * 0.8
        ) * 0.4

        # ==============================================
        # TREMELIQUE
        # ==============================================

        intensidade_tremelique = (
            alpha_flash / 255
        )

        tremelique_x = random.uniform(
            -8,
            8
        ) * intensidade_tremelique

        tremelique_y = random.uniform(
            -8,
            8
        ) * intensidade_tremelique

        tremelique_rotacao = random.uniform(
            -1.5,
            1.5
        ) * intensidade_tremelique

        rotacao_final = (
            rotacao
            +
            tremelique_rotacao
        )

        logo_animada = pygame.transform.rotate(
            logo,
            rotacao_final
        )

        # ==============================================
        # POSIÇÃO
        # ==============================================

        logo_x = (
            tela.get_width()
            -
            logo_animada.get_width()
        ) // 2

        logo_y = (
            tela.get_height()
            -
            logo_animada.get_height()
        ) // 2 - 250

        logo_x += int(
            movimento_x
            +
            tremelique_x
        )

        logo_y += int(
            movimento_y
            +
            tremelique_y
        )

        # ==============================================
        # LOGO
        # ==============================================

        tela.blit(
            logo_animada,
            (
                logo_x,
                logo_y
            )
        )

        # ==============================================
        # TEXTO
        # ==============================================

        if not iniciando:

            texto = fonte.render(
                "Aperte qualquer botão para começar",
                True,
                (
                    255,
                    255,
                    255
                )
            )

            texto.set_alpha(
                int(
                    150
                    +
                    math.sin(tempo * 2) * 80
                )
            )

            texto_rect = texto.get_rect(
                center=(
                    tela.get_width() // 2,
                    tela.get_height() // 2 + 180
                )
            )

            tela.blit(
                texto,
                texto_rect
            )

        # ==============================================
        # FLASH
        # ==============================================

        if iniciando:

            alpha_flash += velocidade_flash

            if alpha_flash > 255:

                alpha_flash = 255

            flash = pygame.Surface(
                tela.get_size()
            )

            flash.fill(
                (
                    255,
                    255,
                    255
                )
            )

            flash.set_alpha(
                alpha_flash
            )

            tela.blit(
                flash,
                (
                    0,
                    0
                )
            )

            # ==========================================
            # CENA
            # ==========================================

            if alpha_flash >= 255:

                return True

        # ==============================================
        # ATUALIZAR TELA
        # ==============================================

        pygame.display.flip()

        clock.tick(60)
