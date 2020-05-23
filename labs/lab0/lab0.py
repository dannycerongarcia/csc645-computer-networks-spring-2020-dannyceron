########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab0: Getting Started with Python
# Goal: Learning the basics of Python
# Student Name: Danny Ceron Garcia
# Student ID:918581149
# Student Github Username:
# Instructions: Complete the TODO sections for each problem
# Guidelines: Read each problem carefully, and implement them correctly. Grade is based on lab correctness/completeness
#               No partial credit will be given. Labs #0 and #1 must be submitted by Monday Feb 3rd at 7:00 pm
#               No unit test are provided for lab #0
########################################################################################################################
import unittest # don't modify this line of code.
########################## Problem 0: Print  ###########################################################################
"""
Print your name, student id and Github username
Sample output:
Name: Jose
SID: 91744100
Github Username:
"""
name = "Danny Ceron Garcia" # TODO: your name
SID = 918581149 # TODO: your student id
git_username = "dannyceron94" # TODO: your github username
print(name)
print(SID)
print(git_username)
print('\n')

########################## Problem 1: Processing user input ############################################################
"""
Accept two int values from the user, and print their product. If their product is greater than 500, then print their sum

Sample output:
Enter the first integer: 2
Enter the second integer: 4
Result is 8
Enter the first integer: 2
Enter the second integer: 1000
Result is 1002
"""
print("Problem 1 ********************") # problem header (don't modify)
# TODO: your code here
userInputOne = int(input("Enter the first integer: "))
userInputTwo = int(input("Enter the first integer: "))
if(userInputOne>500 or userInputTwo >500):
    print("Result is "+str(userInputOne + userInputTwo))
else:
    print("Result is "+str(userInputOne*userInputTwo))


########################## Problem 2: String Processing ##############################################################
"""
Given a string print the number of times the string "Alice" appears anywhere in the given string

For example, given the string: "Alice and Bob go to the same school. They learned today in class how to treat a lice 
infestation, and Alice found the lecture really interesting", the sample output would be: 
Alice appeared 2 times. 
"""
print("Problem 2 ********************") # problem header (don't modify)
# the given string
myString = "Alice and Bob go to the same school. They learned today in class how to treat a lice" \
           "infestation, and Alice found the lecture really interesting"
# TODO: your code here
token = "Alice"
wordCount =0
myList = myString.split(" ")
for word in myList:
    if token == word:
        wordCount=wordCount+1
print(token+" appeared " + str(wordCount))



########################## Problem 3: Loops ############################################################################
"""
Given a list of numbers iterate over them and output the sum of the current number and previous one.

Given: [5, 10, 24, 32, 88, 90, 100] 
Outputs: 5, 15, 34, 56, 120, 178, 190.
"""
print("Problem 3 ********************") # problem header (don't modify)
numbers = [5, 10, 24, 32, 88, 90, 100]
# TODO: your code here
j=0
print("Given:", numbers,"\nOutputs: ",end =" ")
for i in numbers:
    j=j+i
    print(str(j), end=", ")
    j=i
print("")
########################## Problem 4: Functions/Methods/Lists ##########################################################
"""
Create the method mergeOdds(l1, l2) which takes two unordered lists as parameters, and returns a new list with all the 
odd numbers from the first a second list sorted in ascending order. Function signature is provided for you below

For example: Given l1 = [2,1,5,7,9] and l2 = [32,33,13] the function will return odds = [1,5,7,9,13,33] 
"""
print("Problem 4 ********************") # problem header (don't modify)
# function skeleton
def merge_odds(l1, l2):
    odds = []
    # TODO: your code here
    joinList = l1 + l2
    for number in joinList:
        if(number%2 == 1):
            odds.append(number) 
    odds.sort()
    return odds
l1 = [2,1,5,7,9]
l2 = [32,33,13]
odds = merge_odds(l1, l2)
print("odds =",odds)

########################## Problem 5: Functions/Methods/Dictionaries ###################################################
"""
Refactor problem #4 to return a python dictionary instead a list where the keys are the index of the odd numbers in l1,
and l2, and the values are the odd numbers. 

For example: Given l1 = [2,1,5,7,9] and l2 = [32,33,13] the function will return odds = {1: [1, 33], 2: [5,13], 3: [7], 4: [9]} 
"""
print("Problem 5 ********************") # problem header
# function skeleton
def merge_odds(l1, l2):
    odds = {}
    # TODO: your code here
    counter = 0
    if(len(l1)>len(l2)):
        for index, x in enumerate(l1):
            if(x%2):
                counter = counter+1
                odds.update({counter:[x]})
        counter = 0
        for y in l2:
            if(y%2):
                counter = counter+1
                odds[counter].append(y)
        counter = 0
    else:
        for index, x in enumerate(l2):
            if(x%2):
                counter = counter+1
                odds.update({counter:[x]})
        counter = 0
        for y in l1:
            if(y%2):
                counter = counter+1
                odds[counter].append(y)
        counter = 0
    return odds
l1 = [2,1,5,7,9]
l2 = [32,33,13]
odds = merge_odds(l1, l2)
print("odds:",odds)
