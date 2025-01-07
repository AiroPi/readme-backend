import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    prog="readme-generator", description="Generate the README.md file"
)

parser.add_argument("base_url")
parser.add_argument("--template", default="./templates/README.md")
parser.add_argument("--output", default="./README.out.md")
args = parser.parse_args()

BASE_URL = args.base_url[:-1] if args.base_url.endswith("/") else args.base_url
TEMPLATE = Path("./templates/README.md")
OUTPUT = Path(args.output)


def generate_minesweeper_markdown() -> str:
    markdown: list[list[str]] = [
        [
            f'[<img height="50px" src="{BASE_URL}/ms/img/flag-toggle"/>]({BASE_URL}/ms/toggle-flag)',
            f'<img height="50px" width="75px" src="{BASE_URL}/ms/img/header"/>',
            f'[<img height="50px" src="{BASE_URL}/ms/img/face"/>]({BASE_URL}/ms/reset)',
            f'<img height="50px" width="75px" src="{BASE_URL}/ms/img/header"/>',
            f'[<img height="50px" src="{BASE_URL}/ms/img/undo"/>]({BASE_URL}/ms/undo)',
        ]
    ]
    for i in range(10):
        row: list[str] = [
            f'[<img width="25px" src="{BASE_URL}/ms/img/{i}/{j}"/>]({BASE_URL}/ms/play/{i}/{j})'
            for j in range(12)
        ]
        markdown.append(row)

    return "  \n".join("".join(row) for row in markdown)


def generate_connect4_markdown() -> str:
    button = f'<img src="{BASE_URL}/static/connect4/button.png" width="40px"/>'
    margin = f'<img src="{BASE_URL}/static/connect4/margin.png" width="2.5px"/>'

    markdown = [
        [
            margin,
            *[f"[{button}]({BASE_URL}/connect4/play?column={i})" for i in range(7)],
            margin,
        ],
        [f'<img src="{BASE_URL}/connect4/image" width="285px"/>'],
    ]

    return "  \n".join("".join(row) for row in markdown)


#     &nbsp;[1️⃣](https://readme.airopi.dev/connect4/play?column=0)&nbsp;&nbsp;&nbsp;
# [2️⃣](https://readme.airopi.dev/connect4/play?column=1)&nbsp;&nbsp;&nbsp;
# [3️⃣](https://readme.airopi.dev/connect4/play?column=2)&nbsp;&nbsp;&nbsp;
# [4️⃣](https://readme.airopi.dev/connect4/play?column=3)&nbsp;&nbsp;&nbsp;
# [5️⃣](https://readme.airopi.dev/connect4/play?column=4)&nbsp;&nbsp;&nbsp;
# [6️⃣](https://readme.airopi.dev/connect4/play?column=5)&nbsp;&nbsp;&nbsp;
# [7️⃣](https://readme.airopi.dev/connect4/play?column=6)

# <img src="https://readme.airopi.dev/connect4/image" width="240"/>

# Restart : [🔄](https://readme.airopi.dev/connect4/reset)


def main():
    with TEMPLATE.open() as f:
        template = f.read()

    template = template.replace("{{MINESWEEPER}}", generate_minesweeper_markdown())
    template = template.replace("{{CONNECT4}}", generate_connect4_markdown())

    with OUTPUT.open("w") as f:
        f.write(template)


if __name__ == "__main__":
    main()
