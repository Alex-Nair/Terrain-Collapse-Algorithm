import json
import os
import pygame

# --------------------------------------------------
# Configuration
# --------------------------------------------------

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TILE_SIZE = 200
GRID_LINE_WIDTH = 1

CAMERA_SPEED = 15

INFO_PANEL_HEIGHT = 80

# --------------------------------------------------
# Utility Functions
# --------------------------------------------------

def get_text_colour(rgb):
    """
    Returns black or white depending on
    background brightness.
    """

    brightness = (
        rgb[0] * 0.299 +
        rgb[1] * 0.587 +
        rgb[2] * 0.114
    )

    return (0, 0, 0) if brightness > 186 else (255, 255, 255)


def draw_text_fit(
    surface,
    text,
    rect,
    colour
):
    """
    Draws text centred inside rect.
    Shrinks font size until it fits.
    """

    font_size = 32

    while font_size >= 10:

        font = pygame.font.SysFont(
            None,
            font_size
        )

        rendered = font.render(
            text,
            True,
            colour
        )

        if (
            rendered.get_width() <= rect.width - 10
            and
            rendered.get_height() <= rect.height - 10
        ):
            break

        font_size -= 1

    text_rect = rendered.get_rect(
        center=rect.center
    )

    surface.blit(
        rendered,
        text_rect
    )

# --------------------------------------------------
# Load Map
# --------------------------------------------------

if not os.path.exists("map.json"):
    print("map.json not found.")
    raise SystemExit

with open(
    "map.json",
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)

map_size = data["size"]
map_tiles = data["tiles"]

# --------------------------------------------------
# Pygame Setup
# --------------------------------------------------

pygame.init()

screen = pygame.display.set_mode(
    (
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )
)

pygame.display.set_caption(
    "Map Viewer"
)

clock = pygame.time.Clock()

# --------------------------------------------------
# Camera Setup
# --------------------------------------------------

map_pixel_size = map_size * TILE_SIZE

camera_x = (
    map_pixel_size / 2
    -
    SCREEN_WIDTH / 2
)

camera_y = (
    map_pixel_size / 2
    -
    (SCREEN_HEIGHT - INFO_PANEL_HEIGHT) / 2
)

selected_tile = None

# --------------------------------------------------
# Main Loop
# --------------------------------------------------

running = True

while running:

    dt = clock.tick(60)

    # --------------------------
    # Input
    # --------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos

            if mouse_y < SCREEN_HEIGHT - INFO_PANEL_HEIGHT:

                world_x = mouse_x + camera_x
                world_y = mouse_y + camera_y

                tile_x = int(
                    world_x // TILE_SIZE
                )

                tile_y = int(
                    world_y // TILE_SIZE
                )

                if (
                    0 <= tile_x < map_size
                    and
                    0 <= tile_y < map_size
                ):

                    tile = map_tiles[tile_y][tile_x]

                    selected_tile = {
                        "x": tile_x,
                        "y": tile_y,
                        "name": tile[0]
                    }

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        camera_y -= CAMERA_SPEED

    if keys[pygame.K_s]:
        camera_y += CAMERA_SPEED

    if keys[pygame.K_a]:
        camera_x -= CAMERA_SPEED

    if keys[pygame.K_d]:
        camera_x += CAMERA_SPEED

    # --------------------------
    # Drawing
    # --------------------------

    screen.fill((40, 40, 40))

    visible_start_x = max(
        0,
        int(camera_x // TILE_SIZE)
    )

    visible_start_y = max(
        0,
        int(camera_y // TILE_SIZE)
    )

    visible_end_x = min(
        map_size,
        int(
            (camera_x + SCREEN_WIDTH)
            // TILE_SIZE
        ) + 2
    )

    visible_end_y = min(
        map_size,
        int(
            (
                camera_y
                +
                SCREEN_HEIGHT
            )
            // TILE_SIZE
        ) + 2
    )

    for y in range(
        visible_start_y,
        visible_end_y
    ):

        for x in range(
            visible_start_x,
            visible_end_x
        ):

            tile = map_tiles[y][x]

            name = tile[0]
            colour = tile[1]

            screen_x = (
                x * TILE_SIZE
                -
                camera_x
            )

            screen_y = (
                y * TILE_SIZE
                -
                camera_y
            )

            rect = pygame.Rect(
                screen_x,
                screen_y,
                TILE_SIZE,
                TILE_SIZE
            )

            pygame.draw.rect(
                screen,
                colour,
                rect
            )

            pygame.draw.rect(
                screen,
                (0, 0, 0),
                rect,
                GRID_LINE_WIDTH
            )

            draw_text_fit(
                screen,
                name,
                rect,
                get_text_colour(colour)
            )

    # --------------------------
    # Information Panel
    # --------------------------

    panel_rect = pygame.Rect(
        0,
        SCREEN_HEIGHT
        -
        INFO_PANEL_HEIGHT,
        SCREEN_WIDTH,
        INFO_PANEL_HEIGHT
    )

    pygame.draw.rect(
        screen,
        (20, 20, 20),
        panel_rect
    )

    pygame.draw.line(
        screen,
        (100, 100, 100),
        (
            0,
            SCREEN_HEIGHT
            -
            INFO_PANEL_HEIGHT
        ),
        (
            SCREEN_WIDTH,
            SCREEN_HEIGHT
            -
            INFO_PANEL_HEIGHT
        )
    )

    info_font = pygame.font.SysFont(
        None,
        32
    )

    if selected_tile:

        text = (
            f"Tile: {selected_tile['name']} | "
            f"X: {selected_tile['x']} | "
            f"Y: {selected_tile['y']}"
        )

    else:

        text = (
            "Click a tile for information."
        )

    rendered = info_font.render(
        text,
        True,
        (255, 255, 255)
    )

    screen.blit(
        rendered,
        (
            15,
            SCREEN_HEIGHT
            -
            INFO_PANEL_HEIGHT
            +
            25
        )
    )

    pygame.display.flip()

pygame.quit()