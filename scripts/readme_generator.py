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
            '[<img height="50px" src="{{ BASE_URL }}/ms/img/flag-toggle"/>]({{ BASE_URL }}/ms/toggle-flag)',
            '<img height="50px" width="75px" src="{{ BASE_URL }}/static/ms/header.png"/>',
            '[<img height="50px" src="{{ BASE_URL }}/ms/img/face"/>]({{ BASE_URL }}/ms/reset)',
            '<img height="50px" width="75px" src="{{ BASE_URL }}/static/ms/header.png"/>',
            '<img height="50px" src="{{ BASE_URL }}/static/ms/undo.png"/>',
        ]
    ]
    for i in range(10):
        row: list[str] = [
            f'[<img width="25px" src="{{{{ BASE_URL }}}}/ms/img/{i}/{j}"/>]({{{{ BASE_URL }}}}/ms/play/{i}/{j})'
            for j in range(12)
        ]
        markdown.append(row)

    return "  \n".join("".join(row) for row in markdown)


def generate_connect4_markdown() -> str:
    button = '<img src="{{ BASE_URL }}/static/connect4/button.png" width="40px"/>'
    margin = '<img src="{{ BASE_URL }}/static/connect4/margin.png" width="2.5px"/>'

    markdown = [
        [
            margin,
            *[
                f"[{button}]({{{{ BASE_URL }}}}/connect4/play?column={i})"
                for i in range(7)
            ],
            margin,
        ],
        ['<img src="{{ BASE_URL }}/connect4/img/board" width="285px"/>'],
        [
            '[<img src="{{ BASE_URL }}/connect4/img/restart" width="285px"/>]({{ BASE_URL }}/connect4/restart)'
        ],
    ]

    return "  \n".join("".join(row) for row in markdown)


def main():
    with TEMPLATE.open() as f:
        template = f.read()

    template = template.replace("{{ MINESWEEPER }}", generate_minesweeper_markdown())
    template = template.replace("{{ CONNECT4 }}", generate_connect4_markdown())

    template = template.replace("{{ BASE_URL }}", BASE_URL)

    with OUTPUT.open("w") as f:
        f.write(template)


if __name__ == "__main__":
    main()
