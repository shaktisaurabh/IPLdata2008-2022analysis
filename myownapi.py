#API's are functions that exist on server which can be accessed using URL
#And the output of this is in JSON form which can be understood by any progra
#programming language. When we call this function on server, it is called
#making an API call.
#In a basic Flask app, the a local server is made and the computer itself
#acts as both client and server. The browser acts as browser and the Vs code
#VS code acts like server. 
#APIs are function on a server which can be accessed using url , output
#of api is in the form of JSON(java script on notation) which can be understood
#by all programming languages and hence softwares that use various 
#programming languages to make API calls can understand the json output and
#use it for their own purpose, DataFrame.shape[0] is used to find the 
#number of rows of a DataFrame. request.args.get(variable_name) is how we
#get the value of a variable. 
#for some reason list or string as dict value was getting jsonified but
#not int hence they have to be converted into string in order to work 
#Suppose we have a product page which has a lot of products and in order 
#to get info about each product we click on the products, as soon as
#we click the product the id of that respective product is sent through
#API call and info about that is extracted from database and sent to
#desrciption page and added using ninja technique which is used to 
#write python codes on an HTML page. We neednot create crores of HTML
#pages just to deal with description of crores of prodcuts, we can ac
#quire info about products from databases and paste it using ninja 
#technique. Ids are sent to database through URL using GET methods. 

from flask import Flask,request,jsonify 
import myownapisIPLDATAanalysis as mps 

app=Flask(__name__) 

@app.route('/n') 
def amba1():
    return "hello"

@app.route('/') 
def amba():
    teams=mps.teamlist() 
    return jsonify(teams) 

@app.route('/mand') 
def amba2():
    team1=request.args.get('team1') 
    team2=request.args.get('team2') 
    teams=mps.team1Vteam2(team1,team2) 
    return jsonify(teams) 

@app.route('/manman') 
def amba3():
    teamb=request.args.get('team')
    khand=mps.all_record(teamb)
    return jsonify(khand) 

@app.route('/mumba') 
def amba4():
    teamb=request.args.get('team') 
    khand=mps.teamAPI(teamb) 
    return jsonify(khand) 

@app.route('/mumba1') 
def amba5():
    batter=request.args.get('batter') 
    khand1=mps.player_record(batter) 
    return jsonify(khand1) 

@app.route('/mumba2') 
def amba6():
    batter=request.args.get('batter') 
    team=request.args.get('team') 
    khand2=mps.batsmanvsteam(batter,team) 
    return jsonify(khand2) 

@app.route('/mumba3') 
def amba7():
    bowler=request.args.get('bowler') 
    khand3=mps.bowler_record(bowler) 
    return jsonify(khand3) 

@app.route('/mumba4') 
def amba8():
    bowler=request.args.get('bowler') 
    team=request.args.get('team') 
    khand4=mps.bowlervsteam(bowler,team) 
    return jsonify(khand4)   


if __name__=="__main__":
    app.run(debug=True)