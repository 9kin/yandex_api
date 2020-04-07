import pygame_gui
import sys
from io import BytesIO
import requests
from PIL import Image
from geocoder import *
import random
import os
import pygame
from pygame_gui.elements.ui_selection_list import UISelectionList
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine

map_file = "map.png"
map_type = "map"

ZOOM = 15
ll, _ = get_ll_spn(geocoder_request(("Пермь")))

pygame.init()
screen = pygame.display.set_mode((600, 450))

background = pygame.Surface((800, 600))
background.fill(pygame.Color("#000000"))

manager = pygame_gui.UIManager((600, 450))

menu = UIDropDownMenu(
    options_list=["схема", "спутник", "гибрид"],
    starting_option="схема",
    relative_rect=pygame.Rect(0, 0, 200, 30),
    manager=manager,
)

text_entry = UITextEntryLine(relative_rect=pygame.Rect(0, 30, 150, 30), manager=manager)

search_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((150, 30), (50, 30)), text="find", manager=manager
)


def render_map(ll, map_type, z=10):
    try:
        with open(map_file, "wb") as file:
            get_map_ll(ll, map_type, z=z, pt=f"{ll[0]},{ll[1]},pm2dgl").save(map_file)
    except:
        pass


render_map(ll, map_type, z=ZOOM)
clock = pygame.time.Clock()
run = True
while run:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.text == "схема":
                    map_type = "map"
                elif event.text == "спутник":
                    map_type = "sat"
                elif event.text == "гибрид":
                    map_type = "skl"
                render_map(ll, map_type, z=ZOOM)
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == search_button:
                    try:
                        ll, _ = get_ll_spn(geocoder_request((text_entry.text)))
                        render_map(ll, map_type, z=ZOOM)
                    except:
                        pass
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                try:
                    render_map(ll, map_type, z=ZOOM + 1)
                    ZOOM += 1
                except:
                    pass
            elif event.key == pygame.K_PAGEDOWN:
                try:
                    render_map(ll, map_type, z=ZOOM - 1)
                    ZOOM -= 1
                except:
                    pass
            elif event.key == pygame.K_LEFT:
                ll[0] -= 0.075 / ZOOM
                render_map(ll, map_type, z=ZOOM)
            elif event.key == pygame.K_RIGHT:
                ll[0] += 0.075 / ZOOM
                render_map(ll, map_type, z=ZOOM)
            elif event.key == pygame.K_UP:
                ll[1] += 0.05 / ZOOM
                render_map(ll, map_type, z=ZOOM)
            elif event.key == pygame.K_DOWN:
                ll[1] -= 0.05 / ZOOM
                render_map(ll, map_type, z=ZOOM)
        manager.process_events(event)

    manager.update(time_delta)

    screen.blit(background, (0, 0))
    screen.blit(pygame.image.load(map_file), (0, 0))

    manager.draw_ui(screen)
    pygame.display.update()
os.remove("map.png")
