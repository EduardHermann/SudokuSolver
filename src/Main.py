import pygame
import sys
from Solver import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 250)
GREEN = (0, 255, 0)

SIZE = 900
# potential removed spaces
PRS = 60
WIN = pygame.display.set_mode((900, 900))
pygame.display.set_caption("Sudoku by Eduard Hermann")
image = pygame.image.load('icon.png')
pygame.display.set_icon(image)
pygame.init()

class Vertex():

	rows = 9
	cols = 9

	def __init__(self, value, row, col, width, height):
		self.value = value
		self.tempv = 0
		self.row = row
		self.col = col
		self.width = width
		self.height = height
		self.preset = False
		self.selected = False

	def draw_itself(self, win):
		tf = pygame.font.SysFont("timesnewroman", 40)

		gap = self.width / 9
		x = self.col * gap
		y = self.row * gap

		if self.preset:
			text = tf.render(str(self.value), 1, BLUE)
			win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
		elif self.value == 0 and self.tempv != 0:
			text = tf.render(str(self.tempv), 1, GRAY)
			win.blit(text, (x + 5, y + 5))
		elif self.value != 0:
			text = tf.render(str(self.value), 1, BLACK)
			win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
		
		if self.selected:
			pygame.draw.rect(win, RED, (x, y, gap, gap), 5)

	def set_tempv(self, new_tempv):
		self.tempv = new_tempv

	def set_value(self, new_value):
		self.value = new_value

class Grid():

	board = create_board(PRS)

	def __init__(self, rows, cols, width, height):
		self.rows = rows
		self.cols = cols
		self.width = width
		self.height = height
		self.vertex_board = [[Vertex(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				if self.board[i][j] != 0:
					self.vertex_board[i][j].preset = True
		self.model = None
		self.vertex_selected_pos = None

	def update_model(self):
		self.model = [[self.vertex_board[i][j].value for j in range(self.cols)] for i in range(self.rows)]

	def place(self, value):
		row, col = self.vertex_selected_pos
		if self.vertex_board[row][col].value == 0:
			self.vertex_board[row][col].set_value(value)
			self.update_model()

			if check_valid(self.model, value, (row, col)) and solve_board(self.model):
				return True
			else:
				self.vertex_board[row][col].set_value(0)
				self.vertex_board[row][col].set_tempv(0)
				self.update_model()
				return False

	def sketch(self, tempv):
		row, col = self.vertex_selected_pos
		self.vertex_board[row][col].set_tempv(tempv)

	def draw(self, win):
		# draw grid lines
		gap = self.width / 9
		for i in range(self.rows):
			if i % 3 == 0 and i != 0:
				line_thickness = 4
			else:
				line_thickness = 1
			pygame.draw.line(win, BLACK, (i * gap, 0), (i * gap, self.width), line_thickness)
			pygame.draw.line(win, BLACK, (0, i * gap), (self.width, i * gap), line_thickness)	

		# draw vertexes
		for i in range(len(self.vertex_board)):
			for j in range(len(self.vertex_board[0])):
				self.vertex_board[i][j].draw_itself(win)

	def clear(self):
		row, col = self.vertex_selected_pos
		if self.vertex_board[row][col].value == 0:
			if self.vertex_board[row][col].tempv != 0:
				self.vertex_board[row][col].set_tempv(0)
	
	def clear_selected(self):
		for i in range(len(self.vertex_board)):
			for j in range(len(self.vertex_board[0])):
				if self.vertex_board[i][j].selected:
					self.vertex_board[i][j].selected = False
		
	def select(self, row, col):
		self.clear_selected()
		self.vertex_board[row][col].selected = True
		self.vertex_selected_pos = (row, col)

	def clicked_pos(self, pos):
		# coordinates
		x, y = pos
		if x >= 0 and x <= self.width and y >= 0 and y <= self.height:
			gap = self.width / 9
			row = y // gap
			col = x // gap
			return (int(row), int(col))
		else:
			return None

	def is_finished(self):
		for i in range(len(self.vertex_board)):
			for j in range(len(self.vertex_board[0])):
				if self.vertex_board[i][j].value == 0:
					return False
		return True

	def mark(self, win, row, col, color):
		gap = self.width / 9
		pygame.draw.rect(win, color, (col * gap, row * gap, gap, gap), 6)
		pygame.display.update()

	def solve_board_animated(self, win):
		pos = find_empty(self.model)

		if pos == None:
			return True
		else:
			y, x = pos

		for i in range(1, 10):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			
			if check_valid(self.model, i, pos):
				self.model[y][x] = i
				self.vertex_board[y][x].value = i
				redraw_window(win, self)
				self.mark(win, y, x, GREEN)
				
				if self.solve_board_animated(win):
					return True
				
				self.model[y][x] = 0
				self.vertex_board[y][x].value = 0
				redraw_window(win, self)
				self.mark(win, y, x, RED)

		return False

def redraw_window(win, board):
	win.fill(WHITE)
	board.draw(win)
	pygame.display.update()

def main():
	board = Grid(9, 9, SIZE, SIZE)
	run = True
	key = None
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					key = 1
				if event.key == pygame.K_2:
					key = 2
				if event.key == pygame.K_3:
					key = 3
				if event.key == pygame.K_4:
					key = 4
				if event.key == pygame.K_5:
					key = 5
				if event.key == pygame.K_6:
					key = 6
				if event.key == pygame.K_7:
					key = 7
				if event.key == pygame.K_8:
					key = 8
				if event.key == pygame.K_9:
					key = 9
				###########################
				if event.key == pygame.K_UP:
					if board.vertex_selected_pos != None:
						if board.vertex_selected_pos[0] > 0:
							pos = board.vertex_selected_pos
							board.select(pos[0] - 1, pos[1])
							key = None
				if event.key == pygame.K_DOWN:
					if board.vertex_selected_pos != None:
						if board.vertex_selected_pos[0] < 8:
							pos = board.vertex_selected_pos
							board.select(pos[0] + 1, pos[1])
							key = None
				if event.key == pygame.K_RIGHT:
					if board.vertex_selected_pos != None:
						if board.vertex_selected_pos[1] < 8:
							pos = board.vertex_selected_pos
							board.select(pos[0], pos[1] + 1)
							key = None
				if event.key == pygame.K_LEFT:
					if board.vertex_selected_pos != None:
						if board.vertex_selected_pos[1] > 0:
							pos = board.vertex_selected_pos
							board.select(pos[0], pos[1] - 1)
							key = None
				###########################
				if event.key == pygame.K_BACKSPACE:
					board.clear()
					key = None
				if event.key == pygame.K_RETURN:
					row, col = board.vertex_selected_pos
					if board.vertex_board[row][col].tempv != 0:
						if board.place(board.vertex_board[row][col].tempv):
							pass
							# print('True')
						else: 
							pass
							# print('False')
						key = None

						if board.is_finished():
							run = False
				if event.key == pygame.K_SPACE:
					board.clear_selected()
					board.update_model()
					board.solve_board_animated(WIN)
					key = None

				if event.key == pygame.K_g:
					board.board = create_board(PRS)
					board.__init__(9, 9, SIZE, SIZE)
					key = None

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = board.clicked_pos(pygame.mouse.get_pos())
				if pos:
					board.select(pos[0], pos[1])
					key = None

		if board.vertex_selected_pos and key != None:
			board.sketch(key)

		redraw_window(WIN, board)
		pygame.display.update()

main()
sys.exit()
