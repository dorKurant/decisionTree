import pandas as pd
import math
import random
import posixpath
import inspect
#from scipy.stats import chi2
#import chi2
import numpy as np
from scipy.stats import chi2


class Node():
    def __init__(self, atribute_index=None,atribute_list=None,father=None,kids_list=None,answer=None,FalseCounter=None,TrueCounter=None):
        self.atribute_index=atribute_index #question number
        self.atribute_list=atribute_list #List of thresholds
        self.father=father #The branch above me in the tree
        self.kids_list=kids_list #The branch below me in the tree
        self.answer=answer #if the Mode is leaf, that the answer
        self.FalseCounter=FalseCounter #number of false answer to calculate chi square test
        self.TrueCounter=TrueCounter #number of true answer to calculate chi square test


class decisionTree():
    def __init__(self):
        self.root=None

    def calculate_entrupy(self ,answers,data): #The function that calculates the entrupy
        entropy=0;
        for k in answers.values():
            if k[1]==0 or k[2]==0 or k[0]==0:
                entropy=entropy+0;
            else:
                entropy= entropy + (k[0]/len(data))*(-(((k[2]/k[0])*math.log(k[2]/k[0],2))+((k[1]/k[0])*math.log(k[1]/k[0],2))))
        return entropy

    def Calculate_discrete_values(self,uniq_answer,data,attributs_num): #Divide the information into groups for discrete variables
        counter=0 # נספור באיזה שורה אנחנו
        for specipic_ans in [row[attributs_num] for row in data]:
            uniq_answer[specipic_ans][3].append(data[counter]) #We will save all the samples to send to the future tree
            uniq_answer[specipic_ans][0]=uniq_answer[specipic_ans][0]+1 #update counter for The amount of samples in the tree
            if data[counter][-1]==0:
                uniq_answer[specipic_ans][1] = uniq_answer[specipic_ans][1] + 1   #update counter for The amount of not smoking samples in the tree
            else:
                uniq_answer[specipic_ans][2] = uniq_answer[specipic_ans][2] + 1  #update counter for The amount of not smoking samples in the tree
            counter=counter+1
        return uniq_answer

    def Calculate_continuous_values(self,shemati_answer,data,attributs_num,average1,average2,average3): #Divide the information into groups for continuous variables
        counter=0;
        for specipic_ans in [row[attributs_num] for row in data]:
            if specipic_ans<average1:
                shemati_answer[average1][0] = shemati_answer[average1][0] + 1  # update the counter
                shemati_answer[average1][3].append(data[counter]) #We will save all the samples to send to the future tree
                if data[counter][-1]==0:
                    shemati_answer[average1][1] = shemati_answer[average1][1] + 1  # update the counter for no smoking
                else:
                    shemati_answer[average1][2] = shemati_answer[average1][2] + 1  # update the counter for smoking
            elif specipic_ans>average1 and specipic_ans<=average2:
                shemati_answer[average2][0] = shemati_answer[average2][0] + 1
                shemati_answer[average2][3].append(data[counter])

                if data[counter][-1]==0:
                    shemati_answer[average2][1] = shemati_answer[average2][1] + 1
                else:
                    shemati_answer[average2][2] = shemati_answer[average2][2] + 1
            else:
                shemati_answer[average3][0] = shemati_answer[average3][0] + 1
                shemati_answer[average3][3].append(data[counter])
                if data[counter][-1]==0:
                    shemati_answer[average3][2] = shemati_answer[average3][2] + 1
            counter=counter+1
        return shemati_answer

    def Dictionary_uniq_answer(self, uniq_answer):  # make dictionary for every uniq answer
        list_for_value = [0, 0, 0]  # Here I will keep number of impressions, amount correct and amount wrong
        Dictionary_uniq_answer = {}
        for key in uniq_answer:
            Dictionary_uniq_answer[key] = list_for_value.copy()
            Dictionary_uniq_answer[key].append([])
        return Dictionary_uniq_answer

    def make_array_of_answoers(self, attributs_num, data):
        uniq_answer = set(sublist[attributs_num] for sublist in data)  #An array that receives all the unique answers
        if len(uniq_answer) < 4:  #
            Dictionary_uniq_answer=self.Dictionary_uniq_answer(uniq_answer)
            return self.Calculate_discrete_values(Dictionary_uniq_answer, data,attributs_num)  # We will return a dictionary with all possible values for the answer with a count for each answer
        else:  # אם יש לי יותר מ4 (יכול להיות גם 100 או 1000)
            data.sort(key=lambda x: x[attributs_num])  # We will sort the values to split them into 3 groups as homogeneous as possible
            split1 = data[round((len(data) - 1) * 1 / 3)][attributs_num]
            split2 = data[round((len(data) - 1) * 2 / 3)][attributs_num]
            split3 = data[round((len(data) - 1) * 3 / 3)][attributs_num]
            list_for_key = [split1, split2, split3]  #We will set threshold values
            Dictionary_uniq_answer=self.Dictionary_uniq_answer(list_for_key)
            return self.Calculate_continuous_values(Dictionary_uniq_answer, data, attributs_num, split1, split2,split3)

    def plurality_value(self,parent_examples): # A function that checks what the majority was with the father
        count_one=len(list(filter(lambda x: x[len(parent_examples[0])-1] == 1, parent_examples)))
        count_zero=len(list(filter(lambda x: x[len(parent_examples[0])-1] == 0, parent_examples)))
        if(count_one==count_zero):
            rand=random.random();
            if rand>0.5:
                return True
            else:
                return False
        elif count_one>count_zero:
            return True
        else:
            return False

    def classification(self,ans): #Returns true if all examples have the same value
        if ans==0: return False
        else: return True

    def get_best_split(self, dataSet,attributes,plurality_entropy):  #We will take the best split
        best_split = {}
        array_of_optional_answer={}
        max_info_gain = -float("inf")  #The lowest number available
        for atribute in attributes:
            array_of_optional_answer=self.make_array_of_answoers(atribute,dataSet)#Returns me a dictionary with [the remaining examples][amount of error][amount of correct][amount of appearances][the distribution of a feature (say F)]
            atribute_entropy=plurality_entropy-self.calculate_entrupy(array_of_optional_answer,dataSet)
            if atribute_entropy>max_info_gain:
                best_split["atribute_index"]=atribute #We will save the feature we tested from the book
                best_split["atribute_answers"]=array_of_optional_answer #The possible set of answers
                best_split["atribute_entropy"]=atribute_entropy #The entropy value after subtraction from the previous entropy
                max_info_gain=atribute_entropy
        return best_split

    def new_attributes_arry(self,attributes,index):#Creates a new array without the question I checked
        new_arry=attributes.copy()
        new_arry.remove(index)
        return new_arry

    def build_tree(self,dataset,attributes,parent_examples,plurality_entropy=1):
        num_sumples=len(dataset) #The number of examples
        num_atribute=len(attributes) #The number of features
        count_false = len(list(filter(lambda x: x[len(dataset[0]) - 1] == 0, dataset))) #How many non-smoking examples are there in the data
        count_true = len(list(filter(lambda x: x[len(dataset[0]) - 1] == 1, dataset))) #How many smoking examples are there in the data
        if num_sumples==0:
            return Node(answer= self.plurality_value(parent_examples),kids_list=None,FalseCounter=count_false,TrueCounter=count_true) #If I have no examples return a leaf node with a value like your father
        elif len(set(sublist[25] for sublist in dataset))==1: #פונקציה שתבדוק אם לכל הדוגמאות יש את אותו הערך
            return Node(answer=self.classification(dataset[0][len(parent_examples[0])-1]),kids_list=None,FalseCounter=count_false,TrueCounter=count_true) #A function that will return the value that everyone has
        elif num_atribute==0:
            return Node(answer= self.plurality_value(parent_examples),kids_list=None,FalseCounter=count_false,TrueCounter=count_true) #If I don't have additional features, return like your father
        else: # If we got here the node is not a leaf and we have to continue splitting the tree
         best_split=self.get_best_split(dataset,attributes,plurality_entropy)
         tree=Node(atribute_index=best_split["atribute_index"],atribute_list=attributes,kids_list={},FalseCounter=count_false,TrueCounter=count_true)
         new_attributes=self.new_attributes_arry(attributes,best_split["atribute_index"])
         for i in best_split["atribute_answers"]:
             tree.kids_list[i]=self.build_tree(best_split["atribute_answers"][i][3], new_attributes,dataset) #A new tree receives the new values, a list of questions to check minus what was asked, the previous information (if the father needs it)
             tree.kids_list[i].father=tree
        return tree

    def chi_square_test(self,tree): #chi square test
        P=tree.father.TrueCounter #People smoke in the general population
        N=tree.father.FalseCounter #People non-smoke in the general population
        pk=tree.TrueCounter #People smoke in the new population
        nk=tree.FalseCounter #People non-smoke in the new population
        Pk=P*((pk+nk)/(P+N))
        Nk=N*((pk+nk)/(P+N))
        delta=0
        chi2_value=chi2.ppf(0.95,P+N-1) #the critical value
        for kid in tree.kids_list:
            delta=delta+((((tree.kids_list[kid].TrueCounter-Pk)**2)/Pk)+(((tree.kids_list[kid].FalseCounter-Nk)**2)/Nk)) #The statistical value
        if(delta<chi2_value): # The 0 hypothesis is therefore an unnecessary question if a statistic smaller than the critical one is not rejected
            return False
        else: #The split is important, rejected the 0 hypothesis
            return True

    def Delete_question(self,tree,kid): #A set of actions if you want to delete a question from the tree
        tree.kids_list[kid].kids_list = None
        tree.kids_list[kid].attribute_index = None
        tree.kids_list[kid].answer = (True if tree.kids_list[kid].FalseCounter < tree.kids_list[kid].TrueCounter else False)

    def pruning_branches(self,tree):  #We will go over the branches in the tree and check with a chi square test who is redundant
        num_of_child=len(tree.kids_list)
        Deleted = True #A boolean variable that will define whether we deleted a question from the tree or not
        while Deleted==True: #If we deleted, we will not leave the branch but we will check the stage again
            count_Leaves = len(list(filter(lambda x:tree.kids_list[x].answer == None, tree.kids_list)))# Checks how many children of a branch are not pure leaves
            if count_Leaves!=0:# If the number of children that are an answer node is not 0, there is probably a child with additional children and needs to be checked
                for kid in tree.kids_list:
                    if tree.kids_list[kid].answer==None:#I found the child with children
                       Do_delete= self.pruning_branches(tree.kids_list[kid]) #We will check whether his question is necessary with the help of a recursive call to the function
                       if Do_delete==False: #If the question needs to be deleted
                           self.Delete_question(tree,kid)
                           Deleted=True
                           break
                       else:
                           Deleted = False
            else:#If the quantity is equal do chi square test
                important_question=self.chi_square_test(tree)
                if(important_question==False): # The question is redundant and should be deleted
                    return False
                else:
                    return True

    def print_tree(self,tree,attribute_list,level=0):
        if(tree.kids_list!=None):
            num_of_ans=len(tree.kids_list)
            print("\t" * level, "level number", level,":")
            print("\t"*level,"for",attribute_list[tree.atribute_index], "valid options is:", tree.kids_list.keys())
            if(num_of_ans==1):
                print("\t"*level,"for value under",list(tree.kids_list.keys())[0],":")
                self.print_tree(tree.kids_list[list(tree.kids_list.keys())[0]],attribute_list,level+1)
            elif(num_of_ans==2):
                print("\t"*level,"for value under",list(tree.kids_list.keys())[0],":")
                self.print_tree(tree.kids_list[list(tree.kids_list.keys())[0]],attribute_list,level+1)
                print("\t"*level,"for value up then", list(tree.kids_list.keys())[0], "and low or equal to",list(tree.kids_list.keys())[1],":")
                self.print_tree(tree.kids_list[list(tree.kids_list.keys())[1]],attribute_list, level + 1)
            elif(num_of_ans==3):
                print("\t"*level,"for value under", list(tree.kids_list.keys())[0], ":")
                self.print_tree(tree.kids_list[list(tree.kids_list.keys())[0]], attribute_list,level + 1)
                print("\t"*level,"for value up then", list(tree.kids_list.keys())[0], "and low or equal to", list(tree.kids_list.keys())[1], ":")
                self.print_tree(tree.kids_list[list(tree.kids_list.keys())[1]], attribute_list,level + 1)
                print("\t"*level,"for value up then", list(tree.kids_list.keys())[1], "and low or equal to", list(tree.kids_list.keys())[2], ":")
                self.print_tree(tree.kids_list[list(tree.kids_list.keys())[2]], attribute_list,level + 1)
        else:
            print("\t"*level,tree.answer)

    def give_answer(self,row,tree):
        if tree.answer==False:
            return 0
        elif tree.answer==True:
            return 1
        else:
            for kid in tree.kids_list:
                if row[tree.atribute_index]<=kid:
                    return self.give_answer(row,tree.kids_list[kid])

    def reporting_the_eror(self,data,tree):
        counter=0
        for row in data:
            ans=self.give_answer(row,tree)
            if(ans==row[len(row)-1]):
                counter=counter+1
        return counter

def build_tree(ratio):
    df=pd.read_csv('Smoking.csv') #read the data
    data=[] #list from the data, every row is one data
    for index,row in df.iterrows():
        data.append(list(row))
    training_data=data[0:round(len(data)*ratio)] #The data on which we will practice the algorithm
    validate_data=data[round(len(data)*ratio):len(data)+1] #The data on which we will test the algorithm
    headers=pd.read_csv('Smoking.csv',header=None,nrows=1) #reade the head line from the excel
    headers_list = headers.iloc[0, :].tolist() #order the line like the excel
    MyTree=decisionTree();
    attributes_list=list(range(len(training_data[0]) - 1))
    attributes_list.remove(0)
    root=MyTree.build_tree(training_data,attributes_list,training_data)
    MyTree.pruning_branches(root)
    MyTree.print_tree(root,headers_list)
    count_of_true=MyTree.reporting_the_eror(validate_data,root)
    print("eror",1-(count_of_true/len(validate_data)))


def tree_error(k):
    df = pd.read_csv('Smoking.csv')  # read the data
    data = []  # list from the data, every row is one data
    for index, row in df.iterrows():
        data.append(list(row))
    training_data = data[0:round(len(data))]  # The data on which we will practice the algorithm
    headers = pd.read_csv('Smoking.csv', header=None, nrows=1)  # reade the head line from the excel
    #headers_list = headers.iloc[0, :].tolist()  # order the line like the excel
    data_lists=[training_data[i*len(training_data)//k:(i+1)*len(training_data)//k] for i in range(k)] #splite the data to K lists
    attributes_list = list(range(len(training_data[0]) - 1))
    attributes_list.remove(0)
    error_rates=0
    for row in data_lists:
        MyTree = decisionTree();
        new_data=[x for x in training_data if x not in row]
        root = MyTree.build_tree(new_data, attributes_list,new_data)
        MyTree.pruning_branches(root)
        error=1-(MyTree.reporting_the_eror(row,root)/len(row))
        error_rates=error_rates+error
    print ("error average is:",error_rates/k)

def is_busy(row_input):
    df = pd.read_csv('Smoking.csv')  # read the data
    data = []  # list from the data, every row is one data
    for index, row in df.iterrows():
        data.append(list(row))
    training_data = data[0:round(len(data))]  # The data on which we will practice the algorithm
    attributes_list = list(range(len(training_data[0]) - 1))
    attributes_list.remove(0)
    MyTree=decisionTree();
    root = MyTree.build_tree(training_data, attributes_list, training_data)
    MyTree.pruning_branches(root)
    print("my answer is:",MyTree.give_answer(row_input,root))


if __name__ == '__main__':
    build_tree(0.4)
    tree_error(3)
    is_busy([0,'F',40,155,60,81.3,1.2,1,1,1,144,73,94,215,82,73,126,12.9,1,0.7,18,19,27,0,'Y'])

