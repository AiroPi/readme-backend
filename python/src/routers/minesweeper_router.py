import hashlib
import os
from datetime import datetime
from pathlib import Path

import minesweeper
from fastapi import APIRouter, Response
from fastapi.responses import FileResponse, RedirectResponse

GITHUB_PROFILE_URL = os.environ["GITHUB_PROFILE_URL"]
BASE_PATH = Path("./resources/images/minesweeper/png/")
SIZE = (10, 12)
BOMBS = 20

router = APIRouter(prefix="/ms")
game = minesweeper.Minesweeper(SIZE, BOMBS)
flag_mode = False


def load_image(path: Path):
    with path.open("rb") as f:
        return f.read()


RED_MINE = load_image(BASE_PATH / "mine_red.png")
MINE = load_image(BASE_PATH / "mine.png")
FLAG = load_image(BASE_PATH / "flag.png")
DEACTIVATED_FLAG = load_image(BASE_PATH / "deactivated_flag.png")
CLOSED = load_image(BASE_PATH / "closed.png")
HEADER = load_image(BASE_PATH / "header.png")
UNDO = load_image(BASE_PATH / "undo.png")
FACE = load_image(BASE_PATH / "face.png")
FACE_LOSE = load_image(BASE_PATH / "face_lose.png")

DIGITS = {i: load_image(BASE_PATH / f"{i}.png") for i in range(9)}


def get_header(etag: str = ""):
    return {
        "Cache-Control": "no-cache, max-age=0",
        # "Last-Modified": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "ETag": etag,
    }


def response_img(img: str):
    return RedirectResponse(f"/static/ms/{img}.png")
    # return Response("abc")
    etag = hashlib.md5(img).hexdigest()  # noqa: S324

    return Response(img, media_type="image/png", headers=get_header(etag))


def redirect_to_github():
    return RedirectResponse(GITHUB_PROFILE_URL)


@router.get("/img/{i}/{j}")
def get_board_img(i: int, j: int):
    if (i, j) in game.revealed:
        if game.board[i][j] == -1:
            return response_img("mine_red")
        return response_img(str(game.board[i][j]))
    if game.game_over and game.board[i][j] == -1:
        return response_img("mine")
    if (i, j) in game.flags:
        return response_img("flag")
    return response_img("closed")


@router.get("/img/{text}")
def get_img(text: str):
    match text:
        case "flag-toggle":
            if flag_mode:
                return response_img("flag.png")
            else:
                return response_img("deactivated_flag.png")
        case "header":
            return response_img("header.png")
        case "undo":
            return response_img("undo.png")
        case "face":
            if game.game_over:
                return response_img("face_lose.png")
            else:
                return response_img("face.png")
        case _:
            return 404


@router.get("/play/{i}/{j}")
def play(i: int, j: int):
    if game.game_over:
        return redirect_to_github()

    if flag_mode:
        game.toggle_flag(i, j)
    else:
        if (i, j) not in game.flags:
            game.play(i, j)
    return redirect_to_github()


@router.get("/toggle-flag")
def flag_toggle():
    global flag_mode
    flag_mode = not flag_mode
    return redirect_to_github()


@router.get("/reset")
def reset():
    global game
    game = minesweeper.Minesweeper(SIZE, BOMBS)
    return redirect_to_github()


@router.get("/undo")
def undo():
    # TODO: Implement undo
    return redirect_to_github()
