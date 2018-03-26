# Deze code vertelt Python welke packages(externe code) er nodig zijn voor dit programma
# Voor dit programma zijn nodig:
# - pygame -> voor de visuele elementen van de game, de klok, en voor de toetsenbord invoer
# - random -> voor het kiezen van een positie van de 'apple'
# - sys    -> voor het afsluiten van het programma
import pygame, random, sys
from pygame.locals import *


# Deze functie controleert of er een botsing is tussen item 1 en item 2
def collide(x1, x2, y1, y2, w1, w2, h1, h2):
    if x1 + w1 > x2 and x1 < x2 + w2 and y1 + h1 > y2 and y1 < y2 + h2:
        return True
    else:
        return False


# Deze functie bepaalt wat er gebeurt als je af gaat
def die(screen, score):
    font = pygame.font.SysFont('Arial', 30)
    text = font.render('Je score was: ' + str(score), True, (0, 0, 0))
    screen.blit(text, (10, 270))
    pygame.display.update()
    pygame.time.wait(2000)
    sys.exit(0)


# Deze code maakt het programma klaar voor het begin van de game
xs = [290, 290, 290, 290, 290]                                  # De x-posities van alle stukjes van de snake
ys = [290, 270, 250, 230, 210]                                  # De y-posities van alle stukjes van de snake
direction = 0                                                   # De richting waarin de snake beweegt (0 = down, 1 = right, 2 = up, 3 = left)
score = 0                                                       # De score
applepos = (random.randint(0, 590), random.randint(0, 590))     # De positie van de 'apple'
pygame.init()                                                   # Start pygame
screen = pygame.display.set_mode((600, 600))                    # Het scherm van de game - 600 bij 600 pixels
pygame.display.set_caption('Snake')                             # De titel van het scherm is 'Snake'
appleimage = pygame.Surface((10, 10))                           # De 'apple' is een oppervlak van 10 bij 10 pixels
appleimage.fill((0, 255, 0))                                    # Maak de apple groen (Red, Green, Blue)
snakeimage = pygame.Surface((20, 20))                           # Elk stukje van de snake is een oppervlak van 20 bij 20 pixels
snakeimage.fill((255, 0, 0))                                    # Maak de snake rood (Red, Green, Blue)
font = pygame.font.SysFont('Arial', 20)                         # Het lettertype gebruikt in de game
clock = pygame.time.Clock()                                     # De klok


# Dit is de loop met daarin alle instructies voor het runnen van de game
while True:
    # Beperk de snelheid van de loop tot 10x per seconde (10 frames per seconde)
    clock.tick(10)

    # Controleer of er een 'event' is geweest, zoals:
    # - event.type == QUIT -> er is op het kruisje geklikt
    # - event.type == KEYDOWN en event.key == K_UP -> er is op de up-toets gedrukt
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_UP and direction != 0:
                direction = 2
            elif event.key == K_DOWN and direction != 2:
                direction = 0
            elif event.key == K_LEFT and direction != 1:
                direction = 3
            elif event.key == K_RIGHT and direction != 3:
                direction = 1

    # Controleer of de snake botst met zijn staart
    tail = len(xs) - 1
    while tail >= 2:
        if collide(xs[0], xs[tail], ys[0], ys[tail], 20, 20, 20, 20):
            die(screen, score)
        tail -= 1

    # Controleer of de snake botst met een apple
    if collide(xs[0], applepos[0], ys[0], applepos[1], 20, 10, 20, 10):
        score += 1
        xs.append(700)
        ys.append(700)
        applepos = (random.randint(0, 590), random.randint(0, 590))

    # Controleer of de snake botst met de rand
    if xs[0] < 0 or xs[0] > 580 or ys[0] < 0 or ys[0] > 580:
        die(screen, score)

    # Verplaats elk stukje van de snake naar de positie van het volgende stukje
    tail = len(xs) - 1
    while tail >= 1:
        xs[tail] = xs[tail - 1]
        ys[tail] = ys[tail - 1]
        tail -= 1

    # Verplaats de kop van de snake in de richting van de beweging
    if direction == 0:
        ys[0] += 20
    elif direction == 1:
        xs[0] += 20
    elif direction == 2:
        ys[0] -= 20
    elif direction == 3:
        xs[0] -= 20

    # Maak het scherm wit
    screen.fill((255, 255, 255))

    # Teken de stukjes snake op de juiste posities
    for tail in range(0, len(xs)):
        screen.blit(snakeimage, (xs[tail], ys[tail]))

    # Teken de apple op de juiste positie
    screen.blit(appleimage, applepos)

    # Creeer de tekst voor de score
    text = font.render(str(score), True, (0, 0, 0))

    # Teken de tekst op het scherm
    screen.blit(text, (10, 10))

    # Update het scherm zodat de gebruiker alle veranderingen ziet
    pygame.display.update()
