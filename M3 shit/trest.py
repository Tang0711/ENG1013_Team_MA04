def test1():
    global a
    a = 3

def test2():
    global a
    print(a)
    a=5

test1()
print(a)
test2()
print(a)
