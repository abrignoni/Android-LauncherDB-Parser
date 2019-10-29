import sys, os, re, sqlite3, glob
import numpy as np
import os.path
from os import path
import pandas as pd
from datetime import datetime
import datetime

database = 'launcher.db'
#isthere = str (path.isfile('launcher.db'))
#print(isthere)

foldername = ("Launcher.db_Reports_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
os.mkdir('./'+foldername)
os.mkdir('./'+foldername+'/icons')

#connect sqlite databases
db = sqlite3.connect(database)
cursor = db.cursor()

#add query to export icons
cursor.execute('''
select title, icon from favorites where icon is not NULL 
''')

all_rowsi = cursor.fetchall()
for rowi in all_rowsi:
    fname = rowi[0]
    fileicon = rowi[1]
    output_file = open('./'+foldername+'/icons/'+fname+'.png', 'wb')
    output_file.write(fileicon)
    output_file.close()
    
cursor.execute('''
select distinct container from favorites order by container asc
''')

all_rows = cursor.fetchall()
for row in all_rows:
    container = row[0]
    
    if container == -101:
        #print('')
        #print('-101 bottom screen')
        #initialize matrix
        a = 1
        b = 5

        screen101 = np.empty([a,b], dtype = 'object') 
        #print(screen)
        
        #Do all the home icons
        cursor.execute('''
        select * from favorites where container = -101 order by screen, cellX, cellY, spanX, spanY
        ''')
        
        all_rows_101 = cursor.fetchall()
        for row101 in all_rows_101:
            _id = row101[0]
            title = row101[1]

            if not title:
                title = ' '

            screenN = row101[4]
            cellx = row101[5]
            celly = row101[6]
            spanx = row101[7]
            spany = row101[8]
            itemtype = row101[9]
            appwidgetprov = row101[14]
            timemodified = row101[15]
            s = timemodified / 1000.0
            if timemodified > 0:
                modtime = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
            else:
                modtime = '0'
                
            if itemtype == 2:
                itemtype = 'Type: Directory'
                strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime)
                screen101[celly][cellx] = strtest
            elif itemtype == 4:
                itemtype = 'Type: Widget'
                text = appwidgetprov.split('/')
                strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+text[0]+'<br>Modified Time: '+modtime)
                screen101[celly:spany+celly, cellx:cellx+spanx] = strtest
            elif itemtype == 0:
                itemtype = 'App'    
                if path.isfile('./'+foldername+'/icons/'+title+'.png'):
                    strtest = str('Type :'+itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime+'<br>Icon: <br> <img src="./icons/'+title+'.png"')
                    
                else:
                    strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime+'<br>Icon: None')
            
                screen101[celly][cellx] = strtest
            
            elif itemtype == 6:
                itemtype = 'Widget'    
                if path.isfile('./'+foldername+'/icons/'+title+'.png'):
                    strtest = str('Type :'+itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime+'<br>Icon: <br> <img src="./icons/'+title+'.png"')
                    
                else:
                    strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime+'<br>Icon: None')
            
                screen101[celly][cellx] = strtest
            
            else:
                strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+text[0]+'<br>Modified Time: '+modtime)
                screen101[celly][cellx] = strtest
                
            html = '<style>table { table-layout: auto; width: 100%; height: 100%  }</style>'
            df = pd.DataFrame(screen101)
            
            html += df.to_html(escape=False)
            
            output_file = open('./'+foldername+'/Bottom_Bar.html', 'w')
            output_file.write(html)
            output_file.close()
       
    elif container == -100:
        #print('')
        #print('-100 main screens')
        #Do all the home icons
        
        cursor.execute('''
        select distinct screen from favorites where container = -100 order by screen
        ''')
        
        all_rows_scr = cursor.fetchall()
        for rowscr in all_rows_scr:
            scrctrl = rowscr[0] 
            
            a = 5
            b = 5
            homescreen = np.empty([a,b], dtype = 'object') 
            
            #print('')
            #print('Screen: '+ str(scrctrl))
            cursor.execute('''
            select * from favorites where container = -100 and screen = ? order by screen, cellX, cellY, spanX, spanY
            ''', (scrctrl,))

            all_rows_100 = cursor.fetchall()
            for row100 in all_rows_100:
                _id = row100[0]
                title = row100[1]

                if not title:
                    title = ' '

                screenN = row100[4]
                cellx = row100[5]
                celly = row100[6]
                spanx = row100[7]
                spany = row100[8]
                itemtype = row100[9]
                appwidgetprov = row100[14]
                timemodified = row100[15]
                s = timemodified / 1000.0
                
                if timemodified > 0:
                    modtime = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
                else:
                    modtime = '0'
                    
                if itemtype == 2:
                    itemtype = 'Type: Directory'
                    strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime)
                    homescreen[celly][cellx] = strtest
                elif itemtype == 4:
                    itemtype = 'Type: Widget'
                    text = appwidgetprov.split('/')
                    strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+text[0]+'<br>Modified Time: '+modtime)
                    homescreen[celly:spany+celly, cellx:cellx+spanx] = strtest
                elif itemtype == 0:
                    itemtype = 'App'
                    
                    if path.isfile('./'+foldername+'/icons/'+title+'.png'):
                        strtest = str('Type :'+itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime+'<br>Icon: <br> <img src="./icons/'+title+'.png"')
                    else:
                        strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime+'<br>Icon: None')
                    
                    homescreen[celly][cellx] = strtest
                
                elif itemtype == 6:
                    itemtype = 'Widget'
                    
                    if path.isfile('./'+foldername+'/icons/'+title+'.png'):
                        strtest = str('Type :'+itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime+'<br>Icon: <br> <img src="./icons/'+title+'.png"')
                    else:
                        strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime+'<br>Icon: None')
                    
                    homescreen[celly][cellx] = strtest
                
                else:
                    strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+text[0]+'<br>Modified Time: '+modtime)
                    homescreen[celly][cellx] = strtest
                    
            html = '<style>table { table-layout: auto; width: 100%; height: 100%  }</style>'
            df = pd.DataFrame(homescreen)
            html += df.to_html(escape=False)
           
            
            output_file = open('./'+foldername+'/MainScreen'+str(screenN)+'.html', 'w')
            output_file.write(html)
            output_file.close()
            #print(html)
            
    
    elif container > 0:
        cursor.execute('''
        select distinct container from favorites where container = ? order by screen
        ''', (container,))
        
        all_rows_scr = cursor.fetchall()
        for rowscr in all_rows_scr:
            ctrctrl = rowscr[0] 
            
            a = 5
            b = 5
            contX = np.empty([a,b], dtype = 'object') 
        
            cursor.execute('''
            select * from favorites where container = ? order by screen, cellX, cellY, spanX, spanY
            ''', (ctrctrl,))

            all_rows_100 = cursor.fetchall()
            for row100 in all_rows_100:
                _id = row100[0]
                title = row100[1]

                if not title:
                    title = ' '

                screenN = row100[4]
                cellx = row100[5]
                celly = row100[6]
                spanx = row100[7]
                spany = row100[8]
                itemtype = row100[9]
                appwidgetprov = row100[14]
                timemodified = row100[15]
                s = timemodified / 1000.0
                if timemodified > 0:
                    modtime = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
                else:
                    modtime = '0'
                
                if itemtype == 2:
                    itemtype = 'Type: Directory'
                    strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime)
                    contX[celly][cellx] = strtest
                    
                elif itemtype == 4:
                    itemtype = 'Type: Widget'
                    text = appwidgetprov.split('/')
                    strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+text[0]+'<br>Modified Time: '+modtime)
                    contX[celly:spany+celly, cellx:cellx+spanx] = strtest
                    
                elif itemtype == 0:
                    itemtype = 'App'
                    if path.isfile('./'+foldername+'/icons/'+title+'.png'):
                        strtest = str('Type :'+itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime+'<br>Icon: <br> <img src="./icons/'+title+'.png"')
                    else:
                        strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime+'<br>Icon: None')
                    
                    contX[celly][cellx] = strtest
                
                elif itemtype == 6:
                    itemtype = 'Widget'
                    if path.isfile('./'+foldername+'/icons/'+title+'.png'):
                        strtest = str('Type :'+itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime+'<br>Icon: <br> <img src="./icons/'+title+'.png"')
                    else:
                        strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+title+'<br>Modified Time: '+modtime+'<br>Icon: None')
                    
                    contX[celly][cellx] = strtest
                    
                else:
                    strtest = str(itemtype+'<br>ID: '+str(_id)+'<br>Name: '+text[0]+'<br>Modified Time: '+modtime)
                    contX[celly][cellx] = strtest    
                    #print('strstest: '+contX)
                
            html = '<style>table { table-layout: auto; width: 100%; height: 100%  }</style>'
            df = pd.DataFrame(contX)
            
            html += df.to_html(escape=False)
            
            output_file = open('./'+foldername+'/ScreenDirectory'+str(container)+'.html', 'w')
            output_file.write(html)
            output_file.close()
            contX = np.empty([a,b], dtype = 'object')
            #print(html)    