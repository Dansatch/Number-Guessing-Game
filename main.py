from flask import *
import functions

app = Flask(__name__)

#Secret key used in passing flash messages to template file
app.secret_key = "guess123"
    
#Landing Page rendering
@app.route('/')
@app.route('/index')
def index(message = ""): 
    description = "Number Guessing Game"
    if 'trials_left' not in session:
        session['trials_left'] = 11
        session['correct_answer'] = functions.get_random_number()

    return render_template('index.html', title=description, trials_left = session['trials_left'], response = message)

#Gets called using POST request once someone submits a guess
@app.route('/guess',methods=["POST"])
def guess():
    #Decrements trials_left by one for every guess attempt by the user
    session['trials_left'] -= 1
    
    #Checks if the user has failed
    if (session['trials_left'] <= 0):
        flash("You lose")
        flash("Answer: " + str(session['correct_answer']) + ". To play again, hit the restart button")
        flash("error")
        return index("You lose!!")
    
    #Checks if user submitted an empty input
    if(request.form["user_answer"] == ""):
        user_answer = 0
    else:
        user_answer = int(request.form["user_answer"])

    #Checks if user's answer is correct
    if (user_answer == session['correct_answer']):
        flash("You win")
        flash("Answer: " + str(session['correct_answer']) + ". To play again, hit the restart button")
        flash("success")
        return index("You win!!")
    
    #Checks how user's answer is wrong
    if (user_answer > session['correct_answer']):
        return index(str(user_answer) + " is too high, try again!!")
    
    if (user_answer < session['correct_answer']):
        return index(str(user_answer) + " is too low, try again!!")


#Restarting guessing game on button click
@app.route('/restart',methods=["POST", "GET"])
def restart():
    session['trials_left'] = 11
    session['correct_answer'] = functions.get_random_number()
    return index()






