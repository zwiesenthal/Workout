import random
import math
import time
#import spotipy # add spotify playlist functionality later
import copy
from winsound import *
import datetime
import numpy as np

exercises = {"Plank" : 30, "Grinder" : 20, "Normal Crunches" : 15, "Normal Situps" : 15, "In-N-Out": 15, "Leg Raise" : 15, "Leg Lift, Hip Up" : 15, "Up and Down Plank" : 10, "Straight Legs Up Crunches" : 15,
             "Cross Body Mountain Climber" : 45, "Russian Twists Slow" : 20, "Tip Toe Through The Tulips" : 60, "Plank With Hip Dips (side to side)": 20, "Mountain Climber" : 45, "Heel Tap" : 30,
                 "Bicycle Crunch" : 45, "Scissor Drop (grinder going up and down) " : 30, "Regular Pushups" : 15, "Burpees" : 6, "Reverse Lunge (non-jump)" : 12, "Lunge Jumps" : 20, "Jumping Jacks" : 30,
             "Crab Toe Touch" : 20}

unseenExercises = copy.deepcopy(exercises)

def totalWorkoutTime(fileName):
    df = np.genfromtxt(fileName, delimiter=',')
    if(df.ndim == 1): # check if it's one dimensional array, b/c first entry will make a file with only one row = 1d array
        totalMins = df[0]
    else:
        totalMins = sum(df[:,0]) # sum all the entries in the first column
    print("Total workout time: {} hours {} mins".format(totalMins // 60, totalMins % 60))

def oneExercise(currentExercise, amount, lastExercise=False):
    global unseenExercises
    print("{}: {} reps estimated".format(currentExercise, amount))    
    time.sleep(27)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    PlaySound("endSound.wav", SND_FILENAME | SND_ASYNC)

    if(lastExercise):
        print("Finished Workout! Good Job.")
        return None, None
    else:
        print("Finished {}, 5 second break.\n".format(currentExercise))

        if(len(unseenExercises) == 0): # reset unseenExercises if you've visited them all
            unseenExercises = copy.deepcopy(exercises)
            
        nextExercise, amount = random.choice(list(unseenExercises.items()))
        unseenExercises.pop(nextExercise)
            
        print("Next Exercise: {}\n".format(nextExercise))
        time.sleep(5)
        PlaySound("endSound.wav", SND_FILENAME | SND_ASYNC)
        return nextExercise, amount
        
def workout(mins):
    global unseenExercises

    totalExercises = math.ceil(mins * 2) # exercises take 30 seconds
    currentExercise, amount = random.choice(list(unseenExercises.items()))
    unseenExercises.pop(currentExercise)

    for i in range(totalExercises):
        print("Exercise:  {} / {}".format(i+1, totalExercises))
        currentExercise, amount = oneExercise(currentExercise, amount, i+1 >= totalExercises)

    # end of workout, track duration and date/time
    file = open(".trackWorkouts.csv", "a")
    dtNow = datetime.datetime.now()
    file.write("{},{},{}\n".format(mins, dtNow.date(), dtNow.time()))
    file.close()


if __name__ == "__main__":
    mins = float(input("How many minutes would you like to work out for: "))
    workout(mins)
    totalWorkoutTime(".trackWorkouts.csv")

