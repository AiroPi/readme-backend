import minesweeper
from fastapi import APIRouter

from utils import RESOURCES_PATH, load_image, png_response, redirect_to_readme

BASE_PATH = RESOURCES_PATH / "images" / "minesweeper"
SIZE = (10, 12)
BOMBS = 20

router = APIRouter(prefix="/ms")
game = minesweeper.Minesweeper(SIZE, BOMBS)
flag_mode = False


RED_MINE = load_image(BASE_PATH / "mine_red.png")
MINE = load_image(BASE_PATH / "mine.png")
FLAG = load_image(BASE_PATH / "flag.png")
DEACTIVATED_FLAG = load_image(BASE_PATH / "deactivated_flag.png")
CLOSED = load_image(BASE_PATH / "closed.png")
FACE = load_image(BASE_PATH / "face.png")
FACE_LOSE = load_image(BASE_PATH / "face_lose.png")

DIGITS = {i: load_image(BASE_PATH / f"{i}.png") for i in range(9)}


@router.get("/img/{i}/{j}")
def get_board_img(i: int, j: int):
    if (i, j) in game.revealed:
        if game.board[i][j] == -1:
            return png_response(RED_MINE)
        return png_response(DIGITS[game.board[i][j]])
    if game.game_over and game.board[i][j] == -1:
        return png_response(MINE)
    if (i, j) in game.flags:
        return png_response(FLAG)
    return png_response(CLOSED)


@router.get("/img/{text}")
def get_img(text: str):
    match text:
        case "flag-toggle":
            if flag_mode:
                return png_response(FLAG)
            else:
                return png_response(DEACTIVATED_FLAG)
        case "face":
            if game.game_over:
                return png_response(FACE_LOSE)
            else:
                return png_response(FACE)
        case _:
            return 404


@router.get("/play/{i}/{j}")
def play(i: int, j: int):
    if game.game_over:
        return redirect_to_readme("#minesweeper")

    if flag_mode:
        game.toggle_flag(i, j)
    else:
        if (i, j) not in game.flags:
            game.play(i, j)
    return redirect_to_readme("#minesweeper")


@router.get("/toggle-flag")
def flag_toggle():
    global flag_mode
    flag_mode = not flag_mode
    return redirect_to_readme("#minesweeper")


@router.get("/reset")
def reset():
    global game
    game = minesweeper.Minesweeper(SIZE, BOMBS)
    return redirect_to_readme("#minesweeper")


@router.get("/undo")
def undo():
    # TODO: Implement undo
    return redirect_to_readme("#minesweeper")
