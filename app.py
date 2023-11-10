from flask import Flask,request,render_template
import pandas as pd
import numpy as np
import pickle

data = pickle.load(open("data.pkl","rb"))

df = pd.DataFrame(data)

sim_dist = pickle.load(open("cosine_dist.pkl","rb"))




app = Flask(__name__)

def recommend(movie):
    try:
        Movie = movie.lower()
        Movie = Movie.strip()
        indd = df[df["title"]== Movie].index[0]
        dis = sim_dist[indd]
        movies = sorted(list(enumerate(dis)),reverse=True,key= lambda x: x[1])[1:6]
        movie_list = [df["title"].iloc[j] for j in [i[0] for i in movies]]
        return movie_list
    except:
        return("Please Try another movie") 
    
print(recommend("Avatar"))


@app.route("/", methods = ["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/predict",methods =["POST"])
def predict():

    Movie = request.form.get("Movie")
    movie_list = recommend(Movie)


    return render_template("index.html",movie_list=movie_list)



if __name__ == "__main__":
    app.run(debug = True,host="127.0.0.1",port=8000)