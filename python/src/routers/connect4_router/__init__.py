from functools import partial
from pathlib import Path
from time import time

from connect4 import ColumnFull, Connect4
from fastapi import APIRouter, Query

from utils import RESOURCES_PATH, file_response, load_image, png_response, redirect_to_readme

from .go_library import generate_board

GENERATED_BOARD_PATH = Path("./data/connect4.png")
DYNAMIC_IMAGES_PATH = RESOURCES_PATH / "images" / "connect4"

DISABLED_RESTART = load_image(DYNAMIC_IMAGES_PATH / "restart_disabled.png")
RESTART = load_image(DYNAMIC_IMAGES_PATH / "restart.png")

last_play_time = time()
c4 = Connect4()
router = APIRouter(prefix="/connect4", on_startup=[partial(generate_board, c4)])


@router.get("/img/{target}")
def get_image(target: str):
    match target:
        case "board":
            return file_response(GENERATED_BOARD_PATH)
        case "restart":
            if not c4.is_over and time() - last_play_time < 10:
                return png_response(DISABLED_RESTART)
            return png_response(RESTART)
        case _:
            return redirect_to_readme("#connect4")


@router.get("/play")
def play(column: int = Query(title="The column ID you want to play to.", ge=0, le=6)):
    global last_play_time

    if not c4.is_over:
        try:
            c4.play(column)
        except ColumnFull:
            pass
        else:
            generate_board(c4)
            last_play_time = time()
    return redirect_to_readme("#connect4")


@router.get("/restart")
def reset():
    if not c4.is_over and time() - last_play_time < 300:
        return redirect_to_readme("#connect4")

    c4.reset()
    generate_board(c4)
    return redirect_to_readme("#connect4")
