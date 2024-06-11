"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: <Your name here>
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

import colorsys
#from curses import COLORS
import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *
from matplotlib import colors
from matplotlib.pyplot import close
from numpy import integer

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, child, count, delay):
        mp.Process.__init__(self)
        self.conn = child
        self.count = int(count)
        self.delay = float(delay)
        # TODO Add any arguments and variables here

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        queue = []
        for _ in range(self.count):
            queue.append(random.choice(self.colors))
        for _ in queue:
            sendo = queue.pop(0)
            self.conn.send(sendo)
            time.sleep(self.delay)
        self.conn.send("ALL DONE")
        pass


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self,comm, child, count, delay):
        mp.Process.__init__(self)
        self.parent = comm
        self.childe = child
        self.baggie = Bag()
        self.count = int(count)
        self.delay = float(delay)
        # TODO Add any arguments and variables here

    def newbag(self):
        '''making a new bag for ease'''
        self.baggie = Bag()

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        while True:
            ans = self.parent.recv()
            if ans == "ALL DONE":
                self.childe.send(self.baggie)
                self.childe.send(ans)
                break
            if self.baggie.get_size() == self.count:
                self.childe.send(self.baggie)
                self.newbag()
            else:
                self.baggie.add(ans)
        time.sleep(self.delay)


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, comm, child, delay):
        mp.Process.__init__(self)
        self.parent = comm
        self.childe = child
        self.delay = float(delay)
        # TODO Add any arguments and variables here

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            ans = self.parent.recv()
            if ans == "ALL DONE":
                self.childe.send(ans)
                break
            lmarb = random.choice(self.marble_names)
            gifto = Gift(lmarb, ans)
            self.childe.send(gifto)
            time.sleep(self.delay)

class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self,comm, delay, filepath, giftnum):
        mp.Process.__init__(self)
        self.parent = comm
        self.delay = float(delay)
        self.filepath = filepath
        self.giftnum = giftnum
        # TODO Add any arguments and variables here

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        while True:
            ans = self.parent.recv()
            if ans == "ALL DONE":
                break
            #print(f'Created - {datetime.now().time()}: {str(ans)}')
            with open(self.filepath, 'a') as fp:
                fp.write(f'Created - {datetime.now().time()}: {str(ans)} \n')
            self.giftnum[0] = self.giftnum[0] +1
            time.sleep(int(self.delay))


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count                = {settings[MARBLE_COUNT]}')
    log.write(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    log.write(f'settings["bag-count"]       = {settings[BAG_COUNT]}') 
    log.write(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    log.write(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    log.write(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    Marble_Child_conn, Bagger_Parent_conn = mp.Pipe()
    Bagger_Child_conn, Assembler_Parent_conn = mp.Pipe()
    Assembler_Child_conn, Wrapper_Parent_conn = mp.Pipe()

    # TODO create variable to be used to count the number of gifts
    giftNum = mp.Manager().list([0])

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    creator = Marble_Creator(Marble_Child_conn,settings[MARBLE_COUNT], settings[CREATOR_DELAY])
    bag = Bagger(Bagger_Parent_conn, Bagger_Child_conn, settings[BAG_COUNT], settings[BAGGER_DELAY])
    assem = Assembler(Assembler_Parent_conn, Assembler_Child_conn, settings[ASSEMBLER_DELAY])
    wrap = Wrapper(Wrapper_Parent_conn, settings[WRAPPER_DELAY], BOXES_FILENAME, giftNum)
    log.write('Starting the processes')
    # TODO add code here
    creator.start()
    bag.start()
    assem.start()
    wrap.start()
    log.write('Waiting for processes to finish')
    # TODO add code here
    creator.join()
    bag.join()
    assem.join()
    wrap.join()
    display_final_boxes(BOXES_FILENAME, log)

    # TODO Log the number of gifts created.
    print(giftNum[0])


if __name__ == '__main__':
    main()

