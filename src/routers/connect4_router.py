import os
from functools import partial
from pathlib import Path
from time import time

from connect4 import ColumnFull, Connect4, Players
from fastapi import APIRouter, Query
from fastapi.responses import FileResponse, RedirectResponse
from PIL import Image, ImageDraw, ImageFont

GITHUB_PROFILE_URL = os.environ["GITHUB_PROFILE_URL"]

TOKEN_DIAMETER = 70
INTERSPACE = 10
BOX_HEIGHT = 140
BOX_BORDER = 10

FONT_SIZE = 40

BG_COLOR = (100, 100, 255)
BOX_COLOR = (70, 70, 255)
TOKENS_COLORS = ((255, 255, 255), (255, 100, 100), (255, 255, 100))
HIGHLIGHT_WIN_COLOR = (100, 255, 100)

IMAGE_PATH = Path("./data/connect4.png")

font = ImageFont.truetype("./resources/fonts/Roboto-Regular.ttf", FONT_SIZE)


def generate_image(connect4: Connect4, path: Path):
    im = Image.new(
        "RGB",
        (
            7 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE,
            6 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE + BOX_HEIGHT,
        ),
        BG_COLOR,
    )

    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle(
        (
            BOX_BORDER,
            6 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE + BOX_BORDER,
            7 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE - BOX_BORDER,
            6 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE + BOX_HEIGHT - BOX_BORDER,
        ),
        7,
        fill=BOX_COLOR,
    )

    if connect4.is_over:
        if connect4.winner == Players.NONE:
            msg = "It's a tie!"
        else:
            msg = f"Winner : {'red' if connect4.turn == Players.ONE else 'yellow'}"
    else:
        msg = f"Player turn : {'red' if connect4.turn == Players.ONE else 'yellow'}"

    draw.textbbox(
        (
            (7 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE) / 2,
            6 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE + (BOX_HEIGHT) / 2,
        ),
        msg,
        align="center",
        font=font,
    )

    for i in range(6):
        for j in range(7):
            case = connect4.board[i][j]
            if (i, j) in connect4._win_points:  # pyright: ignore[reportPrivateUsage]
                xy = (
                    INTERSPACE + j * (TOKEN_DIAMETER + INTERSPACE) - INTERSPACE / 2,
                    INTERSPACE + i * (TOKEN_DIAMETER + INTERSPACE) - INTERSPACE / 2,
                    INTERSPACE + j * (TOKEN_DIAMETER + INTERSPACE) + TOKEN_DIAMETER + INTERSPACE / 2,
                    INTERSPACE + i * (TOKEN_DIAMETER + INTERSPACE) + TOKEN_DIAMETER + INTERSPACE / 2,
                )
                draw.ellipse(xy, fill=HIGHLIGHT_WIN_COLOR)

            xy = (
                INTERSPACE + j * (TOKEN_DIAMETER + INTERSPACE),
                INTERSPACE + i * (TOKEN_DIAMETER + INTERSPACE),
                INTERSPACE + j * (TOKEN_DIAMETER + INTERSPACE) + TOKEN_DIAMETER,
                INTERSPACE + i * (TOKEN_DIAMETER + INTERSPACE) + TOKEN_DIAMETER,
            )
            draw.ellipse(xy, fill=TOKENS_COLORS[case.value])

    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


last_play_time = time()
c4 = Connect4()
router = APIRouter(prefix="/connect4", on_startup=[partial(generate_image, c4, IMAGE_PATH)])


@router.get("/image")
def get_image():
    return FileResponse("./data/connect4.png", headers={"Cache-Control": "no-cache, max-age=0"})


@router.get("/play")
def play(column: int = Query(title="The column ID you want to play to.", ge=0, le=6)):
    global last_play_time

    if not c4.is_over:
        try:
            c4.play(column)
        except ColumnFull:
            pass
        else:
            generate_image(c4, IMAGE_PATH)
            last_play_time = time()
    return RedirectResponse(GITHUB_PROFILE_URL)


@router.get("/reset")
def reset():
    if not c4.is_over and time() - last_play_time < 300:
        return RedirectResponse(GITHUB_PROFILE_URL)

    c4.reset()
    generate_image(c4, IMAGE_PATH)
    return RedirectResponse(GITHUB_PROFILE_URL)
