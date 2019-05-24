# day/week to calculate for
day, week = 1,2
weights = [45,25,10,5,2.5]
bar_weight = 45
# training max
tm = {
	'Squats':220,
	'Bench Press':180,
	'Deadlift':345,
	'Overhead Press':135,
}

warmup_reps = ['1x5', '1x5', '1x3']
warmup_multipliers = [0.4, 0.5, 0.6]

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
	s += '\nWarmup:\n\t3x5 Box Jumps\n'

	for i in range(2):
		s += day_lifts[day][i] + ':\n'
		s += '\t(Warmup)\n'
		for j in range(len(warmup_reps)):
			s += '\t' + warmup_reps[j] + ' @ '
			weight = warmup_multipliers[j]*tm[day_lifts[day][i]]
			s += str(myRound(weight,weights[-1]*2)) + ' = ' + splitweight(myRound(weight,weights[-1]*2)) + '\n'
		s += '\t(Lifts)\n'
		for j in range(4): 
			s += '\t' + week_reps[week][j] + ' @ '
			weight = week_multipliers[week][j]*tm[day_lifts[day][i]]
			s += str(myRound(weight,weights[-1]*2)) + ' = ' + splitweight(myRound(weight,weights[-1]*2)) + '\n'
		s += '\n'
	s+='\nAssistance Work:\n'
	s+= '\n'.join(['\t50-100x '+i for i in assistance_work])
	
	return s

def splitweight(weight):
	if weight > bar_weight:
		outstr = '%d + 2*(' % bar_weight
		weight = (weight - bar_weight)/2
		while weight > 0:
			i = 0
			while weight < weights[i]:
				i += 1
			outstr += '%.1f + ' % weights[i]
			weight -= weights[i]
		return outstr[:-3] + ')'
	else:
		return str(weight)

if __name__ == '__main__':
	print('Week %d, Day %d:' % (week+1, day+1))
	print(calculate(day,week))
