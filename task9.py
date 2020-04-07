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
from pygame_gui.elements.ui_label import UILabel

map_file = "map.png"
map_type = "map"


ZOOM = 15
json = geocoder_request("Пермь, Революции 21")
ll, _ = get_ll_spn(json)
pt = ll.copy()


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

label = UILabel(
    relative_rect=pygame.Rect(0, 420, 600, 30), text=full_adress(json), manager=manager
)

text_entry = UITextEntryLine(relative_rect=pygame.Rect(0, 30, 150, 30), manager=manager)

search_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((150, 30), (50, 30)), text="find", manager=manager
)


cancel_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 60), (200, 30)), text="cancel", manager=manager
)

postal_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 90), (200, 30)),
    text="wiew postal code",
    manager=manager,
)


def render_map(ll, map_type, z=10):
    if pt:
        img = get_map_ll(ll, map_type, z=z, pt=f"{pt[0]},{pt[1]},pm2dgl")
    else:
        img = get_map_ll(ll, map_type, z=z)
    if img is None:
        return False
    with open(map_file, "wb") as file:
        img.save(map_file)
    return True


render_map(ll, map_type, z=ZOOM)
clock = pygame.time.Clock()
run = True
while run:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                old_map_type = map_type
                if event.text == "схема":
                    map_type = "map"
                elif event.text == "спутник":
                    map_type = "sat"
                elif event.text == "гибрид":
                    map_type = "skl"
                res = render_map(ll, map_type, z=ZOOM)
                if not res:
                    map_type = old_map_type

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == search_button:
                    try:
                        json = geocoder_request(text_entry.text)
                        ll, _ = get_ll_spn(json)
                        pt = ll.copy()
                        render_map(ll, map_type, z=ZOOM)
                        try:
                            label.set_text(full_adress(json) + get_postal_code(json))
                        except:
                            label.set_text(full_adress(json))
                    except:
                        pass
                if event.ui_element == cancel_button:
                    pt = None
                    render_map(ll, map_type, z=ZOOM)
                if event.ui_element == postal_button:
                    json = geocoder_request(to_ll(ll))
                    if postal_button.text == "wiew postal code":
                        label.set_text(full_adress(json) + get_postal_code(json))
                        postal_button.set_text("don't wiew postal code")
                    elif postal_button.text == "don't wiew postal code":
                        label.set_text(full_adress(json))
                        postal_button.set_text("wiew postal code")

        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if render_map(ll, map_type, z=ZOOM + 1):
                    ZOOM += 1
            elif event.key == pygame.K_PAGEDOWN:
                if render_map(ll, map_type, z=ZOOM - 1):
                    ZOOM -= 1
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
