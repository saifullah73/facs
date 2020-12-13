from datetime import date
while True:
	input_str = input("Month Day:")
	month = int(input_str.split(" ")[0])
	day = int(input_str.split(" ")[1])
	f_date = date(2020, 2, 26)
	l_date = date(2020, month, day)
	delta = l_date - f_date
	print(delta.days)
