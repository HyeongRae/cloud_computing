from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="961025r",
	database="olympic"
)

def index(request):
	sql = [
		"SELECT c_name, gold, silver, bronze FROM country ORDER BY gold DESC",
		"SELECT p.player_id, p.p_name, p.gender, p.date_of_birth, c.c_name FROM player AS p" +
		", country AS c WHERE p.c_code = c.c_code",
		"SELECT * FROM olympic_game"
	]
	mycursor = mydb.cursor()
	
	mycursor.execute(sql[0])
	rank = mycursor.fetchall()
	
	mycursor.execute(sql[1])
	athlete = mycursor.fetchall()
	
	mycursor.execute(sql[2])
	game = mycursor.fetchall()
	
	find_game = ""
	
	if request.method == "POST":
		if(request.POST.get("find_athlete")):
			find_athlete = request.POST.get("find_athlete")
			sql[1] += " AND p.p_name LIKE '" + find_athlete+ "%'"
			mycursor.execute(sql[1])
			athlete = mycursor.fetchall()
		if(request.POST.get("find_game")):
			find_game = request.POST.get("find_game")
			sql[2] += " WHERE e_name LIKE '" + find_game +"%'"
			mycursor.execute(sql[2])
			game = mycursor.fetchall()
			
	context = {
		"rank": rank,
		"athlete": athlete,
		"game" : game,
		"find_game" : find_game,
	}
	return render(request, 'index/index.html', context)
