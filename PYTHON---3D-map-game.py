import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from pyrr import Matrix44, Vector3

# Initialize pygame
pygame.init()

# Window dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Map Visualizer")

# Camera settings
camera_position = Vector3([0.0, 0.0, -5.0])
camera_front = Vector3([0.0, 0.0, 1.0])
camera_up = Vector3([0.0, 1.0, 0.0])

# Create perspective
gluPerspective(45, width / height, 0.1, 100.0)

# Terrain data
terrain_width = 50
terrain_height = 50
terrain_data = np.random.rand(terrain_width, terrain_height)

def draw_terrain():
    glBegin(GL_QUADS)
    for x in range(terrain_width - 1):
        for z in range(terrain_height - 1):
            glColor3f(0.1, 0.7, 0.1)  # Green color for terrain
            glVertex3f(x, terrain_data[x][z], z)
            glVertex3f(x + 1, terrain_data[x + 1][z], z)
            glVertex3f(x + 1, terrain_data[x + 1][z + 1], z + 1)
            glVertex3f(x, terrain_data[x][z + 1], z + 1)
    glEnd()

def update_camera_movement(keys, camera_pos, camera_front, camera_up):
    camera_speed = 0.05
    if keys[K_w]:  # Move forward
        camera_pos += camera_speed * camera_front
    if keys[K_s]:  # Move backward
        camera_pos -= camera_speed * camera_front
    if keys[K_a]:  # Move left
        camera_pos -= np.cross(camera_front, camera_up) * camera_speed
    if keys[K_d]:  # Move right
        camera_pos += np.cross(camera_front, camera_up) * camera_speed

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    update_camera_movement(keys, camera_position, camera_front, camera_up)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Set camera view
    camera_target = camera_position + camera_front
    gluLookAt(camera_position[0], camera_position[1], camera_position[2],
              camera_target[0], camera_target[1], camera_target[2],
              camera_up[0], camera_up[1], camera_up[2])
    
    draw_terrain()  # Draw the 3D terrain map
    
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
