# how to to use:

from pyshort.s import *

p() _instead of_ print()

fr_p() _insted of for statement_ |fr_p(_range_, _print value_)|

rpc(_value to replace_, _what to replace_, _what to make the replaced value_)
eg:
m="hello world"
rpc(m, "hello", "hi")

will give output as

hi world

rvs(_value to reverse_)

if elif else eg:
m=input()
if_elif_else(m, 'hello', 'hi', 'bye', 'no', 'good')

will give output same as

if m=="hello":
    print("hi)
elif m=="bye":
    print("no")
else:
    print("good")