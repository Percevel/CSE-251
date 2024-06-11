"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: <Your name>

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- See I-Learn

"""

from multiprocessing import Semaphore
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self,q, lockr, sem):
        # TODO, you need to add arguments that will pass all of data that 1 factory needs
        threading.Thread.__init__(self)
        self.qu = q
        self.s = sem
        self.loc = lockr
        # to create cars and to place them in a queue.
        pass


    def run(self):
        for i in range(CARS_TO_PRODUCE):
            # TODO Add you code here
            with self.s:
                with self.loc:
                    c = Car()
                    if self.qu.size() < MAX_QUEUE_SIZE:
                        self.qu.put(c)
                
            """
            create a car
            place the car on the queue
            signal the dealer that there is a car on the queue
           """

        # signal the dealer that there there are not more cars
        pass
        self.qu.put('DONE')


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self,q,sem,status):
        # TODO, you need to add arguments that pass all of data that 1 Dealer needs
        threading.Thread.__init__(self)
        self.qu = q
        self.s = sem
        self.stat = status
        # to sell a car
        pass
    
    

    def run(self):
        while True:
            # TODO Add your code here
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """
            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))
            with self.s:
                if self.qu.size() > 0:
                    carrr = self.qu.get()
                    if carrr == 'DONE':
                        break
                    self.stat[(self.qu.size()-1)] = self.stat[(self.qu.size()-1)]+1
                pass



def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s)
    sem1 = threading.Semaphore()
    sem2 = threading.Semaphore()
    # TODO Create queue251 
    q = Queue251()
    # TODO Create lock(s) ?
    lock = threading.Lock()

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # TODO create your one factory
    fac = Factory(q,lock,sem1)
    # TODO create your one dealership
    deal = Dealer(q,sem2, queue_stats)
    log.start_timer()

    # TODO Start factory and dealership
    fac.start()
    deal.start()
    # TODO Wait for factory and dealership to complete
    fac.join()
    deal.join()

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    print(queue_stats)
    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()
