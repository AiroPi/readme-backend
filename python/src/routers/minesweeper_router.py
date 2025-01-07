import os
from pathlib import Path

import minesweeper
from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse

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


def get_header():
    return {
        "Cache-Control": "no-cache, max-age=0",
        # "Last-Modified": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
        # "ETag": etag,
    }


def response_img(img: bytes):
    """
    Maybe some optimisations could be done here.
    I'm pretty sure that the request *could* be cached but without being cached.
    Like -> if the content didn't change, don't send it again, otherwise send it.
    Also, the tiles are "shared" between the image, so maybe there is a way for the browser to reuse the same image.
    I don't want to dig more into this, but it's a thought.
    """
    # etag = hashlib.md5(img).hexdigest()
    return Response(img, media_type="image/png", headers=get_header())


def redirect_to_github():
    return RedirectResponse(f"{GITHUB_PROFILE_URL}#minesweeper")


@router.get("/img/{i}/{j}")
def get_board_img(i: int, j: int):
    if (i, j) in game.revealed:
        if game.board[i][j] == -1:
            return response_img(RED_MINE)
        return response_img(DIGITS[game.board[i][j]])
    if game.game_over and game.board[i][j] == -1:
        return response_img(MINE)
    if (i, j) in game.flags:
        return response_img(FLAG)
    return response_img(CLOSED)


@router.get("/img/{text}")
def get_img(text: str):
    match text:
        case "flag-toggle":
            if flag_mode:
                return response_img(FLAG)
            else:
                return response_img(DEACTIVATED_FLAG)
        case "header":
            return response_img(HEADER)
        case "undo":
            return response_img(UNDO)
        case "face":
            if game.game_over:
                return response_img(FACE_LOSE)
            else:
                return response_img(FACE)
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
