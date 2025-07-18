from openai import OpenAI
from dotenv import load_dotenv
import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import playlist
import time
import google.generativeai as genai

r = sr.Recognizer()
# engine= pyttsx3.init(driverName='sapi5')

def speak(text):
    print("Speaking:", text)
    engine = pyttsx3.init('sapi5')  # ✅ Reinitialize each time
    engine.say(text)
    engine.runAndWait()
    engine.stop()

    # who are using OpenAI api

# def aiprocess(command):

#     load_dotenv()
#     api_key=os.getenv("API_key")
#     client = OpenAI(api_key=api_key)
#     # client = OpenAI(api_key="your_api",)


#     completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role":"system","content":"you are a poetic"},
#         {"role":"user","content": command},
#     ]
#     )

#     return completion.choices[0].message.content

def aiprocess(command):
    try:
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY")) 

        # Use Gemini Pro model
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(command)

        return response.text

    except Exception as e:
        print("Gemini API error:", e)
        return "I'm unable to respond right now. Please check your internet or Gemini API key."


def ProcessCommand(c):
    # print("Command:",c)
    # speak(f"You said: {c}")
    # pass
    if "open chrome" in c.lower():
        webbrowser.open("https://chrome.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    # elif "play song" in c.lower():
    #     webbrowser.open("https://www.youtube.com/watch?v=NsUqPzdkFTY&list=RDNsUqPzdkFTY&start_radio=1")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link= playlist.music[song]
        webbrowser.open(link)
    else:
        # Let OpenAi handle the request
        output = aiprocess(c)
        speak(output)
    

if __name__== "__main__":
    speak("Hello Boss, Iam jarvis your personal Assistant how can i help you")
    
    # Listen for the wake word jarvis
    while True:
        # obtain audio from the microphone
        r= sr.Recognizer()

        # recognize speech using sphinx
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio= r.listen(source, timeout=2,phrase_time_limit=1)
            try:
                word = r.recognize_google(audio)
                print("Heard:",word)
                if "jarvis" in word.lower():
                    speak("ya tell me")
                    # time.sleep(0.5)
                    
                    # Listen for command
                    with sr.Microphone() as source:
                        print("Jarvis active...")
                        r.adjust_for_ambient_noise(source, duration=0.5)
                        audio= r.listen(source)
                    try:
                        command = r.recognize_google(audio)
                        ProcessCommand(command)

                    except sr.UnknownValueError:
                        print("Sorry, I couldn't understand your command.")
                        speak("Sorry, I didn't get that.")
                    except sr.RequestError as e:
                        print("API error:", e)
                        speak("I'm having trouble accessing Google Speech API.")

                        
            except sr.UnknownValueError:
                print("Didn't catch that.")
            except sr.RequestError as e:
                print("API error:", e)

        except sr.WaitTimeoutError:
            print("Listening timed out.")           

            
            # except sr.UnknownValueError:
            #     print("audio could'nt understand")

        except Exception as e:
                print("error;{0}".format(e))
