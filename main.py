import curses, os, time
from curses import wrapper
from maptest import Map
from body import Body
from UItimes import ui_times
import concurrent.futures
from endscr import Endscr
import asyncio
        
def main(stdscr):
    level = None
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    #fill background
    window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
    window.bkgd(" ", curses.color_pair(1))
    window.refresh()
    curses.curs_set(0)
    
    global wins
    wins = ui_times(stdscr)

    #get user's choice for the level
    wins.set_startscr()
    #prepare all variables for the game and display
    wins.prepare_all()  

    def resizegame():
        stdscr.clear()
        curses.update_lines_cols()
        wins.show_all()
    
    def rungame(screen):       
        while (screen.game == True) and (screen.t>0):
            if curses.is_term_resized(curses.LINES, curses.COLS):
                resizegame()
            #check if the body's movement is destructive or normal
            screen.movement_checker()
            screen.item_interaction()
            curses.doupdate()

    rungame(wins)
    asyncio.run(wins.end_items())
    ending = Endscr(stdscr)
    
    #in easy/medium level directly show up ending screen
    if wins.level != 'hard':
        if (wins.game == False or wins.t >= 0):
            ending.status = True
        else:
            ending.status = False
        ending.showresult()
        #start new game using recursion if user has chosen new game option
        if ending.newgame == True:
            return main(stdscr)
    
    #in hard level set up hard2 map with time left from the previous map
    elif wins.level == 'hard':
        if (wins.game == False or wins.t >= 0):
            hardergame = ui_times(stdscr)
            hardergame.level = 'hard2'
            hardergame.prepare_all()
            hardergame.t = wins.t
            hardergame.challenge_panel()
            rungame(hardergame)
            asyncio.run(hardergame.end_items())
            #show up ending screen after hard2 map is finished (clear or fail)
            if hardergame.game == False or hardergame.t >= 0:
                ending.status = True
            else:
                ending.status = False
            ending.showresult()
            if ending.newgame == True:
                return main(stdscr)

if __name__ == "__main__":
    try:
        wrapper(main)
    #if system is quit, stop all concurrent.future executors
    except SystemExit:
        wins.executor.shutdown(wait=False, cancel_futures=True)


