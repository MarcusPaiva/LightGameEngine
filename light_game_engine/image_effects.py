"""
Standalone image fade effect, driven by its own render loop.
"""
import sys

import pygame


def fade_image(screen, image, image_rect, duration=2000):
    """
    Fade effect to display images.

    :param screen: Screen to show image.
    :param image: Image to display.
    :param image_rect: Image bounds.
    :param duration: Effect duration, in milliseconds.
    :return: None
    """
    clock = pygame.time.Clock()
    alpha_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)

    fade_in_time = duration // 2
    fade_out_time = duration // 2

    elapsed = 0
    fade_in = True

    while elapsed < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        dt = clock.tick(60)
        elapsed += dt

        if fade_in:
            alpha = min(255, int((elapsed / fade_in_time) * 255))
            if elapsed >= fade_in_time:
                fade_in = False
                elapsed = 0
        else:
            alpha = max(0, 255 - int((elapsed / fade_out_time) * 255))

        alpha_surface.fill((255, 255, 255, 0))
        alpha_surface.blit(image, (0, 0))
        alpha_surface.set_alpha(alpha)

        screen.fill("white")
        screen.draw(alpha_surface, image_rect)
        screen.flip()
