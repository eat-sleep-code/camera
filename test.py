import time

import pygame
from libcamera import ColorSpace
from picamera2 import Picamera2

pygame.init()
appWidth = 1024
appHeight = 768

screen = pygame.display.set_mode((appWidth, appHeight))

camera = Picamera2()

# === Create Configurations ====================================================

camera.preview_configuration.main.size = (appWidth, appHeight)
camera.preview_configuration.main.format = 'BGR888'
camera.configure('preview')

# ------------------------------------------------------------------------------

camera.still_configuration.enable_raw()
camera.still_configuration.main.size = camera.sensor_resolution
#camera.still_configuration.buffer_count = 2
camera.still_configuration.colour_space = ColorSpace.Sycc()

camera.start()

while True:
    events=pygame.event.get()
    for e in events:
        if (e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE):
            filename = 'image.jpg'
            print('Capturing frame...')
            request = camera.switch_mode_and_capture_request('still')
            request.save('main', filename)
            array = request.make_array('main')
            request.release()
            
            print('Displaying the captured frame for 5 seconds...')
            capturedFrame = pygame.image.frombuffer(array.data, camera.sensor_resolution, 'RGB')
            screen.blit(capturedFrame, (0, 0))
            pygame.display.update()
            time.sleep(5)

    array = camera.capture_array()
    previewFrame = pygame.image.frombuffer(array.data, (appWidth, appHeight), 'RGB')
    screen.blit(previewFrame, (0, 0))
    pygame.display.update()
