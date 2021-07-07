import pygame
import random

def print_board(board):
	for i in range(len(board)):
		if i % 3 == 0 and i != 0:
			print('- - - - - - - - - - - -')

		for j in range(len(board[0])):
			if j % 3 == 0 and j != 0:
				print(' | ', end='')

			if j == 8:
				print(board[i][j])
			else:
				print(str(board[i][j]) + ' ', end='')

def find_empty(board):
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 0:
				return (i, j)
	return None

def check_horizontal(board, num, pos):
	y, x = pos
	for i in range(len(board[0])):
		if num == board[y][i] and x != i:
			return False
	return True

def check_vertical(board, num, pos):
	y, x = pos
	for i in range(len(board)):
		if num == board[i][x] and y != i:
			return False
	return True

def check_box(board, num, pos):
	y, x = pos
	box_y = y // 3
	boy_x = x // 3

	for i in range(box_y * 3, box_y * 3 + 3):
		for j in range(boy_x * 3, boy_x * 3 + 3):
			if num == board[i][j] and (i, j) != pos:
				return False
	return True

def check_valid(board, num, pos):
	if check_horizontal(board, num, pos) and check_vertical(board, num, pos) and check_box(board, num, pos):
		return True
	return False

def solve_board(board):
	pos = find_empty(board)
	if pos == None:
		return True
	else:
		y, x = pos

	for i in range(1, 10):
		if check_valid(board, i, pos):
			board[y][x] = i

			if solve_board(board):
				return True

			board[y][x] = 0

	return False

# creates a valid sudoku board
# nums: the potential amount of removed spaces in the board
def create_board(nums):
	SIZE = 9
	if nums >= 0 and nums < SIZE * SIZE:
		new_board = [[0 for i in range(SIZE)] for n in range(SIZE)]
		for i in range(1, 10):
			y = random.randrange(SIZE)
			x = random.randrange(SIZE)
			if new_board[y][x] == 0:
				new_board[y][x] = i
		solve_board(new_board)
		n = nums
		# n = (SIZE * SIZE) - nums - 1
		while(n >= 0):
			y = random.randrange(SIZE)
			x = random.randrange(SIZE)
			if new_board[y][x] != 0:
				new_board[y][x] = 0
				# n -= 1
			n -= 1
		return new_board
	return None
