#import classes from other python files, and modules
from maptest import Map
from body import Body
from items import Items 
from collections import deque
from startscr import Startscr
# from endscr import Endscr
import curses, time, collections, sys, itemstores, random 
import concurrent.futures
import asyncio
import sysmsg
from curses import panel

class ui_times:
    #declaring objects and variables(to be retreived from other classes) as None
    startscr = None
    endingscr = None
    body = None
    t=None
    gamemap = None
    level = None
    numkey = 0
    item = None
    game = True
    executor = None
    sysmsglist = []

    #dictionary to identify if the item is on the use
    itemon = {'key':False, 'bat':False, 'timer':False, 'timetrap':False}
    #boolean to distinguish if body's movement is destructive(break walls) or not
    movement = False
    #deque to store user's interaction with the item.
    itemq = deque([])
        
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
    
    #set up the UIs, including map, other windows, item ascii arts
    def prepare_all(self):
        #set up executor to change time(prevent over initialisation of executors)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self.set_map_pad()
        self.set_map()
        self.set_body()
        self.set_panels()
        self.set_item()
        self.show_all()
        self.bgchange()

    #set up starting screen, retreive user's choice for the level to set up the correct map and items
    def set_startscr(self):
        #start screen obj is build based on Startscr class
        self.startscr = Startscr(self.stdscr)
        self.startscr.user_choice()
        #store user's selection for map, to set up corresponding map, and correct types and number of items
        self.level = self.startscr.level
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLUE)
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        window.bkgd(" ", curses.color_pair(1))
        window.refresh()

    
    def set_map_pad(self):
        global mappad
        mappad = curses.newpad(500, 500)
    
    def set_map(self):
        #pass mappad as a stdscr for the gamemap object
        self.gamemap = Map(mappad)
        #this access time accessor in Map class
        self.t = self.gamemap.get_time(self.level)

    #this function creates item object and distributes correct number of items by choosing item vectors
    def set_item(self):
        self.item = Items(mappad)
        self.item.gamemap = self.body.gamemap
        self.item.level = self.level
        self.item.distribute_key()
        self.item.distribute_bat()
        self.item.distribute_timer()
        self.item.distribute_timetrap()

    #this function shows the items to the map based on the item vectors assigned by the function above
    def load_item(self):
        self.item.show_key()
        self.item.show_bat()
        self.item.show_timer()
        self.item.show_timetrap()
    
    #this function clear and refresh the map
    def show_map_pad(self):
        mappad.clear()
        self.gamemap.showmap(self.level)
        self.load_item()
        mappad.refresh(self.body.mapy, self.body.mapx, 0, 1, (curses.LINES//5)*3-1, curses.COLS//2-1)
    
    #this function creates body object and place it to the Entrance of the map(indicated by 'E')
    #and deterimine position of map to be displayed in the mappad.
    def set_body(self):
        self.body = Body(mappad)
        self.body.level = self.level
        self.body.gamemap = self.body._get_map()
        #loop through the gamemap, to find the index of Entrance ('E')
        #to set the starting position of the body
        for l in range(len(self.body.gamemap)):
            for i in range(len(self.body.gamemap[l])):
                if self.body.gamemap[l][i]=='E':
                    self.body.start_y, self.body.start_x = l, i
        self.body.y, self.body.x = self.body.start_y, self.body.start_x
        self.get_body_mapxy()
        self.numkey = self.gamemap.get_numkey(self.level)
        self.body.set_bodydq()
        self.body.start()

    def get_body_mapxy(self):
        #setting left top corner of the mappad to show:
        #if length of the map is longer than the size of the mappad
        #the exceeding length (based on the position of body) is hidden 
        #if length of the map is equal or shorter than the mappad, all map is shown
        if (len(self.body.gamemap)-((curses.LINES//5)*3-1))>0:
            #cheking if map is vertically longer than the mappad
            self.body.mapy = len(self.body.gamemap)-((curses.LINES//5)*3-1)
        else:
            self.body.mapy = 0
            
        if ((len(self.body.gamemap[0])-(curses.COLS//2-1)))>0:
            #checking if map is horizontally longer than the mappad
            self.body.mapx = (len(self.body.gamemap[0])-(curses.COLS//2-1))
        else:
            self.body.mapx = 0

    #sets basic shape of the timewin, window to display the game time 
    def show_timewin(self):
        global timewin
        timewin = curses.newwin(curses.LINES//6, curses.COLS//4-4, (curses.LINES//6)*5, curses.COLS//2+curses.COLS//4)
        timewin.border('|', '|', '-', '-', '+', '+', '+', '+')
        mins, secs = divmod(int(self.t), 60)
        y,x = timewin.getmaxyx()
        timewin.addstr(y//2, 1, f"time left: [{mins:02d} : {secs:02d}] ")
        timewin.refresh()

    #changes the time displayed in the timewin
    def changetime(self):
        mins, secs = divmod(int(self.t), 60)
        y,x = timewin.getmaxyx()
        timewin.addstr(y//2, 1, f"time left: [{mins:02d} : {secs:02d}] ")
        timewin.noutrefresh()

    #updates timewin every 1 second, displaying the decremented game time
    def wait_t(self):
        #only run when game is running (not all keys are collected)
        while self.game == True:
            time.sleep(1)
            self.t-=1
            self.changetime()     

    #check if the user has interacted with the item and if so, executes the corresponding effects
    def itemonoff(self):
        #only run when game is running
        #every interaction stored in the itemq is popped and the corresponding effect is executed
        while self.game == True:
            try:
                if self.itemq[0] == 'bat':
                    self.itemq.popleft()
                    self.interact_bat()
                if self.itemq[0] == 'timer':
                    self.itemq.popleft()
                    self.interact_timer()
                if self.itemq[0] == 'key':
                    self.itemq.popleft()
                    self.interact_key()
                if self.itemq[0] == 'timetrap':
                    self.itemq.popleft()
                    self.interact_timetrap()
            except:
                pass

    #this function allows game time, item interaction and system message display to be executed in the background
    #so user's game play can be executed concurrently time/item/system message
    def bgchange(self):
        #each functions to be managed concurrently(at the background) are passed to the executor initialised from __init__
        #tc changes game Time per 1 sec
        #ionoff checks for item interaction and executes their effects
        #msgdis display system messages
        tc = self.executor.submit(self.wait_t)
        ionoff = self.executor.submit(self.itemonoff)
        msgdis = self.executor.submit(self.ingame_sismsg)
    
    #creates default window and panel for the itemwin
    def show_item(self):
        global itemwin
        global itempanel
        itemwin = curses.newwin((curses.LINES//6)*4, curses.COLS//4-4, curses.LINES//6+1, curses.COLS//2+curses.COLS//4)
        itemwin.border('|', '|', '-', '-', '+', '+', '+', '+')
        itemwin.addstr(0, 1, "item collected: ")
        itemwin.refresh()

        itempanel = curses.panel.new_panel(itemwin)
        curses.panel.update_panels()
    
    #creates windows and panels to display each items
    def set_panels(self):
        global batwin
        global timerwin
        global keywin
        global timetrapwin

        global batpanel
        global timerpanel
        global keypanel
        global timetrappanel

        batwin = curses.newwin((curses.LINES//6)*4-2, curses.COLS//4-6, curses.LINES//6+2, curses.COLS//2+curses.COLS//4+1)
        timerwin = curses.newwin((curses.LINES//6)*4-2, curses.COLS//4-6, curses.LINES//6+2, curses.COLS//2+curses.COLS//4+1)
        keywin = curses.newwin((curses.LINES//6)*4-2, curses.COLS//4-6, curses.LINES//6+2, curses.COLS//2+curses.COLS//4+1)
        timetrapwin = curses.newwin((curses.LINES//6)*4-2, curses.COLS//4-6, curses.LINES//6+2, curses.COLS//2+curses.COLS//4+1)

        self.show_bat()
        self.show_timer()
        self.show_key()
        self.show_timetrap()

        batwin.refresh()
        timerwin.refresh()
        keywin.refresh()
        timetrapwin.refresh()

        batpanel = curses.panel.new_panel(batwin)
        timerpanel = curses.panel.new_panel(timerwin)
        keypanel = curses.panel.new_panel(keywin)
        timetrappanel = curses.panel.new_panel(timetrapwin)

        #each panels are hidden and only show up when the item is on the use
        batpanel.hide()
        timerpanel.hide()
        keypanel.hide()
        timetrappanel.hide()
        curses.panel.update_panels()

    #sets interaction effect for the bat item
    def interact_bat(self):
            self.movement = True
            #wait few sec before turning itemon['bat'] as False so the program can catch the moment it is turned on True
            time.sleep(1)
            self.itemon['bat'] = False
            time.sleep(4)
            self.movement = False
            #if no other bat item has interacted, hide bat panels, to show the item effect has ended up
            if self.itemon['bat'] == False:
                batpanel.bottom()
                batpanel.hide()
                curses.panel.update_panels()

    #sets interaction effect for the key item
    def interact_key(self):
        #as priority is bat=timetrap>timer>key, key panel is only showed up when no other item interactions available or finised
        if self.itemon['bat'] == True or self.itemon['timer'] == True or self.itemon['timetrap'] == True:
            pass
        else:
            #same as bat, wait few sec before turning itemon['key'] as False to prevent program only getting itemon['key'] as False
            time.sleep(1)
            self.itemon['key'] =False
            time.sleep(4)
            #if no other key item has interacted, hide key panels, indicating key effect has ended up
            if self.itemon['key'] == False:
                keypanel.bottom()
                keypanel.hide()
                curses.panel.update_panels()
    
    #sets interaction effect for the timer item
    def interact_timer(self):
        #timer is only showed up when no bat items are interacting or bat is finished
        if self.itemon['bat'] == True:
            pass
        else:
            #same as bat, wait few sec before turning itemon['timer'] as False to prevent program only getting itemon['timer'] as False
            time.sleep(1)
            self.itemon['timer'] = False
            time.sleep(4) 
            #if no other timer item has interacted, hide timer panels, indicating timer effect has ended up
            if self.itemon['timer'] == False:
                timerpanel.bottom()
                timerpanel.hide()
                curses.panel.update_panels()

    #sets interaction effect for the timetrap item
    def interact_timetrap(self):
        #same as bat, wait few sec before turning itemon['timetrap'] as False to prevent program only getting itemon['timetrap'] as False
        time.sleep(1)
        self.itemon['timetrap'] = False
        time.sleep(4)
        #if no other timetrap item has interacted, hide timer panels, indicating timetrap effect has ended up
        if self.itemon['timetrap'] == False:
            timetrappanel.bottom()
            timetrappanel.hide()
            curses.panel.update_panels()

    #this function sets the basic movement of the body, if it is normal or the bat is applied(destructive to obstacles)
    def movement_checker(self):
        if self.game == True:
            #normal movement is stimulied based on the boolean varaible movement.
            #if bat is applied(i.e. movement == True), body's movement is changed to destructive movement
            if self.movement == False:
                self.body.trymove() 
            else:
                self.body.break_everything()
    
    #this function display ascii art for the key item, retreived from the itemstores file
    def show_keyimg(self):
        try:
            keyimg = itemstores.get_keyimg().split('\n')
            for x, line in enumerate(keyimg):
                keywin.addstr(x+1, 1, line, curses.color_pair(4))
        #in case the terminal size is too small and causing some error, skip img showup
        except curses.error:
            return

    #similar to the function above, display ascii art for the timer item, retreived from the itemstores file
    def show_timerimg(self):
        try:
            timerimg = itemstores.get_timerimg().split('\n')
            for x, line in enumerate(timerimg):
                timerwin.addstr(x+1, 1, line, curses.color_pair(4))
        #in case the terminal size is too small and causing some error, skip img showup
        except curses.error:
            return

    #display ascii art for the bat item, retreived from the itemstores file
    def show_batimg(self):
        try:
            batimg = itemstores.get_batimg().split('\n')
            for x, line in enumerate(batimg):
                batwin.addstr(x+1, 1, line, curses.color_pair(4))
        #in case the terminal size is too small and causing some error, skip img showup
        except curses.error:
            return

    #display ascii art for the timetrap item, retreived from the itemstores file
    def show_timetrapimg(self):
        try:
            timerimg = itemstores.get_timerimg().split('\n')
            for x, line in enumerate(timerimg):
                timetrapwin.addstr(x+1, 1, line, curses.color_pair(4))
        #in case the terminal size is too small and causing some error, skip img showup
        except curses.error:
            return

    #display img and explanations for the key item
    def show_key(self):
        try:
            keywin.addstr(1, 1, "You just got item: KEY!")
            self.show_keyimg()
            txt = "This is all I NEED!!\nCollect them and get\nMY PHONE BACK!"
            txtlist = txt.split('\n')
            for y, line in enumerate(txtlist):
                keywin.addstr(y+(curses.LINES//6)*4-5, 1, line)
        except curses.error:
            return

    #display img and explanations for the timer item
    def show_timer(self):
        try:
            timerwin.addstr(1, 1, "You just got item: TIMER!")
            self.show_timerimg()
            txt = "Mom would return\n10 seconds late!! HOORAY!\nI have more Time!"
            txtlist = txt.split('\n')
            for y, line in enumerate(txtlist):
                timerwin.addstr(y+(curses.LINES//6)*4-5, 1, line)
        except curses.error:
            return

    #display img and explanations for the bat item
    def show_bat(self):
        try:
            self.show_batimg()
            batwin.addstr(1, 1, "You just got item: BAT!")
            txt = "You can destroy EVERYTHING!!\nEnjoy POWER for 5 seconds."
            txtlist = txt.split('\n')
            for y, line in enumerate(txtlist):
                batwin.addstr(y+(curses.LINES//6)*4-5, 1, line)
        except curses.error:
            return

    #display img and explanations for the timetrap item
    def show_timetrap(self):
        try:
            self.show_timetrapimg()
            timetrapwin.addstr(1, 1, "You just got item: TIME TRAP...")
            txt = "OMG so NOISY!! Mom would come \n 10 seconds early!! UrGgg!!"
            txtlist = txt.split('\n')
            for y, line in enumerate(txtlist):
                timetrapwin.addstr(y+(curses.LINES//6)*4-5, 1, line)
        except curses.error:
            return

    def show_level(self):
        global lvlwin
        try:
            lvlwin = curses.newwin(curses.LINES//6, curses.COLS//4-4, 1, curses.COLS//2+curses.COLS//4)
            lvlwin.border('|', '|', '-', '-', '+', '+', '+', '+')
            lvlwin.addstr(0, 1, f"level: {self.level}")
            y,x = lvlwin.getmaxyx()
            lvlwin.addstr(y//2, 2, f"key: [{self.body.keycollect}/{self.numkey}]")
            lvlwin.refresh()
        except curses.error:
            return
    
    #update key numbers in the keywin
    def key_collect(self):
        try:
            y,x = lvlwin.getmaxyx()
            lvlwin.addstr(y//2, 2, f"key: [{self.body.keycollect}/{self.numkey}]")
            lvlwin.refresh()
        except curses.error:
            return
        #end up game if all keys are collected
        if (self.body.keycollect == self.numkey):
            self.game = False

    def time_collect(self):
        self.t +=10
    
    def time_throw(self):
        self.t-=10
    
    def show_consol(self):
        global syswin
        syswin = curses.newwin((curses.LINES//5)*2-1, curses.COLS//2+curses.COLS//4, (curses.LINES//5)*3+1, 1)
        syswin.border('|', '|', '-', '-', '+', '+', '+', '+')
        syswin.refresh()
    
    #call all screen components again with the correct screen size, called when the screen is resized
    def show_all(self):
        self.set_panels()
        self.show_item()
        self.show_level()
        self.show_timewin()
        self.show_consol()
        self.set_sysmsgwin()
        self.get_body_mapxy()
        self.show_map_pad()
        self.body.show_body()

    def set_sysmsgwin(self):
        global sysmsgwin
        sysmsgwin = curses.newwin((curses.LINES//5)*2-3, curses.COLS//2+curses.COLS//4-2, (curses.LINES//5)*3+2, 2)
        self.load_msg()
    
    #retreive system messages from the textfile
    def load_msg(self):
            messages = sysmsg.readmsg()
            for singlemsg in messages:
                self.sysmsglist.append(singlemsg.strip())

    #display and change system messages to the sysmsgwin every 10 seconds
    def ingame_sismsg(self):
        while self.game==True:
            sysmsgwin.erase()
            sysmsgwin.addstr(1, 2, random.choice(self.sysmsglist), curses.color_pair(3))
            sysmsgwin.noutrefresh()
            time.sleep(10)

    #set up explanation panel which only shows up after completing hard1 level.
    def challenge_panel(self):
        challengewin = curses.newwin((curses.LINES//5)*1-1, curses.COLS, (curses.LINES//5)*2, curses.COLS//10)
        txt = 'all done! Now you have to find keys in this REVERSED map too. Have Fun and RESCUE my Phone!!'
        challengewin.addstr(2, 5, txt, curses.color_pair(5))
        challengewin.refresh()
        challenge_panel = curses.panel.new_panel(challengewin)
        time.sleep(3)
        challenge_panel.bottom()
        challenge_panel.hide()
        curses.panel.update_panels()  
        mappad.refresh(self.body.mapy, self.body.mapx, 0, 1, (curses.LINES//5)*3-1, curses.COLS//2-1) 

    #signals item interaction by adding item name to deque and turning its state True in the dictionary
    def decide_next(self, state: str):
        self.itemq.append(state)
        self.itemon[state] = True

    #check and execute correct item effect, with displaying correct ascii art and explanations
    def check_item(self):
        if self.body.touch_bat():
            curses.beep()
            self.decide_next('bat')
            if self.game == True:
                batpanel.top()
                batpanel.show()
                curses.panel.update_panels()
                curses.napms(50)

        if self.body.touch_key():
            curses.beep()
            self.decide_next('key')
            self.key_collect()
            #as bat and timetrap has the highest priority for items, key img is only showed up when no bat/timetrap is being executed
            if self.itemon['bat'] == False and self.itemon['timetrap'] == False:
                keypanel.top()
                keypanel.show()
                curses.panel.update_panels()
                curses.napms(50)

        if self.body.touch_timer():
            curses.beep()
            self.decide_next('timer')
            self.time_collect()
            #as bat and timetrap has the highest priority for items, timer img is only showed up when no bat/timetrap is being executed
            if self.itemon['bat'] == False and self.itemon['timetrap']== False:
                timerpanel.show()
                curses.panel.update_panels()
                curses.napms(50)

        if self.body.touch_timetrap():
            curses.beep()
            self.decide_next('timetrap')
            self.time_throw()
            timetrappanel.top()
            timetrappanel.show()
            curses.panel.update_panels()
            curses.napms(50)
            
    def item_interaction(self):
        if self.game == True:
            self.check_item()

    #this function is called after game is ended (all keys collected or time finished)
    #to stop concurrent execution of functions(time change, system message, checking items)
    #and reset the game and its variables
    async def end_items(self):
        self.executor.shutdown(wait=False, cancel_futures=True)
        self.body.reset_body()
        self.body._item.reset_items()
        self.sysmsglist.clear()
        #waits for a sec without blocking calling ending screen from the main.py
        await asyncio.sleep(3)
