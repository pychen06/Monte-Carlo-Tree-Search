import math
import sys
import numpy as np
from board import Board
from state import State

class Node(object):
	#tree node
	
	def __init__(self, parent=None):
		self.parent = parent
		self.children = []
		self.n_visits = 0
		self.q = 0.0
		self.state = State()
		self.state.compute_move_choices()
	
	def expand(self):
		new_state = self.state.get_next_state_with_remaining_choice()
		new_node = Node()
		new_node.set_state(new_state)
		self.add_child(new_node)
		new_node.parent = self
		return new_node
	
	def get_value(self):
		return self.q
		
	def get_children(self):
		return self.children
		
	def get_state(self):
		return self.state
		
	def set_state(self, state):
		self.state = state
		
	def add_child(self, node):
		self.children.append(node)
	
	def is_leaf(self):
		return len(self.children) == 0
	
	def is_root(self):
		return self.parent is None
		
	def get_n_visits(self):
		return self.n_visits
		
	def is_all_expand(self):
		return len(self.children) == np.size(self.get_state().move, 0)
			
	def best_child(self, is_exploration):
		#計算每個child node的UCB，取最大UCB的node回傳
		#is_exploration == False表示要找出最大Q值的child回傳，作為MCTS player的下棋決策
		
		if is_exploration:
			c = 1.0 / math.sqrt(2.0)
		else:
			c = 0.0
		
		best_child_node = None
		best_ucb = -sys.maxsize
		
		for child in self.get_children():
			left = child.get_value() / child.get_n_visits()
			right = 2.0 * math.log(self.get_n_visits()) / child.get_n_visits()
			ucb = left + c * math.sqrt(right)
			
			if ucb > best_ucb:
				best_ucb = ucb
				best_child_node = child
		return best_child_node
