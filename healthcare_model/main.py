import csv
import re
import warnings

import numpy as np
import pandas as pd
import pyttsx3
import speech_recognition
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, _tree

# warnings.filterwarnings("ignore", category=DeprecationWarning)

recognizer = speech_recognition.Recognizer()
alpha_num = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
             "nine": 9, "zero": 0}
training = pd.read_csv('Data/Training.csv')
testing = pd.read_csv('Data/Testing.csv')
cols = training.columns
cols = cols[:-1]
x = training[cols]
y = training['prognosis']
y1 = y

reduced_data = training.groupby(training['prognosis']).max()

# mapping strings to numbers
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
testx = testing[cols]
testy = testing['prognosis']
testy = le.transform(testy)

clf1 = DecisionTreeClassifier()
clf = clf1.fit(x_train, y_train)
# print(clf.score(x_train,y_train))
# print ("cross result========")
scores = cross_val_score(clf, x_test, y_test, cv=3)
# print (scores)
# print (scores.mean())


model = SVC()
model.fit(x_train, y_train)
# print("for svm: ")
# print(model.score(x_test,y_test))

importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols


def readn(nstr):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[1].id)
    # print(nstr)
    engine.say(nstr)
    engine.runAndWait()
    engine.stop()


severityDictionary = dict()
description_list = dict()
precautionDictionary = dict()

symptoms_dict = {}

for index, symptom in enumerate(x):
    symptoms_dict[symptom] = index


def calc_condition(exp, days):
    sum = 0
    for item in exp:
        sum = sum + severityDictionary[item]
    if ((sum * days) / (len(exp) + 1) > 13):
        print("You should take the consultation from doctor. ")
        readn("You should take the consultation from doctor. ")
    else:
        print("It might not be that bad but you should take precautions.")
        readn("It might not be that bad but you should take precautions.")


def getDescription():
    global description_list
    with open('MasterData/symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _description = {row[0]: row[1]}
            description_list.update(_description)


def getSeverityDict():
    global severityDictionary
    with open('MasterData/symptom_severity.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        try:
            for row in csv_reader:
                _diction = {row[0]: int(row[1])}
                severityDictionary.update(_diction)
        except:
            pass


def getprecautionDict():
    global precautionDictionary
    with open('MasterData/symptom_precaution.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _prec = {row[0]: [row[1], row[2], row[3], row[4]]}
            precautionDictionary.update(_prec)


#
# def getInfo():
#     print("-----------------------------------HealthCare ChatBot-----------------------------------")
#     print("\nYour Name? \t\t\t\t", end="->")
#     name = input("")
#     print("Hello, ", name)


def check_pattern(dis_list, inp):
    pred_list = []
    inp = inp.replace(' ', '_')
    patt = f"{inp}"
    regexp = re.compile(patt)
    pred_list = [item for item in dis_list if regexp.search(item)]
    if (len(pred_list) > 0):
        return 1, pred_list
    else:
        return 0, []


def sec_predict(symptoms_exp):
    df = pd.read_csv('Data/Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
        input_vector[[symptoms_dict[item]]] = 1

    return rf_clf.predict([input_vector])


def print_disease(node):
    node = node[0]
    val = node.nonzero()
    disease = le.inverse_transform(val[0])
    return list(map(lambda x: x.strip(), list(disease)))


def tree_to_code(tree, feature_names):
    global recognizer, alpha_num
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    chk_dis = ",".join(feature_names).split(",")
    symptoms_present = []

    while True:
        print("\nTell the symptom you are experiencing  \t\t", end="->")
        readn("Tell the symptom you are experiencing")
        done = False
        # disease_input = input("")
        while not done:
            try:
                with speech_recognition.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)
                    disease_input = recognizer.recognize_google(audio)
                    print(str(disease_input))
                    done = True
            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
        conf, cnf_dis = check_pattern(chk_dis, disease_input)
        if conf == 1:
            print("searches related to input: ")
            readn("searches related to input: ")
            for num, it in enumerate(cnf_dis):
                print(num, ")", it.replace("_", " "))
                readn(f"{num} {it.replace('_', ' ')}")
            if num != 0:
                print(f"Select the one you meant (0 - {num}):  ", end="")
                readn(f"Select the one you meant (0 - {num})")
                # conf_inp = int(input(""))
                bool_conf = False
                while not bool_conf:
                    try:
                        with speech_recognition.Microphone() as mic:
                            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                            audio = recognizer.listen(mic)
                            result = recognizer.recognize_google(audio)
                            try:
                                conf_inp = int(result)
                            except Exception as e:
                                print(e)
                                conf_inp = int(alpha_num[result.lower()])
                            bool_conf = True
                    except speech_recognition.UnknownValueError:
                        recognizer = speech_recognition.Recognizer()

                print(conf_inp)

            else:
                conf_inp = 0

            disease_input = cnf_dis[conf_inp]
            break
            # print("Did you mean: ",cnf_dis,"?(yes/no) :",end="")
            # conf_inp = input("")
            # if(conf_inp=="yes"):
            #     break
        else:
            print("Please provide a valid symptom.")
            readn("Please provide a valid symptom")
    while True:
        try:
            # num_days = int(input("Okay. From how many days ? : "))
            print("Okay. From how many days ? : ")
            readn("Okay. From how many days?")
            days_done = False
            while not days_done:
                try:
                    with speech_recognition.Microphone() as mic:
                        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                        audio = recognizer.listen(mic)
                        result = recognizer.recognize_google(audio)
                        try:
                            num_days = int(result)
                            print(num_days)
                        except Exception as e:
                            num_days = int(alpha_num[result.lower()])
                            print(num_days)
                        days_done = True
                except speech_recognition.UnknownValueError:
                    recognizer = speech_recognition.Recognizer()

            break
        except:
            print("Please provide a valid input.")
            readn("Please provide a valid input")

    def recurse(node, depth):
        global recognizer
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]

            if name == disease_input:
                val = 1
            else:
                val = 0
            if val <= threshold:
                recurse(tree_.children_left[node], depth + 1)
            else:
                symptoms_present.append(name)
                recurse(tree_.children_right[node], depth + 1)
        else:
            present_disease = print_disease(tree_.value[node])
            # print( "You may have " +  present_disease )
            red_cols = reduced_data.columns
            symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
            # dis_list=list(symptoms_present)
            # if len(dis_list)!=0:
            #     print("symptoms present  " + str(list(symptoms_present)))
            # print("symptoms given "  +  str(list(symptoms_given)) )
            print("Are you experiencing any of the following symptoms")
            readn("Are you experiencing any of the following symptoms")
            symptoms_exp = []
            for syms in list(symptoms_given):
                inp = ""
                print(syms.replace("_", " "), "? : ", end='')
                readn(f"{syms.replace('_', ' ')}?")
                while True:
                    # inp = input("")
                    con = False
                    while not con:
                        try:
                            with speech_recognition.Microphone() as mic:
                                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                                audio = recognizer.listen(mic)
                                inp = recognizer.recognize_google(audio)
                                inp.lower()
                                print(inp)
                                con = True
                        except speech_recognition.UnknownValueError:
                            recognizer = speech_recognition.Recognizer()
                    if (inp in "yes" or inp in "no"):
                        break
                    else:
                        print("provide proper answers i.e. (yes/no) : ", end="")
                        readn("provide proper answers i.e. (yes/no)")
                if (inp in "yes"):
                    symptoms_exp.append(syms)

            second_prediction = sec_predict(symptoms_exp)
            # print(second_prediction)
            calc_condition(symptoms_exp, num_days)
            if (present_disease[0] == second_prediction[0]):
                print("You may have ", present_disease[0])
                print(description_list[present_disease[0]])
                readn(f"You may have {present_disease[0]}")
                readn(f"{description_list[present_disease[0]]}")

            else:
                print("You may have ", present_disease[0], "or ", second_prediction[0])
                print(description_list[present_disease[0]])
                print(description_list[second_prediction[0]])
                readn(f"You ma have {present_disease[0]} or {second_prediction[0]}")
                readn(description_list[present_disease[0]])
                readn(description_list[second_prediction[0]])

            # print(description_list[present_disease[0]])
            precution_list = precautionDictionary[present_disease[0]]
            print("Take following measures : ")
            readn("Take following measures")
            for i, j in enumerate(precution_list):
                print(i + 1, ")", j)
                readn(f"{i + 1} {j}")

            # confidence_level = (1.0 * len(symptoms_present)) / len(symptoms_given)
            # print("confidence level is " + str(confidence_level))

    recurse(0, 1)

