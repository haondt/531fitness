from fivethreeone import myRound, splitweight
day = 1 # 0-3
plates = [45,25,10,5,2.5]
bar_weight = 45

warmup_reps = ['1x5', '1x5', '1x3']
warmup_multipliers = [0.4, 0.5, 0.6]

# day_lifts[day][tier]
day_lifts = [
	["Squat", "Bench Press", "Lat Pulldown"],
	["Overhead Press", "Deadlift", "Dumbbell Row"],
	["Bench Press", "Squat", "Lat Pulldown"],
	["Deadlift", "Overhead Press", "Dumbbell Row"]
]

# reps[stage][tier]
reps = [
	["5x3", "3x10", "3x15+"],
	["6x2", "3x8", "n/a"],
	["10x1", "3x6", "n/a"]
]

# stages[lift][tier] 
# 0-indexed
stages = {
	"Squat": 			[2, 2, 0],
	"Bench Press": 		[0, 0, 0],
	"Lat Pulldown": 	[0, 0, 0],
	"Overhead Press": 	[2, 1, 0],
	"Deadlift": 		[1, 2, 0],
	"Dumbbell Row": 	[0, 0, 0]
}

# weights[lift][tier] 
# 0-indexed
# 3 RM
weights = {
	"Squat": [235, 195, 0],
	"Bench Press": [160, 125, 0],
	"Lat Pulldown": [0, 0, 110],
	"Overhead Press": [120, 100, 0],
	"Deadlift": [345, 310, 0],
	"Dumbbell Row": [0, 0, 30]
}

# rests[tier]
rests= [
	"3-5 min",
	"2-3 min",
	"60-90 sec"
]

# How to test for new 5RM:
# After warming up, start at 5x3 weight and do 5 reps
# add 5 lbs and repeat until unable to do 5 reps
# last successful 5 reps is 5RM

# Progression:
# Add 5 lbs to bench/ohp and 10 lbs to squat/DL T1 and T2 after each workout
# add weight when you can do 25 reps on your AMRAP for T3

# Failure:
# move to the next stage 
# After stage 3, for T1, test for a new 5RM. Use 85% of that to restart cycle
# for T2, find the last weight you lifted using stage 1, add 15-20 lbs to this 
# restart the cycle.

def formatweight(r, w):
	return str(r) + " @ " + str(myRound(w,plates[-1]*2)) + ": " + splitweight(myRound(w, plates[-1]*2)) 

# workout(day)
def workout(day):
	lifts = day_lifts[day]
	for i in range(len(lifts)):
		tier = i
		lift = lifts[tier]
		stage = stages[lift][tier]
		main_reps = reps[stage][tier]
		main_weight = weights[lift][tier]
		#warmup_reps warmup_multipliers
		print(lift, end=':\n')
		if not tier == 2:
			print('\tWarmup:')
			for i in range(len(warmup_reps)):
				# roughly estimate 1rm = 1.25*3rm at T1
				print('\t\t%s' % formatweight(warmup_reps[i], warmup_multipliers[i]*weights[lift][0]*1.25))
		print('\tWorking set:')
		print('\t\t%s' % formatweight(main_reps, main_weight))
		
	'''
	p1 = []
	p2 = []
	p3 = []
	for i in range(len(lifts)):
		tier = i
		lift = lifts[tier]
		stage = stages[lift][tier]
		_reps = reps[stage][tier]
		weight = weights[lift][tier]
		p1.append(lift+":")
		p2.append(" "+ str(_reps) + " @" + str(weight) +": ")
		p3.append(splitweight(myRound(weight, plates[-1]*2))+ " (" + rests[tier] + " rest)")
	
	for i in range(len(p1)):
		for p in [p1, p2]:
			print(p[i].rjust(len(max(p, key=lambda x: len(x)))), end='')
		print(p3[i])
	'''
def main():
	print('Day', str(day+1) + ':')
	workout(day)

if __name__ == '__main__':
	main()
