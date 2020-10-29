import numpy as np
from player import Human, MCTSplayer
from board import Board
import math
import time

class Game(object):
	#整個遊戲的畫面跟流程
	
	def __init__(self, board, **kwargs):
		self.current_player = 1
		self.board = board
	
	def graphic(self):
		#遊戲畫面顯示
		width = self.board.width
		height = self.board.height
		
		#印出整個棋盤的畫面
		print('  ', end = '')
		for i in range(width):
			print(i, end = '')
			print(' ', end = '')
		print()
		
		for i in range(height):
			print(i, end = '')
			print(board.map[i, ])
		
	def start_play(self, player1, player2, start_player = 1):  # 預設為ai玩家下第一步棋
		p1, p2 = [1, 2]
		player1.set_player_ind(p1)
		player2.set_player_ind(p2)
		players = {p1: player1, p2: player2}
		is_mcts = [0, 0]
		if type(player1) == type(MCTSplayer(self.board)):
			is_mcts[0] = 1
		if type(player2) == type(MCTSplayer(self.board)):
			is_mcts[1] = 1
		self.current0_player = start_player #設定第一個移動的玩家
		#display
		self.graphic()
		
		#遊戲開始，持續讀取player和MCTS做出的決策，直到遊戲結束
		while True:
			time_start = time.time()
			player_in_turn = players[self.current_player]  #return human object or MCTSplayer object
			move = player_in_turn.get_action(self.board)   #MCTS algorithm找出好的下一步，或是由real player輸入
			time_end = time.time()
			self.board.move_map(move, self.current_player)
			print(move)
			print(self.current_player)
			self.graphic()
			if is_mcts[0] == 1:
				player1.update_from_movement(move, self.current_player)
			if is_mcts[1] == 1:
				player2.update_from_movement(move, self.current_player)
			
			self.current_player = abs(self.current_player - 2) + 1 
			
			end, winner = player2.mcts.current_node.get_state().is_terminal()
			"""
			print(winner,end=' ')
			print(end)
			print("--------------")
			print(player2.mcts.current_node.get_state().current_board.map)
			print("--------------")
			"""
			print("time cost", time_end - time_start)
			if end:
				if winner != -1:
					print("Game end. Winner is", winner)
				else:
					print("Game end. Tie")
				return winner
			
		
if __name__ == '__main__':
	board = Board()
	game = Game(board)
	human = Human()
	AIplayer1 = MCTSplayer(board)
	AIplayer2 = MCTSplayer(board)
	game.start_play(human, AIplayer2)
	#game.start_play(AIplayer1, AIplayer2)