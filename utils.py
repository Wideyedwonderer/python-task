def infinite_input(prompt, possible_values = None):
    possible_values_string = ' (' + '/'.join(possible_values)+ ')' if possible_values != None else ''
    res = input(prompt +   possible_values_string + '\n')
    if possible_values == None:
        return res
    if not res in possible_values:
        return infinite_input(prompt, possible_values)
    return res