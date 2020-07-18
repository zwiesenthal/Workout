import random
import math
import time
# import spotipy # add spotify playlist functionality later
import copy
from winsound import *
import datetime
import numpy as np
from gtts import gTTS  # text to speech, create files
from pygame import mixer  # text to speech, play files


class Workout:
    exercises = {'Plank', 'Grinder', 'Normal Crunches', 'Normal Situps', 'In-N-Out', 'Leg Raise', 'Leg Lift, Hip Up',
                 'Up and Down Plank', 'Straight Legs Up Crunches',
                 'Cross Body Mountain Climber', 'Russian Twists Slow', 'Tip Toe Through The Tulips',
                 'Plank With Hip Dips (side to side)', 'Mountain Climber', 'Heel Tap',
                 'Bicycle Crunch', 'Scissor Drop (grinder going up and down)', 'Regular Pushups', 'Burpees',
                 'Reverse Lunge (non-jump)', 'Lunge Jumps', 'Jumping Jacks',
                 'Crab Toe Touch', 'Wall Sit', 'V-Up', 'Side Plank Starfish (Left)', 'Side Plank Starfish (Right)'}

    unseenExercises = copy.deepcopy(exercises)

    textToSpeech = False
    intervalTime = 30
    breakTime = 5
    totalExercises = 0
    i = 0
    mins = 0
    currentExercise = ""

    @staticmethod
    def totalWorkoutTime(fileName):
        df = np.genfromtxt(fileName, delimiter=',')
        if df.ndim == 1:  # check if it's one dimensional array, b/c first entry will make a file with only one row = 1d array
            totalMins = df[0]
        else:
            totalMins = sum(df[:, 0])  # sum all the entries in the first column
        print("Total workout time: {} hours {} mins".format(totalMins // 60, totalMins % 60))

    @staticmethod
    def exerciseToFile(exercise):
        return "mp3s/" + exercise + ".mp3"

    def saveAllMP3(self):
        tts = gTTS("Halfway done with workout", lang='en')
        tts.save(self.exerciseToFile("Halfway done with workout"))

        tts = gTTS("Final Exercise", lang='en')
        tts.save(self.exerciseToFile("Final Exercise"))

        tts = gTTS("Finished workout. Good job.", lang='en')
        tts.save(self.exerciseToFile("Finished workout. Good job."))

        for exercise in self.exercises:
            tts = gTTS("Next Exercise is " + exercise, lang='en')
            tts.save(self.exerciseToFile("Next Exercise is " + exercise))

            tts = gTTS(exercise, lang='en')
            tts.save(self.exerciseToFile(exercise))

    def oneExercise(self):
        lastExercise = self.i + 1 >= self.totalExercises

        if self.i == math.ceil(self.totalExercises / 2):
            if self.textToSpeech:
                mixer.music.load(self.exerciseToFile("Halfway done with workout"))
                mixer.music.play()
            print("Halfway done with workout. {} second break".format(self.breakTime * 2))
            time.sleep(self.breakTime * 2)
            PlaySound("endSound.wav", SND_FILENAME | SND_ASYNC)

        time.sleep(self.breakTime)

        print("Exercise:  {} / {}".format(self.i + 1, self.totalExercises))

        print("Current Exercise: {}".format(self.currentExercise))
        if lastExercise and self.textToSpeech: #todo change this
            mixer.music.load(self.exerciseToFile("Final Exercise"))
            mixer.music.play()
        time.sleep(self.intervalTime)

        if not self.textToSpeech:
            PlaySound("endSound.wav", SND_FILENAME | SND_ASYNC)

        if lastExercise:
            if self.textToSpeech:
                mixer.music.load(self.exerciseToFile("Finished workout. Good job."))
                mixer.music.play()
            print("Finished Workout! Good Job.")
            return None
        else:
            print("Finished {}, {} second break.\n".format(self.currentExercise, self.breakTime))

            if len(self.unseenExercises) == 0:  # reset unseenExercises if you've visited them all
                self.unseenExercises = copy.deepcopy(self.exercises)

            nextExercise = random.choice(list(self.unseenExercises))
            self.unseenExercises.remove(nextExercise)

            print("Next Exercise: {}\n".format(nextExercise))
            if self.textToSpeech:
                mixer.music.load(self.exerciseToFile("Next Exercise is {}".format(nextExercise)))
                mixer.music.play()
            time.sleep(self.breakTime)
            PlaySound("endSound.wav", SND_FILENAME | SND_ASYNC)
            return nextExercise

    def trackTime(self):
        file = open(".trackWorkouts.csv", "a")
        dtNow = datetime.datetime.now()
        file.write("{},{},{}\n".format(self.mins, dtNow.date(), dtNow.time()))
        file.close()

    def entireWorkout(self):
        if self.mins == 0:  # If you want to do the entire exercise set, enter 0 for the time
            self.totalExercises = len(self.exercises)
            self.mins = (self.intervalTime + self.breakTime) * len(self.exercises) / 60
        else:
            self.totalExercises = math.ceil(self.mins * 60 / (self.intervalTime + self.breakTime))

        self.currentExercise = random.choice(list(self.unseenExercises))
        self.unseenExercises.remove(self.currentExercise)

        if self.textToSpeech:
            mixer.init()
            mixer.music.load(self.exerciseToFile(self.currentExercise))
            mixer.music.play()

        while(self.i < self.totalExercises):
            self.oneExercise()
            self.i += 1


        # end of workout, track duration and date/time
        self.trackTime()

    def getInputMins(self):
        self.mins = -1
        while self.mins < 0:
            try:
                self.mins = float(input("How many minutes would you like to work out for: "))
            except ValueError:
                print("\tInvalid amount entered, try only using numbers.")

    def run(self):
        # self.saveAllMP3()
        self.getInputMins()
        self.textToSpeech = input("Text to Speech (y/n):").lower() == 'y'
        self.entireWorkout()
        self.totalWorkoutTime(".trackWorkouts.csv")


if __name__ == "__main__":
    workout = Workout()
    workout.run()
