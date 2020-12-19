
def standard_input(): 
    yield ".*ent"
import re
from sys import stdin


user_input = input("Input a regex\n")
while len(user_input) >0:
    print(user_input)
    input_regex = user_input.strip()
    regex = re.compile("^"+input_regex+"$")
    with open("./Oxford_English_Dictionary.txt") as fi:
        for line in fi:
            try: 
                first_word = line.split()[0]
                is_match = regex.findall(first_word.lower()) +  regex.findall(first_word) # Test for both cases
                if len(is_match ) > 0:
                    print(line.strip())
            except:
                pass
    
    user_input = input("Inupt a regex\n")



