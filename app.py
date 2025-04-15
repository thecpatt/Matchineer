import mLists as mL

import re
import os
from datetime import datetime, timedelta
from threading import Thread

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from dotenv import load_dotenv
load_dotenv()

import settings as st

from better_profanity import profanity

app = Flask(__name__)

app.config['SECRET_KEY'] = st.SECRET_KEY

app.config['MYSQL_HOST'] = st.MYSQLHOST
app.config['MYSQL_PORT'] = st.MYSQL_PORT
app.config['MYSQL_USER'] = st.MYSQL_USER
app.config['MYSQL_PASSWORD'] = st.MYSQL_PASSWORD
app.config['MYSQL_DB'] = st.MYSQL_DB
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

questions = {
    "start_form": {
        "title": "Enter your email to get started!",
        "questions": {
            "Enter your App State email" : {"type": "text"},
        }
    },
    "personal_info": {
        "title": "Enter your personal information",
        "questions": {
            mL.name_question : {"type": "text"},
            mL.class_year_question : {"options": mL.class_year, "type": "radio"},
            mL.gender_question : {"options": mL.gender, "type": "radio"},
            mL.age_question : {"options": mL.age, "type": "radio"},
            mL.form_gain_question : {"options": mL.form_gain, "type": "radio"},
        }
    },
    "interests": {
        "title": "Enter your interests and hobbies",
        "questions": {
            mL.interests_question : {"options": mL.sport_hobbies, "type": "checkbox", "min": 0, "max": 3},
            mL.interests_question_2 : {"options": mL.shows_and_movies, "type": "checkbox", "min": 0, "max": 3},
            mL.interests_question_3 : {"options": mL.games_and_puzzles, "type": "checkbox", "min": 0, "max": 3},
            mL.interests_question_4 : {"options": mL.spiritual_and_personal, "type": "checkbox", "min": 0, "max": 3},
            mL.interests_question_5 : {"options": mL.food_and_social, "type": "checkbox", "min": 0, "max": 3},
        }
    },
    "personality_quiz": {
        "title": "Enter your responses to each statement",
        "questions": {
            mL.mbti_1_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_1_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_1_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_1_inverse_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_1_inverse_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_1_inverse_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_2_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_2_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_2_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_2_inverse_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_2_inverse_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_2_inverse_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_3_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_3_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_3_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_3_inverse_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_3_inverse_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_3_inverse_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_4_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_4_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_4_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_4_inverse_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_4_inverse_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
            mL.mbti_4_inverse_random.pop() : {"options": mL.myers_briggs, "type": "radio"},
        }
    },
    "summary": {
        "title": "Here are your matches:"
    }
}

@app.route("/")
def home():
    session.clear()
    return render_template("home.html")

@app.route("/<page_name>", methods=["GET", "POST"])
def page(page_name):
    start_page = "start_form"

    if "Enter your App State email" not in session and page_name != start_page:
        return redirect(url_for("page", page_name=start_page))
    
    if page_name not in questions:
        return redirect(url_for("summary"))
    
    page_data = questions[page_name]
    error = None
    previous_inputs = session.get(page_name, {})

    if request.method == "POST":
        answers = {}
        for question, config in page_data.get("questions", {}).items():
            if config["type"] == "checkbox":
                selected_options = request.form.getlist(question)
                if not (config.get("min", 0) <= len(selected_options) <= config.get("max", float("inf"))):
                    error = f"For '{question}', select between {config['min']} and {config['max']} options."
                    break
                answers[question] = selected_options

            elif config["type"] == "radio":
                selected_option = request.form.get(question)
                if not selected_option:
                    error = f"Please select an option for '{question}'."
                    break
                answers[question] = selected_option

            elif config["type"] == "text":
                input_text = request.form.get(question, "").strip()
                censored_text = profanity.censor(input_text)
                if question == mL.name_question:
                    final_text = re.match(r"^[A-Za-z]+(-[A-Za-z]+)*$", censored_text)
                    if final_text == None:
                        error = f"Enter a valid name for your name."
                        break
                elif question == "Enter your App State email":
                    cursor = mysql.connection.cursor()
                    cursor.execute(''' SELECT user_email, entry_date FROM user_responses ''')
                    users_data = cursor.fetchall() 
                    cursor.close() 
                    total_entry_dates = []  
                    for item in users_data:
                        if item.get("user_email") == input_text:
                            total_entry_dates.append(item.get("entry_date"))

                    if len(total_entry_dates) != 0:
                        date_diff = datetime.now() - datetime.strptime(total_entry_dates[-1], "%Y-%m-%d %H:%M:%S.%f")
                        date_buffer = timedelta(seconds=30)
                        if date_diff < date_buffer:
                            error = f"You cannot fill out a form at this time"
                            break
              
                    final_text = re.match(r"^[A-Za-z0-9._%+-]+@appstate\.edu$", censored_text)
                    if final_text == None:
                        error = f"Enter a valid App State email."
                        break
                answers[question] = censored_text
        
        if not error:
            session.update(answers)  # Save answers
            next_page = get_next_page(page_name)
            return redirect(url_for("page", page_name=next_page))
            
    return render_template("form.html", page_name=page_name, page_data=page_data, error=error, previous_inputs=previous_inputs)

def get_next_page(current_page):
    page_list = list(questions.keys())
    current_index = page_list.index(current_page)
    return page_list[current_index + 1] if current_index + 1 < len(page_list) else "summary"

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/summary")
def summary():

    if len(session) != 35:
        return redirect(url_for("home"))

    user_name = get_answers(mL.name_question)
    user_email = get_answers("Enter your App State email")
    entry_date = datetime.now()
    class_year = get_answers(mL.class_year_question)
    gender = get_answers(mL.gender_question)
    age = get_answers(mL.age_question)
    form_gain = get_answers(mL.form_gain_question)
    sport_hobbies = get_answers(mL.interests_question)
    shows_and_movies = get_answers(mL.interests_question_2)
    games_and_puzzles = get_answers(mL.interests_question_3)
    spiritual_and_personal = get_answers(mL.interests_question_4)
    food_and_social = get_answers(mL.interests_question_5)
    mbti_1 = mbti_score_sum(mbti_score(mL.mbti_1), mbti_score_inverse(mL.mbti_1_inverse))
    mbti_2 = mbti_score_sum(mbti_score(mL.mbti_2), mbti_score_inverse(mL.mbti_2_inverse))
    mbti_3 = mbti_score_sum(mbti_score(mL.mbti_3), mbti_score_inverse(mL.mbti_3_inverse))
    mbti_4 = mbti_score_sum(mbti_score(mL.mbti_4), mbti_score_inverse(mL.mbti_4_inverse))

    cursor = mysql.connection.cursor()
    sql = ''' INSERT INTO user_responses (user_name, user_email, entry_date, class_year, gender, age, form_gain, 
           sport_hobbies, shows_and_movies, games_and_puzzles, spiritual_and_personal, food_and_social, 
           mbti_1, mbti_2, mbti_3, mbti_4) VALUES(%s, %s, %s, %s, %s, %s, %s,
                                              %s, %s, %s, %s, %s,
                                              %s, %s, %s, %s) '''
    val = (user_name, user_email, entry_date, class_year, gender, age, form_gain, 
           sport_hobbies, shows_and_movies, games_and_puzzles, spiritual_and_personal, food_and_social, 
           mbti_1, mbti_2, mbti_3, mbti_4)
    cursor.execute(sql, val)
    

    cursor.execute(''' SELECT * FROM user_responses ''')
    users_data = cursor.fetchall()

    for item in users_data:
        entry = item.get("entry_date")
        date_diff = datetime.now() - datetime.strptime(entry, "%Y-%m-%d %H:%M:%S.%f")
        if date_diff > timedelta(days=180):
            old_entries = item.get("entry_date")
            cursor.execute("DELETE FROM user_responses WHERE entry_date = %s", (old_entries,))

    mysql.connection.commit()
    cursor.close()

    matches = user_matching(users_data)
    """
    mail_message = Message(
            'Hi! Here are your matches', 
            recipients = [get_answers("Enter your App State email")])
    mail_message.body = "This is a test"
    
    thr = Thread(target=mail_sent, args=(app, mail_message))
    thr.start()
    """
    return render_template("summary.html", answers=session, matches=matches)

## MAIL
"""
def async_mail(funct):
    thr = Thread(target=mail_sent, args=[funct])
    thr.start()
    return thr

def mail_sent(app, mail_message):
    with app.app_context():
        mail.send(mail_message)

    return "Mail sent!"
"""
### USER SCORES

def get_answers(question_variable):
    for question, answer in session.items():
        if question == question_variable:
            return str(answer) if answer else 'None'
    
def mbti_score(list):
    session_items = []
    for item in list:
        if item in session:
            session_items.append(mL.myers_briggs.index(session[item]))

    mbti_scores = sum(session_items)

    return mbti_scores
    
def mbti_score_inverse(list):
    session_items = []
    for item in list:      
        if item in session:
            session_items.append(4 - mL.myers_briggs.index(session[item]))

    mbti_scores_inverse = sum(session_items)

    return mbti_scores_inverse

def mbti_score_sum(scores, inverse_scores):
    score_sum = scores + inverse_scores

    return score_sum 

### RETRIEVING USER DATA

def get_users():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT * FROM user_responses ''')
    users_data = cur.fetchall()
    cur.close()

    return users_data

def personal_info_match(user_data, scores):
    for dictionary in user_data:
        entry_index = user_data.index(dictionary)
        class_year = dictionary['class_year']
        gender = dictionary['gender']
        age = dictionary['age']
        if class_year == get_answers(mL.class_year_question):
            pass
        else:
            class_year_index = mL.class_year.index(class_year)
            if 0 < abs(class_year_index - mL.class_year.index(get_answers(mL.class_year_question))) <= 1:
                scores[entry_index] += 1
            else:
                scores[entry_index] += 2
        if gender == get_answers(mL.gender_question):
            pass
        else:
            scores[entry_index] += 2
        if age == get_answers(mL.age_question):
            pass
        else:
            age_index = mL.age.index(age)
            if 0 < abs(age_index - mL.age.index(get_answers(mL.age_question))) <= 1:
                scores[entry_index] += 1
            else:
                scores[entry_index] += 2

def interests_match(user_data, scores):
    for dictionary in user_data:
        entry_index = user_data.index(dictionary)
        sport_hobbies = dictionary['sport_hobbies']
        shows_and_movies = dictionary['shows_and_movies']
        games_and_puzzles = dictionary['games_and_puzzles']
        spiritual_and_personal = dictionary['spiritual_and_personal']
        food_and_social = dictionary['food_and_social']
        try:
            list_set = set(eval(sport_hobbies))
            list_count = []
            for item in get_answers(mL.interests_question):
                if item in list_set:
                    list_count.append(item)
                else:
                    pass
            if len(list_count) > 0:
                pass
            elif len(list_count) == 0 and sport_hobbies == 'None':
                scores[entry_index] += 2
            elif len(list_count) == 0:
                scores[entry_index] += 1
        except TypeError:
            if eval(sport_hobbies) is get_answers(mL.interests_question):
                pass
            elif eval(sport_hobbies) is not get_answers(mL.interests_question):
                scores[entry_index] += 2
        try:
            list_set = set(eval(shows_and_movies))
            list_count = []
            for item in get_answers(mL.interests_question_2):
                if item in list_set:
                    list_count.append(item)
                else:
                    pass
            if len(list_count) > 0:
                pass
            elif len(list_count) == 0 and shows_and_movies == 'None':
                scores[entry_index] += 2
            elif len(list_count) == 0:
                scores[entry_index] += 1
        except TypeError:
            if eval(shows_and_movies) is get_answers(mL.interests_question_2):
                pass
            elif eval(shows_and_movies) is not get_answers(mL.interests_question_2):
                scores[entry_index] += 2
        try:
            list_set = set(eval(games_and_puzzles))
            list_count = []
            for item in get_answers(mL.interests_question_3):
                if item in list_set:
                    list_count.append(item)
                else:
                    pass
            if len(list_count) > 0:
                pass
            elif len(list_count) == 0 and games_and_puzzles == 'None':
                scores[entry_index] += 2
            elif len(list_count) == 0:
                scores[entry_index] += 1
        except TypeError:
            if eval(games_and_puzzles) is get_answers(mL.interests_question_3):
                pass
            elif eval(games_and_puzzles) is not get_answers(mL.interests_question_3):
                scores[entry_index] += 2
        try:
            list_set = set(eval(spiritual_and_personal))
            list_count = []
            for item in get_answers(mL.interests_question_4):
                if item in list_set:
                    list_count.append(item)
                else:
                    pass
            if len(list_count) > 0:
                pass
            elif len(list_count) == 0 and spiritual_and_personal == 'None':
                scores[entry_index] += 2
            elif len(list_count) == 0:
                scores[entry_index] += 1
        except TypeError:
            if eval(spiritual_and_personal) is get_answers(mL.interests_question_4):
                pass
            elif eval(spiritual_and_personal) is not get_answers(mL.interests_question_4):
                scores[entry_index] += 2
        try:
            list_set = set(eval(food_and_social))
            list_count = []
            for item in get_answers(mL.interests_question_5):
                if item in list_set:
                    list_count.append(item)
                else:
                    pass
            if len(list_count) > 0:
                pass
            elif len(list_count) == 0 and food_and_social == 'None':
                scores[entry_index] += 2
            elif len(list_count) == 0:
                scores[entry_index] += 1
        except TypeError:
            if eval(food_and_social) is get_answers(mL.interests_question_5):
                pass
            elif eval(food_and_social) is not get_answers(mL.interests_question_5):
                scores[entry_index] += 2

def personality_quiz_match(user_data, scores):
    for dictionary in user_data:
        entry_index = user_data.index(dictionary)
        mbti_1 = dictionary['mbti_1']
        mbti_2 = dictionary['mbti_2']
        mbti_3 = dictionary['mbti_3']
        mbti_4 = dictionary['mbti_4']
        if abs(mbti_1 - mbti_score_sum(mbti_score(mL.mbti_1), mbti_score_inverse(mL.mbti_1_inverse))) <= 2:
            pass
        else:
            if 2 < abs(mbti_1 - mbti_score_sum(mbti_score(mL.mbti_1), mbti_score_inverse(mL.mbti_1_inverse))) <= 5:
                scores[entry_index] += 1
            else:
                scores[entry_index] += 2
        if abs(mbti_2 - mbti_score_sum(mbti_score(mL.mbti_2), mbti_score_inverse(mL.mbti_2_inverse))) <= 2:
            pass
        else:
            if 2 < abs(mbti_2 - mbti_score_sum(mbti_score(mL.mbti_2), mbti_score_inverse(mL.mbti_2_inverse))) <= 5:
                scores[entry_index] += 1
            else:
                scores[entry_index] += 2
        if abs(mbti_3 - mbti_score_sum(mbti_score(mL.mbti_3), mbti_score_inverse(mL.mbti_3_inverse))) <= 2:
            pass
        else:
            if 2 < abs(mbti_3 - mbti_score_sum(mbti_score(mL.mbti_3), mbti_score_inverse(mL.mbti_3_inverse))) <= 5:
                scores[entry_index] += 1
            else:
                scores[entry_index] += 2
        if abs(mbti_4 - mbti_score_sum(mbti_score(mL.mbti_4), mbti_score_inverse(mL.mbti_4_inverse))) <= 2:
            pass
        else:
            if 2 < abs(mbti_4 - mbti_score_sum(mbti_score(mL.mbti_4), mbti_score_inverse(mL.mbti_4_inverse))) <= 5:
                scores[entry_index] += 1
            else:
                scores[entry_index] += 2

## MATCHING USERS

def user_matching(user_data):
    applicable_user_data = []
    scores = [0] * len(user_data)
    final_data = []
    for dictionary in user_data:
            for items in dictionary.items():
                for item in items:
                    if item == get_answers(mL.form_gain_question):
                        applicable_user_data.append(dictionary)

    if get_answers(mL.form_gain_question) == "To meet people with similar basic information to me":
        personal_info_match(user_data, scores)

    if get_answers(mL.form_gain_question) == "To match with users with similar interests":
        interests_match(user_data, scores)

    if get_answers(mL.form_gain_question) == "To match with users with a similar personality":
        personality_quiz_match(user_data, scores)

    if get_answers(mL.form_gain_question) == "Nothing in particular":
        personal_info_match(user_data, scores)
        interests_match(user_data, scores)
        personality_quiz_match(user_data, scores)

    print(scores)
    scores_index = sorted(range(len(scores)), key=lambda sub: scores[sub])

    best_scores = scores_index[:3]
    print(best_scores)
    for item in best_scores:
        final_data.append(user_data[item])

    return final_data

## RUN IT

if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))