import curses, random
from curses import wrapper
from maptest import Map

class Items:
    #declaring class objects and item positions, symbols as none
    _map = None
    gamemap = None
    level = None
    keyvectors = []
    batvectors = []
    timervectors = []
    timetrapvectors = []
    key = 'K'
    bat = 'B'
    timer = 'T'
    timetrap = 'T'

    def __init__(self, stdscr):
        self.stdscr = stdscr
        #private object _map is created based on the Map class, to access item numbers
        self._map = Map(self.stdscr)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    #this function retreives the key number from Map class and decide vectors to distribute keys
    def distribute_key(self):
        numkey = self._map.get_numkey(self.level)
        i=0
        #loops while the correct number of key items are distributed, excluding same place choosen
        while i< numkey:
            #pick random place from the map, excluding space for walls
            y, x = random.randint(2, len(self.gamemap)-3), random.randint(1, len(self.gamemap[1])-2)
            #prevents the same vector position to be choosen for key distribution.
            if self.gamemap[y][x] in (' ') and ((y,x) not in self.keyvectors):
                self.keyvectors.append((y,x))
                i+=1

    #allow key symbols to be shown in the correct vector of the map
    def show_key(self):
        for v in self.keyvectors:
            self.stdscr.addstr(*v, self.key, curses.color_pair(1))

    def distribute_bat(self):
        numbat = self._map.get_numbat(self.level)
        i=0
        while i< numbat:
            y, x = random.randint(2, len(self.gamemap)-3), random.randint(1, len(self.gamemap[1])-2)
            #as bat is called after key is distributed, key vectors are also checked to prevent same vectors used
            if self.gamemap[y][x] in (' ') and (y,x) not in self.keyvectors and (y,x) not in self.batvectors:
                self.batvectors.append((y,x))
                i+=1

    def show_bat(self):
        for v in self.batvectors:
            self.stdscr.addstr(*v, self.bat, curses.color_pair(1))

    def distribute_timer(self):
        numtimer = self._map.get_numtimer(self.level)
        i=0
        while i< numtimer:
            y, x = random.randint(2, len(self.gamemap)-3), random.randint(1, len(self.gamemap[1])-2)
            #as timer is called after bat and key, vectors not in bat, key and timer vector list is only choosen for new vectors
            if self.gamemap[y][x] in (' ') and (y,x) not in self.keyvectors and (y,x) not in self.batvectors and (y,x)not in self.timervectors:
                self.timervectors.append((y,x))
                i+=1

    def show_timer(self):
        for v in self.timervectors:
            self.stdscr.addstr(*v, self.timer, curses.color_pair(1))

    def distribute_timetrap(self):
        numtimetrap = self._map.get_numtimetrap(self.level)
        i=0
        while i< numtimetrap:
            y, x = random.randint(2, len(self.gamemap)-3), random.randint(1, len(self.gamemap[1])-2)
            #timetrap is called after key, bat and timers; vectors not in all the other item vectorlist including timetrap is choosen
            if self.gamemap[y][x] in (' ') and (y,x) not in self.keyvectors and (y,x) not in self.batvectors and (y,x)not in self.timervectors and (y,x) not in self.timetrapvectors:
                self.timetrapvectors.append((y,x))
                i+=1
                
    def show_timetrap(self):
        for v in self.timetrapvectors:
            self.stdscr.addstr(*v, self.timetrap, curses.color_pair(1))

    #clearing all item vectors
    def reset_items(self):
        self.keyvectors.clear()
        self.batvectors.clear()
        self.timervectors.clear()
        self.timetrapvectors.clear()


