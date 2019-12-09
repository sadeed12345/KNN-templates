from flask import Flask , render_template , request, url_for, redirect
import pandas as pd 
import json
import math
import re
import csv

app = Flask(__name__)
path = r'E:\Sadeed\data.csv'
@app.route('/')
def main():
    return render_template('index.html')


def Superclean(movie):
    listofGenres = []
    movieData = {"title":"","genres":""}

    match = re.findall(r'\'([^\']*)\'', movie[1])
    for item in match:
        listofGenres.append(item)
		
    
    movieData['genres'] = listofGenres
    movieData['title'] = movie[0]
    return movieData




def KNN(standardMovie):
    sortedMoviesList = []
    movieDistance = []
    finalList = []
    index = [1,2,3]
    with open(path) as csv_file:
        moviesList = csv.reader(csv_file, delimiter=',')
        
        next(moviesList, None)
      
        for movie in moviesList:
            movie = Superclean(movie)
            movieTitle = movie['title']
            
            if(movie['title']!=standardMovie['title']):
                movieDistance=[]
                euclideanDistance = 0
                
            
                for genre in movie['genres']:
                    for standardGenre in standardMovie['genres']:
                        
                        if genre!=standardGenre:
                    
                            euclideanDistance+=1
                        
            
               
                
                #euclideanDistance = math.sqrt(euclideanDistance)
                movieDistance.append(euclideanDistance)
                movieDistance.append(movie['title'])
                sortedMoviesList.append(movieDistance)
              
    
    sortedMoviesList.sort()
    
    for i in index:
        finalList.append(sortedMoviesList[i][1])
    #sortedMoviesList = sorted(sortedMoviesList, key=lambda x: x[0])
    return (finalList)











@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        mName = request.form['movieName']
        
        #csv_file = csv.reader(open('test.csv', "rb"), delimiter=",")
        with open(path) as csv_file:
            csv_file = csv.reader(csv_file, delimiter=',')  
            for row in csv_file:
                if row[0]==mName:
                    #return row[2]
                    #csv_file.close()
                    standardMovie = Superclean(row)
                    
                    break
                # mName
        moviesList = KNN(standardMovie)
        return render_template('results.html',movieName=mName,firstName= moviesList[0],secondName = moviesList[1],thirdName = moviesList[2])
        return "******Sorry Record not found******"
    return "abc"
app.run()