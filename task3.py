import sys
from io import BytesIO
import requests
from PIL import Image
from geocoder import *
import random
import os
import pygame


ZOOM = 15
ll, _ = get_ll_spn(geocoder_request(("Пермь")))

pygame.init()
screen = pygame.display.set_mode((600, 450))


def render_map(ll, z=10):
    try:
        map_file = "map.png"
        with open(map_file, "wb") as file:
            get_map_ll(ll, "map", z=z).save(map_file)
            screen.blit(pygame.image.load(map_file), (0, 0))
    except:
        pass


render_map(ll, z=ZOOM)
run = True
while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_PAGEUP:
                try:
                    render_map(ll, z=ZOOM + 1)
                    ZOOM += 1
                except:
                    pass
            elif i.key == pygame.K_PAGEDOWN:
                try:
                    render_map(ll, z=ZOOM - 1)
                    ZOOM -= 1
                except:
                    pass
            elif i.key == pygame.K_LEFT:
                ll[0] -= 0.075 / ZOOM
                render_map(ll, z=ZOOM)
            elif i.key == pygame.K_RIGHT:
                ll[0] += 0.075 / ZOOM
                render_map(ll, z=ZOOM)
            elif i.key == pygame.K_UP:
                ll[1] += 0.05 / ZOOM
                render_map(ll, z=ZOOM)
            elif i.key == pygame.K_DOWN:
                ll[1] -= 0.05 / ZOOM
                render_map(ll, z=ZOOM)
    pygame.display.flip()
os.remove("map.png")
