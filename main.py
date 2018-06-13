import threading
from threading import Thread
import time
import random

redAutobusa = threading.Semaphore(1)  # osigurava da samo jedan autobus prima putnike
stanica = threading.Semaphore(50)  # kontrolise koliko ljudi je na stanici
brojPutnika = 0
putniciUAutobusu = 0
zabranjenUlazak = threading.Semaphore(1)
dozvoljenUlazak = threading.Semaphore(0)


class Stanica(Thread):
    def run(self):
        global brojPutnika

        stanica.acquire()  # 50 putnika moze da udje na stanicu, ostali cekaju

        # print("Putnik ceka")
        # barijera za ulazak na stanicu
        zabranjenUlazak.acquire()
        zabranjenUlazak.release()
        # print("Putnik usao")

        brojPutnika = brojPutnika + 1
        print("Broj putnika {}".format(brojPutnika))

        # barijera za ulazak u autobus
        dozvoljenUlazak.acquire()
        dozvoljenUlazak.release()

        stanica.release()  # putnik kada izadje oslobadja jedno mesto

        # putnik se ukrcava
        self.board_bus()

    @staticmethod
    def board_bus():
        global putniciUAutobusu
        global brojPutnika
        putniciUAutobusu = putniciUAutobusu + 1
        brojPutnika = brojPutnika - 1

        if brojPutnika == 0:
            # print("Putnici ulaze")
            # time.sleep(3)
            Autobusi.kreni()


class Autobusi(Thread):
    def run(self):
        global putniciUAutobusu
        redAutobusa.acquire()  # samo jedan autobus moze da prima putnike
        print("Autobus stigao")
        putniciUAutobusu = 0
        zabranjenUlazak.acquire()
        dozvoljenUlazak.release()

    @staticmethod
    def kreni():
        global putniciUAutobusu
        print("Autobus krece sa {} putnika".format(putniciUAutobusu))
        dozvoljenUlazak.acquire()
        zabranjenUlazak.release()
        redAutobusa.release()  # autobus oslobadja mesto i odlazi sa svojim putnicima


class SaljiAutobuse(Thread):
    # salje autobus svakih 20 sekundi
    def run(self):
        while True:
            time.sleep(20)
            Autobusi().start()


class SaljiPutnike(Thread):
    # salje putnike na stanicu
    def run(self):
        while True:
            Stanica().start()
            time.sleep(random.uniform(0.2, 0.64))


if __name__ == "__main__":
    SaljiAutobuse().start()
    SaljiPutnike().start()
