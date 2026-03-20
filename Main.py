
import pygame

from classes import Enemy, Player
from classes import WHITE, GREEN, YELLOW, PURPLE, RED, BLACK
from classes import x, y, WIDTH, HEIGHT


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lam's Game")
    clock = pygame.time.Clock()
    player = Player()
    enemy = Enemy()
    game_running = True
    game_over = False


    def main_menu():
        pygame.display.set_caption("Menu")
        screen = pygame.display.set_mode((1000, 400))

        while True:
            screen.fill(WHITE)

            # learn how to blit images for buttons and background

    def main_menu(screen):
        running = True

        while running:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.flip()

    main_menu(screen)
    #
    while game_running:
        screen.fill(BLACK)

        if player.health.current <= 0:
            game_over = True

        #if enemy.health.current <= 0:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        keys = pygame.key.get_pressed()
        shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        player.sprint(shift_pressed)
        player.handle_attacks(keys, enemy)


        if not game_over:
            dx, dy = 0, 0

            if keys[pygame.K_RIGHT]:
                dx += 1
            if keys[pygame.K_LEFT]:
                dx -= 1
            if keys[pygame.K_UP]:
                dy -= 1
            if keys[pygame.K_DOWN]:
                dy += 1

            # if keys[pygame.K_SPACE]:
            # player.attacks[0].perform[player, enemy]

            player.move(dx, dy)


        player.draw_self(screen)
        player.draw_stamina_bar(screen)
        player.draw_health_bar(screen)
        enemy.draw_self(screen)
        enemy.draw_health_bar(screen)
        enemy.chase(player)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
