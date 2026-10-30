import curses, collections, time, sys, os
from curses import wrapper
from maptest import Map
from collections import deque
from items import Items

class Body: 
    body = '©' 
    gamemap = [] 
    bodydq = deque([])
    #declaring variables related to body vectors
    change_y, change_x = 0, 0 
    start_x, start_y = 1,1 
    mapy, mapx = 0,0
    y, x = start_y, start_x 
    #number of key collected during the game
    keycollect = 0
    #variables to be class objects are initialised as None
    _map = None
    _item = None
    level = None
    key = None
    #assign vector values to each direction
    KEY_TO_DIR = {
    curses.KEY_UP : (-1, 0), curses.KEY_DOWN : (1, 0),
    curses.KEY_LEFT: (0,-1), curses.KEY_RIGHT: (0, 1),
    ord('w'):(-1,0),
    ord('s'):( 1,0),
    ord('a'):( 0,-1),
    ord('d'):( 0, 1)} 

    def __init__(self, stdscr):
        self.stdscr = stdscr 
        self.stdscr.keypad(True)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        #create private objects
        self._map = Map(self.stdscr)
        self._item = Items(self.stdscr)
    
    def _get_map(self):
        return self._map.generate_map(self.level)
    
    #add body to its starting position of the screen
    def start(self):
        self.stdscr.addstr(self.start_y, self.start_x-1, self.body, curses.color_pair(2))
        self.stdscr.addstr(self.start_y, self.start_x, self.body, curses.color_pair(2))
        self.stdscr.noutrefresh(self.mapy, self.mapx, 0, 1, (curses.LINES//5)*3-1, curses.COLS//2-1)

    def set_bodydq(self):
        self.bodydq.append((self.start_y, self.start_x-1))
        self.bodydq.append((self.start_y, self.start_x))

    #getting direction vector from the dictionary. Quit the game if input is q
    def getdir(self):
        self.stdscr.nodelay(True)
        key = self.stdscr.getch()
        curses.napms(60)
        if key == ord('q'):
            sys.exit()
        else:
            if key in self.KEY_TO_DIR:
                return self.KEY_TO_DIR[key]
            else:
                return (0, 0)

    def add_vectors(self):
        self.y+=self.change_y
        self.x+=self.change_x
    
    def sub_vectors(self):
        self.y-=self.change_y
        self.x-=self.change_x

    #return True if body can move in to the specific vector position
    def check_empty(self):
        try:
            if self.gamemap[self.y][self.x] in self._map.empty or self.gamemap[self.y][self.x].isalnum():
                return True
            else:
                return False
        except IndexError or curses.error:
            return False

    #in case bat is used, modify wall/obstacles in body's vector position as empty space
    def modify_map(self):
        tempmap = [x for x in self.gamemap[self.y]]
        tempmap[self.x] = ' '
        self.gamemap[self.y] = tempmap
            
    #check if body is inside the map
    def check_map(self):
        if 0<self.y<len(self.gamemap)-2 and 0<self.x<len(self.gamemap[0])-1:
            return True

    #check if body can added to the desired vector position of the screen
    def check_dimension(self):
        try:
            self.stdscr.addstr(self.y, self.x, self.body, curses.color_pair(2))
            return True
        except curses.error or Exception:
            return False

    #update left top corner position of the map to be displyed in the mappad along body's movement
    def map_trackmove(self):
        self.stdscr.redrawln(0, self.stdscr.getmaxyx()[0])
        y_dimension = self.y+((curses.LINES//5)*3-2)
        x_dimension = self.x+((curses.COLS//2-1))

        move_check = (((len(self.gamemap)-y_dimension)>0), (len(self.gamemap[0])-x_dimension)>0)

        #y/x vector for the map display in the mappad is only updated if 
        #vertical/horizontal length of the map is longer than the size of the mappad's display
        if move_check[0] ==1 and not move_check[1]==1:
            self.mapy = self.y
        elif not move_check[0] ==1 and move_check[1]==1:
            self.mapx = self.x
        else:
            pass
        
        if move_check[0]==1:
            #refresh mappad with minimum distance of 3 liens from the top/bottom of the map
            self.stdscr.noutrefresh(self.mapy-3, self.mapx, 0, 1, (curses.LINES//5)*3-1, curses.COLS//2-1)
            curses.napms(60)
        else:
            self.stdscr.noutrefresh(self.mapy, self.mapx, 0, 1, (curses.LINES//5)*3-1, curses.COLS//2-1)
            curses.napms(60)
    
    #this function is responsible for body's basic movement mechanism: can go or back, but cannot pass through its own body
    def go_or_back(self):
        try:
            #allow reverse movement using pop of the deque. The popped index is re-filled as a gamemap
            if self.bodydq[-2] == (self.y, self.x) and self.bodydq[-2]!=(self.start_y, self.start_x):
                redraw = self.bodydq.pop()
                y, x = redraw
                self.stdscr.addstr(int(y), int(x), self.gamemap[int(y)][int(x)])
                #left top corner of the map is updated along body's movement
                self.map_trackmove()
            else:
                #if not a reversed movement just add body to the deque and the map
                if (self.y, self.x) not in self.bodydq and self.check_dimension():
                    self.bodydq.append((self.y, self.x))
                    self.map_trackmove()
                else:
                    #if movement is ignored, return to the previous vectors
                    self.sub_vectors()
        except IndexError:
            return


    #default movement for the body; check if the desired map position is empty, then move
    def trymove(self):
        self.change_y, self.change_x = self.getdir()
        self.add_vectors()
        if self.check_empty():
            self.go_or_back()      
        else:
            self.sub_vectors()

    #body's movement during bat's effect; move anywhere in the map, ignoring walls
    def break_everything(self):
        self.change_y, self.change_x = self.getdir()
        self.add_vectors()
        if self.check_map():
            self.go_or_back()
            if self.check_empty()!=True:
                self.modify_map()       
        else:
            self.sub_vectors()

    #touch_ functions checks if the body has interacted with the corresponding items
    #and remove the vector from their list, to prevent duplicate use of items
    def touch_key(self):
        if (self.y, self.x) in self._item.keyvectors:
            self._item.keyvectors.remove((self.y, self.x))
            self.keycollect+=1
            return True

    def touch_bat(self):
        if (self.y, self.x) in self._item.batvectors:
            self._item.batvectors.remove((self.y, self.x))
            return True

    def touch_timer(self):
        if (self.y, self.x) in self._item.timervectors:
            self._item.timervectors.remove((self.y, self.x))
            return True

    def touch_timetrap(self):
        if (self.y, self.x) in self._item.timetrapvectors:
            self._item.timetrapvectors.remove((self.y, self.x))
            return True

    #add all body parts to the screen, called when the screen is resized
    def show_body(self):
        for x in self.bodydq:
            self.stdscr.addstr(*x, self.body, curses.color_pair(2))
        self.stdscr.noutrefresh(self.mapy, self.mapx, 0, 1, (curses.LINES//5)*3-1, curses.COLS//2-1)
    
    #remove all body vectors from the deque, before starting up new games
    def reset_body(self):
        self.bodydq.clear()

    
