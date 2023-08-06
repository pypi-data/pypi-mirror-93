from brainFuckInterpreter import BrainF
# import sys
# sys.setrecursionlimit(10**4)
TEXT="""WOW! Is the flower very beautiful! very pretty! The flower have blue, tiffany blue, yellow, no green and red, this is very bad colour. Can you see? Have people on the flower, this is very bad, is very NO OK! The law are the very sad, don't small. Can you hear? Is flower sad, it very sad, is very NO OK!
I am people, I can see and hear, I see people on the flower, I hear flower sad, I am very angry! Oh NO! That not people, that no heart, that is monkey, that is zoo's animal, that are very bad, is very NO OK! I am people, I love flower and all people, I am very good, My friend is Frankin, not on the flower's monkey or zoo's animal."""
def text2bf(text,print_output=False,limit_a=2,limit_b=10):
    assert (limit_b>=limit_a),'error!'
    _ascii = [ord(i) for i in text]
    if print_output:
        print(_ascii)
    code=""
    brainF=BrainF(print_memory=False,input_func=BrainF.input_in_ASCII)

    def execute(_code):
        nonlocal code
        code+=_code
        return brainF.execute(_code)
    def addTo(target):
        dist=target-brainF.memory[brainF.MemoryIdx]
        operator='+' if dist > 0 else '-'
        if abs(dist)<=limit_b:
            return execute(operator * abs(dist))
        execute('>')
        to = abs(dist) // limit_b
        left = abs(dist) % limit_b
        addTo(to)
        execute('['+ ('>' +('+' * (limit_b//limit_a)) + '[<<'+operator *limit_a+'>>-]<<'+operator*(limit_b%limit_a)) + '>-]<' + operator * left)
        # execute('[<'+ (operator*limit_b) + '>-]<' + operator * left)


    execute('')
    for char in _ascii:
        addTo(char)
        output_char=execute('.')
        if print_output:
            print(output_char,end='')
    if print_output:
        print()
    return code

def text2bf2(text,print_output=False,limit=2):
    _ascii = [ord(i) for i in text]
    if print_output:
        print(_ascii)
    code=""
    brainF=BrainF(print_memory=False,input_func=BrainF.input_in_ASCII)

    def execute(_code):
        nonlocal code
        code+=_code
        return brainF.execute(_code)
    def addTo(target):
        dist=target-brainF.memory[brainF.MemoryIdx]
        operator='+' if dist > 0 else '-'
        if abs(dist)<=limit:
            return execute(operator * abs(dist))
        def addMultipleOperatorInLoop(number,depth):
            if number<=limit:
                return operator*number
            return '>'*depth+'+'*limit+\
                       '['+'<'*depth+\
                            addMultipleOperatorInLoop(number=(number // limit),depth=depth+1)+\
                       '>'*depth+'-]'+\
                   '<'*depth+operator*(number % limit)
        execute(addMultipleOperatorInLoop(number=abs(dist),depth=1))


    execute('')
    for char in _ascii:
        addTo(char)
        output_char=execute('.')
        if print_output:
            print(output_char,end='')
    if print_output:
        print()
    return code

# print(text2bf2(TEXT,print_output=True,limit=2))
# print(text2bf(TEXT,print_output=True,limit_a=2,limit_b=10))