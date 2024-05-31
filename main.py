import pygame
import math
import random
import sys

pygame.init()

sw = 800
sh = 800

try:
    bg = pygame.image.load('asteroidsPics/starbg.png')
    alienImg = pygame.image.load('asteroidsPics/alienShip.png')
    playerRocket = pygame.image.load('asteroidsPics/spaceRocket.png')
    star = pygame.image.load('asteroidsPics/star.png')
    asteroid50 = pygame.image.load('asteroidsPics/asteroid50.png')
    asteroid100 = pygame.image.load('asteroidsPics/asteroid100.png')
    asteroid150 = pygame.image.load('asteroidsPics/asteroid150.png')
except pygame.error as e:
    print(f"No se pudo cargar la imagen: {e}")
    pygame.quit()
    sys.exit()

try:
    shoot = pygame.mixer.Sound('sounds/shoot.wav')
    bangLargeSound = pygame.mixer.Sound('sounds/bangLarge.wav')
    bangSmallSound = pygame.mixer.Sound('sounds/bangSmall.wav')
    shoot.set_volume(.25)
    bangLargeSound.set_volume(.25)
    bangSmallSound.set_volume(.25)
except pygame.error as e:
    print(f"No se pudo cargar el sonido: {e}")
    pygame.quit()
    sys.exit()

pygame.display.set_caption('Asteroids')
win = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()

gameover = False
lives = 3
score = 0
rapidFire = False
rfStart = -1
isSoundOn = True
highScore = 0

class Player(object):
    def __init__(self):
        self.img = playerRocket
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = sw//2
        self.y = sh//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def draw(self, win):
        win.blit(self.rotatedSurf, self.rotatedRect)

    def turnLeft(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def turnRight(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def moveForward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def updateLocation(self):
        if self.x > sw + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        elif self.y < -50:
            self.y = sh
        elif self.y > sh + 50:
            self.y = 0

class Bullet(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self):
        return self.x < -50 or self.x > sw or self.y > sh or self.y < -50

class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = asteroid50
        elif self.rank == 2:
            self.image = asteroid100
        else:
            self.image = asteroid150
        self.w = 50 * rank
        self.h = 50 * rank
        self.ranPoint = random.choice([(random.randrange(0, sw-self.w), random.choice([-1*self.h - 5, sh + 5])), (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1,3)
        self.yv = self.ydir * random.randrange(1,3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

class Star(object):
    def __init__(self):
        self.img = star
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

class Alien(object):
    def __init__(self):
        self.img = alienImg
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

class AlienBullet(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 4
        self.h = 4
        self.dx, self.dy = player.x - self.x, player.y - self.y
        self.dist = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx / self.dist, self.dy / self.dist
        self.xv = self.dx * 5
        self.yv = self.dy * 5

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])

def redrawGameWindow():
    win.blit(bg, (0, 0))
    font = pygame.font.SysFont('arial', 30)
    livesText = font.render('Vidas: ' + str(lives), 1, (255, 255, 255))
    playAgainText = font.render('Presiona Tab para Jugar de Nuevo', 1, (255, 255, 255))
    scoreText = font.render('Puntuación: ' + str(score), 1, (255, 255, 255))
    highScoreText = font.render('Puntuación Máxima: ' + str(highScore), 1, (255, 255, 255))
    win.blit(livesText, (10, 10))
    win.blit(scoreText, (sw - scoreText.get_width() - 10, 10))
    win.blit(highScoreText, (sw - highScoreText.get_width() - 10, 40))
    if gameover:
        win.blit(playAgainText, (sw//2 - playAgainText.get_width()//2, sh//2 - playAgainText.get_height()//2))

    for b in playerBullets:
        b.draw(win)
    for a in asteroids:
        a.draw(win)
    for s in stars:
        s.draw(win)
    for al in aliens:
        al.draw(win)
    for ab in alienBullets:
        ab.draw(win)
    player.draw(win)
    pygame.display.update()

def main():
    global gameover, lives, score, rapidFire, rfStart, isSoundOn, highScore
    global player, playerBullets, asteroids, stars, aliens, alienBullets, count, run

    player = Player()
    playerBullets = []
    asteroids = []
    count = 0
    stars = []
    aliens = []
    alienBullets = []
    run = True

    while run:
        clock.tick(60)
        count += 1
        if not gameover:
            spawn_objects()
            handle_collisions()
            update_objects()
            handle_input()
        redrawGameWindow()
        handle_events()

    pygame.quit()

def spawn_objects():
    global count, asteroids, stars, aliens
    if count % 50 == 0:
        ran = random.choice([1, 1, 1, 2, 2, 3])
        asteroids.append(Asteroid(ran))
    if count % 1000 == 0:
        stars.append(Star())
    if count % 750 == 0:
        aliens.append(Alien())

def handle_collisions():
    global lives, score, rfStart, rapidFire, isSoundOn
    for b in playerBullets:
        for a in asteroids:
            if a.rank == 3:
                if a.x < b.x < a.x + a.w and a.y < b.y < a.y + a.h:
                    asteroids.append(Asteroid(2))
                    asteroids.append(Asteroid(2))
                    if isSoundOn:
                        bangLargeSound.play()
                    asteroids.pop(asteroids.index(a))
                    playerBullets.pop(playerBullets.index(b))
                    score += 10
            elif a.rank == 2:
                if a.x < b.x < a.x + a.w and a.y < b.y < a.y + a.h:
                    asteroids.append(Asteroid(1))
                    asteroids.append(Asteroid(1))
                    if isSoundOn:
                        bangSmallSound.play()
                    asteroids.pop(asteroids.index(a))
                    playerBullets.pop(playerBullets.index(b))
                    score += 20
            elif a.rank == 1:
                if a.x < b.x < a.x + a.w and a.y < b.y < a.y + a.h:
                    if isSoundOn:
                        bangSmallSound.play()
                    asteroids.pop(asteroids.index(a))
                    playerBullets.pop(playerBullets.index(b))
                    score += 30
        for s in stars:
            if s.x < b.x < s.x + s.w and s.y < b.y < s.y + s.h:
                rfStart = count
                rapidFire = True
                playerBullets.pop(playerBullets.index(b))
                stars.pop(stars.index(s))

    for a in asteroids:
        if a.rank == 3:
            if a.x < player.x < a.x + a.w and a.y < player.y < a.y + a.h:
                asteroids.append(Asteroid(2))
                asteroids.append(Asteroid(2))
                if isSoundOn:
                    bangLargeSound.play()
                asteroids.pop(asteroids.index(a))
                lives -= 1
        elif a.rank == 2:
            if a.x < player.x < a.x + a.w and a.y < player.y < a.y + a.h:
                asteroids.append(Asteroid(1))
                asteroids.append(Asteroid(1))
                if isSoundOn:
                    bangSmallSound.play()
                asteroids.pop(asteroids.index(a))
                lives -= 1
        elif a.rank == 1:
            if a.x < player.x < a.x + a.w and a.y < player.y < a.y + a.h:
                if isSoundOn:
                    bangSmallSound.play()
                asteroids.pop(asteroids.index(a))
                lives -= 1

    for al in aliens:
        if al.x < player.x < al.x + al.w and al.y < player.y < al.y + al.h:
            aliens.pop(aliens.index(al))
            lives -= 1

    for ab in alienBullets:
        if ab.x < player.x < ab.x + ab.w and ab.y < player.y < ab.y + ab.h:
            alienBullets.pop(alienBullets.index(ab))
            lives -= 1

def update_objects():
    global asteroids, aliens, playerBullets, alienBullets, stars
    player.updateLocation()
    for a in asteroids:
        a.x += a.xv
        a.y += a.yv
        if a.x < -a.w - 10:
            asteroids.pop(asteroids.index(a))
        if a.x > sw + a.w + 10:
            asteroids.pop(asteroids.index(a))
        if a.y < -a.h - 10:
            asteroids.pop(asteroids.index(a))
        if a.y > sh + a.h + 10:
            asteroids.pop(asteroids.index(a))

    for al in aliens:
        al.x += al.xv
        al.y += al.yv
        if al.x < -al.w - 10:
            aliens.pop(aliens.index(al))
        if al.x > sw + al.w + 10:
            aliens.pop(aliens.index(al))
        if al.y < -al.h - 10:
            aliens.pop(aliens.index(al))
        if al.y > sh + al.h + 10:
            aliens.pop(aliens.index(al))
        if random.randrange(0, 150) == 1:
            alienBullets.append(AlienBullet(al.x + al.w//2, al.y + al.h//2))

    for b in playerBullets:
        b.move()
        if b.checkOffScreen():
            playerBullets.pop(playerBullets.index(b))

    for ab in alienBullets:
        ab.x += ab.xv
        ab.y += ab.yv

    if count - rfStart > 500:
        rapidFire = False

def handle_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.turnLeft()
    if keys[pygame.K_RIGHT]:
        player.turnRight()
    if keys[pygame.K_UP]:
        player.moveForward()
    if keys[pygame.K_SPACE]:
        if rapidFire:
            playerBullets.append(Bullet())
            if isSoundOn:
                shoot.play()

def handle_events():
    global run, gameover, isSoundOn, score, highScore, lives
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    if not rapidFire:
                        playerBullets.append(Bullet())
                        if isSoundOn:
                            shoot.play()
            if event.key == pygame.K_m:
                isSoundOn = not isSoundOn
            if event.key == pygame.K_TAB:
                if gameover:
                    reset_game()

def reset_game():
    global gameover, lives, asteroids, aliens, alienBullets, stars, score, highScore
    gameover = False
    lives = 3
    asteroids.clear()
    aliens.clear()
    alienBullets.clear()
    stars.clear()
    playerBullets.clear()
    if score > highScore:
        highScore = score
    score = 0

if __name__ == "__main__":
    main()
