day, week = 0,1
# zero indexed
# Calculator / help tool for 5/3/1 program
# percentages are a percentage of your training max
# Training max = theorhetical one rep max

# Week 1:
# 1x5 @ 65%
# 1x5 @ 75%
# 1x5+ @ 85%

# Week 2:
# 1x3 @ 70%
# 1x3 @ 80%
# 1x3+ @ 90%

# Week 3:
# 1x5 @ 75%
# 1x3 @ 85%
# 1x1+ @ 95%

# FSL
# -> same percentage as first set for that day

# Warm up
# box jumps OR broad jumps OR medicine ball throws

# main lift warmup 
# 1x5 @ 40%
# 1x5 @ 50%
# 1x3 @ 60%

# Program

# Day 1
# squats 5/3/1 then 5x5 FSL
# Bench 5/3/1 then 5x5 FSL
# Assistance work

# Day 2
# DL 5/3/1 then 5x5 FSL
# OHP 5/3/1 then 5x5 FSL
# Assistance work

# Day 3
# Bench 5/3/1 then 5x5 FSL
# squats 5/3/1 then 5x5 FSL

# At the end of each 3 week cycle, 
# add 5 lbs to Bench & OHP tm
# add 10 lbs to Squat & DL

# training max
tm = {
	'Squats':290,
	'Bench Press':160,
	'Deadlift':310,
	'Overhead Press':120,
}

week_reps = [
	['1x5', '1x5', '1x5+', '5x5'],
	['1x3', '1x3', '1x3+', '5x5'],
	['1x5', '1x3', '1x1+', '5x5']
]

week_multipliers = [
	[0.65, 0.75, 0.85, 0.65],
	[0.7, 0.8, 0.9, 0.7],
	[0.75, 0.85, 0.95, 0.75]
]

day_lifts = [
	['Squats', 'Bench Press'],
	['Deadlift', 'Overhead Press'],
	['Bench Press', 'Squats']
]

assistance_work = ['Dips', 'Pullups', 'hanging leg raises']

def myRound(num, base):
	return round( base*round(float(num)/base),1)

def calculate(day, week):
	s = ''
	for i in range(2):
		s += day_lifts[day][i] + ':\n'
		for j in range(4): 
			s += '\t' + week_reps[week][j] + ' @ '
			weight = week_multipliers[week][j]*tm[day_lifts[day][i]]
			s += str(myRound(weight,5)) + ' = ' + splitweight(myRound(weight,5)) + '\n'
		s += '\n'
	s+='\nAssistance Work:\n'
	s+= '\n'.join(['\t50-100x '+i for i in assistance_work])
	
	return s

def splitweight(weight):
	outstr = '45 + 2*('
	weight = (weight - 45)/2
	while weight > 0:
		i = 0
		weights = [45,25,10,5,2.5]
		while weight < weights[i]:
			i += 1
		outstr += '%.1f + ' % weights[i]
		weight -= weights[i]
	return outstr[:-3] + ')'

print(calculate(day,week))
