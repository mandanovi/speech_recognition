import speech_recognition
from translate import Translator
import pyaudio
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
from tkinter import font as tkFont
from datetime import datetime
from tkinter import filedialog as fd
from gtts import gTTS
import os
import playsound


class SpeechRecognition(Tk):
    def __init__(self):
        super().__init__()
        self.title("Speech Recognition")
        self.geometry("920x650")
        self.configure(bg="#A75D5D")
        self.r = speech_recognition.Recognizer()
        self.widget()

    def widget(self):
        self.helv26 = tkFont.Font(family='Helvetica', size=26, weight=tkFont.BOLD)
        self.helv12 = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
        title = Label(text="Speech Recognition", font=self.helv26, anchor=CENTER, background='#A75D5D',
                      foreground='white')
        title.grid(column=1, row=1, rowspan=3)

        from_label = Label(width=35, text="From", font=self.helv12, background='#A75D5D', foreground="white")
        from_label.grid(column=1, row=4, pady=15)

        choices = ['en-US', 'id', 'de']
        self.from_lang = Combobox(self, values=choices, font=self.helv12)
        self.from_lang.grid(column=1, row=4)

        style = Style()
        style.configure('TButton', background='#A75D5D')
        style.configure('TButton', foreground="#A75D5D")
        style.configure("TButton", font=('Helvetica', 12, "bold"))

        record_voice = Button(text="Your Own Voice", width=20, command=self.parser)
        record_voice.grid(column=0, row=6, pady=20, padx=20)

        ask_file = Button(text="Select a WAV File", width=20, command=self.select_file)
        ask_file.grid(column=2, row=6, pady=20, padx=20)

    def end_result(self, result):
        self.text_speech = Text(height=7, width=40)
        self.text_speech.grid(column=1, row=11)
        self.speech_result = self.text_speech.insert(END, f"DETECTED VOICE: {result}")

        to_label = Label(width=45, text="Translate to: ", font=self.helv12, background='#A75D5D', foreground="white")
        to_label.grid(column=1, row=15, pady=20, padx=20)

        choices = ['en-US', 'id', 'de']
        self.to_lang = Combobox(self, values=choices, font=self.helv12)
        self.to_lang.grid(column=1, row=15, pady=20, padx=20)

        translate_button = Button(text="Translate", width=20, command=self.another_parser)
        translate_button.grid(column=1, row=16, pady=20, padx=20)

    def parser(self):
        self.from_language = self.from_lang.get()

        if self.from_language == "":
            tkinter.messagebox.showwarning("Uncomplete", "Specify the -From- Language")

        else:
            say_something = Label(text="Say something after you close the YES or NO prompt", font=("Helvetica", 8, "bold"), anchor=CENTER,
                                  background='#A75D5D', foreground='white')
            say_something.grid(column=1, row=7, rowspan=3)

            voice_save = tkinter.messagebox.askyesno("Saving voice", "Do you want to save your voice?")

            if voice_save == True:
                print(voice_save)
                self.end_result(self.saving_voice(self.from_language))

            else:
                print(voice_save)
                self.end_result(self.audio_from_mic(self.from_language))

    def audio_from_mic(self, lang):
        with speech_recognition.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, duration=0.7)
            self.audio = self.r.listen(source)

            # recognize speech using Google API
            self.result = self.r.recognize_google(self.audio, language=lang)
            try:
                return self.result
            except speech_recognition.UnknownValueError:
                tkinter.messagebox.showerror("Not Clear", "Could not understand your voice")
            except speech_recognition.RequestError as e:
                tkinter.messagebox.showerror("ERROR", f"Error; {0}".format(e))

    def saving_voice(self, lang):
         with speech_recognition.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, duration=0.7)
            audio = self.r.listen(source)
            self.result = self.r.recognize_google(audio, language=lang)

            try:
                with open("microphone-results.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                return self.result
            except speech_recognition.UnknownValueError:
                print("Could not understand audio")
            except speech_recognition.RequestError as e:
                print("Error; {0}".format(e))
            # saving voice

    def audio_from_wav_file(self, file):
        with speech_recognition.WavFile(file) as source:
            audio = self.r.record(source)
            try:
                self.result = self.r.recognize_google(audio)
                self.result = self.result.lower()
                return self.result
            except LookupError:
                tkinter.messagebox.showerror("Error", "Could not understand audio")

    def text_translate(self, to_lang, from_lang, text_to_translate):
        translator = Translator(to_lang=to_lang, from_lang=from_lang)
        self.translation = translator.translate(text_to_translate)
        return self.translation

    def another_parser(self):
        label_translate = Label(text=f"RESULT : ", font=self.helv12, anchor=CENTER,
                                background='#A75D5D', foreground='white')
        label_translate.grid(column=1, row=16, rowspan=3)
        self.translate_result = Text(height=7, width=40)
        self.translate_result.grid(column=1, row=17)
        self.translate_result.insert(END, self.text_translate(to_lang=self.to_lang.get(), from_lang=self.from_lang.get(), text_to_translate=self.result))
        self.speak_button = Button(text="Speak", width=10, command=self.speak_parser)
        self.speak_button.grid(column=1, row=18)


    def select_file(self):
        filetypes = (
            ("Audio Files", ".wav"),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='ONLY WAV FILE',
            initialdir='/',
            filetypes=filetypes)

        selected_file = Label(text=filename, font=("Helvetica", 8, "bold"), anchor=CENTER,
                              background='#A75D5D', foreground='white')
        selected_file.grid(column=1, row=7, rowspan=3)
        self.end_result(self.audio_from_wav_file(filename))

    def speak(self, text, lang):
        tts = gTTS(text=text, lang=lang)

        filename = "speak.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)

    def speak_parser(self):
        self.speak(self.translate_result.get(1.0, END), self.to_lang.get())



App = SpeechRecognition()
App.mainloop()
