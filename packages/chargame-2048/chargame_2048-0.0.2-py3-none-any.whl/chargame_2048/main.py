import curses
from curses import KEY_LEFT, KEY_UP, KEY_DOWN, KEY_RIGHT

from render import render_gameboard, render_gameover, render_menubar, render_scorebox, BLOCK_H, BLOCK_W
from logic import init_logic, insertNew, ST_GAMEOVER, ST_PLAYING, ST_LEAVING, handle_down, handle_left, handle_up, handle_right
from util import newwin

def resetGame(game):
	game['board'], game['state'] = init_logic()
	game['score'] = 0

def curses_mainloop(screen):
	screen.clear()

	curses.curs_set(0)

	render_menubar(screen)
	screen.refresh()

	game = dict()

	game['board'], game['state'] = init_logic()
	game['score'] = 0
	
	gameBoardScreen = newwin(4 * BLOCK_H + 1, 4 * BLOCK_W + 1, 10, 0)
	scoreBox = newwin(5, 19, 6, 0)

	# screen.refresh()

	while game['state'] != ST_LEAVING:
		changed = False
		render_scorebox(screen, game['score'])
		render_gameboard(gameBoardScreen, game['board'])

		gameBoardScreen.refresh()

		action = gameBoardScreen.getch()

		delta = 0
		alive = False
		# quit on 'q' is pressed
		if action == ord('q'):
			break
		elif action == ord('r'):
			resetGame(game)
			continue

		elif action == KEY_RIGHT:
			alive, changed, game['board'], delta = handle_right(game['board'])
		elif action == KEY_LEFT:
			alive, changed, game['board'], delta = handle_left(game['board'])
		elif action == KEY_UP:
			alive, changed, game['board'], delta = handle_up(game['board'])
		elif action == KEY_DOWN:
			alive, changed, game['board'], delta = handle_down(game['board'])
		
		if not alive:
			game['state'] = ST_GAMEOVER
			render_gameover(gameBoardScreen, game['score'])
			gameBoardScreen.refresh()
			
			gameover_action = screen.getch()
			
			if gameover_action == ord('q'):
				break
			elif gameover_action == ord('r'):
				resetGame(game)
				continue

		game['score'] += delta
		if changed:
			game['board'] = insertNew(tuple(map(tuple, game['board'])))

def main():
	try:
		curses.wrapper(curses_mainloop)
	except Exception as err:
		print(err)
		print('make sure the terminal is larger than 41x31')

if __name__=='__main__':
	main()