import curses, time, sys 

class Startscr:      
    level = None   
    menu = ['easy', 'medium', 'hard', 'exit']
    choice = False 

    def __init__(self, stdscr):     
        self.stdscr = stdscr         
        self.stdscr.keypad(True)   
        curses.curs_set(0)         
        curses.start_color()        
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN) 
    
    #highlight the user's chosen option from the menu list
    def show_start(self, selected_row_idx):     
        self.stdscr.clear()     
        for idx, row in enumerate(self.menu):       
            maxy, maxx = curses.LINES, curses.COLS  
            y= maxy//2-len(self.menu)//2+idx        
            x=maxx//2-len(self.menu[idx])//2  
            #highlight the relevant option       
            if idx == selected_row_idx:                    
                self.stdscr.attron(curses.color_pair(1))    
                self.stdscr.addstr(y, x, row)              
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)  
        try:    
            self.stdscr.addstr(y+3, x-12, 'press keys to select the level') 
        except:
            pass
        self.stdscr.refresh()     

    #track user's change in option choice and store the index 
    def user_choice(self): 
        current_row_idx = 0
        self.show_start(current_row_idx) 
        while self.choice == False:     
            key = self.stdscr.getch()   
            self.stdscr.clear() 
            #change index depending on user's key press and highlight the corresponding option       
            if key == curses.KEY_UP and current_row_idx>0: 
                current_row_idx-=1
                self.show_start(current_row_idx)
                self.stdscr.refresh()
            elif key==curses.KEY_DOWN and current_row_idx<len(self.menu)-1: 
                current_row_idx+=1
                self.show_start(current_row_idx)
                self.stdscr.refresh()
            #if enter pressed, store the level chosen
            elif key == curses.KEY_ENTER or key in [10, 13]: 
                #if exit is chosen, quit the game
                if current_row_idx == len(self.menu)-1:     
                    sys.exit()
                self.stdscr.clear()
                self.level = self.menu[current_row_idx]    
                curses.beep()                              
                self.choice = True  
            #ignore any other key press/operations                       
            else:
                self.show_start(current_row_idx)           
                self.stdscr.refresh()


