from random import randint, random, choice
from math import log2

from util import padEnd, filterFunc, removeByIndex, mutateTuple, mapFunc, reduce

EMPTY = ('EMPTY', None)
_NUM = lambda x: ('NUM', x)
_nums = []
def NUM(x: int):
	if 2 ** len(_nums) > x:
		return _nums[int(log2(x)) - 1]
	num = _NUM(x)
	_nums.append(num)
	return num

nextNum = lambda n: NUM(n[1] * 2)

ST_PLAYING = 'ST_PLAYING'
ST_GAMEOVER = 'ST_GAMEOVER'
ST_LEAVING = 'ST_LEAVING'

def init_logic():
	_nums.clear()
	for i in range(1, 5):
		_nums.append(_NUM(2 ** i))

	board = tuple( tuple( EMPTY for y in range(4)) for x in range(4))

	for _ in range(2):
		board = insertNew(board)

	# board = (
	# 	(NUM(2), NUM(2),NUM(2), NUM(2),),
	# 	(NUM(2), NUM(2),NUM(2), NUM(2),),
	# 	(NUM(2), NUM(2),NUM(2), NUM(2),),
	# 	(NUM(2), NUM(2),NUM(2), NUM(2),),
	# )

	return board, ST_PLAYING

def _calc_blocks(bs):
	changed = False
	l = len(bs)
	delta = 0
	idx = 0
	while idx < l - 1:
		b0 = bs[idx]
		b1 = bs[idx + 1]
		if b0 == b1:
			changed = True
			bs = removeByIndex(bs, idx)
			newNum = nextNum(b0)
			delta += newNum[1]
			bs[idx] = newNum
			l -= 1
		else:
			idx += 1
	return (changed, padEmpty(bs), delta)

padEmpty = lambda xs: padEnd( [EMPTY] )(4)(xs)
mapReverse = mapFunc(lambda xs: xs[-1::-1])

def reduceBoard(board):
	"""
		Reduce the board in leftward direction
	"""
	newBoard = []
	scoreChange = 0
	alive = True

	full = True
	changed = False

	for blocks in board:
		# special case that number doesn't change but blocks moved
		idx = 0
		while idx < 4 and blocks[idx] != EMPTY:
			idx += 1
		while idx < 4 and blocks[idx] == EMPTY:
			idx += 1
		if idx < 4:
			changed = True # such EMP -> NUM case will definitely change

		compactBlocks = filterFunc(lambda b: b!=EMPTY)(blocks)
		if len(compactBlocks) < 4:
			full = False
		(numChanged, newBlocks, blocksScoreChange) = _calc_blocks(compactBlocks)
		newBoard.append(newBlocks)
		scoreChange += blocksScoreChange

		changed = changed or numChanged

	if not changed and full:
		alive = False

	return alive, changed, newBoard, scoreChange

def insertNew(board):
	x, y = randint(0, 3), randint(0, 3)
	while board[x][y] != EMPTY:
		x, y = randint(0, 3), randint(0, 3)
	
	bs = board[x]
	bs = mutateTuple(bs, y, NUM(2))
	return mutateTuple(board, x, bs)

def handle_right(board):
	board = mapReverse(board)
	alive, changed, newBoard, delta = reduceBoard(board)
	return alive, changed, mapReverse(newBoard), delta

def handle_left(board):
	alive, changed, newBoard, delta = reduceBoard(board)
	return alive, changed, newBoard, delta

def handle_up(board):
	transformedBoard = tuple(tuple(board[j][i] for j in range(4)) for i in range(4))
	alive, changed, newBoard, delta = reduceBoard(transformedBoard)
	return alive, changed, tuple(tuple(newBoard[j][i] for j in range(4)) for i in range(4)), delta

def handle_down(board):
	transformedBoard = tuple(tuple(board[3-j][3-i] for j in range(4)) for i in range(4))
	alive, changed, newBoard, delta = reduceBoard(transformedBoard)
	return alive, changed, tuple(tuple(newBoard[3-j][3-i] for j in range(4)) for i in range(4)), delta