import pygame

WHITE = (255, 255, 255)

def main_menu():
    pygame.display.set_caption("Menu")
    screen = pygame.display.set_mode((1000, 400))

    while True:
        screen.fill(WHITE)