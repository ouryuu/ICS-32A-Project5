#Yongxuan Fu ICS32A Project4

import random

GAME_OVER = 'GAME OVER'

class InvalidMoveError():
    pass

class NoneExistColumn():
    pass

class GameOverError():
    pass

class NotOnlyOneFallerError():
    pass

class Game:
    def __init__(self):

        self._faller_list = []
        self._faller_column_num = 0
        self._the_lowest_row_of_faller = 2
        self._num_row_of_board = 12
        self._num_column_of_board = 6
        field_list =[]
        for row in range(15):
            field_list.append([])
            for column in range(7):
                field_list[-1].append('   ')
        self._current_board = field_list
        self._matching_list = []

        
        self._if_falling = False
        self._if_frozing = False
        self._if_landing = False
        self._if_matching = False
        self._game_is_over = False
        self._removing_cell =False
        

    def command(self) ->None:
        '''
        This funtion only run when the user call for a faller.
        
        This function will collect the information of the faller and put the
        faller into the first three row of the current board which is not visible
        
        Also it will raise exceptions if there have errors.
        
        '''
        if self._if_falling == False and self._if_landing == False and\
           self._if_frozing == False and self._if_matching == False and\
           self._removing_cell == False:
            color_list = ['A','B','C','D','E','F','G','H','I','J']
            faller_list = []
            for x in range(3):
                faller_list.append(random.choice(color_list))
            self._faller_list = faller_list
            self._faller_column_num = random.randint(0,5)       
            self._the_lowest_row_of_faller = 2
            self._if_falling = True
        
            for row in range(0,3):
                self._current_board[row][self._faller_column_num] = '['+ self._faller_list[row] + ']'

        else:
            raise NotOnlyOneFallerError


    def check_if_game_over(self) ->bool:
        '''
        This function will check if the game over and return the varible
        _game_is_over, if there is any cell on the invisible third row which
        exceed the visible game board row, then the game_is_over will be true.
        '''
        
        if self._if_landing:
            for column in range(self._num_column_of_board):
                if self._current_board[2][column] != '   ':
                    self._game_is_over = True

        return self._game_is_over

        
    def move_left(self) ->None:
        '''
        This function will make the faller move to left if possible.

        This function only can be run if the faller is falling.

        If it cannot move to left, there will be an InvalidMoveError exception
        raised
        '''
         
        if self._if_falling:
            if self._faller_column_num == 0:
                raise InvalidMoveError()

            if self._current_board[self._the_lowest_row_of_faller][self._faller_column_num-1] != '   ':
                raise InvalidMoveError()
            else:
                self._faller_column_num -= 1
                num = 0
                for row in range(self._the_lowest_row_of_faller-2,self._the_lowest_row_of_faller+1):
                    self._current_board[row][self._faller_column_num+1] = '   '
                    self._current_board[row][self._faller_column_num] = '['+ self._faller_list[num] + ']'
                    num +=1


    def move_right(self) ->None:
        '''
        This function will make the faller move to right if possible.

        This function only can be run if the faller is falling.

        If it cannot move to right, there will be an InvalidMoveError exception
        raised
        '''
         

        if self._if_falling:
            if self._faller_column_num == self._num_column_of_board-1:
                raise InvalidMoveError()
            if self._current_board[self._the_lowest_row_of_faller][self._faller_column_num+1] !='   ':
                raise InvalidMoveError()
            else:
                self._faller_column_num += 1
                num = 0
                for row in range(self._the_lowest_row_of_faller-2,self._the_lowest_row_of_faller+1):
                    self._current_board[row][self._faller_column_num-1] = '   '
                    self._current_board[row][self._faller_column_num] = '['+ self._faller_list[num] + ']'
                    num +=1



    def rotate(self) ->None:
        '''
        This function will make the faller rotation - the bottom will be the top

        This function only can be run if the faller is falling.

        '''

        if self._if_falling:
            temp = self._faller_list[2]
            self._faller_list.remove(self._faller_list[2])
            self._faller_list.insert(0,temp)

            num = 0
            for row in range(self._the_lowest_row_of_faller-2,self._the_lowest_row_of_faller+1):
                self._current_board[row][self._faller_column_num] = '['+ self._faller_list[num] + ']'
                num +=1

    
    def fall(self) ->None:
        '''
        This function will fall the faller if not landing.

        This function will change situations, if there is the faller is landind,
        the _if_landing will be True

        If there if no matching and faller is landing, the if_frozing will be
        True

        If there have matching cells, it the _removing_cell will be true
        '''
        
        if self._find_bottom_empty_row_in_column() != -1:
            for row in range(self._the_lowest_row_of_faller,self._the_lowest_row_of_faller-3,-1):
                temp = self._current_board[row][self._faller_column_num]
                self._current_board[row][self._faller_column_num] = '   '
                self._current_board[row+1][self._faller_column_num] = temp

            self._the_lowest_row_of_faller += 1
    
        else:
            
            if self._if_landing:
                self._if_landing = False
                self._if_frozing = True
    
                
            if self._if_falling:
                self._if_falling = False
                self._if_landing = True




            
    def _find_bottom_empty_row_in_column(self) ->int:
        '''
        Determines the bottommost empty row within a given column
        if the entire column in filled with cells, this function returns -1
        '''
        
        for row in range(self._num_row_of_board+2,self._the_lowest_row_of_faller,-1):
            if self._current_board[row][self._faller_column_num] == '   ':
                return row
        return -1

    def match(self) ->None:
        '''
        This function will check if there is any matching cells when the faller
        is landing and the game is not over. And then the function will record
        all the row and column of the matching cell store into _matching_list
        
        If there have mathching cells the if_matching and _removing_cell
        will be True.

        When _removing_cell if True, it will remove all the matching cell and
        become False when it finish

        The _if_matching will be True until there are no matching cells on the
        board
        '''
        if self._removing_cell:
            change_column_list = []
            for row,column in self._matching_list:
                if column not in change_column_list:
                    change_column_list.append(column)
                self._current_board[row][column] = '   '
                
            for column in change_column_list:
                temp = []
                last_row =self._num_row_of_board+2 
                for row in range(last_row,0,-1):
                    if self._current_board[row][column] != '   ':
                        temp.append(self._current_board[row][column])
                        self._current_board[row][column] = '   '

                cell_amount = len(temp)

                if cell_amount !=0:
                    n = 0
                    for row in range(last_row,last_row - cell_amount,-1):
                        self._current_board[row][column] = temp[n]
                        n +=1
            self._matching_list = []
            
        
        if self._if_frozing or self._if_matching:
            
            test_list = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
            for x,y in test_list:
                for row in range(self._num_row_of_board+2,2,-1):
                    for column in range(self._num_column_of_board):
                        match_count = self._match_in_a_row(row, column, x, y)
                        if match_count != -1:
                            for i in range(0,match_count+1):
                                self._matching_list.append([row + i*x,column+i*y])
                                
            temp = []
            for row_col in self._matching_list:
                if row_col not in temp:
                    temp.append(row_col)

            self._matching_list = temp


            if len(self._matching_list) >0:
                if self._if_frozing:
                    self._if_matching = True
                if self._if_matching:
                    pass
                self._removing_cell = True
            else:
                self._if_matching = False
                self._removing_cell = False

    
                


    def _match_in_a_row(self,row:int,col:int,rowx:int,colx) ->int:
        '''
        Returns -1 if there is no matching cells

        If there have matching cells, it will return the number of cells that
        matched
        '''
        #the maximun number of matching cells(a line) will be the maximum between
        #the row and the column of the board
        max_num =max(self._num_row_of_board,self._num_column_of_board)
        cell = self._current_board[row][col][1]
        if cell == ' ':
            return -1
        else:
            n = 0
            for i in range(1,max_num):
                if self._is_valid_column_number(col + colx * i) \
                        and self._is_valid_row_number(row + rowx * i):
                    if self._current_board[row + rowx * i][col + colx *i][1] ==cell:
                        n +=1
                    else:
                        if n < 2:
                            return -1
                        else:
                            return n
            if n < 2:
                return -1
            else:
                return n
                    

    def _is_valid_column_number(self,col:int) ->bool:
        '''return true if the column number is valid'''
        
        return 0<= col <self._num_column_of_board


    
    def _is_valid_row_number(self,row:int) ->bool:
        '''return true if the row number is valid'''
         
        return 3<= row < self._num_row_of_board+3

    def current_board(self) ->list:
        return self._current_board

    


    def board(self) ->None:
        '''
        This function will draw the current board and change the specifc cells
        base on the different situations

        If the faller is landing and game is over, an exception GameOverError
        will raised.
        
        '''
        
        if self._if_falling:
            pass

        if self._if_frozing:
            num = 0
            for row in range(self._the_lowest_row_of_faller-2,self._the_lowest_row_of_faller+1):
                cell_content = self._current_board[row][self._faller_column_num][1]
                self._current_board[row][self._faller_column_num] = ' '+ cell_content + ' '
            self._if_frozing = False
        
        if self._if_landing:
            for row in range(self._the_lowest_row_of_faller-2,self._the_lowest_row_of_faller+1):
                cell_content = self._current_board[row][self._faller_column_num][1]
                self._current_board[row][self._faller_column_num] = '|'+ cell_content + '|'       
        
        if self._if_matching:
            for row,column in self._matching_list:
                cell_content = self._current_board[row][column].strip()
                self._current_board[row][column] = '*'+ cell_content + '*'

                

        for row in range(3,self._num_row_of_board + 3):
            print('|',end = '')
            for column in range(self._num_column_of_board):
                print(self._current_board[row][column],end = '')
            print('|')

        print(' '+ self._num_column_of_board*'---'+ ' ')

        

        if self._if_landing:
            if self.check_if_game_over():
                print(GAME_OVER)
                raise GameOverError()
                
        
        
    
