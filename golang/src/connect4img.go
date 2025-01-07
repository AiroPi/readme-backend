package main

import (
	"image/color"
	"log"

	"git.sr.ht/~sbinet/gg"
	"golang.org/x/image/font"

	"C"
)

const TOKEN_DIAMETER int = 70
const INTERSPACE int = 10
const BOX_HEIGHT int = 140
const BOX_BORDER int = 10

const FONT_SIZE int = 40

var BG_COLOR = color.RGBA{100, 100, 255, 255}
var BOX_COLOR = color.RGBA{70, 70, 255, 255}
var TOKENS_COLORS = []color.RGBA{
	{255, 255, 255, 255},
	{255, 100, 100, 255},
	{255, 255, 100, 255},
}
var HIGHLIGHT_WIN_COLOR = color.RGBA{100, 255, 100, 255}

var FACE font.Face

func init() {
	var err error
	FACE, err = gg.LoadFontFace("./resources/fonts/Roboto-Regular.ttf", float64(FONT_SIZE))
	if err != nil {
		log.Fatalf("could not load font face: %+v", err)
	}
}

//export GenerateBoard
func GenerateBoard(board [][]int, isOver bool, winner int, turn int, winPositions [][]int) {
	log.Print(winPositions)
	const width = 7*(TOKEN_DIAMETER+INTERSPACE) + INTERSPACE
	const heigh = 6*(TOKEN_DIAMETER+INTERSPACE) + INTERSPACE + BOX_HEIGHT
	dc := gg.NewContext(
		width, heigh,
	)
	dc.SetColor(BG_COLOR)
	dc.DrawRectangle(0, 0, float64(width), float64(heigh))
	dc.Fill()

	// Draw message
	var msg string
	if isOver {
		if winner == 0 {
			msg = "It's a tie!"
		} else {
			if turn == 1 {
				msg = "Winner : red"
			} else {
				msg = "Winner : yellow"
			}
		}
	} else {
		if turn == 1 {
			msg = "Player turn : red"
		} else {
			msg = "Player turn : yellow"
		}
	}

	dc.SetColor(color.Black)
	dc.SetFontFace(FACE)
	dc.DrawStringAnchored(
		msg,
		float64((7*(TOKEN_DIAMETER+INTERSPACE)+INTERSPACE)/2),
		float64(6*(TOKEN_DIAMETER+INTERSPACE)+INTERSPACE+(BOX_HEIGHT)/2),
		0.5,
		0.5,
	)

	// Draw tokens
	for i := 0; i < 6; i++ {
		for j := 0; j < 7; j++ {
			caseVal := board[i][j]
			x := float64(INTERSPACE + j*(TOKEN_DIAMETER+INTERSPACE))
			y := float64(INTERSPACE + i*(TOKEN_DIAMETER+INTERSPACE))

			if contains(winPositions, [2]int{i, j}) {
				log.Println(true)
				dc.SetColor(HIGHLIGHT_WIN_COLOR)
				dc.DrawCircle(x+float64(TOKEN_DIAMETER)/2, y+float64(TOKEN_DIAMETER)/2, float64(TOKEN_DIAMETER)/2+float64(INTERSPACE)/2)
				dc.Fill()
			}

			dc.SetColor(TOKENS_COLORS[caseVal])
			dc.DrawCircle(x+float64(TOKEN_DIAMETER)/2, y+float64(TOKEN_DIAMETER)/2, float64(TOKEN_DIAMETER)/2)
			dc.Fill()
		}
	}

	err := dc.SavePNG("./data/connect4.png") // TODO
	if err != nil {
		log.Fatalf("could not save to file: %+v", err)
	}
}

func contains(points [][]int, point [2]int) bool {
	for _, p := range points {
		if [2]int(p) == point {
			return true
		}
	}
	return false
}

func main() {}
