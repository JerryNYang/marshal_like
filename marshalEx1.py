import marshal

# this is a function
def say_hello():
	print("from say_hello()")

# Get the "code object" (the bytecode part)
code = say_hello.__code__

# "Marshal" it ... turn bytecode into bytes (like Python does for .pyc)
packed = marshal.dump(code)
print(len(packed)) # compact number

# Later ... "unmarshal" it back
unpackedCode = marshal.load(packed)
# Turn it back into a function
newFunction = types.FunctionType(unpackedCode, globals())
newFunction()	# Prints "from say_hello()"