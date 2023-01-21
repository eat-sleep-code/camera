from picamera2 import Picamera2
import pygame

pygame.init()
res = (1024,768)
screen = pygame.display.set_mode(res)

camera = Picamera2()
camera.preview_configuration.main.size = res
camera.preview_configuration.main.format = 'BGR888'
camera.configure("preview")
camera.start()

i = 0
while True:
    i = i+1
    array = camera.capture_array()
    img = pygame.image.frombuffer(array.data, res, 'RGB')
    screen.blit(img, (0, 0))
    pygame.display.update()
    camera.capture_file("test" + str(i) + ".png")