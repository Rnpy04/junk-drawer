import pygame
from datetime import datetime
import sys 

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Set the font and color for the calendar widget
font = pygame.font.SysFont(None, 32)
black = (0, 0, 0)
white = (255, 255, 255)

# Get the current date
current_date = datetime.today()

# Create a calendar widget
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the calendar widget with the current date
    screen.fill(white)
    text = font.render_to(screen, (20, 20), f"{current_date.day} {current_date.strftime('%B')}",black )
    pygame.display.flip()
    clock.tick(60)
