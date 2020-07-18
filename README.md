# Workout
This is a core workout program that uses 30 second intervals and 5 second transitions. 

# Functionality:
  Prompts you to pick duration of the workout.
  
  Allows you to have the exercises spoken outloud with Google's Text to Speech library, gtts.
  
  It logs your workout progress at the end of each workout in ".trackWorkouts.csv".

# Required:
Windows 10 for Winsound, if you don't care about audio, you can comment out the lines that say PlaySound().

pygame - pip install pygame (Used for playing mp3 files)

gtts - pip install gtts (Google Text to Speech)
