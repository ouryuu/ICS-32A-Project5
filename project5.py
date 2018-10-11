#Yongxuan Fu ICS 32A Project5

import pygame
import columns_game

BLACK = (0,0,0)
DARK_GREY = (150,150,150)
LITTER_GREEN =(175,255,0)

class GameWindow():
    def __init__(self):
        self._columns_game = columns_game.Game()
        self._running = True

        self._topleft_frac_x = 50/400
        self._topleft_frac_y = 50/700

        self._bottomleft_frac_x = 50/400
        self._botomleft_frac_y = 650/700

        self._cell_length_frac_x = 50/400
        self._cell_length_frac_y = 50/700

        self._color_dict = dict()
        self._color_dict = {'A':pygame.image.load('A.png'),'B':pygame.image.load('B.png'),\
                      'C':pygame.image.load('C.png'),'D':pygame.image.load('D.png'),\
                      'E':pygame.image.load('E.png'),'F':pygame.image.load('F.png'),\
                      'G':pygame.image.load('G.png'),'H':pygame.image.load('H.png'),\
                      'I':pygame.image.load('I.png'),'J':pygame.image.load('J.png'),\
                            'M':pygame.image.load('check.png'),'GameOver':pygame.image.load('GO.png')}
        self._game_over = False

        
    def run(self):
        pygame.init()
        self._resize_surface((400,700))
        clock = pygame.time.Clock()
        
        while self._running:
            clock.tick(5)
            self._fall()
            self._handle_events_and_keys()
            self._matching()
            try:
                self._columns_game.board()
            except:
                self._end_game()

            if self._game_over == False:
                self._redraw()
            else:
               surface = pygame.display.get_surface()
               surface.blit(self._color_dict['GameOver'],(0,0))
               surface.flip()
               

        
        pygame.quit()
            


    def _handle_events_and_keys(self) ->None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._move_to_left()

                if event.key == pygame.K_RIGHT:
                    self._move_to_right()

                if event.key == pygame.K_SPACE:
                    self._rotate()

                
    def _fall(self):
        try:
            self._columns_game.command()
        except:
            pass
        self._columns_game.fall()

    def _move_to_left(self):
        try:
            self._columns_game.move_left()
        except:
            pass

    def _move_to_right(self):
        try:
            self._columns_game.move_right()
        except:
            pass

    def _rotate(self):
        self._columns_game.rotate()

    def _matching(self):
        self._columns_game.match()

    def _redraw(self):
        surface = pygame.display.get_surface()
       
        width = surface.get_width()
        height = surface.get_height()

        topleft_pixel_x = self._topleft_frac_x * width
        topleft_pixel_y = self._topleft_frac_y * height
        
        surface.fill(pygame.Color(225,225,225))


        for y in range(12):
            for x in range(7):
                rect_upperleft_pixel_x = width*(self._topleft_frac_x + x*self._cell_length_frac_x)
                rect_upperleft_pixel_y = height*(self._topleft_frac_y + y*self._cell_length_frac_y)

                cell_length_pixel_x = width*self._cell_length_frac_x
                cell_length_pixel_y = height*self._cell_length_frac_y
            
                pygame.draw.rect(surface,DARK_GREY,\
                             [rect_upperleft_pixel_x,rect_upperleft_pixel_y,cell_length_pixel_x,cell_length_pixel_y],2)

        
        current_board = self._columns_game.current_board()
        
        
        for row in range(14,2,-1):
            for col in range(6):
                cell_content = current_board[row][col]
                cell_state = cell_content[0]
                jewel = cell_content[1]
                if jewel != ' ':
                    cell_upperleft_pixel_x = width*(self._topleft_frac_x + col*self._cell_length_frac_x)
                    cell_upperleft_pixel_y = height*(self._topleft_frac_y + (row-3)*self._cell_length_frac_y)
                    
                    image_surface = pygame.transform.scale(self._color_dict[jewel],\
                                                           (int(width*self._cell_length_frac_x),\
                                                            int(height*self._cell_length_frac_y)))
        
                    surface.blit(image_surface,(cell_upperleft_pixel_x,cell_upperleft_pixel_y))

                    if cell_state == '|':
                        pygame.draw.rect(surface,LITTER_GREEN, [cell_upperleft_pixel_x,cell_upperleft_pixel_y,\
                                                                width*self._cell_length_frac_x,\
                                                                height*self._cell_length_frac_y], 5)
                    if cell_state == '*':
                        surface.blit(self._color_dict['M'],(cell_upperleft_pixel_x,cell_upperleft_pixel_y))
                        
        


        pygame.display.flip()

        
        
    def _end_game(self) ->None:
        self._running = False

    def _resize_surface(self,size:(int,int))->None:
        pygame.display.set_mode(size, pygame.RESIZABLE)





if __name__ == '__main__':
    GameWindow().run()
