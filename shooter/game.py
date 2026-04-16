from pygame import *
from constantes import *
from random import *
init()


# FUNCIONALIDAD
puntos = 0
fallos = 0
vidas = 5

# TRABAJO CON FUENTES
font.init()

font_1 = font.Font(TEXT_FONT, 25)

# MAIN WINDOW
screen = display.set_mode((ANCHO, ALTO))
display.set_caption(TITULO)

# CLASE PRINCIPAL
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, cord_x, cord_y, width, height, speed=0):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(sprite_img), (self.width, self.height))
        # Creamos una superficie para la imagen
        self.rect = self.image.get_rect()
        self.rect.x = cord_x
        self.rect.y = cord_y
        self.speed = speed

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x <= ANCHO - self.rect.w:
            self.rect.x += self.speed
        elif keys[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed

    def shoot(self):
        # Que hara el jugador cuando dispare?
        bullet = Bullet(ENEMY_IMG, self.rect.centerx -5, self.rect.top, 10, 15, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        # REFERENCIA A LA VARIABLE GLOBAL
        global fallos
        self.rect.y += self.speed
        if self.rect.y >= ALTO:
            self.rect.x = randint(0, ANCHO - 50)
            self.rect.y = -50
            self.speed = randint(1, 7) 
            fallos += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

# OBJETOS
background = transform.scale(image.load(BG_IMG), (ANCHO, ALTO))
player = Player(PLAYER_IMG, (ANCHO - 80) // 2, ALTO - 70, 80, 60, 5)
# trabajando con grupos:
aliens = sprite.Group()
bullets = sprite.Group() # CONTENEDOR PARA BALAS

for i in range(5):
    enemy = Enemy(ENEMY_IMG, randint(0, ANCHO - 50), -50, 50, 50, randint(1, 7))
    aliens.add(enemy)

# CICLO DE JUEGO
run = True
finish = False # ESTADO DE JUEGO
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False # bandera de estado
        if e.type == KEYDOWN:
            if e.key == K_r:
                finish = False
                aliens.draw(screen)
            if e.key == K_SPACE:
                player.shoot()
    
    misses_text = font_1.render(f'Fallos: {fallos}', 1, WHITE)
    points_text = font_1.render(f'Puntos: {puntos}', 1, WHITE)
    life_text = font_1.render(f'Vidas: {vidas}', 1, (91, 245, 39))

    if not finish:
        screen.blit(background, (0, 0))
        screen.blit(points_text, (15, 10))
        screen.blit(misses_text, (15, 40))
        screen.blit(life_text, (ANCHO - 130, 15))

        player.reset()
        player.update()
        aliens.draw(screen)
        aliens.update()
        bullets.draw(screen)
        bullets.update()

        if sprite.groupcollide(aliens, bullets, True, True):
            puntos += 1
            enemy = Enemy(ENEMY_IMG, randint(0, ANCHO - 50), -50, 50, 50, randint(1, 7))
            aliens.add(enemy)

        if sprite.spritecollide(player, aliens, True):
            vidas -= 1
            enemy = Enemy(ENEMY_IMG, randint(0, ANCHO - 50), -50, 50, 50, randint(1, 7))
            aliens.add(enemy)

            
        # CONDICION VICTORIA
        if puntos == 10:
            finish = True
            screen.fill(BLACK)
            victory_text = font_1.render(f'ERES EL MEJOR, FELICIDADES!', 1, (238, 245, 39))
            screen.blit(victory_text, ((ANCHO - 350)// 2, ALTO // 2))

        # CONDICION DERROTA
        if vidas == 0 or fallos >= 10:
            finish = True
            screen.fill(BLACK)




    # NO TOCAR
    display.update()
    clock.tick(FPS)


quit()

