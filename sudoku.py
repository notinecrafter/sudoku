import sys
import itertools
import timeit

#function inject: replaces blanks in list template with numbers in list replacement
def inject(template, replacement):
	template = "".join(template)
	for num in replacement:
		template = template.replace("x", num, 1)
	result = []
	for char in template:
		result.append(char)
	return result

def matchtest(template, fill):
	for i in range(0,9):
		if template[i] == "x":
			pass
		elif template[i] == fill[i]:
			pass
		else:
			return False
	return True

def rowtest(template, answer, rownum):
	for row in range(0,9):
		if row != rownum:
			for column in range(0,9):
				if template[row][column] == answer[column]:
					return False
	#check for 3x3 squares
	if rownum < 3:
		for row in range(0,3):
			for column in range (0,3):
				if template[row][column] != 'x':
					for matchrow in range(row, 3):
						for matchcolumn in range(0, 3):
							if (template[row][column] == template[matchrow][matchcolumn]) & (row != matchrow) & (column != matchcolumn):
								return False
			for column in range(3,6):
				if template[row][column] != 'x':
					for matchrow in range(row, 3):
						for matchcolumn in range(3, 6):
							if (template[row][column] == template[matchrow][matchcolumn]) & (row != matchrow) & (column != matchcolumn):
								return False
			for column in range(6,9):
				if template[row][column] != 'x':
					for matchrow in range(row, 3):
						for matchcolumn in range(6,9):
							if (template[row][column] == template[matchrow][matchcolumn]) & (row != matchrow) & (column != matchcolumn):
								return False
	elif rownum >= 3 & rownum < 6:
		for row in range(3,6):
			for column in range(0,3):
				if template[row][column] != 'x':
					for matchrow in range(row, 6):
						for matchcolumn in range(0,3):
							if (template[row][column] == template[matchrow][matchcolumn]) & (row != matchrow) & (column != matchcolumn):
								return False
			for column in range(3,6):
				if template[row][column] != 'x':
					for matchrow in range(row, 6):
						for matchcolumn in range(3,6):
							if (template[row][column] == template[matchrow][matchcolumn]) & (row != matchrow) & (column != matchcolumn):
								return False
			for column in range(6,9):
				if template[row][column] != 'x':
					for matchrow in range(row, 6):
						for matchcolumn in range(6,9):
							if (template[row][column] == template[matchrow][matchcolumn]) & (row != matchrow) & (column != matchcolumn):
								return False

	elif rownum >= 6:
		for row in range(6,9):
			for column in range(0,3):
				if template[row][column] != 'x':
					for matchrow in range(row, 9):
						for matchcolumn in range(0,3):
							if (template[row][column] == template[matchrow][matchcolumn]) & (row != matchrow) & (column != matchcolumn):
								return False
			for column in range(3,6):
				if template[row][column] != 'x':
					for matchrow in range(row, 9):
						for matchcolumn in range(3,6):
							if (template[row][column] == template[matchrow][matchcolumn]) & (row != matchrow) & (column != matchcolumn):
								return False
			for column in range(6,9):
				if template[row][column] != 'x':
					for matchrow in range(row, 9):
						for matchcolumn in range(6,9):
							if (template[row][column] == template[matchrow][matchcolumn]) & (row != matchrow) & (column != matchcolumn):
								return False

	return True

def ranking(sudoku):
	ranking = {}
	for rownum in range(0,9):
		count = 0
		for char in sudoku[rownum]:
			if char == 'x':
				count += 1
		ranking[rownum] = count
	order = sorted(ranking, key=ranking.__getitem__)
	#print order
	return order

def findmissing(row):
	nums = range(1,10)
	for i in range(0,9):
		nums[i] = str(nums[i])
	for char in row:
		try:
			nums.remove(char)
		except ValueError:
			pass
	return nums

#start of the actual program
if len(sys.argv) > 3 | len(sys.argv) == 0:
	print("proper usage: \npython sudoku.py <file.txt> [-a]\nfile.txt: file that contains the sudoku, with blank squares filled with x\n-a: computes all sudoku's instead of stopping at one")
	sys.exit()
#switch is here to allow for both calling python from bash/cmd command line and running script directly from python command line
if len(sys.argv) == 1:
	text = open(sys.argv[0], 'r',  90)
	compute_all = False
elif len(sys.argv) == 2:
	if sys.argv[1].lower() == "-a":
		text = open(sys.argv[0], 'r', 90)
		compute_all = True
	else:
		text = open(sys.argv[1], 'r', 90)
		compute_all = False
elif len(sys.argv) == 3:
	text = open(sys.argv[1], 'r',  90)
	if sys.argv[2].lower() == "-a":
		compute_all = True
	else:
		compute_all = False

#doing some things only needed at the very end
outfile = open("answer.txt", "w")
answercount = 0
starttime = timeit.default_timer()

sudoku = text.read()
text.close()
sudoku = sudoku.replace(" ","x")

#format sudoku from single string to two-dimensional array
rows = sudoku.split("\n")
sudoku = []
for row in rows:
	array = []
	for char in row:
		array.append(char)
	sudoku.append(array)

#find row with most numbers filled in
order = ranking(sudoku)
startrow = order[0]

#find numbers missing from startrow
missingnums = findmissing(sudoku[startrow])

#generate permutations for startrow
permutations = itertools.permutations(missingnums)
for permutation in permutations:
	# print "l1", startrow, permutation
	#start with a copy to preserve original
	template = list(sudoku)

	#test if permutation is correct
	if rowtest(template, inject(template[startrow], permutation), startrow):
		template[startrow] = inject(template[startrow], permutation)

		row2 = order[1]
		missingnums2 = findmissing(template[row2])
		#generate permutations for row 2
		permutations2 = itertools.permutations(missingnums2)
		for permutation2 in permutations2:
			# print "l2", row2, permutation2
			template2 = list(template)
			if rowtest(template2, inject(template2[row2], permutation2), row2):
				template2[row2] = inject(template2[row2], permutation2)

				row3 = order[2]
				missingnums3 = findmissing(template2[row3])
				permutations3 = itertools.permutations(missingnums3)
				for permutation3 in permutations3:
					# print "l3", row3, permutation3
					template3 = list(template2)
					if rowtest(template3, inject(template3[row3], permutation3), row3):
						template3[row3] = inject(template3[row3], permutation3)

						row4 = order[3]
						missingnums4 = findmissing(template3[row4])
						permutations4 = itertools.permutations(missingnums4)
						for permutation4 in permutations4:
							# print "l4", row4, permutation4
							template4 = list(template3)
							if rowtest(template4, inject(template4[row4], permutation4), row4):
								template4[row4] = inject(template4[row4], permutation4)

								row5 = order[4]
								missingnums5 = findmissing(template4[row5])
								permutations5 = itertools.permutations(missingnums5)
								for permutation5 in permutations5:
									# print "l5", row5, permutation5
									template5 = list(template4)
									if rowtest(template5, inject(template5[row5], permutation5), row5):
										template5[row5] = inject(template5[row5], permutation5)
										
										row6 = order[5]
										missingnums6 = findmissing(template5[row6])
										permutations6 = itertools.permutations(missingnums6)
										for permutation6 in permutations6:
											# print "l6", row6, permutation6
											template6 = list(template5)
											if rowtest(template6, inject(template6[row6], permutation6), row6):
												template6[row6] = inject(template6[row6], permutation6)

												row7 = order[6]
												missingnums7 = findmissing(template6[row7])
												permutations7 = itertools.permutations(missingnums7)
												for permutation7 in permutations7:
													# print "l7", row7, permutation7
													template7 = list(template6)
													if rowtest(template7, inject(template7[row7], permutation7), row7):
														template7[row7] = inject(template7[row7], permutation7)
														
														row8 = order[7]
														missingnums8 = findmissing(template7[row8])
														permutations8 = itertools.permutations(missingnums8)
														for permutation8 in permutations8:
															# print "l8", row8, permutation8
															template8 = list(template7)
															if rowtest(template8, inject(template8[row8], permutation8), row8):
																template8[row8] = inject(template8[row8], permutation8)
																
																row9 = order[8]
																missingnums9 = findmissing(template8[row9])
																permutations9 = itertools.permutations(missingnums9)
																for permutation9 in permutations9:
																	# print "l9", row9, permutation9
																	template9 = list(template8)
																	if rowtest(template9, inject(template9[row9], permutation9), row9):
																		template9[row9] = inject(template9[row9], permutation9)

																		#time to write it down
																		answer = []
																		for y in template9:
																			answer.append("".join(y))
																		answer = "\n".join(answer)
																		answer += "\n\n"

																		outfile.write(answer)
																		answercount += 1

																		if not compute_all:
																			stoptime = timeit.default_timer()
																			runtime = stoptime - starttime
																			outfile.close()
																			print("found " + str(answercount) + " answers in " + str(runtime) + " seconds")
																			sys.exit()
stoptime = timeit.default_timer()
runtime = stoptime - starttime
outfile.close()
print("found " + str(answercount) + " answers in " + str(runtime) + " seconds")
