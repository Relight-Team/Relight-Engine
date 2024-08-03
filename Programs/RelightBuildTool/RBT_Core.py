import os


# The worst code you have ever fucking seen in your life, but hey, it works


def contains_no_letters(s):
    return not any(char.isalpha() for char in s)

def contains_Array(s):
    i = 0
    while i < len(s):
        if s[i] == "[":
            return True
        i += 1
    return False

def contains_dot(s):
    i = 0
    while i < len(s):
        if s[i] == ".":
            return True
        i += 1
    return False


def Private_NameGet(string):
    ret = ""
    ind = 0
    while string[ind] != "=":
        if string[ind] != " ":
            ret += string[ind]
        ind += 1

    return ret



def Private_VarGet(string):
    ret = ""
    ind = 0
    while string[ind] != "=":
        ind += 1

    if string[ind] == "=" and string[ind + 1] == " ":
        ind += 2
    else:
        ind += 1

    while ind < len(string):
        if string[ind] != "=":
            ret += string[ind]
            ind += 1


    # Remove the "

    ret = ret.replace('"', '')
    ret = ret.replace("\n", "")

    # convert string to different type

    # string to int
    if contains_no_letters(ret) == True and contains_Array(ret) == False and contains_dot(ret) == False:
        ret_New = int(ret)

    # string to float
    elif contains_no_letters(ret) == True and contains_Array(ret) == False and contains_dot(ret) == True:
        ret_New = float(ret)

    # string to Array
    elif contains_Array(ret) == True:
        ret = ret.replace("[", "")
        ret = ret.replace("]", "")
        ret = ret.replace(" ", "")
        #shitty fucking hack, I hate python, but this will fix a bug where for some odd reason it cannot convert the last value to array
        ret += ",PH"
        #print(ret)
        ret_New = []

        inde = 0 # use for the current index of ret
        indeArray = 0 # use for current index of ret_New
        while inde < len(ret) - 2:
            tmp = ""
            while ret[inde] != ',':
                tmp += ret[inde]
                inde += 1

                #print(inde)
            ret_New.append(tmp)
            indeArray += 1
            inde += 1


        #ret_New = ret

    else:
        ret_New = ret


    return ret_New




def GetVar(URL, VarName):
    with open(URL, 'r') as file:
        # Read each line
        for line in file:
            # Seperate Var name with value
            if not line == "" and line != "\n":
                NameTmp = Private_NameGet(line)
                if NameTmp == VarName:
                    return Private_VarGet(line)
