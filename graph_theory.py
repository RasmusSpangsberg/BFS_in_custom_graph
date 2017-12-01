import pygame
from math import sqrt
import queue

from time import sleep
from time import time

from random import randint

# TODO
# draw name inside circles
# draw length next to edges
# chose some search algorithems to implement
# If list index ot of range error, then make combinations of the letter, like AB, AC, AD
# picks the next available name (that has not been used) in the names list
# Make an option to have REAL length (distance on screen) and an option to customize length
# When making a new edge, check if it already exists, if it does, don't draw it, but let the user "reset" the marked node

class Node:
	def __init__(self, pos, name=""):
		self.pos = pos
		self.name = name

		self.edges = []
		self.neighbors = []
		self.outer_radius = 25
		self.inner_radius = 20

		self.draw("BLACK")

	def draw(self, color):
		pygame.draw.circle(gameDisplay, colors[color], self.pos, self.outer_radius)
		pygame.draw.circle(gameDisplay, colors["WHITE"], self.pos, self.inner_radius)

	def edges(self):
		return self.edges

class edge:
	def __init__(self, node_from, node_to, length=None):
		self.node_from = node_from
		self.node_to = node_to
		self.length = length

		self.name = node_from.name + node_to.name + "_edge"

		self.node_from.edges.append(self)
		self.node_to.edges.append(self)
		self.node_from.neighbors.append(node_to)
		self.node_to.neighbors.append(node_from)

		self.draw1()

		# if there is no custome length, make the actual length
		if self.length == None:
			self.length = sqrt((node_from.pos[0] - node_to.pos[0])**2 + (node_from.pos[1] - node_to.pos[1])**2)

	# What i hoped to be a slow way of drawing.
	def draw2(self, color="BLACK"):
		pygame.draw.line(gameDisplay, colors[color], self.node_from.pos, self.node_to.pos, 4)

		pygame.draw.circle(gameDisplay, colors[color], self.node_to.pos, self.node_to.outer_radius)
		pygame.draw.circle(gameDisplay, colors["WHITE"], self.node_to.pos, self.node_to.inner_radius)

	# I hoped this would be a faster way of drawing, but it is about the same.
	def draw1(self, color="BLACK"):
		# A + t*(B-A) + s*(B-C) = A + t*(B-A) + s*(B-A)

		a = self.node_from.pos[0]
		b = self.node_from.pos[1]
		c = self.node_to.pos[0]
		d = self.node_to.pos[1]

		r = self.node_to.outer_radius

		r1 = c - a
		r2 = d - b

		A = r1**2 + r2**2
		B = 2*a*r1 + 2*b*r2 - 2*r1*c - 2*r2*d
		C = a**2 + b**2 + c**2 + d**2 - r**2 - 2*a*c - 2*b*d

		try:
			t1 = (-B + sqrt(B**2 - 4*A*C)) / (2*A) 
			t2 = (-B - sqrt(B**2 - 4*A*C)) / (2*A)
		except ValueError:
			print("Distance cannot be 0")

			pygame.quit()
			quit()

		if t1 < t2:
			new_pos1 = [a + r1 * t1, b + r2 * t1]
			pygame.draw.line(gameDisplay, colors[color], self.node_from.pos, new_pos1, 4)
		else:
			new_pos2 = [a + r1 * t2, b + r2 * t2]
			pygame.draw.line(gameDisplay, colors[color], self.node_from.pos, new_pos2, 4)

		if self.length != None:
			pass

def breadth_first_search(start_node):
	
	# The frontier's datatype is a queue (FIFO)
	frontier = queue.Queue()
	frontier.put(start_node)

	# Using a set, instead of a list, 
	# because we don't care about the order, 
	# we only care if we have explored the node or not
	explored = set()
	
	while not frontier.empty():

		node = frontier.get()

		if node.name == "G":
			print("FOUND GOAL NODE")
			searching = False
			break

		node.draw("TEAL")
		print("TEAL:", node.name)

		pygame.display.update()
		sleep(1)

		explored.add(node)

		for neighbor in node.neighbors:
			not_in_frontier = True
			not_in_explored = True

			for item in list(frontier.queue):
				if item == neighbor:
					not_in_frontier = False

			if neighbor in explored:
				not_in_explored = False

			if not_in_explored and not_in_frontier:
				frontier.put(neighbor)
				e = edge(node, neighbor)
				e.draw2(color="GREEN")
				pygame.display.update()

				sleep(2)
				e.draw2(color="BLACK")

		print("BLACK:", node.name)
		node.draw("BLACK")

pygame.init()

colors = {"WHITE":(255, 255, 255), "BLACK":(0, 0, 0), "GREEN":(0,255,0), "TEAL":(0, 127, 127), "YELLOW":(255, 255, 0), "CYAN":(0, 255, 255), "PURPLE":(127, 0, 127)}

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Graph theory")

gameExit = False

gameDisplay.fill(colors["WHITE"])

button_pos_x = 350
button_pos_y = 0
button_heigth = 50
button_width = 100
pygame.draw.rect(gameDisplay, colors["TEAL"], [button_pos_x, button_pos_y, button_width, button_heigth])

pygame.display.update()

nodes = []
names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "X", "Y", "Z"]
searching = False

marked_node = None
start_node = None
goal_node = None

""" # draw a lot of nodes and connect them all in order to test whether draw1 or draw2 is faster
start_time = time()
for x in range(100):
	a = Node([randint(1, 800), randint(1, 600)])
	b = Node([randint(1, 800), randint(1, 600)])
	edge(a, b).draw2()
	pygame.display.update()

print(time() - start_time)

start_time = time()
for x in range(100):
	a = Node([randint(1, 800), randint(1, 600)])
	b = Node([randint(1, 800), randint(1, 600)])
	edge(a, b).draw1()
	pygame.display.update()

print(time() - start_time)
"""

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
		
		elif searching:
			if goal_node == None:
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = pygame.mouse.get_pos()

					for n in nodes:
						if n.pos[0] - n.outer_radius < x and x < n.pos[0] + n.outer_radius:
							if n.pos[1] - n.outer_radius < y and y < n.pos[1] + n.outer_radius:

								if start_node == None:
									start_node = n
									start_node.draw("YELLOW")
									start_node.name = "S"

								elif goal_node == None:
									goal_node = n
									goal_node.draw("GREEN")
									goal_node.name = "G"
								break
					pygame.display.update()
			else:
				breadth_first_search(start_node)
				searching = False
				

		elif event.type == pygame.MOUSEBUTTONDOWN:
			x, y = pygame.mouse.get_pos()
			
			if x > button_pos_x and x < button_pos_x + button_width and y > button_pos_y and y < button_pos_y + button_heigth:
				print("Starting search...")
				print("Click the start node (S) and the goal node (G)")
				searching = True
			else:
				draw = True

				for node in nodes:
					if node.pos[0] - (2 * node.outer_radius) < x and x < node.pos[0] + (2 * node.outer_radius):
						if node.pos[1] - (2 * node.outer_radius) < y and y < node.pos[1] + (2 * node.outer_radius):
							draw = False

					# if a node is clicked
					if node.pos[0] - node.outer_radius < x and x < node.pos[0] + node.outer_radius:
						if node.pos[1] - node.outer_radius < y and y < node.pos[1] + node.outer_radius:

							if marked_node == None:
								marked_node = node
								marked_node.draw("CYAN")
							elif marked_node != None and marked_node not in node.neighbors:
								edge(marked_node, node)
								marked_node.draw("BLACK")
								marked_node = None
							else:
								marked_node.draw("BLACK")
								marked_node = None
							break

				if draw:
					name = names[len(nodes)]
					nodes.append(Node([x, y], name))


				pygame.display.update()

pygame.quit()
quit()