import curses, sys, time

class Endscr:
    menu = ['New game', 'Exit']
    choice = False 
    newgame = False
    #decide if user cleared the game or failed
    status = None

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        curses.start_color()
        #unlike body receive user's input 1 by 1
        self.stdscr.nodelay(False)
        curses.cbreak(True)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        window.bkgd(" ", curses.color_pair(1))
        window.refresh()

    def showresult(self):
        if self.status == True:
            self.show_success()
        else:
            self.show_timeover()
        self.user_choice()

    #display success ascii art to the screen
    def show_success(self):
        self.stdscr.clear()
        txt = self.success()
        try:
            x = (curses.COLS-len(txt[0]))//2-curses.COLS//5
            for y, line in enumerate(txt):
                self.stdscr.addstr(y, x, line)
            self.stdscr.refresh()
            time.sleep(2)
        except:
            pass

    def success(self):
        success = """   
⣿⣿⣿⣿⣿⡿⠿⠛⠛⠛⠛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⣽⣿⣿⣿
⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢰⣿⣿⣿⣿
⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⠟⠁⠏⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⡿⢫⡿⠋⠉⠉⢻⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿
⡟⠀⠀⠀⠀⢀⣠⣤⣦⣤⡀⢿⣿⣿⣿⣿⣿⡁⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⠟⠁⠈⠀⠀⠀⠀⢾⣿⣿⡏⠀⢸⡿⠋⣽⣿⣿
⠇⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⢰⡟⠀⢸⣿⣿⣿⣿⣿⣿⡀⠀⣴⠎⠀⠀⣤⠀⢹⣿⠇⠀⠉⠀⠀⠉⠀⠈
⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠉⠉⠛⢿⠀⠀⢸⡇⠀⣿⣿⠋⠀⠀⠈⡿⠃⠀⣿⣄⣀⣼⣿⠀⠀⠁⠀⠀⣤⠄⠀⣠⣶⣴
⡇⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⠏⠀⠀⣀⡀⠀⠀⠀⠀⢸⡇⠀⠹⠇⠀⣠⡀⠀⠀⣸⠀⣿⡿⠋⠉⠀⠀⠐⣿⠀⢰⣿⡆⠀⢿⣿⣿
⣿⡀⠀⠀⠀⠙⠛⠛⠛⠋⠁⠀⠀⢠⣿⣷⡀⠀⠀⠀⣾⣇⠀⠀⠀⠀⣿⣇⠀⢠⡇⠀⢻⠀⢰⣾⠇⠀⠀⠿⠀⢸⠻⢿⣄⠈⠛⣿
⣿⣿⣤⡀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠈⣿⣿⡇⠀⠀⡀⣿⣿⣄⠀⠀⠀⢻⠇⠀⡼⠀⠀⢸⠀⠘⠉⠀⡀⠀⠀⠀⢸⡆⠀⢾⠆⠀⠈
⣿⣿⣿⣿⣿⣶⣶⣶⣾⣿⣿⠀⠀⠀⠘⠋⠀⠀⢠⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⣥⣶⣦⣬⣷⣶⣶⣿⣿⣶⣦⠀⠈⢿⡀⠀⠀⠀⣠
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⠀⠀⠀⠀⣠⣿⣿⠟⠀⣿⣿⣿⣶⣶⡆⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠈⠻⢷⣶⣾⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣿⣿⣟⠁⠀⠀⠘⣿⣿⣿⣿⠃⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⢩⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠘⢿⣿⠏⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⢀⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⢸⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⢀⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡶⢾⣿⣿⣿"""
        return success.split('\n')

    #display gameover ascii art to the screen
    def show_timeover(self):
        txt = self.gameover()
        try:
            x = (curses.COLS-len(txt[0]))-curses.COLS//5
            for y, line in enumerate(txt):
                self.stdscr.addstr(y, x, line)
            self.stdscr.refresh()
            time.sleep(2)
        except:
            pass  

    def gameover(self):
        gameover = """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⠋⠉⠉⠉⠉⠁⠀⠀⠉⠉⠉⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠀⠀⢀⣀⣤⣤⣴⣶⣶⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠈⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⣀⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄⠀⠀⠉⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠙⢿⣿⡿⠟⠛⠉⢻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⢉⣉⣤⣤⣴⣶⣶⣤⣤⣌⣉⡛⠻⢿⣿⣿⣿⣿⣿⣿⣿⠿⠗⠀⠀⠀⢀⣀⣤⣤⡀⠀⢿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⣡⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡉⠻⠟⠛⠉⠉⢀⣀⣠⣤⣶⣾⡿⠿⣿⣿⣧⠀⠸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⠟⢁⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠋⠉⠁⠀⣀⣠⣴⣶⣿⡿⠿⠋⢋⠁⠀⠀⠀⠈⢻⣿⡆⠀⢻⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⠁⠀⣸⣿⣿⣿⣿⣿⣿⣿⠋⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠉⠁⠀⣀⣤⣴⣶⣿⣿⣿⡟⠉⠁⠀⠀⣀⣠⣼⡆⠀⢻⣷⠀⠘⣿⣿⠀⠘⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠃⠀⢰⣿⣿⣿⣿⣿⣿⣿⠃⣴⣿⣿⣿⡿⠿⠛⠛⠉⠁⢀⣀⣤⣤⣶⣾⡿⠛⠛⠻⣇⠀⠹⣿⣇⠀⢸⡀⠘⣿⡿⠟⣷⠀⠈⠉⠀⢰⣿⣿⣇⠀⠸⣿⣿
⣿⣿⣿⣿⣿⡟⠀⠀⣾⣿⣿⣿⣿⣿⣿⠇⠰⠟⠛⠉⠀⢀⣀⣠⣤⣶⣿⣿⣿⣿⣿⣿⣿⠁⠀⣄⠀⠘⣆⠀⠹⣿⠀⢸⣇⠀⠀⠀⣀⣸⣇⠀⢰⡄⠀⠹⣿⣿⡀⠀⢿⣿
⣿⣿⣿⣿⣿⡇⠀⢠⣿⣿⠿⠟⠋⠉⠀⠀⣀⣠⣴⣶⣿⡿⠟⠛⠉⠁⠘⣿⣿⣿⣿⣿⣿⠀⠀⣿⣷⠀⠘⣧⠀⠹⠀⠀⣿⡄⠀⢻⣿⣿⠿⡄⠀⢿⣦⠀⠈⣻⣧⠀⠘⣿
⣿⣿⣿⡿⠿⠁⠀⠈⠁⢀⣀⣤⣴⣶⣿⣿⠛⠛⣿⡇⠀⢳⠀⠀⣴⣶⣾⣿⣿⣿⣿⣿⣿⣇⠀⠸⣿⡇⠀⢸⣧⠀⠁⠀⣿⣷⠀⠈⠁⠀⢀⣑⣤⣼⣿⡿⠿⠟⠛⠁⠀⣻
⠋⠉⠁⢀⣀⣤⣤⣶⣾⣿⣿⣿⠉⠀⠹⣿⡆⠀⠘⠇⠀⠘⣇⠀⠙⠛⠉⠹⣿⣿⣿⣿⣿⣿⡄⠀⠻⡿⠀⢸⣿⣧⠀⠀⢹⣿⣧⣤⣶⣾⠿⠟⠛⠉⠁⠀⣀⣠⣤⣶⣾⣿
⡆⠀⠸⣿⣿⣿⠋⠀⠀⠈⢻⣿⡆⢀⠀⠹⣷⠀⠀⠀⠀⡀⠹⡄⠀⣠⣴⣶⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⢀⣼⣿⣿⣿⣿⠿⠟⠋⠉⠀⠀⣀⣠⣴⡖⠀⠀⣿⣿⣿⣿⣿⣿
⣿⡀⠀⢿⣿⣿⠀⠠⣷⣤⣴⣿⡇⠀⣷⠀⠹⣇⠀⠄⠀⢁⠀⢳⠀⠸⠿⠛⠋⢹⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠉⠁⠀⣀⠀⣤⣶⣾⣿⣿⣿⣿⡇⠀⢠⣿⣿⣿⣿⣿⣿
⣿⣇⠀⠘⣿⣿⡄⠀⣿⠉⠁⠘⣧⠀⠈⠁⠀⠹⡀⠘⣶⣾⡄⠘⡆⠀⢀⣀⣤⣼⣿⡿⠿⠛⠋⠉⢁⢀⣠⣴⣤⣶⣾⣿⠏⣰⣿⣿⣿⣿⣿⣿⣿⠀⠀⣸⣿⣿⣿⣿⣿⣿
⣿⣿⡆⠀⢻⣿⣷⠀⠘⣦⣦⠀⢹⠀⠠⣶⣧⠀⠁⠀⢹⣿⣿⣤⣾⡿⠿⠟⠛⠉⠀⢀⣀⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⠋⣠⣿⣿⣿⣿⣿⣿⣿⠇⠀⢰⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⠀⠈⣿⣿⣧⠀⠈⠋⠀⢰⠀⢀⣿⣿⣷⣶⡿⠿⠟⠋⠉⠀⢀⣀⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢁⣴⣿⣿⣿⣿⣿⣿⣿⠏⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣇⠀⢹⣿⣿⣷⣤⣤⣴⣿⡿⠿⠛⠋⠉⠀⢀⣀⠀⠴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢁⣴⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡄⠀⢻⡿⠿⠛⠋⠉⠀⣀⣀⣤⣴⣶⣿⣿⣿⣷⣦⣌⡙⠛⠿⠿⣿⣿⣿⣿⣿⡿⠿⠟⠛⣉⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣷⠀⠀⢀⣀⣤⣦⡀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣦⣤⣤⣤⣤⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⡀⠀⠈⠙⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠉⠀⠀⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⣀⠀⠀⠀⠀⠈⠉⠉⠉⠁⠀⠀⠀⠀⢀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"""
        return gameover.split('\n')

    #highlight the user's chosen option from the menu list
    def show_end(self, selected_row_idx): 
        self.stdscr.clear()         
        for idx, row in enumerate(self.menu):       
            maxy, maxx = curses.LINES, curses.COLS  
            y= maxy//2-len(self.menu)//2+idx        
            x=maxx//2-len(self.menu[idx])//2
            #highlight the relevant option    
            if idx == selected_row_idx:                    
                self.stdscr.attron(curses.color_pair(6))    
                self.stdscr.addstr(y, x, row)              
                self.stdscr.attroff(curses.color_pair(6))
            else:
                self.stdscr.addstr(y, x, row)   
        try:   
            txt = 'press keys to go for next game or quit'
            self.stdscr.addstr(y+curses.LINES//10, maxx//2-len(txt)//2, txt) 
        except:
            pass
        self.stdscr.refresh()

    #track user's change in option choice and store the index
    def user_choice(self): 
        self.stdscr.keypad(True)
        current_row_idx = 0
        self.show_end(current_row_idx) 
        while self.choice == False:     
            key = self.stdscr.getch()   
            self.stdscr.clear()
            #change index depending on user's key press and highlight the corresponding option       
            if key == curses.KEY_UP and current_row_idx>0: 
                current_row_idx-=1
                self.show_end(current_row_idx)
                self.stdscr.refresh()
            elif key==curses.KEY_DOWN and current_row_idx<len(self.menu)-1: 
                current_row_idx+=1
                self.show_end(current_row_idx)
                self.stdscr.refresh()
            #if enter pressed, store the level chosen 
            elif key == curses.KEY_ENTER or key in [10, 13]: 
                #if exit is chosen, quit the game
                if current_row_idx == len(self.menu)-1:      
                    sys.exit()
                self.stdscr.clear()
                curses.beep() 
                self.newgame = True                              
                self.choice = True 
            #ignore any other key press/operations                         
            else:
                self.show_end(current_row_idx)            
                self.stdscr.refresh()

