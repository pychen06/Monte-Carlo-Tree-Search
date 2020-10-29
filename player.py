from MCTS import MCTS
from node import Node
import numpy as np
from board import Board

class Human(object):
	#真實玩家
	
	def __init__(self):
		self.player = None
		
	#設定真實玩家的玩家ID
	def set_player_ind(self, p):
		self.player = p
		
	#要求真實玩家輸入一步棋的移動
	def get_action(self, board):
		location = input('Your move(seperated by ,): ')
		if isinstance(location, str):
			location = [int(n, 10) for n in location.split(",")]
		#print(location)  #[2,3,4,5]
		
		#輸入不為4個數字
		if len(location) != 4:
			print('input format error')
			location = self.get_action(board)

		if not board.is_available(location, self.player):
			print('input value error')
			location = self.get_action(board)
		
		return location
		
class MCTSplayer:
	#AI玩家
	
	def __init__(self, board, n_playout = 50):
		self.mcts = MCTS(board, n_playout)
		self.n_playout = n_playout
		
	#設定AI玩家的玩家ID
	def set_player_ind(self, p):
		self.player = p
		
	#得到AI玩家的下一步棋
	def get_action(self, board):
		for i in range(self.n_playout):
			selected_node = self.mcts.tree_policy()
			#print(selected_node.state.current_board.map)
			reward = self.mcts.default_policy(selected_node)
			self.mcts.backup(selected_node, reward)
			
		return self.mcts.best_next_choice(False)    
		"""
			上一行回傳值有錯
		"""
			
	def update_from_movement(self, move, player):
		self.mcts.update_current_node(move, player)
		
			

if __name__ == "__main__":
	human = Human()
	board = Board()
	location = human.get_action(board)
	