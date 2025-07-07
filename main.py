import os
import pandas as pd
from tkinter import *
from tkinter import filedialog
import tkinter.font as font
from functools import partial
from pyresparser import ResumeParser
from sklearn.ensemble import RandomForestClassifier
from importlib_metadata import version, PackageNotFoundError


class TrainModel:
    def __init__(self):
        self.rf_model = None

    def train(self):
        data = pd.read_csv('training_dataset.csv')
        data['Gender'] = data['Gender'].apply(lambda x: 1 if x.lower() == "male" else 0)

        features = data.iloc[:, :-1].values
        labels = data.iloc[:, -1].values

        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.rf_model.fit(features, labels)

    def test(self, test_data):
        try:
            test_data = [int(i) for i in test_data]
            prediction = self.rf_model.predict([test_data])[0]
            return prediction
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None


def display_result(top, name, resume_path, personality_values):
    top.withdraw()
    personality = model.test(personality_values)

    resume_data = ResumeParser(resume_path).get_extracted_data()
    if resume_data:
        resume_data = {k: v for k, v in resume_data.items() if v is not None}

    result_window = Tk()
    result_window.geometry("800x600")
    result_window.configure(background="white")
    result_window.title("Predicted Personality")

    title_font = font.Font(family='Arial', size=20, weight='bold')
    Label(result_window, text="Personality Prediction Result", font=title_font, bg="white", fg="green").pack(pady=10)

    Label(result_window, text=f"Candidate Name: {name}", bg="white").pack(anchor="w", padx=20)
    if resume_data:
        for key, value in resume_data.items():
            Label(result_window, text=f"{key.title()}: {value}", bg="white").pack(anchor="w", padx=20)

    Label(result_window, text=f"Predicted Personality: {personality}", bg="white", fg="blue").pack(anchor="w", padx=20, pady=10)

    exit_button = Button(result_window, text="Exit", command=result_window.destroy)
    exit_button.pack(pady=20)

    result_window.mainloop()


def predict_personality():
    root.withdraw()
    top = Toplevel()
    top.geometry('700x500')
    top.configure(background='black')
    top.title("Personality Prediction")

    title_font = font.Font(family='Helvetica', size=20, weight='bold')
    Label(top, text="Personality Prediction", font=title_font, bg="black", fg="red").pack(pady=10)

    Label(top, text="Applicant Name", fg="white", bg="black").place(x=50, y=100)
    Label(top, text="Age", fg="white", bg="black").place(x=50, y=140)
    Label(top, text="Gender", fg="white", bg="black").place(x=50, y=180)
    Label(top, text="Upload Resume", fg="white", bg="black").place(x=50, y=220)

    feature_labels = [
        "Openness (1-10):",
        "Neuroticism (1-10):",
        "Conscientiousness (1-10):",
        "Agreeableness (1-10):",
        "Extraversion (1-10):"
    ]

    inputs = {}
    inputs['name'] = Entry(top)
    inputs['name'].place(x=200, y=100, width=200)

    inputs['age'] = Entry(top)
    inputs['age'].place(x=200, y=140, width=200)

    gender = IntVar()
    Radiobutton(top, text="Male", variable=gender, value=1, bg="black", fg="white").place(x=200, y=180)
    Radiobutton(top, text="Female", variable=gender, value=0, bg="black", fg="white").place(x=270, y=180)
    inputs['gender'] = gender

    resume_path = StringVar()

    def select_file():
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")])
        resume_path.set(file_path)

    Button(top, text="Upload Resume", command=select_file).place(x=200, y=220)

    for i, label in enumerate(feature_labels, start=1):
        Label(top, text=label, fg="white", bg="black").place(x=50, y=220 + i * 40)
        inputs[f'feature_{i}'] = Entry(top)
        inputs[f'feature_{i}'].place(x=200, y=220 + i * 40, width=200)

    def submit_data():
        personality_values = [
            inputs['gender'].get(),
            inputs['age'].get(),
            *(inputs[f'feature_{i}'].get() for i in range(1, 6))
        ]
        display_result(top, inputs['name'].get(), resume_path.get(), personality_values)

    Button(top, text="Submit", command=submit_data, bg="red", fg="white").place(x=200, y=460, width=100)

    top.mainloop()


if __name__ == "__main__":
    model = TrainModel()
    model.train()

    root = Tk()
    root.geometry('700x500')
    root.configure(background='white')
    root.title("Personality Prediction System")

    title_font = font.Font(family='Helvetica', size=25, weight='bold')
    Label(root, text="Personality Prediction System", font=title_font, bg="white").pack(pady=30)

    Button(root, text="Predict Personality", command=predict_personality, bg="black", fg="white", font=("Arial", 12)).place(relx=0.5, rely=0.5, anchor=CENTER)

    root.mainloop()
