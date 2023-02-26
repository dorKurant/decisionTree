import pandas as pd
import math
import posixpath
import inspect


class question():
    def __init__(self, data, attributs_num):
        self.data = data
        self.attributs_num = attributs_num
        self.entropy = 0

    ''' def calculate_entrupy_for_Discrete_variable(self,uniq_answer): #לשקול להחליף למילון
        entrupy=0
        for ans in uniq_answer:
            counter=0 #how many attribute have this answer
            countTrue=0 #for how many examples that gave  this answer gut True
            countFalse=0 #"..." False
            for specipic_ans in [row[self.attributs_num] for row in self.data]:
                if specipic_ans==ans:
                    if self.data[counter][-1]==0:#נניח כרגע כלא מעשן
                        countFalse=countFalse+1
                    else:
                        countTrue=countTrue+1
                counter=counter+1
            entrupy=entrupy+self.calculate_entrupy(counter,countTrue,countFalse)
        self.entropy=entrupy
       '''

    def calculate_entrupy(self, answers):
        #  return (counter / len(self.data)) * (-(((countTrue / counter) * math.log(countTrue / counter), 2) + ((countFalse / counter) * math.log(countFalse / counter), 2)))
        entropy = 0;
        for k in answers.values():
            if k[1] == 0 or k[2] == 0 or k[0] == 0:
                entropy = entropy + 0;
            else:
                entropy = entropy + (k[0] / len(self.data)) * (
                    -(((k[2] / k[0]) * math.log(k[2] / k[0], 2)) + ((k[1] / k[0]) * math.log(k[1] / k[0], 2))))
        return entropy

    def calculate_entrupy_for_Discrete_variable(self, uniq_answer):  # לשקול להחליף למילון
        # entropy=0
        counter = 0  # נספור באיזה שורה אנחנו
        for specipic_ans in [row[self.attributs_num] for row in self.data]:
            uniq_answer[specipic_ans][0] = uniq_answer[specipic_ans][0] + 1  # update the counter
            if self.data[counter][-1] == 0:
                uniq_answer[specipic_ans][1] = uniq_answer[specipic_ans][1] + 1  # update the לא מעשנים
            else:
                uniq_answer[specipic_ans][2] = uniq_answer[specipic_ans][2] + 1  # update the כן מעשנים
            counter = counter + 1
        self.entropy = self.calculate_entrupy(uniq_answer)

    def calculate_entrupy_for_continuous_variable(self, average, shemati_answer):
        entrupy = 0;
        counter = 0;
        for specipic_ans in [row[self.attributs_num] for row in self.data]:
            if specipic_ans < shemati_answer[0]:
                shemati_answer[0][0] = shemati_answer[0][0] + 1  # update the counter
                if self.data[counter][-1] == 0:
                    shemati_answer[0][1] = shemati_answer[0][1] + 1  # update the counter for לא מעשנים
                else:
                    shemati_answer[0][2] = shemati_answer[0][2] + 1  # update the counter for מעשנים

            if specipic_ans > shemati_answer[0] and specipic_ans <= shemati_answer[1]:
                shemati_answer[1][0] = shemati_answer[1][0] + 1  # update the counter
                if self.data[counter][-1] == 0:
                    shemati_answer[1][1] = shemati_answer[1][1] + 1  # update the counter for לא מעשנים
                else:
                    shemati_answer[1][2] = shemati_answer[1][2] + 1  # update the counter for מעשנים

            else:
                shemati_answer[2][0] = shemati_answer[2][0] + 1  # update the counter
                if self.data[counter][-1] == 0:
                    shemati_answer[2][2] = shemati_answer[2][2] + 1  # update the counter for לא מעשנים


    def make_array_of_answoers(self):
        uniq_answer=set(sublist[self.attributs_num] for sublist in self.data) #מערך שמקבל את כל התשובות הייחודיות
        list_for_value = [0, 0, 0]  # כאן אני אשמור כמות הופעות, כמות נכון וכמות טעות
        if len(uniq_answer)<4: #אם יש לי   עד 4 תשובות שונות
            Dictionary_uniq_answer={}
            for key in uniq_answer:
                Dictionary_uniq_answer[key] = list_for_value.copy()
            self.calculate_entrupy_for_Discrete_variable(Dictionary_uniq_answer)
            print()
        else: #אם יש לי יותר מ4 (יכול להיות גם 100 או 1000)
            average = ((sum(uniq_answer)/len(uniq_answer))/ 3);  # נגדיר כי נחלק את המערך ל3 חלקים
            list_for_key =[average,average*2,average*3]
            shemati_answer={}
            for key in list_for_key:
                shemati_answer[key] = list_for_value.copy()
            #shemati_answer=dict.fromkeys(list_for_key,list_for_value)
            self.entropy=self.calculate_entrupy_for_continuous_variable(average,shemati_answer)


class decisionTree():
    def __init__(self):
        self.root = None
        self.min_samples_split = 0

    def get_best_split(self, dataSet, num_sumples, num_atribute):  # ניקח את הפיצול הטוב יבותר
        best_split = {}  # נגדיר את הפיצול הטוב ביותר כמילון
        max_info_gain = -float("inf")  # המספר הכי נמוך שקיים

    def make_array_of_answoers(self, ):
        uniq_answer = set(sublist[self.attributs_num] for sublist in self.data)  # מערך שמקבל את כל התשובות הייחודיות

    list_for_value = [0, 0, 0]  # כאן אני אשמור כמות הופעות, כמות נכון וכמות טעות
    if len(uniq_answer) < 4:  # אם יש לי   עד 4 תשובות שונות
        Dictionary_uniq_answer = {}
        for key in uniq_answer:
            Dictionary_uniq_answer[key] = list_for_value.copy()
        self.calculate_entrupy_for_Discrete_variable(Dictionary_uniq_answer)
        print()
    else:  # אם יש לי יותר מ4 (יכול להיות גם 100 או 1000)
        average = ((sum(uniq_answer) / len(uniq_answer)) / 3);  # נגדיר כי נחלק את המערך ל3 חלקים
        list_for_key = [average, average * 2, average * 3]
        shemati_answer = {}
        for key in list_for_key:
            shemati_answer[key] = list_for_value.copy()
        # shemati_answer=dict.fromkeys(list_for_key,list_for_value)
        self.entropy = self.calculate_entrupy_for_continuous_variable(average, shemati_answer)

    def build_tree(self, dataset, curr_depth=0):
        question_list = []
        num_sumples = len(dataset)  # מספר הדוגמאות
        num_atribute = len(dataset[0])  # מספר התכונות

        #   if num_sumples==0:
        #     return self.Like_Your_Father #אם אין לי דוגמאות תחזיר כמו אבא שלך
        #  elif self.Same_classification: #פונקציה שתבדוק אם לכל הדוגמאות יש את אותו הערך
        #       return self.classification #פונקציה שתחזיר את הערך שיש לכולם
        #  elif num_atribute==0: #אם מספר התכונות הוא אפס
        #        return self.Like_Your_Father # אם אין לי תכונות נוספות תחזיר כמו אבא שלך
        #   else: #אם הגענו לכאן זה לא עלה ועלינו להמשיך את הפיצול בעץ
        #      #best_split=self.get_best_split(dataset,num_sumples,num_atribute)

        best_split = {}
        for atribute in range(1, len(dataset[0]) - 1):  # נעבור על כל התכונות ונבדוק מי התכונה הכי טובה כרגע

            # new_question = question(dataset, atribute)
            # new_question.make_array_of_answoers()
            # question_list.append(new_question)
            if len(question_list) > 0:
                if new_question.entropy > question_list[0].entropy:
                    question_list.clear()
                    question_list.append(new_question)
                    best_split["atribute_index"] = atribute  # נשמור את מהספר התכונה שבדקנו
                    best_split["question"] = new_question
            else:
                question_list.append(new_question)

        # if dataset["info_gain"]>0: #נבדוק שהפיצול לא יוביל אותנו לצומת טהורה
        # עבור כל פיצול אפשרי של העץ ניצור עץ חדש


def build_tree(ratio):
    df = pd.read_excel('Smoking1_smal.xlsx')  # read the data
    data = []  # list from the data, every row is one data
    for index, row in df.iterrows():
        data.append(list(row))
    training_data = data[0:round(len(data) * ratio)]  # The data on which we will practice the algorithm
    validate_data = data[round(len(data) * ratio):len(data) + 1]  # The data on which we will test the algorithm
    # print (training_data)
    MyTree = decisionTree();
    MyTree.build_tree(training_data, 0)
    # for atribute in range(1,len(training_data[0])-1):
    #   new_question=question(training_data,atribute)
    #  new_question.make_array_of_answoers()
    # question_list.append(new_question)


#  root=None #נגדיר את שורש העץ


if __name__ == '__main__':
    build_tree(0.01)
