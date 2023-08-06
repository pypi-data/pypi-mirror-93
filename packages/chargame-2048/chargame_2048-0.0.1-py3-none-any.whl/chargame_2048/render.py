from util import padCenter
from logic import EMPTY, NUM

# ┌ ─ ┐
# │ ┼ │
# └ ─ ┘

centerText = lambda width, text: padCenter(' ')(width)(text)

BLOCK_W = 10
BLOCK_H = 5

def render_menubar(screen):
	screen.addstr(0, 0, '┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
	screen.addstr(1, 0, '┃                                      ┃')
	screen.addstr(2, 0, '┃           CHAR GAME | 2048           ┃')
	screen.addstr(3, 0, '┃                                      ┃')
	screen.addstr(4, 0, '┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')

	screen.addstr(7, 20, "  Arrow keys control")
	screen.addstr(8, 20, "[R] restart [Q] exit")

def render_scorebox(screen, score: int):
	strScore = str(score)
	L = len(strScore)

	screen.addstr(6, 0, "┏━━━━━━━━━" + "━" * L + "┓")
	screen.addstr(7, 0,f"┃ SCORE: {  strScore   } ┃")
	screen.addstr(8, 0, "┗━━━━━━━━━" + "━" * L + "┛")

	screen.refresh()

def render_gameboard(screen, board):
	for i in range(4):
		for j in range(4):
			block = board[i][j]
			
			left = BLOCK_W * j
			top  = BLOCK_H * i

			if block == EMPTY:
				screen.addstr(top + 0,	left,	'┌────────┐')
				screen.addstr(top + 1,	left,	'│        │')
				screen.addstr(top + 2,	left,	'│        │')
				screen.addstr(top + 3,	left,	'│        │')
				screen.addstr(top + 4,	left,	'└────────┘')

				continue
			
			if block[0] == 'NUM':
				num = block[1]
				s = centerText(BLOCK_W - 2, str(num))

				screen.addstr(top, 		left, 	'┌────────┐')
				screen.addstr(top + 1, left, 	'│        │')
				screen.addstr(top + 2, left,   f'│{   s  }│')
				screen.addstr(top + 3, left, 	'│        │')
				screen.addstr(top + 4, 	left, 	'└────────┘')

def render_gameover(screen, score: int):
	screen.clear()

	screen.addstr(10, 0, "               GAME OVER                ")
	screen.addstr(13, 0, "          [R] restart [Q] exit          ")
	screen.addstr(11, 0,centerText(40, f"YOUR SCORE: {score}"))
