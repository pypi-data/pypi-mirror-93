class A:
    foo = 42

class B(A):
    foo = 43

a = A()
print (a.foo)

b = B()
print (b.foo)
