from board import Board
import numpy as np
import random

class State(object):
  """
  蒙特卡罗树搜索的游戏状态，记录在某一个Node节点下的状态数据，包含当前的游戏得分、当前的游戏round数、从开始到当前的执行记录。
  需要实现判断当前状态是否达到游戏结束状态，支持从Action集合中随机取出操作。
  """

  def __init__(self):
    self.current_board = Board()
    #1 is black, 2 is white
    self.current_player = 1
    # For the first root node, the index is 0 and the game should start from 1
    self.current_round_index = 0
    self.cumulative_choices = []
    self.move = []

  def get_current_board(self):
    return self.current_board

  def set_current_board(self, board):
    self.current_board = board
    
  def get_current_player(self):
    return self.current_player

  def set_current_player(self, player):
    self.current_player = player

  def get_current_round_index(self):
    return self.current_round_index

  def set_current_round_index(self, turn):
    self.current_round_index = turn

  def get_cumulative_choices(self):
    return self.cumulative_choices

  def set_cumulative_choices(self, choices):
    self.cumulative_choices = choices   

  def is_terminal(self):
    if self.current_player == 1:
        if int(np.size(self.current_board.black)/2) == 1:
            #print("one black")
            return True, 2
        
    if self.current_player == 2:
        if int(np.size(self.current_board.white)/2) == 1:
            #print("one white")
            return True, 1
    black_all_in_line = False
    white_all_in_line = False
    """
    if self.current_player == 1:
        black_all_in_line = True
        #print(self.current_board.black)
        for i in range(len(self.current_board.black) - 1):
            if not self.is_surround(self.current_board.black[i], self.current_board.black[i + 1]):
                black_all_in_line = False
    if self.current_player == 2:
        white_all_in_line = True
        #print(self.current_board.white)
        for i in range(len(self.current_board.white) - 1):
            if not self.is_surround(self.current_board.white[i], self.current_board.white[i + 1]):
                white_all_in_line = False
    """
    if self.current_player == 1:
        tem_arr = np.array(self.current_board.black)
        black_all_in_line  = True
    else:
        tem_arr = np.array(self.current_board.white)
        white_all_in_line  = True
    
    cluster = [[tem_arr[0][0],tem_arr[0][1]]]
    index = [0, 1]
    tem_arr = np.delete(tem_arr, index)
    tem_arr = tem_arr.reshape(-1, 2)
    tem_arr = tem_arr.astype(int)
    while int(np.size(tem_arr)/2) > 0:          
        for i in range(int(np.size(tem_arr)/2)):
            neighbor = False
            for j in range(len(cluster)):
                if self.is_surround(tem_arr[i], cluster[j]):
                    neighbor = True
                    cluster.append([tem_arr[i][0], tem_arr[i][1]])
                    index = [i*2, i*2+1]
                    tem_arr = np.delete(tem_arr, index)
                    tem_arr = tem_arr.reshape(-1, 2)
                    tem_arr = tem_arr.astype(int)
                    #print(tem_arr)
                    #print(cluster)
                    break;
            if neighbor:
                break
        if not neighbor:
            if self.current_player == 1:
                black_all_in_line = False
            else:
                white_all_in_line = False
            break
    if black_all_in_line:
        #print('black_all_in_line')
        return True, 1
    if white_all_in_line:
        #print('white_all_in_line')
        return True, 2
    
    if self.compute_move_choices().size == 0:
        #print("no move chioces")
        return True, abs(self.current_player - 2) + 1
    
    return False, -1
        
        
  def find_surround(self, location, player):
    if location[0] + 1 <= 7:
        if self.current_board.map[location[0] + 1, location[1]] == player:
            return True
        
    if location[0] - 1 >= 0:
        if self.current_board.map[location[0] - 1, location[1]] == player:
            return True
        
    if location[1] + 1 <= 7:
        if self.current_board.map[location[0], location[1] + 1] == player:
            return True
        
    if location[1] - 1 >= 0:
        if self.current_board.map[location[0], location[1] - 1] == player:
            return True
        
    if location[0] + 1 <= 7 and location[1] + 1 <= 7:
        if self.current_board.map[location[0] + 1, location[1] + 1] == player:
            return True
        
    if location[0] + 1 <= 7 and location[1] - 1 >= 0:
        if self.current_board.map[location[0] + 1, location[1] - 1] == player:
            return True

    if location[0] - 1 >= 0 and location[1] + 1 <= 7:
        if self.current_board.map[location[0] - 1, location[1] + 1] == player:
            return True

    if location[0] - 1 >= 0 and location[1] - 1 >= 0:
        if self.current_board.map[location[0] - 1, location[1] - 1] == player:
            return True
        
    return False

  def is_surround(self, location, target):
    return abs(location[0] - target[0]) <= 1 and abs(location[1] - target[1]) <= 1

        
  def compute_reward(self):
    if self.current_player == 1:
        return 0
    elif self.current_player == 2:
        return 1

  def compute_move_choices(self):
    move = np.array([])
    if self.current_player == 1:
      for i in range(len(self.current_board.black)):
          step = self.right_move(self.current_board.black[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.black[i], [self.current_board.black[i][0], self.current_board.black[i][1] + step]])
                  
          step = self.left_move(self.current_board.black[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.black[i], [self.current_board.black[i][0], self.current_board.black[i][1] - step]])  
            
          step = self.top_move(self.current_board.black[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.black[i], [self.current_board.black[i][0] - step, self.current_board.black[i][1]]])
            
          step = self.down_move(self.current_board.black[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.black[i], [self.current_board.black[i][0] + step, self.current_board.black[i][1]]])    
              
          step = self.top_right_move(self.current_board.black[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.black[i], [self.current_board.black[i][0] - step, self.current_board.black[i][1] + step]])
              
          step = self.top_left_move(self.current_board.black[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.black[i], [self.current_board.black[i][0] - step, self.current_board.black[i][1] - step]])    
          
          step = self.bottom_right_move(self.current_board.black[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.black[i], [self.current_board.black[i][0] + step, self.current_board.black[i][1] + step]])
              
          step = self.bottom_left_move(self.current_board.black[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.black[i], [self.current_board.black[i][0] + step, self.current_board.black[i][1] - step]])    
          
      move = move.reshape(-1, 4)
    else :
      for i in range(len(self.current_board.white)):
          step = self.right_move(self.current_board.white[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.white[i], [self.current_board.white[i][0], self.current_board.white[i][1] + step]])
                  
          step = self.left_move(self.current_board.white[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.white[i], [self.current_board.white[i][0], self.current_board.white[i][1] - step]])  
            
          step = self.top_move(self.current_board.white[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.white[i], [self.current_board.white[i][0] - step, self.current_board.white[i][1]]])
            
          step = self.down_move(self.current_board.white[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.white[i], [self.current_board.white[i][0] + step, self.current_board.white[i][1]]])    
              
          step = self.top_right_move(self.current_board.white[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.white[i], [self.current_board.white[i][0] - step, self.current_board.white[i][1] + step]])
              
          step = self.top_left_move(self.current_board.white[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.white[i], [self.current_board.white[i][0] - step, self.current_board.white[i][1] - step]])    
          
          step = self.bottom_right_move(self.current_board.white[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.white[i], [self.current_board.white[i][0] + step, self.current_board.white[i][1] + step]])
              
          step = self.bottom_left_move(self.current_board.white[i], self.current_player)
          if step != 0:
              move = np.append(move,[self.current_board.white[i], [self.current_board.white[i][0] + step, self.current_board.white[i][1] - step]])    
          
      move = move.reshape(-1, 4)
    
    append_zeros = np.zeros((np.size(move,0),1))
    move = np.append(move,append_zeros,axis = 1)
    move = move.astype(int)
    self.move = move
    return move
          
                  
  def right_move(self, location, player):
    count = 0
    for i in range(8):
      if self.current_board.map[location[0], i] != 0:
        count += 1
              
    if (location[1] + count) > 7:
       return 0
   
    if self.current_board.map[location[0], location[1] + count] == player: 
      return 0
   
    is_movable = True
    for i in range(count):
        if self.current_board.map[location[0], location[1] + i] != player and self.current_board.map[location[0], location[1] + i] != 0:
           is_movable = False
    
    if is_movable:
        return count
    else: return 0
    

  def left_move(self, location, player):
    count = 0
    for i in range(8):
      if self.current_board.map[location[0], i] != 0:
        count += 1
              
    if location[1] - count < 0:
       return 0
   
    if self.current_board.map[location[0], location[1] - count] == player: 
      return 0
   
    is_movable = True
    for i in range(count):
        if self.current_board.map[location[0], location[1] - i] != player and self.current_board.map[location[0], location[1] - i] != 0:
           is_movable = False
    
    if is_movable:
        return count
    else: return 0
        
  def top_move(self, location, player):
    count = 0
    for i in range(8):
      if self.current_board.map[i, location[1]] != 0:
        count += 1
              
    if location[0] - count < 0:
       return 0
   
    if self.current_board.map[location[0] - count, location[1]] == player: 
      return 0
   
    is_movable = True
    for i in range(count):
        if self.current_board.map[location[0] - i, location[1]] != player and self.current_board.map[location[0] - i, location[1]] != 0:
           is_movable = False
    
    if is_movable:
        return count
    else: return 0
    
  def down_move(self, location, player):
    count = 0
    for i in range(8):
      if self.current_board.map[i, location[1]] != 0:
        count += 1
              
    if location[0] + count > 7 :
       return 0

    if self.current_board.map[location[0] + count, location[1]] == player: 
      return 0
   
    is_movable = True
    for i in range(count):
        if self.current_board.map[location[0] + i, location[1]] != player and self.current_board.map[location[0] + i, location[1]] != 0:
           is_movable = False
    
    if is_movable:
        return count
    else: return 0
    
  def top_right_move(self, location, player):
    count = 0
    point = list(location)

    
    while point[0] < 7 and point[1] > 0:
      point[0] += 1
      point[1] -= 1
    
    while point[0] >= 0 and point[1] <= 7:
      if self.current_board.map[point[0], point[1]] != 0:
        count += 1
      point[0] -= 1
      point[1] += 1
      
    if location[0] - count < 0 or location[1] + count > 7:
      return 0
    
    if self.current_board.map[location[0] - count, location[1] + count] == player: 
      return 0
    
    is_movable = True
    for i in range(count):
        if self.current_board.map[location[0] - i, location[1] + i] != player and self.current_board.map[location[0] - i, location[1] + i] != 0:
           is_movable = False
          
    if is_movable:
        return count
    else: return 0    
    
  def top_left_move(self, location, player):
    count = 0
    point = list(location)

    
    while point[0] < 7 and point[1] < 7:
      point[0] += 1
      point[1] += 1
    
    while point[0] >= 0 and point[1] >= 0:
      if self.current_board.map[point[0], point[1]] != 0:
        count += 1
      point[0] -= 1
      point[1] -= 1
      
    if location[0] - count < 0 or location[1] - count < 0:
      return 0
    
    if self.current_board.map[location[0] - count, location[1] - count] == player: 
      return 0
    
    is_movable = True
    for i in range(count):
        if self.current_board.map[location[0] - i, location[1] - i] != player and self.current_board.map[location[0] - i, location[1] - i] != 0:
           is_movable = False
          
    if is_movable:
        return count
    else: return 0        
        
  def bottom_right_move(self, location, player):
    count = 0
    point = list(location)

    
    while point[0] > 0 and point[1] > 0:
      point[0] -= 1
      point[1] -= 1
    
    while point[0] <= 7 and point[1] <= 7:
      if self.current_board.map[point[0], point[1]] != 0:
        count += 1
      point[0] += 1
      point[1] += 1
      
    if location[0] + count > 7 or location[1] + count > 7:
      return 0
    
    if self.current_board.map[location[0] + count, location[1] + count] == player: 
      return 0
    
    is_movable = True
    for i in range(count):
        if self.current_board.map[location[0] + i, location[1] + i] != player and self.current_board.map[location[0] + i, location[1] + i] != 0:
           is_movable = False
          
    if is_movable:
        return count
    else: return 0    
        
  def bottom_left_move(self, location, player):
    count = 0
    point = list(location)

    
    while point[0] > 0 and point[1] < 7:
      point[0] -= 1
      point[1] += 1
    
    while point[0] <= 7 and point[1] >= 0:
      if self.current_board.map[point[0], point[1]] != 0:
        count += 1
      point[0] += 1
      point[1] -= 1
      
    if location[0] + count > 7 or location[1] - count < 0:
      return 0
    
    if self.current_board.map[location[0] + count, location[1] - count] == player: 
      return 0
    
    is_movable = True
    for i in range(count):
        if self.current_board.map[location[0] + i, location[1] - i] != player and self.current_board.map[location[0] + i, location[1] - i] != 0:
           is_movable = False
          
    if is_movable:
        return count
    else: return 0        
          
  def get_next_state_with_random_choice(self):
    random_choice = random.choice([choice for choice in self.move[:, ]])
    
    next_state = State()
    """
    new_board = Board()
    self.current_board.copy_board(new_board)
    new_board.move_map(random_choice, self.current_player)
    next_state.set_current_board(new_board)
    """
    self.current_board.move_map(random_choice, self.current_player)
    next_state.set_current_board(self.current_board)
    #print(self.current_board.map)
	
    next_state.current_player = abs(self.current_player - 2) + 1 
    
    next_state.set_current_round_index(self.current_round_index + 1)
    next_state.set_cumulative_choices(self.cumulative_choices +
                                      [random_choice])
    #print(random_choice)
    next_state.compute_move_choices()
    return next_state

  def get_next_state_with_move(self, move, player):
    next_state = State()
    new_board = Board()
    self.current_board.copy_board(new_board)
    new_board.move_map(move, player)
    next_state.set_current_board(new_board)
    next_state.current_player = abs(self.current_player - 2) + 1 
    #print(self.current_player)
    
    next_state.set_current_round_index(self.current_round_index + 1)
    next_state.set_cumulative_choices(self.cumulative_choices +
                                      [move])
    next_state.compute_move_choices()
    #print(next_state.move)
    #print(next_state.current_board.map)
    return next_state

  def get_next_state_with_remaining_choice(self):
    available_list = []
    for i in range(np.size(self.move,0)):
      if self.move[i][4] == 0:
        available_list.append(i)
    random_choice = random.choice(available_list)
    self.move[random_choice][4] = 1
    next_state = State()
    new_board = Board()
    self.current_board.copy_board(new_board)
    new_board.move_map(self.move[random_choice], self.current_player)
    next_state.set_current_board(new_board)
    next_state.current_player = abs(self.current_player - 2) + 1
    next_state.set_current_round_index(self.current_round_index + 1)
    next_state.set_cumulative_choices(self.cumulative_choices +
                                      [self.move[random_choice]])
    next_state.compute_move_choices()
    return next_state
  def copy_state(self, new_state):
    self.current_board.copy_board(new_state.current_board)
    new_state.current_player = self.current_player
    new_state.current_round_index = self.current_round_index
    new_state.cumulative_choices = list(self.cumulative_choices)
    new_state.move = np.array(self.move)    