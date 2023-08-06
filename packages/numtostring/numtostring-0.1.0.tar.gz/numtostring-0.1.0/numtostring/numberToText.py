#How is the english language made?
#We say 1 = one, 2 = two etc.
#Then at 10 = ten, 20=twenty
#Every one of these have their own rule, 20+ we do for eg twentyfive.
#Specials are 11-19, they have their own rule.
#Then 100+ it is five hundred and [number] or just five hundred.
#For example, 20 - twenty, 21 - twenty one, 423 - four hundred and twenty three
#So that means that there are patterns, wich we will use.

#This code is for numbers zero to one thousand.

singulars = {0:"zero", 1:"one", 2:"two", 3:"three", 4:"four", 5:"five", 6:"six", 7:"seven", 8:"eight", 9:"nine", "binder":" "} #This way we can cound how many ones, hundreds and thousands we have!
teens = {10:"ten", 11:"eleven", 12:"twelve", 13:"thirteen", 14:"forteen", 15:"fifteen", 16:"sixteen", 17:"seventeen", 18:"eighteen", 19:"nineteen", "binder":" "} #We need them to check for any numbers between 10 and 19.
tenths = {2:"twenty", 3:"thirty", 4:"forty", 5:"fifty", 6:"sixty", 7:"seventy", 8:"eighty", 9:"ninety", "binder":" "}#For anything between 20 to 99
hundreds = {1:"one hundred", 2:"two hundred", 3:"three hundred", 4:"four hundred", 5:"five hundred", 6:"six hundred", 7:"seven hundred", 8:"eight hundred", 9:"nine hundred", "binder":" and "} #No need for anything more than usual
#Binder is what binds the number with later numbers, can be useful.

def convert(number):
    '''
    Converts "number" into a string consisting of letters
    convert(10) >> ten
    '''
    if (number < 0):
        raise ValueError("The number is negative") #We will not be treating negative numbers
    if (number > 1000):
        raise ValueError("The number is too big") #Nothing above one thousand works
    if (number == 1000):
        return "one thousand" #We add this, just to even out from 999
    numberForProcess = splitNumber(number) #We want the numbers for processing
    if (number < 20): #If the number is less than 20, it will be between 0 and 19, meaning it is in either singulars and teens
        if number > 9: #If it is then greater than 9, it has to be 10+, therefore in teens
            return teens[number]
        else: #Otherwise it is less than 10, and therefore in singulars
            return singulars[number]

    #If we get over here, the number is 20+, therefore we need to process it more hardly

    if (number < 100): #We can easily do something with numbers under one hundred
        if numberForProcess[1] == 0: #Any number 20-99 should have two digits, and the last one should therefore always be at index 1
            return tenths[numberForProcess[0]] #We can now return only the number from tenths
        #If we get here, it is not in the ten times table, and need a bit more work
        return tenths[numberForProcess[0]] + tenths["binder"] + singulars[numberForProcess[1]] #We will combine the one from tenths and the singular with the tenths binder.
    
    #The number is 100+, we do the same as above, but add on a number of hundreds in the beginning too
    if (numberForProcess[1] == 0 and numberForProcess[2] == 0): #If only the hundreds are over zero, like 100, 200, 300, then it is simple
        return hundreds[numberForProcess[0]]
    retVal = "" #We need to store what we return
    if (numberForProcess[1] == 0): #If the middle number is zero, it will be easy too!
        return hundreds[numberForProcess[0]] + hundreds["binder"] + singulars[numberForProcess[2]] #We just need the "one hundred", "two hundred" and bind with the last number!
    if (numberForProcess[1] > 0): #We can easily do something with the 2 last digits
        if numberForProcess[1] == 0:
            retVal = tenths[numberForProcess[0]] #We can now store only the number from tenths
        else: #If it is not in the tenths times table, we need to do something a bit more advanced
            retVal = tenths[numberForProcess[0]] + tenths["binder"] + singulars[numberForProcess[1]] #We will combine the one from tenths and the singular with the tenths binder.
    #Now we can just add on our hundred and the binder :)
    return hundreds[numberForProcess[0]] + hundreds["binder"] + retVal
def splitNumber(number):
    '''
    Splits the number "number" into list of digits
    '''
    out = [] #We need a empty list for the output
    for num in list(str(number)): #We get each digit, in the shape of a string
        out.append(int(num)) #We convert it back, and adds it to the output
    return out #We give back the output
