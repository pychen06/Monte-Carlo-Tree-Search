import numpy as np

class Board(object):
    
    def __init__(self):
        self.map = np.array([[0,1,1,1,1,1,1,0],
                             [2,0,0,0,0,0,0,2],
                             [2,0,0,0,0,0,0,2],
                             [2,0,0,0,0,0,0,2],
                             [2,0,0,0,0,0,0,2],
                             [2,0,0,0,0,0,0,2],
                             [2,0,0,0,0,0,0,2],
                             [0,1,1,1,1,1,1,0]])
    
        self.width = 8
        self.height = 8
        self.black = np.array([[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[7,1],[7,2],[7,3],[7,4],[7,5],[7,6]])
        self.white = np.array([[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[1,7],[2,7],[3,7],[4,7],[5,7],[6,7]])
        
    def move_map(self, choice, players):
        self.map[int(choice[0]), int(choice[1])] = 0
        self.map[int(choice[2]), int(choice[3])] = players
        self.set_black_white()
        
        
    def get_black(self):
        return self.black
    
    def get_white(self):
        return self.white
    
    def set_black_white(self):
        black = np.array([])
        white = np.array([])
        for i in range(8):
            for j in range(8):
                if self.map[i, j] == 1:
                    black = np.append(black,[i, j])
                    black = black.reshape(-1, 2)
                    black = black.astype(int)
                elif self.map[i, j] == 2:
                    white = np.append(white,[i, j])
                    white = white.reshape(-1, 2)
                    white = white.astype(int)
        
        self.black = black
        self.white = white

    def copy_board(self, new_board):
        new_board.map = np.array(self.map)
        new_board.width = self.width
        new_board.height = self.height
        new_board.black = np.array(self.black)
        new_board.white = np.array(self.white)

    def is_available(self, choice, player):
      move = np.array([])
      if player == 1:
        for i in range(len(self.black)):
          step = self.right_move(self.black[i], player)
          if step != 0:
              move = np.append(move,[self.black[i], [self.black[i][0], self.black[i][1] + step]])
                  
          step = self.left_move(self.black[i], player)
          if step != 0:
              move = np.append(move,[self.black[i], [self.black[i][0], self.black[i][1] - step]])  
            
          step = self.top_move(self.black[i], player)
          if step != 0:
              move = np.append(move,[self.black[i], [self.black[i][0] - step, self.black[i][1]]])
            
          step = self.down_move(self.black[i], player)
          if step != 0:
              move = np.append(move,[self.black[i], [self.black[i][0] + step, self.black[i][1]]])    
              
          step = self.top_right_move(self.black[i], player)
          if step != 0:
              move = np.append(move,[self.black[i], [self.black[i][0] - step, self.black[i][1] + step]])
              
          step = self.top_left_move(self.black[i], player)
          if step != 0:
              move = np.append(move,[self.black[i], [self.black[i][0] - step, self.black[i][1] - step]])    
          
          step = self.bottom_right_move(self.black[i], player)
          if step != 0:
              move = np.append(move,[self.black[i], [self.black[i][0] + step, self.black[i][1] + step]])
              
          step = self.bottom_left_move(self.black[i], player)
          if step != 0:
              move = np.append(move,[self.black[i], [self.black[i][0] + step, self.black[i][1] - step]])    
          
        move = move.reshape(-1, 4)
      else :
        for i in range(len(self.white)):
          step = self.right_move(self.white[i], player)
          if step != 0:
              move = np.append(move,[self.white[i], [self.white[i][0], self.white[i][1] + step]])
                  
          step = self.left_move(self.white[i], player)
          if step != 0:
              move = np.append(move,[self.white[i], [self.white[i][0], self.white[i][1] - step]])  
            
          step = self.top_move(self.white[i], player)
          if step != 0:
              move = np.append(move,[self.white[i], [self.white[i][0] - step, self.white[i][1]]])
            
          step = self.down_move(self.white[i], player)
          if step != 0:
              move = np.append(move,[self.white[i], [self.white[i][0] + step, self.white[i][1]]])    
              
          step = self.top_right_move(self.white[i], player)
          if step != 0:
              move = np.append(move,[self.white[i], [self.white[i][0] - step, self.white[i][1] + step]])
              
          step = self.top_left_move(self.white[i], player)
          if step != 0:
              move = np.append(move,[self.white[i], [self.white[i][0] - step, self.white[i][1] - step]])    
          
          step = self.bottom_right_move(self.white[i], player)
          if step != 0:
              move = np.append(move,[self.white[i], [self.white[i][0] + step, self.white[i][1] + step]])
              
          step = self.bottom_left_move(self.white[i], player)
          if step != 0:
              move = np.append(move,[self.white[i], [self.white[i][0] + step, self.white[i][1] - step]])    
          
      move = move.reshape(-1, 4)
      for i in range(int(np.size(move)/4)):
        if choice[0] == move[i][0] and choice[1] == move[i][1] and choice[2] == move[i][2] and choice[3] == move[i][3]:
          return True
      return False
          
                  
    def right_move(self, location, player):
      count = 0
      for i in range(8):
        if self.map[location[0], i] != 0:
          count += 1
              
      if (location[1] + count) > 7:
         return 0
   
      if self.map[location[0], location[1] + count] == player: 
        return 0
   
      is_movable = True
      for i in range(count):
          if self.map[location[0], location[1] + i] != player and self.map[location[0], location[1] + i] != 0:
             is_movable = False
    
      if is_movable:
          return count
      else: return 0
    
    def left_move(self, location, player):
      count = 0
      for i in range(8):
        if self.map[location[0], i] != 0:
          count += 1
              
      if location[1] - count < 0:
         return 0
   
      if self.map[location[0], location[1] - count] == player: 
        return 0
   
      is_movable = True
      for i in range(count):
          if self.map[location[0], location[1] - i] != player and self.map[location[0], location[1] - i] != 0:
             is_movable = False
    
      if is_movable:
          return count
      else: return 0
        
    def top_move(self, location, player):
      count = 0
      for i in range(8):
        if self.map[i, location[1]] != 0:
          count += 1
              
      if location[0] - count < 0:
         return 0
   
      if self.map[location[0] - count, location[1]] == player: 
        return 0
   
      is_movable = True
      for i in range(count):
          if self.map[location[0] - i, location[1]] != player and self.map[location[0] - i, location[1]] != 0:
             is_movable = False
    
      if is_movable:
          return count
      else: return 0
    
    def down_move(self, location, player):
      count = 0
      for i in range(8):
        if self.map[i, location[1]] != 0:
          count += 1
              
      if location[0] + count > 7 :
        return 0

      if self.map[location[0] + count, location[1]] == player: 
        return 0
   
      is_movable = True
      for i in range(count):
        if self.map[location[0] + i, location[1]] != player and self.map[location[0] + i, location[1]] != 0:
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
        if self.map[point[0], point[1]] != 0:
          count += 1
        point[0] -= 1
        point[1] += 1
      
      if location[0] - count < 0 or location[1] + count > 7:
        return 0
    
      if self.map[location[0] - count, location[1] + count] == player: 
        return 0
    
      is_movable = True
      for i in range(count):
          if self.map[location[0] - i, location[1] + i] != player and self.map[location[0] - i, location[1] + i] != 0:
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
        if self.map[point[0], point[1]] != 0:
          count += 1
        point[0] -= 1
        point[1] -= 1
      
      if location[0] - count < 0 or location[1] - count < 0:
        return 0
    
      if self.map[location[0] - count, location[1] - count] == player: 
        return 0
    
      is_movable = True
      for i in range(count):
          if self.map[location[0] - i, location[1] - i] != player and self.map[location[0] - i, location[1] - i] != 0:
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
        if self.map[point[0], point[1]] != 0:
          count += 1
        point[0] += 1
        point[1] += 1
      
      if location[0] + count > 7 or location[1] + count > 7:
        return 0
    
      if self.map[location[0] + count, location[1] + count] == player: 
        return 0
    
      is_movable = True
      for i in range(count):
        if self.map[location[0] + i, location[1] + i] != player and self.map[location[0] + i, location[1] + i] != 0:
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
        if self.map[point[0], point[1]] != 0:
          count += 1
        point[0] += 1
        point[1] -= 1
      
      if location[0] + count > 7 or location[1] - count < 0:
        return 0
    
      if self.map[location[0] + count, location[1] - count] == player: 
        return 0
    
      is_movable = True
      for i in range(count):
          if self.map[location[0] + i, location[1] - i] != player and self.map[location[0] + i, location[1] - i] != 0:
             is_movable = False
          
      if is_movable:
          return count
      else: return 0 