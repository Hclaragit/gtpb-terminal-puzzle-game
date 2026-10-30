import curses
import mapstores

class Map:
    #declaring all variables needed
    time = 60
    key = None
    level = None
    gamemap = None

    #these sets the number of items/time per each level
    keynums = {"easy": 3, "medium": 5, "hard": 10, "hard2": 10}
    batnums = {"easy": 2, "medium": 4, "hard": 10, "hard2": 10}
    timernums = {"easy": 2, "medium": 3, "hard": 7, "hard2": 6}
    timetrapnums = {"easy": 0, "medium": 2, "hard": 3, "hard2": 4}
    time = {"easy":60*1.5, "medium": 60*3.5, "hard": 60*7.5, "hard2": 60*6}

    #defining the empty spaces for the map
    empty = ('', ' ')
    
    def __init__(self, stdscr):
        self.stdscr = stdscr

    #giving controlled access to time (so other class can access same time variable)
    def get_time(self, level="easy"):
        return self.time[level]

    #reading map from mapstores and returning it in a form of list
    def generate_map(self, level = "easy"):

        if level == "easy":
            self.gamemap = mapstores.map1()
        elif level == "medium":
            self.gamemap = mapstores.map2()
        elif level == "hard":
            self.gamemap = mapstores.map3()
        elif level == "hard2":
            self.gamemap = mapstores.map4()[::-1]
            
        return self.gamemap.split("\n")
    
    #returning number of items (so items class can access num of each items)
    def get_numkey(self, level = "easy"):
        return self.keynums[level]

    def get_numbat(self, level="easy"):
        return self.batnums[level]

    def get_numtimer(self, level="easy"):
        return self.timernums[level]

    def get_numtimetrap(self, level="easy"):
        return self.timetrapnums[level]
    
    #showing map in the stdscr passed
    def showmap(self, level = "easy"):
        mapprint = self.generate_map(level)
        for z, row in enumerate(mapprint):
            self.stdscr.addstr(z, 0, row)


