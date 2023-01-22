from picamera2 import Picamera2
from libcamera import ColorSpace
import pygame
import time

pygame.init()
appWidth = 1024
appHeight = 768

screen = pygame.display.set_mode((appWidth, appHeight))

camera = Picamera2()

# === Create Configurations ====================================================

configPreview = camera.create_preview_configuration()
camera.preview_configuration.main.size = (appWidth, appHeight)
camera.preview_configuration.main.format = 'BGR888'
camera.configure('preview')

# ------------------------------------------------------------------------------

configStill = camera.create_still_configuration()
camera.still_configuration.enable_raw()
camera.still_configuration.main.size = camera.sensor_resolution
camera.still_configuration.buffer_count = 2
camera.still_configuration.colour_space = ColorSpace.Sycc()

camera.start()

while True:
    events=pygame.event.get()
    for e in events:
        if (e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE):
            filename = 'image.jpg'
            print('Capturing frame...')
            camera.switch_mode_and_capture_file(configStill, filename)
            
            print('Displaying the captured frame for 5 seconds...')
            capturedFrame = pygame.image.load(filename).convert()
            capturedFrameRectangle = capturedFrame.get_rect()
            screen.blit(capturedFrame, capturedFrameRectangle)
            pygame.display.update()
            time.sleep(5)

    array = camera.capture_array()
    previewFrame = pygame.image.frombuffer(array.data, (appWidth, appHeight), 'RGB')
    screen.blit(previewFrame, (0, 0))
    pygame.display.update()
