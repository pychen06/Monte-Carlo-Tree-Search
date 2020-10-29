from node import Node
from state import State

class MCTS(object):
	#MCTS algorithm
	
	def __init__(self, board, n_playout):
		self.root = Node()
		self.n_playout = n_playout
		self.current_node = self.root
		
	def tree_policy(self):
		#select
		#若這個node還有可以被擴展的點，則優先選擇擴展新的點，否則就選擇UCB最大的child node
		sub_node = self.current_node
		is_end, winner = sub_node.state.is_terminal()
		while not is_end:
			if not sub_node.is_all_expand():
				return sub_node.expand()
			else:
				sub_node = sub_node.best_child(True)
			is_end, winner = sub_node.state.is_terminal()
		return sub_node
		
	def default_policy(self, selected_node):
		#current_state = selected_node.get_state()
		current_state = State()
		selected_node.get_state().copy_state(current_state)
		is_end, winner = current_state.is_terminal()
		while not is_end:
			current_state = current_state.get_next_state_with_random_choice()
			is_end, winner = current_state.is_terminal()
		return current_state.compute_reward()
	
	def backup(self, selected_node, leaf_value):
		sub_node = selected_node
		v = leaf_value
		while sub_node != None:
			sub_node.n_visits += 1
			sub_node.q += v
			sub_node = sub_node.parent
			v = -v
			
	def best_next_choice(self, is_exploration):
		#print(self.current_node.best_child(is_exploration).state.cumulative_choices)
		return self.current_node.best_child(is_exploration).state.cumulative_choices[-1]
		
	def update_current_node(self, move, player):
		for child in self.current_node.get_children():
			is_equal = True
			last_move = child.get_state().cumulative_choices[-1]  #return 移動到child_node的movement
			for i in range(4):
				if last_move[i] != move[i]:
					is_equal = False
			if is_equal:
				self.current_node = child
				return
		#建立新的node來儲存新的移動
		new_node = Node(self.current_node)
		new_node.set_state(self.current_node.get_state().get_next_state_with_move(move, player))
		self.current_node = new_node
		
					