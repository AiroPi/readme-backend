from connect4 import Connect4
from PIL import Image, ImageDraw

TOKEN_DIAMETER = 35
INTERSPACE = 5

BG_COLOR = (100, 100, 255)
TOKENS_COLORS = ((255, 255, 255), (255, 100, 100), (255, 255, 100))


def generate_image(connect4: Connect4, filename: str):
    im = Image.new('RGB', (7 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE, 6 * (TOKEN_DIAMETER + INTERSPACE) + INTERSPACE), BG_COLOR)

    draw = ImageDraw.Draw(im)

    for i in range(6):
        for j in range(7):
            case = connect4.board[i][j]
            xy = (INTERSPACE + j * (TOKEN_DIAMETER + INTERSPACE),
                  INTERSPACE + i * (TOKEN_DIAMETER + INTERSPACE),
                  INTERSPACE + j * (TOKEN_DIAMETER + INTERSPACE) + TOKEN_DIAMETER,
                  INTERSPACE + i * (TOKEN_DIAMETER + INTERSPACE) + TOKEN_DIAMETER)
            draw.ellipse(xy, fill=TOKENS_COLORS[case])

    im.save(filename)
