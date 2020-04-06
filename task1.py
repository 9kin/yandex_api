import sys
from io import BytesIO
import requests
from PIL import Image
from geocoder import *
import random
import os
import pygame


ZOOM = 15
ll = get_ll_spn(geocoder_request(("Пермь")))

pygame.init()
screen = pygame.display.set_mode((600, 450))


def render_map(ll, z=10):
    map_file = "map.png"
    with open(map_file, "wb") as file:
        get_map_ll(ll, "map", z=z).save(map_file)
        screen.blit(pygame.image.load(map_file), (0, 0))


render_map(ll, z=ZOOM)

run = True
while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
    pygame.display.flip()
os.remove("map.png")
