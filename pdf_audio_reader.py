from tkinter import *
from tkinter import filedialog
import PyPDF2
import pyttsx3
import threading

# Initialize variables
extracted_text = ""
engine = None
is_speaking = False  # Global flag to control speech

def initialize_engine():
    global engine
    if engine is None:
        engine = pyttsx3.init()

def extract_text():
    global extracted_text
    extracted_text = ""  # Reset the text for new file selection
    file = filedialog.askopenfile(parent=root, mode="rb", title="Choose a PDF File")
    if file:
        try:
            pdf_file_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_file_reader.pages)):
                pdf_page = pdf_file_reader.pages[page_num]
                extracted_text += pdf_page.extract_text()
            file.close()
        except Exception as e:
            print(f"Error reading PDF: {e}")
    else:
        print("No file selected.")

def speak_text():
    global is_speaking, engine
    if not extracted_text.strip():
        print("No text to read. Please select a PDF file first.")
        return

    initialize_engine()  # Ensure the engine is initialized

    def speech():
        global is_speaking, engine
        try:
            rate_value = int(rate.get())
            engine.setProperty('rate', rate_value)
        except ValueError:
            rate_value = 200  # Default rate
            engine.setProperty('rate', rate_value)

        all_voices = engine.getProperty('voices')
        if male.get() == 1:
            engine.setProperty('voice', all_voices[0].id)  # Male voice
        elif female.get() == 1:
            engine.setProperty('voice', all_voices[1].id)  # Female voice
        else:
            engine.setProperty('voice', all_voices[0].id)  # Default to male

        is_speaking = True
        engine.say(extracted_text)
        engine.runAndWait()
        is_speaking = False

    # Run speech in a separate thread
    speech_thread = threading.Thread(target=speech)
    speech_thread.start()

def stop_speaking():
    global is_speaking, engine
    if is_speaking and engine:
        engine.stop()  # Stop speech
        is_speaking = False
        engine = None  # Reset engine to ensure it works for subsequent calls

def Application(root):
    root.geometry("700x600")
    root.resizable(width=False, height=False)
    root.title("PDF to AUDIO")
    root.configure(background="light grey")

    global rate, male, female

    # Frame 1: Title and Subtitle
    frame1 = Frame(root, width=500, height=200, bg='indigo')
    frame2 = Frame(root, width=500, height=450, bg='light grey')

    frame1.pack(side="top", fill="both")
    frame2.pack(side="top", fill="y")

    name1 = Label(frame1, text="PDF to Audio", fg="black", bg="blue", font="Arial 28 bold")
    name1.pack()
    name2 = Label(frame1, text="Hear your PDF file", fg="red", bg="indigo", font="Calibri 25 bold")
    name2.pack()

    # Frame 2: Buttons and Options
    button_1 = Button(frame2, text="Select PDF File", activeforeground="red", command=extract_text,
                      padx="70", pady="10", fg="white", bg="black", font="Arial 12")
    button_1.grid(row=0, pady=20, columnspan=2)

    rate_of_speech = Label(frame2, text="Enter the rate of speech:", fg="black", bg="aqua", font="Arial 12")
    rate_of_speech.grid(row=1, column=0, pady=15, padx=0, sticky=W)
    rate = Entry(frame2, fg="black", bg="white", font="Arial 12")
    rate.insert(0, "200")  # Default speech rate
    rate.grid(row=1, column=1, padx=30, pady=15, sticky=W)

    voice_text = Label(frame2, text="Select voice:", fg="black", bg="aqua", font="Arial 12")
    voice_text.grid(row=2, column=0, pady=15, padx=0, sticky=E)

    male = IntVar()
    maleOpt = Checkbutton(frame2, text="Male", bg="pink", variable=male, onvalue=1, offvalue=0)
    maleOpt.grid(row=2, column=1, pady=0, padx=30, sticky=W)

    female = IntVar()
    femaleOpt = Checkbutton(frame2, text="Female", bg="pink", variable=female, onvalue=1, offvalue=0)
    femaleOpt.grid(row=3, column=1, pady=0, padx=30, sticky=W)

    submit_button = Button(frame2, text="Play PDF File", command=speak_text, activeforeground="red",
                           padx="60", pady="10", fg="white", bg="black", font="Arial 12")
    submit_button.grid(row=4, column=0, pady=65)

    stop_button = Button(frame2, text="Stop Playing", command=stop_speaking, activeforeground="red",
                         padx="60", pady="10", fg="white", bg="black", font="Arial 12")
    stop_button.grid(row=4, column=1, pady=65)

if __name__ == "__main__":
    root = Tk()
    Application(root)
    root.mainloop()
