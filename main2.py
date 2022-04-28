
from random import sample
import time
from bundled.game_messages import MessageLog
from bundled.item_loader import ascii_loader, make_item, place_item
from entity import Entity
from fov_functions import initialize_fov
from game_states import GameStates
from map_objects.game_map import GameMap
from unit_components.ai import BasicMerchant, Wander
from unit_components.inventory import Inventory
import tcod as libtcod
import tcod.render
import tcod.sdl.render



import copy
import math
import os
import random
import sys
import time
import warnings
from typing import Any, List

import numpy as np
import tcod
import tcod.render
import tcod.sdl.render
from numpy.typing import NDArray



WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
LIGHT_BLUE = (63, 63, 255)
LIGHT_YELLOW = (255, 255, 63)

SAMPLE_SCREEN_WIDTH = 46
SAMPLE_SCREEN_HEIGHT = 20
SAMPLE_SCREEN_X = 20
SAMPLE_SCREEN_Y = 10
FONT = "drd15x15.png"

# Mutable global names.
context: tcod.context.Context
tileset: tcod.tileset.Tileset
console_render: tcod.render.SDLConsoleRender  # Optional SDL renderer.
sample_minimap: tcod.sdl.render.Texture  # Optional minimap texture.
root_console = tcod.Console(80, 50, order="F")
sample_console = tcod.console.Console(SAMPLE_SCREEN_WIDTH, SAMPLE_SCREEN_HEIGHT, order="F")
cur_sample = 0  # Current selected sample.
frame_times = [time.perf_counter()]
frame_length = [0.0]



def init_context(renderer: int) -> None:
    """Setup or reset a global context with common parameters set.

    This function exists to more easily switch between renderers.
    """
    global context, console_render, sample_minimap
    if "context" in globals():
        context.close()
    libtcod_version = "%i.%i.%i" % (
        tcod.lib.TCOD_MAJOR_VERSION,
        tcod.lib.TCOD_MINOR_VERSION,
        tcod.lib.TCOD_PATCHLEVEL,
    )
    context = tcod.context.new(
        columns=root_console.width,
        rows=root_console.height,
        title=f"python-tcod samples" f" (python-tcod {tcod.__version__}, libtcod {libtcod_version})",
        renderer=renderer,
        vsync=False,  # VSync turned off since this is for benchmarking.
        tileset=tileset,
    )
    if context.sdl_renderer:  # If this context supports SDL rendering.
        # Start by setting the logical size so that window resizing doesn't break anything.
        context.sdl_renderer.logical_size = (
            tileset.tile_width * root_console.width,
            tileset.tile_height * root_console.height,
        )
        assert context.sdl_atlas
        # Generate the console renderer and minimap.
        console_render = tcod.render.SDLConsoleRender(context.sdl_atlas)
        sample_minimap = context.sdl_renderer.new_texture(
            SAMPLE_SCREEN_WIDTH,
            SAMPLE_SCREEN_HEIGHT,
            format=tcod.lib.SDL_PIXELFORMAT_RGB24,
            access=tcod.sdl.render.TextureAccess.STREAMING,  # Updated every frame.
        )



def main() -> None:
    global context, tileset
    tileset = tcod.tileset.load_tilesheet(FONT, 32, 8, tcod.tileset.CHARMAP_TCOD)
    init_context(tcod.RENDERER_SDL2)
    try:
        #SAMPLES[cur_sample].on_enter()

        while True:
            root_console.clear()
            #draw_samples_menu()
            #draw_renderer_menu()

            # render the sample
            #SAMPLES[cur_sample].on_draw()
            sample_console.blit(root_console, SAMPLE_SCREEN_X, SAMPLE_SCREEN_Y)
            #draw_stats()
            if context.sdl_renderer:
                # SDL renderer support, upload the sample console background to a minimap texture.
                sample_minimap.update(sample_console.rgb.T["bg"])
                # Render the root_console normally, this is the drawing step of context.present without presenting.
                context.sdl_renderer.copy(console_render.render(root_console))
                # Render the minimap to the screen.
                context.sdl_renderer.copy(
                    sample_minimap,
                    dest=(
                        tileset.tile_width * 24,
                        tileset.tile_height * 36,
                        SAMPLE_SCREEN_WIDTH * 3,
                        SAMPLE_SCREEN_HEIGHT * 3,
                    ),
                )
                context.sdl_renderer.present()
            else:  # No SDL renderer, just use plain context rendering.
                context.present(root_console)

            #handle_time()
            #handle_events()
    finally:
        # Normally context would be used in a with block and closed
        # automatically. but since this context might be switched to one with a
        # different renderer it is closed manually here.
        context.close()















if __name__ == "__main__":
    main()





