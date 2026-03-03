import pygame

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
x = 100
y = 100
WIDTH, HEIGHT = 1000, 400



class Health():
    def __init__(self, max_health, current, hurt_rate):
        self.max_health = max_health
        self.current = current
        self.hurt_rate = hurt_rate

    def hurt(self):
        self.current -= self.hurt_rate
        if self.current < 0:
            self.current = 0

    def heal(self, potion_used):
        self.current += potion_used.enhance_rate
        if self.current > self.max_health:
            self.current = self.max_health

class Stamina():
    def __init__(self, max_stamina, current, regen_rate, drain_rate):
        self.max_stamina = max_stamina
        self.current = current
        self.regen_rate = regen_rate
        self.drain_rate = drain_rate

    def use(self):
        self.current -= self.drain_rate
        if self.current < 0:
            self.current = 0

    def recover(self):
        self.current += self.regen_rate
        if self.current > self.max_stamina:
            self.current = self.max_stamina

    def is_empty(self):
        if self.current <= 0:
            return True
        else:
            return False


class Potion():
    def __init__(self, name, enhance_rate):
        self.name = name
        self.enhance_rate = enhance_rate


class HealthPotion(Potion):
    def __init__(self):
        super().__init__("Health enhance potion", enhance_rate=3)



class SpeedPotion(Potion):
    def __init__(self):
        super().__init__("Speed enhance potion", enhance_rate=3)

class StaminaPotion(Potion):
    def __init__(self):
        super().__init__("Stamina enhance potion", enhance_rate=3)



class Attack():
    def __init__(self, attack_type, damage):
        self.attack_type = attack_type
        self.damage = damage

    def use(self, attacker, target):
        target.health.current -= self.damage
        if target.health.current < 0:
            target.health.current = 0



class Player():
    def __init__(self):
        self.position = [x, y]
        self.speed = 5.0  # normal speed
        self.is_sprinting = False
        self.speed_multiplier = 1.0
        self.size = [50, 50]  # width, height
        self.stamina = Stamina(max_stamina=100, current=100, regen_rate=0.5, drain_rate=1.0)
        self.health = Health(max_health=500, current=500, hurt_rate=5.0)
        self.attacks = [Attack(attack_type="Sword Slash", damage=15),    # when key h is pressed
                        Attack(attack_type="Sword thrust", damage=20),   # when key j is pressed
                        Attack(attack_type="Fireball", damage=15),       # when key k is pressed
                        Attack(attack_type="Thunder strike", damage=25)] # when key l is pressed

    # Basic movements
    def move(self, dx, dy):
        self.position[0] += dx * self.speed * self.speed_multiplier
        self.position[1] += dy * self.speed * self.speed_multiplier

    def sprint(self, shift_pressed):

        INCREASE_IN_SPEED_WHEN_SPRINT = 1.5
        MIN_STAMINA_TO_SPRINT = 5  # minimum stamina to allow sprinting

        if shift_pressed and self.stamina.current > MIN_STAMINA_TO_SPRINT:
            self.is_sprinting = True
            self.speed_multiplier = INCREASE_IN_SPEED_WHEN_SPRINT  #sprinting so increased in speed
            self.stamina.use()
        else:
            self.is_sprinting = False
            self.speed_multiplier = 1  #not sprinting so no change in speed
            self.stamina.recover()

    def draw_self(self, surface):
        pygame.draw.rect(surface, WHITE, (self.position[0], self.position[1], self.size[0], self.size[1]))

    def draw_stamina_bar(self, surface):
        bar_width = self.size[0]
        bar_height = 5
        stamina_ratio = self.stamina.current / self.stamina.max_stamina  # Ratio for green:red display
        yellow_width = bar_width * stamina_ratio
        pygame.draw.rect(surface, PURPLE, (self.position[0], self.position[1] - 15, bar_width, bar_height))
        pygame.draw.rect(surface, YELLOW, (self.position[0], self.position[1] - 15, yellow_width, bar_height))

    def draw_health_bar(self, surface):
        bar_width = 250
        bar_height = 20
        spacing_from_the_edge = 10
        x = WIDTH - bar_width - spacing_from_the_edge
        y = spacing_from_the_edge
        health_ratio = self.health.current / self.health.max_health
        green_width = bar_width * health_ratio
        pygame.draw.rect(surface, RED, (x, y, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (x, y, green_width, bar_height))


class Enemy():
    def __init__(self):
        self.position = [700, 200]
        self.size = [50, 50]
        self.speed = 3.0
        self.health = Health(max_health=300, current=300, hurt_rate=10)
        self.attacks = [Attack(attack_type="Magic Projectiles", damage=20)]

    def draw_self(self, surface):
        pygame.draw.rect(surface, RED, (self.position, self.size))

    # def attack(self):


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lam's Game")
    clock = pygame.time.Clock()
    player = Player()
    enemy = Enemy()
    game_running = True
    game_over = False
    while game_running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        keys = pygame.key.get_pressed()
        shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        player.sprint(shift_pressed)

        # INCREASE_IN_SPEED_WHEN_SPRINT = 1.5
        # MIN_STAMINA_TO_SPRINT = 5  # minimum stamina to allow sprinting
        #
        # if shift_pressed and player.stamina.current > MIN_STAMINA_TO_SPRINT:
        #     current_speed = player.speed * INCREASE_IN_SPEED_WHEN_SPRINT
        #     player.stamina.use()
        # else:
        #     current_speed = player.speed
        #     player.stamina.recover()

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

            #if keys[pygame.K_SPACE]:
                #player.attacks[0].perform[player, enemy]

            player.move(dx, dy)

        player.draw_self(screen)
        player.draw_stamina_bar(screen)
        player.draw_health_bar(screen)
        enemy.draw_self(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
