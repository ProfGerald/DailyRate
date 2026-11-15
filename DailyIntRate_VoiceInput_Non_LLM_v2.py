181# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 02:58:44 2024

@author: ProfGerald
"""

import speech_recognition as sr
import pyttsx3

import traceback


engine = pyttsx3.init()

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

def list_microphones():
    mic_list = sr.Microphone.list_microphone_names()
    for index, name in enumerate(mic_list):
        print(f"Microphone {index}: {name}")
    return mic_list

def listen_for_rate(mic_index):
    recognizer = sr.Recognizer()
    try:
        print(f"Opening microphone {mic_index}")
        with sr.Microphone(device_index=mic_index) as source:
            print("Microphone opened successfully")
            speak("Adjusting for ambient noise, please wait...")
            recognizer.adjust_for_ambient_noise(source)
            speak("Please say the interest rate or say 'default' to use the standard rate.")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")  # Debugging statement
            if text.lower() == 'default':
                return None
            else:
                return text
        except sr.UnknownValueError:
            speak("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            speak(f"Could not request results; {e}")
            return None
    except OSError as e:
        speak(f"OSError: {e}. Please ensure the microphone is enabled and not in use by another application.")
        print(f"OSError: {e}. Please ensure the microphone is enabled and not in use by another application.")
    except Exception as e:
        print("FULL ERROR:")
        traceback.print_exc()
        #speak(f"An error occurred: {e}. Please check the input and try again.")
        print(f"An error occurred: {e}. Please check the input and try again.")

def calculate_daily_interest_rate(rate=None):
    try:
        # Check if rate is provided and is numeric
        if rate is not None:
            try:
                rate = float(rate)
                if rate < 0 or rate > 100:
                    raise ValueError("Interest rate must be between 0 and 100.")
            except ValueError:
                raise ValueError("Interest rate must be a numeric value.")
        else:
            # Use standard interest rate if rate is not provided
            rate = 15.6

        # Calculate daily interest rate
        daily_rate = rate / 365

        # Display the rate to 2 decimal places
        speak(f"The daily interest rate for savings or money market accounts is {daily_rate:.2f} percent.")
        print(f"The daily interest rate for savings or money market accounts is {daily_rate:.2f}%")

    except ValueError as ve:
        speak(f"ValueError: {ve}. Please ensure the interest rate is a numeric value between 0 and 100.")
        print(f"ValueError: {ve}. Please ensure the interest rate is a numeric value between 0 and 100.")
    except TypeError as te:
        speak(f"TypeError: {te}. Please ensure the interest rate is a numeric value.")
        print(f"TypeError: {te}. Please ensure the interest rate is a numeric value.")
    except Exception as e:
        speak(f"An error occurred: {e}. Please check the input and try again.")
        print(f"An error occurred: {e}. Please check the input and try again.")

# List available microphones
mic_list = list_microphones()
if not mic_list:
    speak("No microphones found.")
    print("No microphones found.")
else:
    # Select the microphone index for the Logitech USB camera
    mic_index = int(input("Enter the index of the microphone you want to use: "))
    speak(f"Using Microphone {mic_index}: {mic_list[mic_index]}")
    print(f"Using Microphone {mic_index}: {mic_list[mic_index]}")

    # Example usage
    rate_input = listen_for_rate(mic_index)
    if rate_input is not None:
        calculate_daily_interest_rate(rate_input)
    else:
        calculate_daily_interest_rate()
