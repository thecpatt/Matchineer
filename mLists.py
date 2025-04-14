### Matchineer: Form Lists ###
### Uses these lists to create form question response options ###

import random

name_question = "What is your first or preferred name (eg. Anna, Bob, CJ)?"
class_year = ["Freshman", "Sophomore", "Junior", "Senior", "Graduate or Doctorate"]
class_year_question = "What year are you?"
gender = ["Male", "Female", "Other"]
gender_question = "What is your gender?"
age = ["17 or Younger", "18", "19", "20", "21", "22", "23 or Older"]
age_question = "How old are you?"
form_gain = ["To meet people with similar basic information to me", "To match with users with similar interests", "To match with users with a similar personality", "Nothing in particular"]
form_gain_question = "Why do you want to complete this form?"

interests_question = "Select up to THREE options for: sport-related hobbies"
interests_question_2 = "Select up to THREE options for: shows and movies"
interests_question_3 = "Select up to THREE options for: games and puzzles"
interests_question_4 = "Select up to THREE options for: spiritual and identity interests"
interests_question_5 = "Select up to THREE options for: social events and activities"

sport_hobbies = ["Football", "Baseball", "Basketball", "Volleyball", "Soccer", "Skiing", "Rugby", "Tennis", "Cricket", "Badminton",
                  "Gymnastics", "Swimming", "Track and Field", "Hockey", "Croquet", "Pickleball", "Boxing", "Wrestling", "Cycling", 
                  "Shooting", "Skateboard", "Snowboard", "Surfing", "Skating", "Golf", "Martial Arts", "Water Polo", "Equestrian",
                  "Fencing", "Table Tennis", "Auto Racing", "Disc Golf", "Ultimate"]
sport_hobbies.sort()
shows_and_movies = ["Action", "Drama", "Romance", "Documentary", "Comedy", "Coming-of-Age", "Horror", "Thriller", "Western", "Sci-Fi",
                    "Fantasy", "Anime", "Animation", "Adventure", "Historical Fiction", "Melodrama", "Musical", "Star Wars", "Marvel",
                    "DC Comics", "Jurassic Park", "Fast and the Furious", "Lord of the Rings", "Harry Potter", "James Bond", 
                    "Indiana Jones", "Star Trek", "Back to the Future", "Mission: Impossible", "Walking Dead", "Stranger Things",
                    "Breaking Bad", "Friends", "Seinfeld", "The Sopranos", "The Office", "Severance", "Hallmark"]
shows_and_movies.sort()
games_and_puzzles = ["Video games", "Tabletop puzzles", "Breakout rooms", "Strategy board games", "Luck board games", "Sudoku", "Chess",
                     "Grand Theft Auto", "Fallout", "Fortnite", "Call of Duty", "First person shooter", "Real time strategy", "RPG",
                     "Crosswords", "Monopoly", "Catan", "Ticket To Ride", "Jackbox Games", "Yahtzee", "Sorry",
                     "Deduction games", "Hanayama puzzles", "World of Warcraft", "Red Dead Redemption", "Stardew Valley", 
                     "Animal Crossing", "Mario Kart", "Civilization series", "Wingspan", "Azul", "The Sims", "Mobile games", "Minecraft",
                     "Roblox"]
games_and_puzzles.sort()
spiritual_and_personal = ["Evangelical Chrisitan ministries and clubs", "Catholic Campus Ministry", "LGBTQ / Henderson Springs",
                          "Muslim / MSA", "Neurodivergent", "Diabetes", "Jewish / Hillel", "Asian Student Association", "Black Student Association",
                          "Chinese Cultural Club", "College Democrats", "College Republicans", "Fraternity organizations",
                          "Sorority organizations", "International Student", "Latin Hispanic Alliance", "Autism", "South Asian Student Association",
                          "Student American Indian Movement", "First Generation college student"]
spiritual_and_personal.sort()
food_and_social = ["Bars and breweries", "Eating out", "Ordering food in", "Parties", "Hiking", "Noble Kava", "SouthEnd", "Lost Province", "Booneshine",
                   "TAPP Room", "Boone Saloon", "Rivers Street Ale House", "Appalachian Mountain Brewery", "Lily's", "Parallel Brewing",
                   "Stick Boy", "Espresso News", "Kovu's Coffee", "Higher Grounds", "Just hanging out", "Walking around Boone",
                   "Going on the Parkway", "Going skiing/snowboarding", "Watching shows or movies", "Playing games"]
food_and_social.sort()

myers_briggs = ["Strongly Disagree", "Somewhat Disagree", "Neutral", "Somewhat Agree", "Strongly Agree"]

mbti_1 = ["\"I enjoy being social at parties\"", 
          "\"I feel energized by being around people\"", 
          "\"I consider myself to be a social butterfly\"", 
          "\"I enjoy non-routine conversation with people\"", 
          "\"I often initiate conversation with people\""]

mbti_1_inverse = ["\"When talking on the phone, I often have to rehearse what to say\"", 
                  "\"I prefer to have a few close friends instead of having many friends\"", 
                  "\"I struggle talking to strangers\"", 
                  "\"I often keep to myself\"", 
                  "\"Foreign social situations make me anxious\""]

mbti_2 = ["\"I go off of facts more often than feelings\"",
          "\"I consider myself to think realistically\"",
          "\"I gravitate towards people that are sensible rather than imaginative\"",
          "\"I rather would think small and feasible rather than think big and unrealistic\"",
          "\"I like talking about facts and events instead of ideas\""]

mbti_2_inverse = ["\"I would rather do things my own way than do it the proven way\"",
                  "\"I enjoy expressing my unique personality\"",
                  "\"I would rather do something creative and study something factual\"",
                  "\"I charter my own path instead of following the staus quo\"",
                  "\"When making a presentation, I like designing the slides more than\""]

mbti_3 = ["\"I am more convinced by arguments that are logical than emotional\"",
          "\"I judge people on feelings and vibes rather than objective facts\"",
          "\"I would prefer someone that is kind but unfair over someone that is mean but just\"",
          "\"Even if the facts lead me one way, I trust my gut feeling on important decisions\"",
          "\"I would rather just agree with someone than to have a heated debate\""]

mbti_3_inverse = ["\"I prefer using my head over my heart\"",
                  "\"I tend to value things depending on their utility rather than sentiment\"",
                  "\"I approach social situations more logically than sympathetically\"",
                  "\"It's worse to be too compassionate than too analytical\"",
                  "\"The world would be a better place if people could just think more rationally than emotionally\""]

mbti_4 = ["\"I prefer to make plans with friends in advance than to do things spur of the moment\"",
          "\"I think things through long and hard rather than impulsively\"",
          "\"I always make a point to arrive to events on-time\"",
          "\"I am determined to reach my goals and aspirations\"",
          "\"I believe that people need to create their own destiny\""]

mbti_4_inverse = ["\"I prefer to adapt on the fly than to make a plan\"",
                  "\"I tend to procrastinate on school work\"",
                  "\"In relationships, I deal with issues as they happen instead of talking about things in advance\"",
                  "\"I thrive without structure\"",
                  "\"I am a spontaneous person\""]

def myers_briggs_questions(questions):

    list = []
    list.extend(random.sample(questions, 3))

    return list

mbti_1_random = myers_briggs_questions(mbti_1)
mbti_1_inverse_random = myers_briggs_questions(mbti_1_inverse)
mbti_2_random = myers_briggs_questions(mbti_2)
mbti_2_inverse_random = myers_briggs_questions(mbti_2_inverse)
mbti_3_random = myers_briggs_questions(mbti_3)
mbti_3_inverse_random = myers_briggs_questions(mbti_3_inverse)
mbti_4_random = myers_briggs_questions(mbti_4)
mbti_4_inverse_random = myers_briggs_questions(mbti_4_inverse)