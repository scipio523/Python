def split_string(source, splitlist):
    result = ''
    for c in source:
        if c not in splitlist: result += c 
        else: result += ' '
    print(result.split())

split_string("This is a test-of the,string separation-code!", " ,!-")