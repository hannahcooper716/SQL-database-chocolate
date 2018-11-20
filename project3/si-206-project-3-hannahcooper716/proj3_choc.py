import sqlite3
import csv
import json

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from CSV and JSON into a new database called choc.db
DBNAME = 'choc.db'
BARSCSV = 'flavors_of_cacao_cleaned.csv'
COUNTRIESJSON = 'countries.json'


def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'Bars';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Countries';
    '''
    cur.execute(statement)

    conn.commit()

    statement = '''
        CREATE TABLE 'Bars' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Company' TEXT NOT NULL,
                'SpecificBeanBarName' TEXT NOT NULL,
                'REF' TEXT NOT NULL,
                'ReviewDate' TEXT NOT NULL,
                'CocoaPercent' REAL,
                'CompanyLocation' TEXT NOT NULL,
                'CompanyLocationId' INTEGER,
                'Rating' REAL,
                'BeanType' TEXT NOT NULL,
                'BroadBeanOrigin' TEXT NOT NULL,
                'BroadBeanOriginId' INTEGER

        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Countries' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Alpha2' TEXT NOT NULL,
                'Alpha3' TEXT NOT NULL,
                'EnglishName' TEXT NOT NULL,
                'Region' TEXT NOT NULL,
                'Subregion' REAL,
                'Population' INTEGER,
                'Area' REAL

        );
    '''
    cur.execute(statement)
    conn.commit() #any time you are changing data or adding new tables you have to do this (not with queries)
    conn.close()

def opencsv():
    # file = open(BARSCSV, 'r')
    # data = list(file.readlines())
    # file.close()
    # with open(BARSCSV, newline='') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         print(row)
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    header = 0
    with open(BARSCSV) as csvfile:
        spamreader = csv.reader(csvfile)
        for x in spamreader:
            header += 1
            if header == 1:
                continue
            Company = x[0]
            SpecificBeanBarName = x[1]
            REF = x[2]
            ReviewDate = x[3]
            CocoaPercent = (float(x[4][:-1]))/100
            CompanyLocation = x[5]
            Rating = x[6]
            BeanType = x[7]
            BroadBeanOrigin = x[8]
            CompanyLocationId = ''
            BroadBeanOriginId = ''

            insertion = (None, Company,SpecificBeanBarName,REF,ReviewDate,CocoaPercent,CompanyLocation, CompanyLocationId, Rating,BeanType,BroadBeanOrigin, BroadBeanOriginId)
            statement = 'INSERT INTO "Bars" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
            conn.commit()

        conn.close()

        # for row in spamreader:
        #     print(', '.join(row))


def openjson():
    file = open(COUNTRIESJSON, 'r')
    json_str=file.read()
    data = json.loads(json_str)
    file.close()

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    for x in data:
        Alpha2 = x['alpha2Code']
        Alpha3 = x['alpha3Code']
        EnglishName = x['name']
        Region = x['region']
        Subregion = x['subregion']
        Population = x['population']
        Area = x['area']


        insertion = (None, Alpha2, Alpha3, EnglishName, Region, Subregion, Population, Area)
        statement = 'INSERT INTO "Countries" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
        conn.commit()
    conn.close()

#openjson()

def update_Id():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT Countries.Id, Bars.Id
        FROM Countries
	    JOIN Bars
	    ON Countries.EnglishName = Bars.CompanyLocation
    '''
    y = cur.execute(statement).fetchall()
    #print(y)
    for x in y:
        CountriesId= x[0]
        #print(CountriesId)
        barId = x[1]
        insert = (CountriesId, barId)
        statement = 'UPDATE Bars '
        statement += 'SET CompanyLocationId= ? '
        statement += 'WHERE Id=?'
        cur.execute(statement, insert)
        conn.commit()
    conn.close()

#update_Id()

def update_Id1():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT Countries.Id, Bars.Id
        FROM Countries
	    JOIN Bars
	    ON Countries.EnglishName = Bars.BroadBeanOrigin
    '''
    y = cur.execute(statement).fetchall()
    #print(y)
    for x in y:
        CountriesId= x[0]
        #print(CountriesId)
        barId = x[1]
        insert = (CountriesId, barId)
        statement = 'UPDATE Bars '
        statement += 'SET BroadBeanOriginId= ? '
        statement += 'WHERE Id=?'
        cur.execute(statement, insert)
        conn.commit()
    conn.close()

#update_Id1()




# Part 2: Implement logic to process user commands
def command_bars(command):
    name = {}
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    # if 'rating' in command:
    #     ratings = ''
    #     statement = 'SELECT SpecificBeanBarName, Company, CompanyLocation, Rating, CocoaPercent, BroadBeanOrigin '
    #     statement += 'FROM Bars '
    #     statement += 'ORDER BY Rating DESC'
    #
    # if 'cocoa' in command:
    #     cocoa =

    list_command = command.split()
    #print(list_command)
    #print(list_command)
    #print(list_command[1])
    if 'sellcountry'in list_command[1]:
        splitequal = list_command[1].split('=')
        name['firstparam'] = splitequal
    elif 'sourcecountry'in list_command[1]:
        splitequal = list_command[1].split('=')
        name['firstparam'] = splitequal
    elif 'sellregion'in list_command[1]:
        splitequal = list_command[1].split('=')
        name['firstparam'] = splitequal
    elif 'sourceregion'in list_command[1]:
        splitequal = list_command[1].split('=')
        name['firstparam'] = splitequal
    else:
        name['firstparam'] = 'None'
        try:
            if 'cocoa' in list_command[1]:
                name['Secondparam'] = 'CocoaPercent'
            else:
                name['Secondparam'] = 'Rating'
        except:
            name['Secondparam'] = 'Rating'
        try:
            if 'top' in list_command[-1]:
                splitequal = list_command[-1].split('=')
                name['Lastparam'] = splitequal
            elif 'bottom' in list_command[-1]:
                splitequal = list_command[-1].split('=')
                name['Lastparam'] = splitequal
            else:
                name['Lastparam'] = ["top", 10]
            return bars_execute(name)
        except:
            name['Lastparam'] = ["top", 10]
            return bars_execute(name)
    try:
        if 'ratings' in list_command[2]:
            name['Secondparam'] = "Rating"
        elif 'cocoa' in list_command[2]:
            name['Secondparam'] = "CocoaPercent"
        else:
            name['Secondparam'] = 'Rating'
    except:
        name['Secondparam'] = 'Rating'
    try:
        if 'top' in list_command[-1]:
            splitequal = list_command[-1].split('=')
            name['Lastparam'] = splitequal
        elif 'bottom' in list_command[-1]:
            splitequal = list_command[-1].split('=')
            name['Lastparam'] = splitequal
        else:
            name['Lastparam'] = ["top", 10]
        return bars_execute(name)
    except:
        name['Lastparam'] = ["top", 10]
        return bars_execute(name)

    #print(name)
    return bars_execute(name)

def bars_execute(name):
    #print(name)
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    first = name['firstparam'][0]
    next_ = name['firstparam'][1]
    second = name['Secondparam']
    last = name['Lastparam'][0]
    n = name['Lastparam'][1]
    if last == 'top':
        last = 'DESC'
    else:
        last = 'ASC'
    if type(n) == int:
        n = str(n)
    if name['firstparam'] == 'None':
        statement = 'SELECT SpecificBeanBarName, Company, CompanyLocation, Rating, CocoaPercent, BroadBeanOrigin '
        statement += 'FROM Bars '
        statement += 'ORDER BY ' + second + " "+ last + " "
        statement += 'LIMIT ' + n
        cur.execute(statement)
        # for x in cur:
        #     print(x)

    if "sellcountry" == first:
        statement = 'SELECT SpecificBeanBarName, Company, Bars.CompanyLocation, Rating, CocoaPercent, BroadBeanOrigin '
        statement += 'FROM Bars '
        statement += 'JOIN Countries '
        statement += 'ON Countries.Id = Bars.CompanyLocationId '
        statement += 'WHERE Countries.Alpha2 LIKE ? '
        statement += 'ORDER BY ' + second + ' ' + last + ' '
        statement += 'LIMIT ? '
        insert = (next_, n)
        cur.execute(statement, insert)
        # for x in cur:
        #     print(x)


    if "sourcecountry" == first:
        statement = 'SELECT SpecificBeanBarName, Company, Bars.CompanyLocation, Rating, CocoaPercent, BroadBeanOrigin '
        statement += 'FROM Bars '
        statement += 'JOIN Countries '
        statement += 'ON Countries.Id = Bars.BroadBeanOriginId '
        statement += 'WHERE Countries.Alpha2 LIKE ? '
        statement += 'ORDER BY ' + second + ' ' + last + ' '
        statement += 'LIMIT ? '
        insert = (next_, n)
        cur.execute(statement, insert)
        # for x in cur:
        #     print(x)

    if "sellregion" == first:
        statement = 'SELECT SpecificBeanBarName, Company, Bars.CompanyLocation, Rating, CocoaPercent, BroadBeanOrigin '
        statement += 'FROM Bars '
        statement += 'JOIN Countries '
        statement += 'ON Countries.EnglishName = Bars.CompanyLocation '
        statement += 'WHERE Countries.Region LIKE ? '
        statement += 'ORDER BY ' + second + ' ' + last + ' '
        statement += 'LIMIT ? '
        insert = (next_, n)
        cur.execute(statement, insert)
        # for x in cur:
        #     print(x)

    if "sourceregion" == first:
        statement = 'SELECT SpecificBeanBarName, Company, Bars.CompanyLocation, Rating, CocoaPercent, BroadBeanOrigin '
        statement += 'FROM Bars '
        statement += 'JOIN Countries '
        statement += 'ON Countries.EnglishName = Bars.BroadBeanOrigin '
        statement += 'WHERE Countries.Region LIKE ? '
        statement += 'ORDER BY ' + second + ' ' + last + ' '
        statement += 'LIMIT ? '
        insert = (next_, n)
        cur.execute(statement, insert)
        # for x in cur:
        #     print(x)
    l = []
    for x in cur:
        l.append(x)
    return l

# command_bars('bars sourceregion=Asia ratings top=6')


def command_companies(command):
    name = {}
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    list_command = command.split()
    #print(list_command)
    if 'region'in list_command[1]:
        splitequal = list_command[1].split('=')
        name['firstparam'] = splitequal
    elif 'country'in list_command[1]:
        splitequal = list_command[1].split('=')
        name['firstparam'] = splitequal
    else:
        name['firstparam'] = 'None'
        try:
            if 'cocoa' in list_command[1]:
                name['Secondparam'] = 'CocoaPercent'
            elif 'bars_sold' in list_command[1]:
                name['Secondparam'] = 'COUNT(*)'
            else:
                name['Secondparam'] = 'Rating'
        except:
            name['Secondparam'] = 'Rating'
        try:
            if 'top' in list_command[-1]:
                splitequal = list_command[-1].split('=')
                name['Lastparam'] = splitequal
            elif 'bottom' in list_command[-1]:
                splitequal = list_command[-1].split('=')
                name['Lastparam'] = splitequal
            else:
                name['Lastparam'] = ["top", 10]
            return companies_execute(name)
        except:
            name['Lastparam'] = ["top", 10]
            return companies_execute(name)
    try:
        if 'ratings' in list_command[2]:
            name['Secondparam'] = 'Rating'
        elif 'cocoa' in list_command[2]:
            name['Secondparam'] = 'CocoaPercent'
        elif 'bars_sold' in list_command[2]:
            name['Secondparam'] = 'COUNT(*)'
    except:
        name['Secondparam'] = 'Rating'
    try:
        if 'top' in list_command[-1]:
            splitequal = list_command[-1].split('=')
            name['Lastparam'] = splitequal
        elif 'bottom' in list_command[-1]:
            splitequal = list_command[-1].split('=')
            name['Lastparam'] = splitequal
        else:
            name['Lastparam'] = ["top", 10]
        return companies_execute(name)
    except:
        name['Lastparam'] = ["top", 10]
        return companies_execute(name)

    return companies_execute(name)

def companies_execute(name):
    #print(name)
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    first = name['firstparam'][0]
    next_ = name['firstparam'][1]
    second = name['Secondparam']
    last = name['Lastparam'][0]
    n = name['Lastparam'][1]
    if last == 'top':
        last = 'DESC'
    else:
        last = 'ASC'
    if type(n) == int:
        n = str(n)
    if name['firstparam'] == 'None':
        if 'CocoaPercent' == second:
            second = "AVG(Bars.CocoaPercent)"
        elif 'Rating' == second:
            second = "AVG(Bars.Rating)"
        statement = 'SELECT Company, CompanyLocation, ' + second + ' '
        statement += 'FROM Bars '
        statement += 'GROUP BY Company '
        statement += 'HAVING COUNT(*) > 4 '
        statement += 'ORDER BY ' + second + " "+ last + " "
        statement += 'LIMIT ' + n
        #print(statement)
        cur.execute(statement)
        # for x in cur:
        #     print(x)


    if "country" == first:
        if 'CocoaPercent' == second:
            second = "AVG(Bars.CocoaPercent)"
        elif 'Rating' == second:
            second = "AVG(Bars.Rating)"
        statement = 'SELECT Bars.Company, Bars.CompanyLocation, ' + second + ' '
        statement += 'FROM Bars '
        statement += 'JOIN Countries '
        statement += 'ON Countries.Id = Bars.CompanyLocationId '
        statement += 'WHERE Countries.Alpha2 LIKE ? '
        statement += 'GROUP BY Bars.Company '
        statement += 'HAVING COUNT(*) > 4 '
        statement += 'ORDER BY ' + second + ' ' + last + ' '
        statement += 'LIMIT ? '
        insert = (next_, n)
        #print(statement, insert)
        cur.execute(statement,insert)
        # for x in cur:
        #     print(x)


    if "region" == first:
        if 'CocoaPercent' == second:
            second = "AVG(Bars.CocoaPercent)"
        elif 'Rating' == second:
            second = "AVG(Bars.Rating)"
        statement = 'SELECT Bars.Company, Bars.CompanyLocation, ' + second + ' '
        statement += 'FROM Bars '
        statement += 'JOIN Countries '
        statement += 'ON Countries.Id = Bars.CompanyLocationId '
        statement += 'WHERE Countries.Region LIKE ? '
        statement += 'GROUP BY Bars.Company '
        statement += 'HAVING COUNT(*) > 4 '
        statement += 'ORDER BY ' + second + ' ' + last + ' '
        statement += 'LIMIT ? '
        insert = (next_, n)
        #print(statement, insert)
        cur.execute(statement,insert)
        # for x in cur:
        #     print(x)
    l = []
    for x in cur:
        l.append(x)
    return l

#command_companies('companies region=Europe bars_sold top=5')

def command_countries(command):
    name = {}
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    list_command = command.split()
    #print(list_command)
    if 'region'in list_command[1]:
        splitequal = list_command[1].split('=')
        name['firstparam'] = splitequal
    else:
        name['firstparam'] = 'None'
        #print('line')
        try:
            #print('line')
            if 'sellers'in list_command[1]:
                name['Secondparam'] = 'sellers'
            elif 'sources'in list_command[1]:
                name['Secondparam'] = 'sources'
            else:
                name['Secondparam'] = 'sellers'
                #print('line')
                try:
                    #print('line')
                    if 'cocoa' == list_command[1]:
                        name['Thirdparam'] = 'CocoaPercent'
                    elif 'bars_sold' == list_command[1]:
                        name['Thirdparam'] = 'COUNT(*)'
                    else:
                        name['Thirdparam'] = 'Rating'
                    #print(name)
                except:
                    name['Thirdparam'] = 'Rating'
                try:
                    if 'top' in list_command[-1]:
                        splitequal = list_command[-1].split('=')
                        name['Lastparam'] = splitequal
                    elif 'bottom' in list_command[-1]:
                        splitequal = list_command[-1].split('=')
                        name['Lastparam'] = splitequal
                    else:
                        name['Lastparam'] = ["top", 10]
                    return countries_execute(name)
                except:
                    name['Lastparam'] = ["top", 10]
                    return countries_execute(name)
        except:
            name['Secondparam'] = 'sellers'
            #print('line')
            try:
                print('line')
                if 'cocoa' == list_command[1]:
                    name['Thirdparam'] = 'CocoaPercent'
                elif 'bars_sold' == list_command[1]:
                    name['Thirdparam'] = 'COUNT(*)'
                else:
                    name['Thirdparam'] = 'Rating'
            except:
                name['Thirdparam'] = 'Rating'
            try:
                if 'top' in list_command[-1]:
                    splitequal = list_command[-1].split('=')
                    name['Lastparam'] = splitequal
                elif 'bottom' in list_command[-1]:
                    splitequal = list_command[-1].split('=')
                    name['Lastparam'] = splitequal
                else:
                    name['Lastparam'] = ["top", 10]
                return countries_execute(name)
            except:
                name['Lastparam'] = ["top", 10]
                return countries_execute(name)
        try:
            if 'ratings' in list_command[2]:
                name['Thirdparam'] = 'Rating'
            elif 'cocoa' in list_command[2]:
                name['Thirdparam'] = 'CocoaPercent'
            elif 'bars_sold' in list_command[2]:
                name['Thirdparam'] = 'COUNT(*)'
        except:
            name['Thirdparam'] = 'Rating'
        try:
            if 'top' in list_command[-1]:
                splitequal = list_command[-1].split('=')
                name['Lastparam'] = splitequal
            elif 'bottom' in list_command[-1]:
                splitequal = list_command[-1].split('=')
                name['Lastparam'] = splitequal
            else:
                name['Lastparam'] = ["top", 10]
            return countries_execute(name)
        except:
            name['Lastparam'] = ["top", 10]
            return countries_execute(name)
    try:
        if 'sellers'in list_command[2]:
            name['Secondparam'] = 'sellers'
        elif 'sources'in list_command[2]:
            name['Secondparam'] = 'sources'
        else:
            name['Secondparam'] = 'sellers'
    except:
        name['Secondparam'] = 'sellers'
        try:
            if 'ratings' in list_command[2]:
                name['Thirdparam'] = 'Rating'
            elif 'cocoa' in list_command[2]:
                name['Thirdparam'] = 'CocoaPercent'
            elif 'bars_sold' in list_command[2]:
                name['Thirdparam'] = 'COUNT(*)'
        except:
            name['Thirdparam'] = 'Rating'
        try:
            if 'top' in list_command[-1]:
                splitequal = list_command[-1].split('=')
                name['Lastparam'] = splitequal
            elif 'bottom' in list_command[-1]:
                splitequal = list_command[-1].split('=')
                name['Lastparam'] = splitequal
            else:
                name['Lastparam'] = ["top", 10]
            return countries_execute(name)
        except:
            name['Lastparam'] = ["top", 10]
            return countries_execute(name)
    try:
        if 'ratings' in list_command[3]:
            name['Thirdparam'] = 'Rating'
        elif 'cocoa' in list_command[3]:
            name['Thirdparam'] = 'CocoaPercent'
        elif 'bars_sold' in list_command[3]:
            name['Thirdparam'] = 'COUNT(*)'
    except:
        name['Thirdparam'] = 'Rating'
        try:
            if 'top' in list_command[-1]:
                splitequal = list_command[-1].split('=')
                name['Lastparam'] = splitequal
            elif 'bottom' in list_command[-1]:
                splitequal = list_command[-1].split('=')
                name['Lastparam'] = splitequal
            else:
                name['Lastparam'] = ["top", 10]
            return countries_execute(name)
        except:
            name['Lastparam'] = ["top", 10]
            return countries_execute(name)
    try:
        if 'top' in list_command[-1]:
            splitequal = list_command[-1].split('=')
            name['Lastparam'] = splitequal
        elif 'bottom' in list_command[-1]:
            splitequal = list_command[-1].split('=')
            name['Lastparam'] = splitequal
        else:
            name['Lastparam'] = ["top", 10]
        return countries_execute(name)
    except:
        name['Lastparam'] = ["top", 10]
        return countries_execute(name)

    #print(name)
    return countries_execute(name)
def countries_execute(name):
    #print(name)
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    first = name['firstparam'][0]
    next_ = name['firstparam'][1]
    second = name['Secondparam']
    third = name['Thirdparam']
    last = name['Lastparam'][0]
    n = name['Lastparam'][1]
    if last == 'top':
        last = 'DESC'
    else:
        last = 'ASC'
    if type(n) == int:
        n = str(n)
    if name['firstparam'] == 'None':
        if 'sellers' == second:
            second = 'Bars.CompanyLocationId'
        elif 'sources' == second:
            second = 'Bars.BroadBeanOriginId'
        if 'CocoaPercent' == third:
            third = "AVG(Bars.CocoaPercent)"
        elif 'Rating' == third:
            third = "AVG(Bars.Rating)"
        statement = 'SELECT Countries.EnglishName, Countries.Region, ' + third + ' '
        statement += 'FROM Countries '
        statement += 'JOIN Bars '
        statement += 'ON Countries.Id = ' + second + ' '
        statement += 'GROUP BY ' + second + ' '
        statement += 'HAVING COUNT(*) > 4 '
        statement += 'ORDER BY ' + third + " "+ last + " "
        statement += 'LIMIT ' + n
        #print(statement)
        cur.execute(statement)
        # for x in cur:
        #     print(x)

    if 'region' == first:
        if 'sellers' == second:
            second = 'Bars.CompanyLocationId'
        elif 'sources' == second:
            second = 'Bars.BroadBeanOriginId'
        if 'CocoaPercent' == third:
            second = "AVG(Bars.CocoaPercent)"
        elif 'Rating' == third:
            third = "AVG(Bars.Rating)"
        #print(second)
        statement = 'SELECT Countries.EnglishName, Countries.Region, ' + third + ' '
        statement += 'FROM Bars '
        statement += 'JOIN Countries '
        statement += 'ON Countries.Id = ' + second + ' '
        statement += 'WHERE Countries.Region LIKE ? '
        statement += 'ORDER BY ' + third + ' ' + last + ' '
        statement += 'LIMIT ? '
        #print(statement)
        #print(second)
        insert = (next_, n)
        cur.execute(statement,insert)
        # for x in cur:
        #     print(x)
    l = []
    for x in cur:
        l.append(x)
    return l

#command_countries('countries sellers cocoa')


def command_regions(command):
    name = {}
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    list_command = command.split()
    #print(list_command)
    if 'sellers' in list_command[1]:
        name['firstparam'] = 'sellers'
        #print('line')
    elif 'sources'in list_command[1]:
        name['firstparam'] = 'sources'
    else:
        name['firstparam'] = 'sellers'
        try:
            if 'cocoa' in list_command[1]:
                name['Secondparam'] = 'CocoaPercent'
            elif 'bars_sold' in list_command[1]:
                name['Secondparam'] = 'COUNT(*)'
            else:
                name['Secondparam'] = 'Rating'
        except:
            name['Secondparam'] = 'Rating'
        try:
            if 'top' in list_command[-1]:
                splitequal = list_command[-1].split('=')
                name['Lastparam'] = splitequal
            elif 'bottom' in list_command[-1]:
                splitequal = list_command[-1].split('=')
                name['Lastparam'] = splitequal
            else:
                name['Lastparam'] = ["top", 10]
            return regions_execute(name)
        except:
            name['Lastparam'] = ["top", 10]
            return regions_execute(name)
    try:
        if 'ratings' in list_command[2]:
            name['Secondparam'] = 'Rating'
        elif 'cocoa' in list_command[2]:
            name['Secondparam'] = 'CocoaPercent'
        elif 'bars_sold' in list_command[2]:
            name['Secondparam'] = 'COUNT(*)'
    except:
        name['Secondparam'] = 'Rating'
    try:
        if 'top' in list_command[-1]:
            splitequal = list_command[-1].split('=')
            name['Lastparam'] = splitequal
        elif 'bottom' in list_command[-1]:
            splitequal = list_command[-1].split('=')
            name['Lastparam'] = splitequal
        else:
            name['Lastparam'] = ["top", 10]
        return regions_execute(name)
    except:
        name['Lastparam'] = ["top", 10]
        return regions_execute(name)

    #print(name)

    return regions_execute(name)

def regions_execute(name):
    #print(name)
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    first = name['firstparam']
    #next_ = name['firstparam'][1]
    second = name['Secondparam']
    last = name['Lastparam'][0]
    n = name['Lastparam'][1]
    if last == 'top':
        last = 'DESC'
    else:
        last = 'ASC'
    if type(n) == int:
        n = str(n)
    # if name['firstparam'] == 'None':
    #     statement = 'SELECT Countries.Region, ' + second + ' '
    #     statement += 'FROM Countries '
    #     statement += 'JOIN Bars '
    #     statement += 'ON Countries.Id = Bars.CompanyLocationId '
    #     statement += 'ORDER BY ' + second + " "+ last + " "
    #     statement += 'LIMIT ' + n
    #     print(statement)
    #     cur.execute(statement)
    #     for x in cur:
    #         print(x)
    if "sellers" == first:
        if 'CocoaPercent' == second:
            second = "AVG(Bars.CocoaPercent)"
        elif 'Rating' == second:
            second = "AVG(Bars.Rating)"
        statement = 'SELECT Countries.Region, ' + second + ' '
        statement += 'FROM Bars '
        statement += 'JOIN Countries '
        statement += 'ON Countries.Id = Bars.CompanyLocationId '
        #statement += 'WHERE Countries.Region LIKE ? '
        statement += 'GROUP BY Countries.Region '
        statement += 'HAVING COUNT(*) > 4 '
        statement += 'ORDER BY ' + second + ' ' + last + ' '
        statement += 'LIMIT ? '
        insert = (n,)
        #print(statement, insert)
        cur.execute(statement,insert)
        # for x in cur:
        #     print(x)
    if "sources" == first:
        if 'CocoaPercent' == second:
            second = "AVG(Bars.CocoaPercent)"
        elif 'Rating' == second:
            second = "AVG(Bars.Rating)"
        statement = 'SELECT Countries.Region, ' + second + ' '
        statement += 'FROM Bars '
        statement += 'JOIN Countries '
        statement += 'ON Countries.Id = Bars.BroadBeanOriginId  '
        #statement += 'WHERE Countries.Region LIKE ? '
        statement += 'GROUP BY Countries.Region '
        statement += 'HAVING COUNT(*) > 4 '
        statement += 'ORDER BY ' + second + ' ' + last + ' '
        statement += 'LIMIT ? '
        insert = (n,)
        #print(statement, insert)
        cur.execute(statement,insert)
        # for x in cur:
        #     print(x)
    l = []
    for x in cur:
        l.append(x)
    return l


#command_regions('regions sellers cocoa top=5')


def process_command(command):
    x = []
    if 'bars'== command.split()[0]:
        b = command_bars(command)
        return b
    if 'companies' == command.split()[0]:
        b = command_companies(command)
        return b
    if 'regions' == command.split()[0]:
        b = command_regions(command)
        return b
    if 'countries' == command.split()[0]:
        b = command_countries(command)
        return b



def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 3: Implement interactive prompt. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'help':
            print(help_text)
            continue
        c = process_command(response)
        if 'bars'== response.split()[0]:
            for x in c:
                print(x[0], x[1], x[2], x[3], x[4], x[5])
        elif 'companies' == response.split()[0]:
            for x in c:
                print(x[0], x[1], x[2])
        elif 'regions' == response.split()[0]:
            for x in c:
                print(x[0], x[1])
        elif 'countries' == response.split()[0]:
            for x in c:
                print(x[0], x[1], x[2])
        elif 'exit' in response:
            print('Bye')
        else:
            print('command not recognized: ')
            print(response)

# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    interactive_prompt()
    # init_db()
    # opencsv()
    # openjson()
    # update_Id()
    # update_Id1()
    #print(process_command('bars sourceregion=Asia ratings top=6'))
