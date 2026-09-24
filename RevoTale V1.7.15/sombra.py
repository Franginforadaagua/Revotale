import pygame


class SistemaSombras:

    def __init__(
            self,
            posicao_luz=(120, -180),
            cor=(10, 13, 24),
            intensidade=0.40
    ):

        self.posicao_luz = pygame.Vector2(posicao_luz)
        self.cor = cor
        self.intensidade = intensidade

    def definir_luz(self, x, y):

        self.posicao_luz.update(x, y)

    @staticmethod
    def _pegar_sprite(objeto):

        pegar_sprite = getattr(objeto, "pegar_sprite", None)

        if pegar_sprite is None:
            return None

        return pegar_sprite()

    def _desenhar_sombra(self, camada, objeto):

        sprite = self._pegar_sprite(objeto)

        if sprite is None or not getattr(objeto, "projeta_sombra", True):
            return

        sprite_rect = sprite.get_rect(
            topleft=(objeto.x, objeto.y)
        )
        limite_visivel = sprite.get_bounding_rect()

        if limite_visivel.width == 0 or limite_visivel.height == 0:
            return

        ponto_base = pygame.Vector2(
            objeto.x + limite_visivel.centerx,
            objeto.y + limite_visivel.bottom
        )
        direcao = ponto_base - self.posicao_luz

        if direcao.length_squared() == 0:
            direcao = pygame.Vector2(0, 1)
        else:
            direcao.normalize_ip()

        sprite_visivel = sprite.subsurface(
            limite_visivel
        ).copy()
        sprite_invertido = pygame.transform.flip(
            sprite_visivel,
            False,
            True
        )
        mascara = pygame.mask.from_surface(sprite_invertido)
        sombra_sprite = mascara.to_surface(
            setcolor=(
                *self.cor,
                int(92 * self.intensidade)
            ),
            unsetcolor=(0, 0, 0, 0)
        )
        escala_x = 1.0 + abs(direcao.x) * 0.30
        escala_y = 0.55 + max(0, direcao.y) * 0.18
        sombra_sprite = pygame.transform.smoothscale(
            sombra_sprite,
            (
                max(1, int(sombra_sprite.get_width() * escala_x)),
                max(1, int(sombra_sprite.get_height() * escala_y))
            )
        )

        tamanho_borrado = (
            max(1, sombra_sprite.get_width() // 4),
            max(1, sombra_sprite.get_height() // 4)
        )
        sombra_borrada = pygame.transform.smoothscale(
            sombra_sprite,
            tamanho_borrado
        )
        sombra_borrada = pygame.transform.smoothscale(
            sombra_borrada,
            sombra_sprite.get_size()
        )
        sombra_rect = sombra_borrada.get_rect()
        sombra_rect.midtop = (
            int(ponto_base.x),
            int(ponto_base.y)
        )
        camada.blit(
            sombra_borrada,
            sombra_rect
        )

    def desenhar(self, tela, objetos):

        camada = pygame.Surface(
            tela.get_size(),
            pygame.SRCALPHA
        )

        for objeto in objetos:
            self._desenhar_sombra(camada, objeto)

        tela.blit(camada, (0, 0))
