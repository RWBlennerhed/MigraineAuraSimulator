import pygame
import os
import csv
import time
import webbrowser

# Initiera Pygame
pygame.init()

# Ladda och sätt programikon
icon_path = "icon32x32.png"  # Byt ut till din ikonfil
if os.path.exists(icon_path):
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)


# Migraine Aura Simulation
# Collaboration between Robert William Blennerhed & ChatGPT
# Developed in Python using Pygame


# Färger
WHITE = (0, 0, 0)  # Bakgrundsfärg svart
BLACK = (255, 255, 255)  # Textfärg vit
RED = (200, 0, 0)

# Ladda inställningar från settings.csv
settings_file = "settings.csv"
def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, mode='r') as file:
            reader = csv.reader(file)
            settings = {rows[0]: float(rows[1]) for rows in reader}
            return settings
    return {"frame_delay": 30, "scale_step": 0.045}  # Standardvärden

def save_settings(settings):
    with open(settings_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        for key, value in settings.items():
            writer.writerow([key, value])

settings = load_settings()
status_message = "Settings loaded successfully." if os.path.exists(settings_file) else "Using default settings."
screen_width, screen_height = 800, 600  # Ökat fönsterstorlek
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Migraine Aura Simulator")

# Teckensnitt
font = pygame.font.Font(None, 30)
title_text = "- Main Menu - use arrow keys to navigate"

# Menyalternativ
menu_options = ["About", "My Aura Phenomenon", "My Statistics", "Settings", "Quit"]
selected_option = 0
menu_spacing = 50

# About-text
about_text = [
    "WARNING: Use at your own risk!",
    "This migraine aura simulation is developed",
    "by Robert William Blennerhed & ChatGPT.",
    "It is intended for educational purposes only.",
    "",
    "By using this program, you acknowledge that",
    "you do so at your own risk.",
    "The creators are not responsible for any",
    "effects that may occur from viewing the aura simulation.",
    "",

    "Migraine Aura Simulation v1.0",
    "Developed by Robert William Blennerhed",
    "",
    "I have suffered from migraine aura since I was 7 years old.",
    "For decades, I have searched for a solution, testing medications,",
    "tracking patterns, and even developing my own software,",
    "since 1994 in Basic, object Pascal, C, C++ and now in Python.",
    "",
    "Now at 67 years old, I am still fighting for an answer.",
    "Like Bill Bixby’s character in The Incredible Hulk,",
    "I am constantly searching for a way to stop the transformation",
    "before the migraine takes control.",
    "",
    "Usage and License:",
    "This program is free to use and develop",
    "as long as the copyright is respected.",
    "All aura images used in this program were",
    "created by me, Robert William Blennerhed.",
    "https://www.rpiforalla.se/"
]

# Statistics-text
statistics_text = [
    "Migraine Statistics since 2013:",
    "- Total migraine attacks: 303",
    "- Average per month: 3.1",
    "- Common triggers: Stress, White light, strong smells",
    "- 60hz screens, Noice, Red vine, Strong cheese,",
    "- Red grapes, Disappointments, Nervousness and more.",
    "- Longest migraine-free period average: 34 days",
    "",
    "The statistics come from My Migraine DB,",
    "developed by Robert W. Blennerhed in the",
    "Memento Database app, from Google Play.",
    "https://www.rpiforalla.se/"
]

# Funktion för att visa textskärmar
def show_text_screen(text_lines):
    link_rects = []  # Lista för att lagra positionsrektanglar för länkar
    screen.fill(BLACK)
    
    y_offset = 50
    line_height = 30
    visible_lines = (screen_height - 100) // line_height  # Antal rader som får plats
    scroll_index = 0  # Startposition för rullning
    
    running = True
    while running:
        screen.fill(BLACK)
        
        link_rects.clear()  # Rensa tidigare länkpositioner
        for i in range(visible_lines):
            text_content = text_lines[scroll_index + i] if scroll_index + i < len(text_lines) else ""
            is_link = text_content.startswith("http")  # Kolla om det är en länk
            if scroll_index + i < len(text_lines):
                text = font.render(text_content, True, RED if is_link else WHITE)
                text_rect = text.get_rect(center=(screen_width // 2, 50 + i * line_height))
            if is_link:
                link_rects.append((text_rect, text_content))
            screen.blit(text, text_rect)
        
        instruction_text = font.render("Use UP/DOWN to scroll, ENTER to return", True, RED)
        instruction_rect = instruction_text.get_rect(center=(screen_width // 2, screen_height - 50))
        screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, link in link_rects:
                    if rect.collidepoint(mouse_pos):
                        webbrowser.open(link)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and scroll_index + visible_lines < len(text_lines):
                    scroll_index += 1
                elif event.key == pygame.K_UP and scroll_index > 0:
                    scroll_index -= 1
                elif event.key == pygame.K_RETURN:
                    running = False
    screen.fill(BLACK)
    pygame.display.flip()
    return
    instruction_text = font.render("Press ENTER to return to the main menu", True, RED)
    instruction_rect = instruction_text.get_rect(center=(screen_width // 2, screen_height - 50))
    screen.blit(instruction_text, instruction_rect)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_setting = 3 if selected_setting == 2 else 2
                elif event.key == pygame.K_UP:
                    selected_setting = 2 if selected_setting == 3 else 3
                elif event.key == pygame.K_RETURN:
                    waiting = False

# Funktion för att köra aura-animationen
def run_aura_animation():
    global screen, settings
    frame_delay = int(settings["frame_delay"])
    scale_step = float(settings["scale_step"])
    global screen
    screen.fill(BLACK)
    
    # Ladda bilder för animation
    image_folder = "images"
    image_paths = [os.path.join(image_folder, f"aura{i}.png") for i in range(1, 4)]
    images = [pygame.image.load(img) for img in image_paths]

    frame_delay = settings["frame_delay"]  # Fördröjning mellan bilderna i millisekunder
    scale_factor = 0.1  # Startstorlek
    scale_step = settings["scale_step"]  # Hur mycket storleken ändras per frame

    warning_text = [
        "WARNING: This simulation may trigger migraines.",
        "You watch at your own risk.",
        "If you feel discomfort, close the window immediately."
    ]
    y_offset = screen_height // 2 - 40
    for line in warning_text:
        text_render = font.render(line, True, RED)
        text_rect = text_render.get_rect(center=(screen_width // 2, y_offset))
        screen.blit(text_render, text_rect)
        y_offset += 40
    pygame.display.flip()
    pygame.time.delay(5000)  # Visa varningen i 5 sekunder
    

    running = True
    image_index = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BLACK)
        img = images[image_index]
        scaled_width = int(img.get_width() * scale_factor)
        scaled_height = int(img.get_height() * scale_factor)
        
        if scaled_width > screen_width * 2 or scaled_height > screen_height * 2:
            running = False  # Avsluta när bilden blivit för stor

        scale_factor += scale_step
        
        img_scaled = pygame.transform.scale(img, (scaled_width, scaled_height))
        img_rect = img_scaled.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(img_scaled, img_rect)
        pygame.display.flip()
        pygame.time.delay(int(frame_delay))
        image_index = (image_index + 1) % len(images)
    
    # Visa slutmeddelande
    screen.fill(BLACK)
    message = [
        "The aura is now over.",
        "But it usually takes 35 minutes to progress.",
        "The migraine headache is coming now."
    ]
    y_offset = screen_height // 2 - 40
    for line in message:
        text_render = font.render(line, True, RED)
        text_rect = text_render.get_rect(center=(screen_width // 2, y_offset))
        screen.blit(text_render, text_rect)
        y_offset += 40
    pygame.display.flip()
    pygame.time.delay(8000)

def adjust_settings():
    global settings
    selected_setting = 2  # Börja med att markera Frame Delay
    global settings
    adjusting = True
    while adjusting:
        screen.fill(BLACK)
        settings_text = [
            "Settings",
            "For Frame Delay adjustment of value, use key 1 and 3.",
            "For Scale Step adjustment of value, use key 2 and 4.",
            f"1. Frame Delay: {settings['frame_delay']} ms (Default: 30.0ms)",
            f"2. Scale Step: {settings['scale_step']:.3f} (Default: 0.045)",
            "Press ENTER to save & return"
        ]
        y_offset = 50
        for index, line in enumerate(settings_text):
            highlight_color = RED if index == selected_setting else WHITE
            color = RED if index in [3, 4] else WHITE
            text = font.render(line, True, color)
            text_rect = text.get_rect(center=(screen_width // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 40
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    save_settings(settings)
                    adjusting = False
                elif event.key == pygame.K_1:
                    settings["frame_delay"] += 10 if settings["frame_delay"] < 500 else 0
                elif event.key == pygame.K_2:
                    settings["scale_step"] += 0.005 if settings["scale_step"] < 0.1 else 0
                elif event.key == pygame.K_3:
                    settings["frame_delay"] -= 10 if settings["frame_delay"] > 10 else 0
                elif event.key == pygame.K_4:
                    settings["scale_step"] -= 0.005 if settings["scale_step"] > 0.01 else 0
    return settings

# Huvudmeny-loop
running = True
while running:
    screen.fill(WHITE)
    title_render = font.render(title_text, True, RED)
    title_rect = title_render.get_rect(center=(screen_width // 2, 50))
    screen.blit(title_render, title_rect)
    
    total_height = len(menu_options) * menu_spacing
    start_y = (screen_height - total_height) // 2
    
    for i, option in enumerate(menu_options):
        color = BLACK if i != selected_option else RED  # Markera vald med röd
        text = font.render(option, True, color)
        text_rect = text.get_rect(center=(screen_width // 2, start_y + i * menu_spacing))
        screen.blit(text, text_rect)
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:
                    show_text_screen(about_text)
                elif selected_option == 1:
                    run_aura_animation()
                elif selected_option == 2:
                    show_text_screen(statistics_text)
                elif selected_option == 3:
                    settings = adjust_settings()
                elif selected_option == 4:
                    running = False

pygame.quit()
