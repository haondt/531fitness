class Gzclp:
	day = 0
	plates = []
	bar_weight = 0
	warmup_reps = ['1x5', '1x5', '1x3']
	warmup_multipliers = [0.4, 0.5, 0.6]
	
	# day_lifts[day][tier]
	# day and tier are both strings
	dayLifts = [{} for i in range(4)]
	
	# reps[stage][tier]
	# stage and tier are both ints
	reps = [
		["5x3", "3x10", "3x15+"],
		["6x2", "3x8", "n/a"],
		["10x1", "3x6", "n/a"]
	]
	
	# stages[lift][tier]
	# 0-indexed
	# lift is str, tier is int
	stages = {}

	# weights[lift][tier]
	# 0-indexed
	# 3 RM
	# lift is str, tier is int
	weights = {}

	# rests[tier]
	rests = [
		"3-5 min"
		"2-3 min"
		"60-90 sec"
	]

	def __init__(self, plates, bar_weight):
		self.plates = plates
		self.bar_weight = bar_weight

	# Get the (0-indexed) day
	def getDay(self):
		return self.day
	
	# Change the (0-indexed) day
	def setDay(self, day):
		if day >= 4 or day < 0:
			return False
		else:
			self.day = day
			return True

	# Returns helptext describing the GZCLP progression
	def helptext(self):
		return """
		How to test for new 5RM: 
		After warming up, start at last successful 5x3 weight and do 5 reps
		Add 5 lbs and repeat until unable to do 5 reps
		Last successful reps is 5RM

		Progression:
		Add 5 lbs to bench/ohp and 10 lbs to squat/DL T1 and T2 after each workout
		Add weight when you can do 25 reps on your AMRAP for T3

		Failure:
		Move to the next stage
		After stage 3, for T1, test for a new 5RM. Use 85% of that to restart cycle
		For T2, find the last weight you lifted using stage 1, add 15-20 lbs to this to restart cycle
		"""
	
	# Rounds a number to the precision of base
	def round(self, num, base):
		return round(base*round(float(num)/base),1)

	# Returns a string representing the weight in a form showing how to load the barbell
	def splitweight(self, weight):
		if weight > self.bar_weight:
			outstr = '%d + 2*(' % self.bar_weight
			weight = (weight - self.bar_weight)/2
			while weight > 0:
				i = 0
				while weight < self.plates[i]:
					i += 1
				outstr += '%.1f + ' % self.plates[i]
				weight -= self.plates[i]
			return outstr[:-3] + ')'
		else:
			return str(weight)
	
	# Given reps r and weight w, formats weight into readable string
	# weight is rounded to 2*smallest plate
	def formatweight(self, r, w):
		# Get plate weight, subtracting bar weight if possible
		plateWeight = w
		if w > self.bar_weight:
			plateWeight -= self.bar_weight
		
		# Round plateweight, according to 2x the smallest plate
		roundedPlateWeight = self.round(plateWeight, (self.plates[-1]*2))
		
		# calculate total weight based on method for calculating plate weight
		roundedWeight = roundedPlateWeight
		if w > self.bar_weight:
			roundedWeight += self.bar_weight
		
		return str(r) + " @ " + str(roundedWeight) + ": " + self.splitweight(roundedWeight)
	
	# Adds a lift with the given name
	# Weights is a 3-item list with the weight for [T1, T2, T3]
	# dayLifts is a 4-item list with the tier chosen for each of the 4 days
	# e.g liftName = "Squat", weight = [120, 110, 100], dayLifts = ["T1","","T2", ""]
	def addLift(self, liftName, weights, dayLifts):
		# Add to daylifts if liftname and/or tier aren't already in there
		for i in range(4):
			if dayLifts[i] is not None and dayLifts[i] is not "":
				if dayLifts[i] not in self.dayLifts[i]:
					self.dayLifts[i][dayLifts[i]] = []
				if liftName not in self.dayLifts[i][dayLifts[i]]:
					self.dayLifts[i][dayLifts[i]].append(liftName)
		# Add to stages
		self.stages[liftName] = [0,0,0]
		
		# Add to weights (make copy)
		self.weights[liftName] = weights[:]

	# Get the workout for the given day in a human-readable string
	def getWorkoutString(self, day):
		outstr = ""
		lifts = self.dayLifts[day]
		# Go through each tier
		for tierInt in range(3):
			tierStr = ['T1','T2','T3'][tierInt]
			# Check if lifts for that tier exist
			if tierStr in lifts:
				for lift in lifts[tierStr]:
					# Get stage of lift
					stage = self.stages[lift][tierInt]
					
					# Get reps and weights for main part of lift
					main_reps = self.reps[stage][tierInt]
					main_weight = self.weights[lift][tierInt]
					
					# Add label for lift
					outstr += lift + ":\n"

					# Only generate warmup for T1 and T2 lifts
					if tierStr != 'T3':
						# Add Warmup label
						outstr += '\tWarmup:\n'
						for j in range(len(self.warmup_reps)):
							# Roughly estimate 1rm = 1.25*3rm at T1 and calculate warmup weights as a percentage of that
							warmup_weights = self.warmup_multipliers[j]*self.weights[lift][0]*1.25
							# Build format string for warmup
							outstr += '\t\t%s' % self.formatweight(self.warmup_reps[j], warmup_weights) + '\n'

					# Generate working set
					outstr += '\tWorkingset:\n'
					outstr += '\t\t%s' % self.formatweight(main_reps, main_weight) + '\n'

		return outstr

