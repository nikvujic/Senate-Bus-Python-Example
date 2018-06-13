import threading
from threading import Thread
import time
import random

redAutobusa = threading.Semaphore(1)  # makes sure only one bus takes passengers
stanica = threading.Semaphore(50)  # controls how many people are at the station
brojPutnika = 0
putniciUAutobusu = 0
zabranjenUlazak = threading.Semaphore(1)
dozvoljenUlazak = threading.Semaphore(0)


class Stanica(Thread):
    def run(self):
        global brojPutnika

        stanica.acquire()  # 50 passengers can enter the station, the rest have to wait

        # print("Passenger waiting")
        # barrier for entry to station
        zabranjenUlazak.acquire()
        zabranjenUlazak.release()
        # print("Passengers entered")

        brojPutnika = brojPutnika + 1
        print("Number of passengers: {}".format(brojPutnika))

        # barrier for entry to the bus
        dozvoljenUlazak.acquire()
        dozvoljenUlazak.release()

        stanica.release()  # passenger left, made more room

        # passenger boards the bus
        self.board_bus()

    @staticmethod
    def board_bus():
        global putniciUAutobusu
        global brojPutnika
        putniciUAutobusu = putniciUAutobusu + 1
        brojPutnika = brojPutnika - 1

        if brojPutnika == 0:
            # print("Passengers entering")
            # time.sleep(3)
            Autobusi.kreni()


class Autobusi(Thread):
    def run(self):
        global putniciUAutobusu
        redAutobusa.acquire()  # only one bus can take passengers
        print("The bus arrives")
        putniciUAutobusu = 0
        zabranjenUlazak.acquire()
        dozvoljenUlazak.release()

    @staticmethod
    def kreni():
        global putniciUAutobusu
        print("The bus leaves with {} passengers".format(putniciUAutobusu))
        dozvoljenUlazak.acquire()
        zabranjenUlazak.release()
        redAutobusa.release()  # the bus releases and goes off with its passengers


class SaljiAutobuse(Thread):
    # sends a bus every 20 seconds
    def run(self):
        while True:
            time.sleep(20)
            Autobusi().start()


class SaljiPutnike(Thread):
    # sends passengers to the station
    def run(self):
        while True:
            Stanica().start()
            time.sleep(random.uniform(0.2, 0.64))


if __name__ == "__main__":
    SaljiAutobuse().start()
    SaljiPutnike().start()
