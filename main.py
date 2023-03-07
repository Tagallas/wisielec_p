import os
import string
import random
from time import sleep
import keyboard
from colorama import Fore

color = Fore.LIGHTGREEN_EX
default = Fore.WHITE


def clear():
    #os.system('cls')
    print(20 * '\n')


def menu(mode=0):
    clear()
    sleep(0.3)
    print(default + """
        \t\t\tWISIELEC
            """)
    print((color if mode == 0 else default) + "\t\tNowa Gra")
    print((color if mode == 1 else default) + "\t\tWczytaj gre")
    print((color if mode == 2 else default) + "\t\tStatystyka wygranych")
    print((color if mode == 3 else default) + "\t\tZasady Gry")
    print(default + "Do gory: q + q, w dol: a\nPotwierdz: enter")
    if keyboard.read_key() == "enter":
        sleep(0.1)
        if mode == 0:
            newgame()
        elif mode == 1:
            reload()
        elif mode == 2:
            statistic(10)
        elif mode == 3:
            zasady()
    if keyboard.read_key() == "a":
        if mode < 3:
            mode += 1
        else:
            mode = 0
        sleep(0.1)
        menu(mode)
    if keyboard.read_key() == "q":
        if mode > 0:
            mode -= 1
        else:
            mode = 3
        sleep(0.1)
        menu(mode)


def newgame(mode=0):
    clear()
    print(default + """
            \t\t\tWISIELEC\n\n\tWybierz Poziom trudnosci:""")
    print((color if mode == 0 else default) + "\t\tLatwy")
    print((color if mode == 1 else default) + "\t\tSredni")
    print((color if mode == 2 else default) + "\t\tTrudny" + default)
    if keyboard.read_key() == "enter":
        word = draw(mode)
        game(word)
    if keyboard.read_key() == "a":
        if mode < 2:
            mode += 1
        else:
            mode = 0
        sleep(0.1)
        newgame(mode)
    if keyboard.read_key() == "q":
        if mode > 0:
            mode -= 1
        else:
            mode = 2
        sleep(0.1)
        newgame(mode)


def draw(level) -> str:
    if level == 0:
        word = open("DataBase/short.txt").readlines()
        return word[random.randrange(len(word))]
    if level == 1:
        word = open("DataBase/mid.txt").readlines()
        return word[random.randrange(len(word))]
    if level == 2:
        word = open("DataBase/long.txt").readlines()
        return word[random.randrange(len(word))]


def reload():
    clear()
    try:
        alfabet = set(string.ascii_uppercase)
        nazwa = input("\nPodaj nazwę zapisu: \n")
        while nazwa == "":
            nazwa = input()
        f = open(nazwa)
        word = f.readline()
        zycie = int(f.readline())
        word = word[:-1]
        nietrafione_litery_pom = (f.readline().replace('\'', ''))
        uzyte_litery_pom = (f.readline().replace('\'', ''))
        nietrafione_litery = [i for i in nietrafione_litery_pom if i in alfabet]
        uzyte_litery = [i for i in uzyte_litery_pom if i in alfabet]
        f.close()
        game(word, zycie, nietrafione_litery, uzyte_litery)

    except FileNotFoundError:
        print("Taki zapis nie istnieje ")
        sleep(3)
        reload()


def statistic(wybor: int):
    clear()
    f = open("DataBase/statistic.txt", "r")
    wgr = int(f.readline())
    prz = int(f.readline())
    f.close()
    if wybor == 0:
        prz += 1
    elif wybor != 10:
        wgr += 1
    f = open("DataBase/statistic.txt", "w")
    f.write(str(wgr)+'\n')
    f.write(str(prz))
    f.close()

    print("Statystyki:\n")
    print("Gry wygrane:  ", wgr)
    print("Gry przegrane:  ", prz)
    print("procent wygranych: ", round(wgr / (wgr + prz) * 100, 2), "%")

    print("\nEnter - kontynuuj")
    if keyboard.read_key() == "enter":
        menu()


def zasady():
    clear()
    print("Zasady gry: \n-----------------------\n")
    print("Gracz biorący udział w grze ma za zadanie w odgadnąć słowo. Jedyną informacje jaką uczestnik gry dostaje jest liczba liter, które zawiera")
    print("odgadywany wyraz. Istenieją trzy poziomy trudności jakie gracz może wybrać z menu: Łatwy, Średni, Trudny. Od wybranego poziomu trudności")
    print("zależy złożoność i unikalność danego słowa, a liczba prób dla każdego poziomu jest jednakowa i wynosi 8.")
    print("Jeżeli chcesz powrócić do gry naciśnij enter")
    if keyboard.read_key() == "enter":
        menu()


def other_action(word, zycie, nietrafione_litery, uzyte_litery, podpowiedz):
    clear()
    print("""
            Co chesz zrobić? 
    s - zapisz grę
    l - wczytaj grę
    p - skorzystaj z podpowiedzi (pamiętaj masz tylko jedną)
    m - wróć do menu bez zapisu
    dowolny klawisz - kontunuuj
    """)
    alfabet = set(string.ascii_uppercase)
    wybrana_akcja = input("")
    if wybrana_akcja == 's':
        clear()
        nazwa = input("\nPodaj nazwę zapisu:")
        while nazwa == "":
            nazwa = input()
        f = open(nazwa, "w")
        f.write(word + "\n")
        f.write(str(zycie) + "\n")
        f.write(str(nietrafione_litery) + "\n")
        f.write(str(uzyte_litery) + "\n")
        f.write(str(podpowiedz))
        f.close()
        menu()
    elif wybrana_akcja == 'l':
        clear()
        nazwa = input("\nPodaj nazwę zapisu:")
        while nazwa == "":
            nazwa = input()
        if os.path.exists(nazwa):
            f = open(nazwa, "r")
            word = f.readline()
            zycie = int(f.readline())
            word = word[:-1]
            nietrafione_litery_pom = (f.readline().replace('\'', ''))
            uzyte_litery_pom = (f.readline().replace('\'', ''))
            podpowiedz = int(f.readline())
            nietrafione_litery = [i for i in nietrafione_litery_pom if i in alfabet]
            uzyte_litery = [i for i in uzyte_litery_pom if i in alfabet]
            f.close()
        else:
            print("\nTaki zapis nie istnieje: ", nazwa)
            sleep(2)
            other_action(word, zycie, nietrafione_litery, uzyte_litery, podpowiedz)
    elif wybrana_akcja == 'p':
        sleep(0.3)
        if podpowiedz:
            podpowiedz = 0
            indeks = input("\nPodaj miejsce, w którym chcesz znać litere: ")
            while indeks == "":
                indeks = input()
            if len(word) > int(indeks) - 1 >= 0:
                print("Litera to: ", word[int(indeks) - 1])
                sleep(3)
            else:
                print("Niestety niepoprawnie wykorzystana podpowiedź, powodzenia w dalszym zgadywaniu")
                sleep(3)
        else:
            clear()
            print("Niestety wykorzystałeś wszystkie podpowiedzi!")
            sleep(3)
    elif wybrana_akcja == 'm':
        menu()
    game(word, zycie, nietrafione_litery, uzyte_litery, podpowiedz)


def end_game(word, x):
    underline = "\n-----------------------\n"
    if x == 0:
        clear()
        print("""
                            |
                            O
                         ___|___
                            |
                           /|
                          / |""")
        print(f"\n{underline}Niestety zawisłeś na szubienicy. Szukanym słowem było: '{word}'{underline}")
        sleep(3)
        statistic(x)
    else:
        clear()
        print(f"\n{underline}Gratulacje! Odgadłeś całe słowo: '{word}'{underline}")
        sleep(3)
        statistic(x)


def game(word: str = "WISIELEC", zycie=8, nietrafione_litery: list = [], uzyte_litery: list = [], podpowiedz=1):
    clear()
    odgadniente_litery = [letter if letter in uzyte_litery else "_" for letter in word]
    if "_" not in odgadniente_litery:
        end_game(word, 1)
    underline = "\n-----------------------\n"
    print("Witaj w grze Wisielec!")
    alfabet = set(string.ascii_uppercase)
    word = word.strip()

    if zycie <= 7:
        print("\t|")
    if zycie <= 6:
        print("\tO")
    if zycie <= 3:
        print(" ___|___")
    elif zycie <= 4:
        print(" ___|")
    elif zycie <= 5:
        print("\t|")
    if zycie <= 2:
        print("\t|")
    if zycie <= 0:
        print("   /|\n  / |")
    elif zycie <= 1:
        print("   /\n  /")
    print(f"Wykorzystane litery: {nietrafione_litery}")
    print("\nObecne słowo: ", " ".join(odgadniente_litery))
    print("Odgadnij literę\n\n"
          "spacja - inne działanie")

    podana_litera = input("").upper()
    if podana_litera == " ":
        other_action(word, zycie, nietrafione_litery, uzyte_litery, podpowiedz)
    elif podana_litera in uzyte_litery or podana_litera in nietrafione_litery:
        print(f"Litera {podana_litera} została już użyta!")
        sleep(1)
        game(word, zycie, nietrafione_litery, uzyte_litery, podpowiedz)
    elif podana_litera in alfabet:
        if podana_litera in word:
            clear()
            print(f"{underline}Odgadłeś litere: '{podana_litera}'{underline}")
            sleep(1.5)
            uzyte_litery.append(podana_litera)
            game(word, zycie, nietrafione_litery, uzyte_litery, podpowiedz)
        else:
            clear()
            print(f"{underline}Pudło, spróbuj ponownie odgadnąć litere{underline}")
            sleep(1.5)
            nietrafione_litery.append(podana_litera)
            zycie -= 1
            if zycie == 0:
                end_game(word, 0)
            game(word, zycie, nietrafione_litery, uzyte_litery, podpowiedz)
    else:
        print("Podaj prawidłową literę!")
        sleep(1)
        game(word, zycie, nietrafione_litery, uzyte_litery, podpowiedz)


menu()
