import pygame

from config import (
    LARGURA,
    ALTURA,
    TAMANHO_TILE,
    TAMANHO_TILE_FONTE
)


# ==========================================
# CONFIGURAÇÕES DO MAPA
# ==========================================

COLUNAS = LARGURA // TAMANHO_TILE
LINHAS = ALTURA // TAMANHO_TILE


# ==========================================
# MAPA DO CHÃO
# ==========================================
#
# 0 = vazio
# 1 = usa chao.png
#
# O chão não possui colisão.
#


# ==========================================
# MAPA TESTE 1
# ==========================================

COLUNAS = (
    (LARGURA + TAMANHO_TILE - 1)
    // TAMANHO_TILE
)

LINHAS = (
    (ALTURA + TAMANHO_TILE - 1)
    // TAMANHO_TILE
)

MAPA_CHAO = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

MAPA_PAREDE = [

    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


# ==========================================
# PEGAR TILE DO TILESET
# ==========================================

def pegar_tile(
    tileset,
    indice
):

    # ======================================
    # VERIFICAR ÍNDICE
    # ======================================

    if indice < 0:
        return None

    if indice >= 9:
        return None

    # ======================================
    # POSIÇÃO NO TILESET
    # ======================================

    coluna = indice % 3

    linha = indice // 3

    # ======================================
    # RECORTAR TILE
    # ======================================

    tile = tileset.subsurface(
        pygame.Rect(
            coluna * TAMANHO_TILE_FONTE,
            linha * TAMANHO_TILE_FONTE,
            TAMANHO_TILE_FONTE,
            TAMANHO_TILE_FONTE
        )
    )

    tile = pygame.transform.scale(
        tile,
        (
            TAMANHO_TILE,
            TAMANHO_TILE
        )
    )

    return tile


# ==========================================
# DESENHAR CHÃO
# ==========================================

def desenhar_chao(
    tela,
    chao
):

    for linha in range(
        len(MAPA_CHAO)
    ):

        for coluna in range(
            len(MAPA_CHAO[linha])
        ):

            tile_id = MAPA_CHAO[
                linha
            ][
                coluna
            ]

            # ==================================
            # TILE VAZIO
            # ==================================

            if tile_id == 0:
                continue

            # ==================================
            # POSIÇÃO
            # ==================================

            x = (
                coluna
                *
                TAMANHO_TILE
            )

            y = (
                linha
                *
                TAMANHO_TILE
            )

            # ==================================
            # DESENHAR CHÃO
            # ==================================

            tile = pegar_tile(
                chao,
                tile_id - 1
            )

            if tile is None:
                continue

            tela.blit(
                tile,
                (
                    x,
                    y
                )
            )


# ==========================================
# DESENHAR PAREDES
# ==========================================

def desenhar_paredes(
    tela,
    parede
):

    for linha in range(
        len(MAPA_PAREDE)
    ):

        for coluna in range(
            len(MAPA_PAREDE[linha])
        ):

            tile_id = MAPA_PAREDE[
                linha
            ][
                coluna
            ]

            # ==================================
            # 0 = VAZIO
            # ==================================

            if tile_id == 0:
                continue

            # ==================================
            # PEGAR TILE
            # ==================================

            tile = pegar_tile(
                parede,
                tile_id
            )

            if tile is None:
                continue

            # ==================================
            # POSIÇÃO
            # ==================================

            x = (
                coluna
                *
                TAMANHO_TILE
            )

            y = (
                linha
                *
                TAMANHO_TILE
            )

            # ==================================
            # DESENHAR
            # ==================================

            tela.blit(
                tile,
                (
                    x,
                    y
                )
            )


# ==========================================
# DESENHAR MAPA COMPLETO
# ==========================================

def desenhar_mapa(
    tela,
    chao,
    parede
):

    # ======================================
    # PRIMEIRO: CHÃO
    # ======================================

    desenhar_chao(
        tela,
        chao
    )

    # ======================================
    # SEGUNDO: PAREDE
    # ======================================

    desenhar_paredes(
        tela,
        parede
    )
