import sqlite3, matplotlib, folium, pandas, os
from functions import *
# https://data.edmonton.ca/browse

menu = {'1':bar, '2':map}
# Manual db file selection:
'''while True:
        print('Input db filename:')
        file = input()
        if os.path.isfile(file):
            conn = sqlite3.connect(file)
            break
        else:
            print('Invalid file')'''
conn = sqlite3.connect('crime.db')
while True: 
    print('1: Bar plot of a crime type in a given year range')
    print('2: Map of the top-N neigborhoods for crime occurances in a given year range')
    print('1/2/Q')
    action = input().lower()
    if action in menu:
        menu[action](conn)
    elif action == 'q':
        exit()
    print()
