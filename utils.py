
def isValidISBN(isbn):
 
    # check for length
    if len(isbn) != 10:
        return False
     
    # Computing weighted sum
    # of first 9 digits
    _sum = 0
    for i in range(9):
        if 0 <= int(isbn[i]) <= 9:
            _sum += int(isbn[i]) * (10 - i)
        else:
            return False
         
    # Checking last digit
    if(isbn[9] != 'X' and
       0 <= int(isbn[9]) <= 9):
        return False
     
    # If last digit is 'X', add
    # 10 to sum, else add its value.
    _sum += 10 if isbn[9] == 'X' else int(isbn[9])
     
    # Return true if weighted sum of
    # digits is divisible by 11
    return (_sum % 11 == 0)

def infinite_input(prompt, possible_values = None):
    possible_values_string = ' (' + '/'.join(possible_values)+ ')' if possible_values != None else ''
    res = input(prompt +   possible_values_string + '\n')
    if possible_values == None:
        return res
    if not res in possible_values:
        return infinite_input(prompt, possible_values)
    return res