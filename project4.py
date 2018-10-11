#Yongxuan Fu ICS32A Project4

#This moodule impelments the user interface

import columns_game


def _get_input() ->(list,list):
    '''
    This function store the input from user and return the list of size of the field and the 2d list
    of field.
    
    The row of the field will be created three more than what user want.
    
    If there have contents, it will store in the 2d list of field and return it.
    
    if there have contents, it will return an empty 2d list of field and return it.
    '''
    row_num = int(input())
    column_num = int(input())
    filed_size = []
    filed_size = [row_num,column_num]
    initial_field = input()
    field_list =[]
    for row in range(row_num+3):
        field_list.append([])
        for column in range(column_num):
            field_list[-1].append('   ')
    if initial_field == 'CONTENTS':
        for row in range(3,row_num+3):
            content_row = input()
            for column in range(column_num):
                if content_row[column] != ' ':
                    field_list[row][column] = ' '+ content_row[column]+ ' '


    return filed_size,field_list


def user_inter() ->None:
    '''
    This function will be the main function for running the whole project.
    '''
    field_size,field_list = _get_input()
    game = columns_game.Game(field_size,field_list)
    while True:
        try:
            #If the game is over, a exception GameOverError will raise and will break the loop and
            #end the game
            game.draw_board()
        except:
            break

        command = input()
        command_list = command.split()
        try:
            #If the command is a space, it means the timer and in my program will go the fall function.
            if command_list == []:
                game.fall()

            elif command_list[0] == 'F':
                column_num = int(command_list[1])
                faller_list = command_list[2:]
                game.command(faller_list,column_num)
                game.fall()
            elif command_list[0] == 'R':
                game.rotate()
            elif command_list[0] == '<':
                game.move_left()
            elif command_list[0] == '>':
                game.move_right()
            elif command_list[0] == 'Q':
                break
            else:
                pass
            game.match()
        #If there is a invalid movement or invalid column number, exceptions will be raise and pass it.
        except:
            pass

            
if __name__ == "__main__":
    user_inter()
        
