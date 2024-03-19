BASE_URL = "http://localhost/ms"

markdown: list[list[str]] = [
    [
        f'[<img height="50px" src="{BASE_URL}/img/flag-toggle"/>]({BASE_URL}/toggle-flag)',
        f'<img height="50px" width="75px" src="{BASE_URL}/img/header"/>',
        f'[<img height="50px" src="{BASE_URL}/img/face"/>]({BASE_URL}/reset)',
        f'<img height="50px" width="75px" src="{BASE_URL}/img/header"/>',
        f'[<img height="50px" src="{BASE_URL}/img/undo"/>]({BASE_URL}/undo)',
    ]
]
for i in range(10):
    row: list[str] = [f'[<img width="25px" src="{BASE_URL}/img/{i}/{j}"/>]({BASE_URL}/play/{i}/{j})' for j in range(12)]
    markdown.append(row)

with open("./minesweeper.md", "w") as f:
    f.write("  \n".join("".join(row) for row in markdown))
