import pygame
pygame.init()

dis = pygame.display.set_mode((500, 500))
x = 50
y = 50
height = 40
width = 100
run = True
vel = 10
clock = pygame.time.Clock()
direction = 'Right'

def animate(x, y, height, width, direction):
    if x < 0:
        direction = 'Right'

    elif x > 500:
        direction = 'Left'

    if direction == 'Right':
        x += vel

    elif direction == 'Left':
        x -= vel

    pygame.draw.rect(dis, (255, 0, 0), pygame.Rect(x, y, width, height))

    return x, direction

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    dis.fill((0, 0, 0))


    x, direction = animate(x, y, height, width, direction)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()