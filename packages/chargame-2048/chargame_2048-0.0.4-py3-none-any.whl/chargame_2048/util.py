from math import floor, ceil
from curses import newwin as _newwin

padStart = lambda padding: lambda length: lambda x: max(0, length - len(x)) * padding + x
padEnd = lambda padding: lambda length: lambda x: x + max(0, length - len(x)) * padding

padCenter = lambda padding: lambda length: lambda x: max(0, floor((length-len(x))/2)) * padding + x + max(0, ceil((length-len(x))/2)) * padding

filterFunc = lambda fn: lambda xs: [x for x in xs if fn(x)]
mapFunc = lambda fn: lambda xs: [fn(x) for x in xs]
reduce = lambda fn: lambda xs, y = None: [(y := fn(x, y)) for x in xs][-1]

removeByIndex = lambda xs, idx: xs[:idx] + xs[idx + 1:]
mutateTuple = lambda ts, idx, val: ts[:idx] + (val,) + ts[idx+1:]

def newwin(nlines: int, ncols: int, begin_y: int, begin_x: int):
	win = _newwin(nlines ,ncols ,begin_y ,begin_x)
	win.keypad(True)

	return win
