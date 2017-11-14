# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 18:04:01 2017

@author: Alexander Schreiner e1525684
Aufgabe 2: Textbasierte Parametereingabe

****************************************
Format configfile:
    [Section_1]
    option_11 = parameter_11
    option_12 = parameter_12
    .
    .
    .
    [Section_n]
    option_n1 = parameter_n1
    option_n2 = parameter_n2
***************************************    
Implementierung set_Parameters(configfile):
    
    1.Prüfen ob das configfile existiert
    2.Lesen der Parameter aus dem configfile und der Datenbank
    3.Durchführung der Parameterchecks 1 und 2
        3.1 Type_check
        3.2 Parameter_missing_check
    4.Schreiben der Paramter in das globale Dictionary
    5.Condition_check
    
"""

import configparser as cp
import os

class InvalidParametersError(Exception):
    pass

#***************************************************************************

def  set_Parameters(configfile):
    """
    liest aus dem übergebenen configfile die Parameter und prüft sie auf Korrektheit.
    Ist der Typ- und Parameter_missing_check positiv werden die Defaultwerte überschrieben
    Danach wird der Condition_check durchgeführt
    
    FileNotFoundError(): Wenn der Dateiname vom configfile im Arbeitsverzeichnis nicht gefunden wurde
    InvalidParametersError(): Wenn einer der checks nicht bestanden wurde
    """

    db_file = os.path.join(os.path.dirname(__file__), 'parameters.db')
    database_dict = __read_configfile(db_file)
    config_dict = __read_configfile(configfile) 
        
    for key, value in database_dict.items():
        globals()[key] = value[0]
    
    check1 = __Parameter_missing_check(database_dict, config_dict)  
    check2 = __Parameter_type_check(config_dict)
    
    if(check1 and check2):
        for key, value in config_dict.items():
            if(type(globals()[key]) == float or globals()[key] == float):
                globals()[key] = float(value)
            else:
                globals()[key] = value
                
        check3 = __Parameter_condition_check(database_dict)  
            
    if((check1 and check2 and check3) == False):
        raise InvalidParametersError() 
    

        
#***************************************************************************

def __read_configfile(configfile):
    """ 
    Liest das config-file aus dem übergebenen Pfad und retoniert die
    Parameter als Dictionary: {'Parametername': Parameterwert...
                                  
    Falls die Datei nicht gefunden wurde wird ein "FileNotFoundError" ausgegeben
    """

    if(os.path.exists(configfile) == False):
       raise FileNotFoundError(str(configfile) + ' doesnt exist in working directory!')
    
    config = cp.ConfigParser()
    config.read(configfile)

    config_dict = {}
    
    for section in config.sections():
       for option in config.options(section):
           config_dict[option.upper()] = eval(config.get(section,option),{},{})
            
    return config_dict      
              
                
#***************************************************************************               
            
def __Parameter_type_check(config_dict):
    """ 
    Prüft die Datentypen der Parameter im übergebenen config_dict.
    Ist der Datentyp korrekt, wird der Defatultwert überschrieben,
    andernfalls erfolgt eine spezifische Fehlerausgabe auf der Konsole
    """

    check_passed = True
    for key, value in config_dict.items():
    
            #1. Prüfen ob Parameter aus der Datenbank in die Parameterliste
            #aufgenommen wurde
            #Fehlermeldung
            if(key in globals()): 
        
                #2. Prüfen ob der Datentyp des Parameters im configfile ungleich 
                #dem Defaultwert aus der Datenbank ist          
                if(type(globals()[key]) != type(value)):
                
                    #2.1 Fallunterscheidung
                
                    #Fall 1: Datentyp des Defaultwertes ist 'type'
                    if(type(globals()[key]) == type):
                   
                        #Prüfen ob Datentyp des Parameters im configfile gleich
                        #dem des Defaultwertes ist.
                        if(not(globals()[key] == type(value) or (globals()[key] == float and type(value) == int))):                           
                          
                            check_passed = False
                       
                    #Fall 2: Datentyp des Defaultwertes ist 'float'
                    elif(type(globals()[key]) == float and type(value) != int):
                    
                        print('Type of parameter "' + key + '" should be "' + str(type(globals()[key]))+ '"')
                        check_passed = False
                
                    #Fall 3: Datentyp ist nicht 'float' oder 'type' und unterscheidet sich vom
                    #Datentyp des Defaultwertes
                    else:
                        print('Type of parameter "' + key + '" should be "' + str(type(globals()[key]))+ '"')
                        check_passed = False
            
            else:
                print('Undefined parameter "'+ key)
                check_passed = False
    
    return check_passed
    
#***************************************************************************

def __Parameter_missing_check(database_dict, config_dict):
    """
    Prüft ob alle notwendigen Parameter im config-file angegeben wurden.
    Notwendigkeit wird determiniert, wenn der Defaultwert in der Datenbank ein Datentyp ist
    Im Fehlerfall erfolgt eine spezifische Fehelermeldung auf der Konsole
    """
    
    check_passed = True
    
    for key, value in database_dict.items():
        if(type(value[0]) == type):
            if key in config_dict:
                continue
            else:
                print ('Parameter "' + key + '" must be configured')
                check_passed = False
       
    return check_passed
    
#*************************************************************************** 

def __Parameter_condition_check(database_dict):
    """ 
    Prüft ob die Parameter im config-file der geforderten Bedingung aus der Datenbank
    entspricht
    Im Fehlerfall erfolgt eine spezifische Fehelermeldung auf der Konsole
    """
    
    check_passed = True
    
    for key, value in database_dict.items():
        
        if((value[1]) == None):
            continue
        else:
            if (eval(value[1]) == False):
                print('Condition "' + value[1] + '" is not conformed')
                check_passed = False
                
    return check_passed

#*************************************************************************** 
   

    
    
    

