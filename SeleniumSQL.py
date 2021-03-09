
import time
import mysql.connector

mydb = mysql.connector.connect(
    host="yourHost",
    user="yourUsername",
    passwd="yourPassword",
    database="yourDatabaseName"
)

mycursor = mydb.cursor()



def NewOverallRaiderioEntry(currentArr, tableName):
    for x in range(100):
        sqlStatement = "INSERT INTO `"+ tableName +"` (`rank`, `name`, score, class, spec, `role`, covenant, faction, region, `date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        val = (currentArr[x][0], currentArr[x][1], currentArr[x][2], currentArr[x][3], currentArr[x][4], currentArr[x][5], currentArr[x][6], currentArr[x][7], currentArr[x][8], currentArr[x][9]) 
        mycursor.execute(sqlStatement, val)
        mydb.commit()
        print( currentArr[x][1] + "'s record inserted!")


def NewRoleRaiderioEntry(currentArr, tableName, whichRole):
    for x in range(100):
        sqlStatement = "INSERT INTO `"+ tableName +"` (`rank`, `name`, score, class, spec, `role`, covenant, faction, region, `date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        val = (currentArr[whichRole][x][0], currentArr[whichRole][x][1], currentArr[whichRole][x][2], currentArr[whichRole][x][3], currentArr[whichRole][x][4], currentArr[whichRole][x][5], currentArr[whichRole][x][6], currentArr[whichRole][x][7], currentArr[whichRole][x][8], currentArr[whichRole][x][9]) 
        mycursor.execute(sqlStatement, val)
        mydb.commit()
        print( currentArr[whichRole][x][1] + "'s record inserted!")
        

def NewSpecRaiderioEntry(currentArr, tableName, whichSpec):
    for x in range(100):
        sqlStatement = "INSERT INTO `"+ tableName +"` (`rank`, `name`, score, covenant, faction, region, `date`) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        val = (currentArr[whichSpec][x][0], currentArr[whichSpec][x][1], currentArr[whichSpec][x][2], currentArr[whichSpec][x][3], currentArr[whichSpec][x][4], currentArr[whichSpec][x][5], currentArr[whichSpec][x][6]) 
        mycursor.execute(sqlStatement, val)
        mydb.commit()
        print( currentArr[whichSpec][x][1] + "'s record inserted!")
        





