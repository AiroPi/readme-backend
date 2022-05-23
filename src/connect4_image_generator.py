from connect4 import Connect4
from PIL import Image, ImageDraw, ImageFont

TOKEN_DIAMETER = 70
INTERSPACE = 10
BOX_HEIGHT = 140
BOX_BORDER = 10

FONT_SIZE = 40

BG_COLOR = (100, 100, 255)
BOX_COLOR = (70, 70, 255)
TOKENS_COLORS = ((255, 255, 255), (255, 100, 100), (255, 255, 100))
HIGHLIGHT_WIN_COLOR = (100, 255, 100)

font = ImageFont.truetype("./resources/fonts/Roboto-Regular.ttf", FONT_SIZE)


def generate_image(connect4: Connect4, filename: str):
    im = Image.new('RGB', (7 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE,
                           6 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE + BOX_HEIGHT), BG_COLOR)

    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((BOX_BORDER,
                            6 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE + BOX_BORDER,
                            7 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE - BOX_BORDER,
                            6 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE + BOX_HEIGHT - BOX_BORDER),
                           7, fill=BOX_COLOR)

    if connect4.is_over:
        msg = f"Winner : {'red' if connect4.get_turn() == 1 else 'yellow'}"
    else:
        msg = f"Player turn : {'red' if connect4.get_turn() == 1 else 'yellow'}"

    w, h = draw.textsize(msg, font=font)

    draw.text(((7 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE - w) / 2,
               6 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE + (BOX_HEIGHT - h) / 2),
              msg, align='center', font=font)

    for i in range(6):
        for j in range(7):
            case = connect4.board[i][j]
            if (i, j) in connect4._win_points:
                xy = (INTERSPACE + j * (TOKEN_DIAMETER + INTERSPACE) - INTERSPACE / 2,
                      INTERSPACE + i * (TOKEN_DIAMETER + INTERSPACE) - INTERSPACE / 2,
                      INTERSPACE + j * (TOKEN_DIAMETER + INTERSPACE) + TOKEN_DIAMETER + INTERSPACE / 2,
                      INTERSPACE + i * (TOKEN_DIAMETER + INTERSPACE) + TOKEN_DIAMETER + INTERSPACE / 2)
                draw.ellipse(xy, fill=HIGHLIGHT_WIN_COLOR)

            xy = (INTERSPACE + j * (TOKEN_DIAMETER + INTERSPACE),
                  INTERSPACE + i * (TOKEN_DIAMETER + INTERSPACE),
                  INTERSPACE + j * (TOKEN_DIAMETER + INTERSPACE) + TOKEN_DIAMETER,
                  INTERSPACE + i * (TOKEN_DIAMETER + INTERSPACE) + TOKEN_DIAMETER)
            draw.ellipse(xy, fill=TOKENS_COLORS[case])

    im.save(filename)
