import wolframalpha as wf
import speech_recognition as sr
import pyttsx3




app = wf.Client("3YEQYW-RA6A8LREGV")
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices)
engine.setProperty('voice', voices[1].id)
def speak(audio):
           engine.say(audio)
           engine.runAndWait()



# NEW FEATURES WILL COME IN SOON


def takeCommand():
            r = sr.Recognizer()
            with sr.Microphone() as m:
              print("Listening...")
              # r.pause_threshold=1
              audio = r.listen(m)

            try:
              print("Recognizing...")
              query = r.recognize_google(audio, language="eng-in")
              print(f"User Said:{query}\n")
        
            except Exception as e:
                # print(e)

                print("Say that again Please...")
                speak("Say that again Please...")

            query1 = query.lower()
        
            return  query1

class Query:
     
        class normal_query():
          def printing(querys):
            querys= querys.lower()
            res = app.query(querys)
            # speak(next(res.results).text)
            try: 
              return f"{(next(res.results).text)}"
            except Exception:
              print("There is an error!")

          def speaking(querys):
            querys= querys.lower()
            res = app.query(querys)
            # speak(next(res.results).text)
            try: 
              speak(next(res.results).text)
              return f"{(next(res.results).text)}"
            except Exception:

              print("There is an error!")
              speak("There is an error!")
