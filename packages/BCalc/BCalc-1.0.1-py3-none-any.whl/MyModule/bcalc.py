def add(x, y):
	sum = x + y
	return float(sum)
def sub(x,y):
	sum = x-y
	return float(sum)
def mult(x,y):
	sum = x*y
	return float(sum)
def div(x,y):
	sum = x/y
	return sum
def p(var):
	print(var)
def padd(x,y):
	print(add(x,y))
def psub(x,y):
	print(sub(x,y))
def pmult(x,y):
	print(mult(x,y))
def pdiv(x,y):
	print(div(x,y))
def average(num):
    sumOfNumbers = 0
    for t in num:
        sumOfNumbers = sumOfNumbers + t
    avg = sumOfNumbers / len(num)
    return float(avg)
def paverage(num):
	print(average(num))
def compare(num1,num2):
	if num1 == num2:
		num3 = str(num1)
		num4 = str(num2)
		return(float(num3) + " = " + float(num4))
	if num1 < num2:
		num3 = str(num1)
		num4 = str(num2)
		return(float(num3) + " < " + float(num4))
	if num1 > num2:
		num3 = str(num1)
		num4 = str(num2)
		return(float(num3) + " > " + float(num4))
def pcompare(num1,num2):
	print(compare(num1,num2))
def isequal(num1,num2):
	if num1 != num2:
		return ("Not Equal")
	if num1 == num2:
		return ("Equal")
def pisequal(num1,num2):
	print(isequal(num1,num2))
def exponent(num, times):
	total = num ** times
	return float(total)
def pexponent(num,times):
	print(exponent(num,times))
