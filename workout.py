import random
import math
import time
#import spotipy # add spotify playlist functionality later
import copy
from winsound import *
import datetime
import numpy as np
from gtts import gTTS # text to speech, create files
from pygame import mixer # text to speech, play files

exercises = set(['Plank', 'Grinder', 'Normal Crunches', 'Normal Situps', 'In-N-Out', 'Leg Raise', 'Leg Lift, Hip Up', 'Up and Down Plank', 'Straight Legs Up Crunches',
             'Cross Body Mountain Climber', 'Russian Twists Slow', 'Tip Toe Through The Tulips', 'Plank With Hip Dips (side to side)', 'Mountain Climber', 'Heel Tap',
             'Bicycle Crunch', 'Scissor Drop (grinder going up and down)', 'Regular Pushups', 'Burpees', 'Reverse Lunge (non-jump)', 'Lunge Jumps', 'Jumping Jacks',
             'Crab Toe Touch', 'Wall Sit', 'V-Up', 'Side Plank Starfish (Left)', 'Side Plank Starfish (Right)'])

unseenExercises = copy.deepcopy(exercises)

def totalWorkoutTime(fileName):
    df = np.genfromtxt(fileName, delimiter=',')
    if(df.ndim == 1): # check if it's one dimensional array, b/c first entry will make a file with only one row = 1d array
        totalMins = df[0]
    else:
        totalMins = sum(df[:,0]) # sum all the entries in the first column
    print("Total workout time: {} hours {} mins".format(totalMins // 60, totalMins % 60))

def exerciseToFile(exercise):
    return "mp3s/" + exercise + ".mp3"

def saveAllMP3():
    tts = gTTS("Halfway done with workout", lang='en')
    tts.save(exerciseToFile("Halfway done with workout"))

    
    tts = gTTS("Final Exercise", lang='en')
    tts.save(exerciseToFile("Final Exercise"))
    
    tts = gTTS("Finished workout. Good job.", lang='en')
    tts.save(exerciseToFile("Finished workout. Good job."))
    
    for exercise in exercises:
        tts = gTTS("Next Exercise is " + exercise, lang='en')
        tts.save(exerciseToFile("Next Exercise is " + exercise))

        tts = gTTS(exercise, lang='en')
        tts.save(exerciseToFile(exercise))

def oneExercise(currentExercise, lastExercise=False, textToSpeech=True, intervalTime = 30, breakTime = 5):
    global unseenExercises
        
    print("Current Exercise: {}".format(currentExercise))
    if lastExercise and textToSpeech:
        mixer.music.load(exerciseToFile("Final Exercise"))
        mixer.music.play()
    time.sleep(intervalTime)

    if not textToSpeech:
        PlaySound("endSound.wav", SND_FILENAME | SND_ASYNC)

    if lastExercise:
        if textToSpeech:
            mixer.music.load(exerciseToFile("Finished workout. Good job."))
            mixer.music.play()
        print("Finished Workout! Good Job.")
        return None
    else:
        print("Finished {}, {} second break.\n".format(currentExercise, breakTime))

        if len(unseenExercises) == 0: # reset unseenExercises if you've visited them all
            unseenExercises = copy.deepcopy(exercises)
            
        nextExercise = random.choice(list(unseenExercises))
        unseenExercises.remove(nextExercise)
            
        print("Next Exercise: {}\n".format(nextExercise))
        if textToSpeech:
            mixer.music.load(exerciseToFile("Next Exercise is {}".format(nextExercise)))
            mixer.music.play()
        time.sleep(breakTime)
        PlaySound("endSound.wav", SND_FILENAME | SND_ASYNC)
        return nextExercise

def trackTime(mins):
    file = open(".trackWorkouts.csv", "a")
    dtNow = datetime.datetime.now()
    file.write("{},{},{}\n".format(mins, dtNow.date(), dtNow.time()))
    file.close()

def workout(mins, textToSpeech, intervalTime, breakTime):
    global unseenExercises

    if(mins == 0): # If you want to do the entire exercise set, enter 0 for the time
        totalExercises = len(exercises)
        mins = (intervalTime + breakTime) * len(exercises) / 60 
    else:
        totalExercises = math.ceil(mins * 60 / (intervalTime + breakTime))

    currentExercise = random.choice(list(unseenExercises))
    unseenExercises.remove(currentExercise)

    if(textToSpeech):
        mixer.init()
        mixer.music.load(exerciseToFile(currentExercise))
        mixer.music.play()

    for i in range(totalExercises):
        if i == math.ceil(totalExercises / 2) and textToSpeech:
            mixer.music.load(exerciseToFile("Halfway done with workout"))
            mixer.music.play()
            print("{} Second Break".format(breakTime*2))
            time.sleep(breakTime*2)
            PlaySound("endSound.wav", SND_FILENAME | SND_ASYNC)

        print("Exercise:  {} / {}".format(i+1, totalExercises))
        currentExercise = oneExercise(currentExercise, i+1 >= totalExercises, textToSpeech, intervalTime, breakTime)

    # end of workout, track duration and date/time
    trackTime(mins)

def getInputMins():
    mins = -1
    while(mins < 0):
        try:
            mins = float(input("How many minutes would you like to work out for: "))
        except ValueError:
            print("\tInvalid amount entered, try only using numbers.")
    return mins
    

if __name__ == "__main__":
   # saveAllMP3() # commment this out after first run, you don't need to re save the mp3's for text to speech multiple times.
    mins = getInputMins()
    textToSpeech = input("Text to Speech (y/n):")

    intervalTime = 30 # duration of each exercise
    breakTime = 5 # time to switch to next exercise or take a break in between each exercise
    
    workout(mins, textToSpeech.lower() == 'y', intervalTime, breakTime)
    totalWorkoutTime(".trackWorkouts.csv")

