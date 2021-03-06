# Identical to runRight but with different sleep offsets 
# (the left sphero is the second to turn blue and reset)

from multiprocessing import Process
import sphero

# Controller Libraries
import time
import os
import json
# from pprint import pprint
import math

# Tracking code
import cv2

# Modify from Simon Tordensky's Base 
from tracker.trackingfilter import FilterSpheroBlueCover, FilterGlow
from tracker.traceable import TraceableObject
from tracker.trackerbase import ColorTracker

from util import Vector2D
from SpheroController.tracablesphero import TraceableSphero

# Import to make the sphero team library accessible from other folders
import sys
sys.path.append('./')

import SpheroTeam
from SpheroTeam import initialize
# use reload(SpheroTeam) to refresh lib as it gets updated

# Library written to help with tracking

from SpheroTeam.teamutil import readJsonFile, normalize_angle, angle_between_points

slowTime = 3
normalTime = 2
fastTime = 1
returnTime = 1

fastSpeed = 140
normalSpeed = 80
slowSpeed = 55
returnSpeed = 183 # different from runRights' because of room tilt

# Integrate camera

#Track Camera Size: 
tracker = ColorTracker()

# Check dimensions of your field. We're using the Logitech C920
tracker.image_size

# Use blue because it's the most reliable color filter
traceable_blue = TraceableObject("BLUE")
print traceable_blue
traceable_blue.filter = FilterSpheroBlueCover()

TRACEABLE_COLOR = [0, 0, 255]
tracklist = [traceable_blue]
offsets = []
# initialize globally so accessible
startX = -1
startY = -1
startTime = 0

def main():
	global startTime
	startTime = time.time()

	# Config management
	PROJ_ROOT = os.pardir
	CONFIG = os.path.join(PROJ_ROOT, "config.json")

	# Class for managing multiple spheros
	manager = sphero.SpheroManager()

	manager= SpheroTeam.initialize.load_sphero_roster(manager, CONFIG)

	# Verify that proper robots have been added
	for name, device in manager._spheros.iteritems():
		print "{}: {}".format(name, device.bt_addr)

	# Manually pick out the robots to include by specifying their abbreviation.
	# example: bots = [devices[4], devices[1]]
	activeBots = ['RWR']

	# Connect to these robots
	bots = SpheroTeam.initialize.connect_sphero_team(manager, activeBots)

	# All robots start with lights off to save power
	for bot in bots:
		bot.set_rgb(0,0,0)

	# Check team power state
	SpheroTeam.print_team_status(bots)

	# set starting positions for closed loop control
	# time for right to calibrate
	time.sleep(20)
	for bot in bots:
		bot.set_rgb(0, 0, 255)
		time.sleep(2)
		global startX
		global startY
		startX, startY = get_bot_position(bot, traceable_blue, tracker)
		print startX
		print startY
		global offsets
		print "calibrating"
		offsets.append(calibrate_bot_direction(bot,  traceable_blue, [0, 0, 255], tracker, True))
	# reset bot post calibration
	time.sleep(15)
	bot_to_point(bots[0], offsets[0], startX, startY, TIMEOUT=400)
	bot.set_rgb(0,0,0)

	# run behaviors
	while (time.time() < startTime + 45):
	 	continue
	bot = bots[0]
	with open('newBehaviorsOrderLeft.json') as f:
		order = json.load(f)
	runAllBehaviors(bot, order)

	exit()

def runAllBehaviors(bot, order):
	timeFromStart = 50
	for item in order:
		for key in item:
			if key == "direction":
				direction = item[key]
			elif key == "behavior":
				behavior = item[key]

		# direction and behavior should be set
		if direction == "left":
			outAngle = 270
			returnAngle = 90
		elif direction == "fwd":
			outAngle = 0
			returnAngle = 180
		else:
			outAngle = 90
			returnAngle = 260

		while (time.time() < startTime + timeFromStart):
			continue
		timeFromStart = timeFromStart + 28
		runSingleBehavior(bot, behavior, outAngle, returnAngle)
		time.sleep(2)

		# call reset here
		time.sleep(8) # time for right to reset
		bot.set_rgb(0,0,255)
		# time.sleep(1)
		bot_to_point(bot, offsets[0], startX, startY, TIMEOUT=400)
		bot.set_rgb(0,0,0)
		

def runSingleBehavior(bot, behavior, outAngle, returnAngle):
	if behavior == "slow":
		goAtSpeed(bot, slowSpeed, outAngle, slowTime, returnSpeed, returnAngle, returnTime)
	elif behavior == "fast":
		goAtSpeed(bot, fastSpeed, outAngle, fastTime, returnSpeed, returnAngle, returnTime)
	else:
		if behavior == "blink":
			goBlink(bot, normalSpeed, outAngle, normalTime, returnSpeed, returnAngle, returnTime)
		elif behavior == "solid_light":
			goSolidLight(bot, normalSpeed, outAngle, normalTime, returnSpeed, returnAngle, returnTime)
	time.sleep(0.25)
	bot.set_rgb(0,0,0)
	bot.set_motion_timeout(returnTime * 1000)
	bot.roll(returnSpeed, returnAngle, 1)
	time.sleep(returnTime)

def goAtSpeed(bot, outSpeed, outAngle, outTime, returnSpeed, returnAngle, returnTime):
	bot.set_motion_timeout(outTime * 1000)
	bot.roll(outSpeed, outAngle, 1)
	time.sleep(6)


def goBlink(bot, outSpeed, outAngle, outTime, returnSpeed, returnAngle, returnTime):
	bot.set_motion_timeout(outTime * 1000)
	bot.roll(outSpeed, outAngle, 1)
	on = True
	for quarter_second in range(0, 4 * 6):
		if on:
			bot.set_rgb(0,0,0)
			on = False
		else:
			bot.set_rgb(138,191,255)
			on = True
		time.sleep(0.25)

def goSolidLight(bot, outSpeed, outAngle, outTime, returnSpeed, returnAngle, returnTime):
	bot.set_rgb(138,191,255)
	bot.set_motion_timeout(outTime * 1000)
	bot.roll(outSpeed, outAngle, 1)
	time.sleep(6 - outTime)

# For Debugging
def display_current_view(tracker):
	image = tracker.get_video_frame()
	cv2.imshow("img", image)
	cv2.waitKey(0)
	
	cv2.destroyAllWindows()
	
def display_current_video(tracker):
	"""
		Displays current video feed, press 'q' to escape
	"""
	cam = tracker.cam
	while(True):
		# Capture frame-by-frame
		ret, frame = cam.read()

		# Display the resulting frame
		cv2.imshow('frame', frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
			
	cv2.destroyAllWindows()

	
# For Navigation
def get_bot_position(bot, traceable_object, tracker, samples=3, debug=False):  
	xSamples = []
	ySamples = []
	 
	for sample in range(samples):
		image = tracker.get_video_frame()

		timestamp = time.time()
		
		if sample > 0: # ignore the first sample
			x, y = tracker._find_traceable_in_image(image, traceable_object) # side effect: adds mask to tracker  
			if x:
				xSamples.append(x)
			if y:
				ySamples.append(y)

			traceable_object.add_tracking(Vector2D(x, y), timestamp)

	if debug:	  
		display_current_view(tracker)
	print "{} | {} ".format(xSamples, ySamples)

	return (sum(xSamples) / len(xSamples)), (sum(ySamples) / len(ySamples))


def calibrate_bot_direction(bot, traceable_object, traceable_color, tracker, debug=False):
	"""
		Routine for making all robots line up in the same direction
		"""
	TIMEOUT = 1500  # in MILLISECONDS
	
	
	bot.set_rgb(traceable_color[0], traceable_color[1], traceable_color[2])
	bot.set_motion_timeout(TIMEOUT)
	startX, startY =  get_bot_position(bot, traceable_object, tracker)

	cv2.waitKey(250)  # not sure how long this has to be
	
	
	if (startX is None) or (startY is None):
		print("Error: Robot not in view")
		return -1
	
	print "Start ({},{})".format( startX, startY)

	bot.roll(30, 0)
	time.sleep(TIMEOUT / 1000)

	endX, endY	   =  get_bot_position(bot, traceable_object, tracker)
	  
	print "End   ({},{})".format(   endX, endY)
	offset = normalize_angle(angle_between_points(startX, startY, endX, endY))
	

	print "Angle {}".format(offset) 
	
	return offset

# Video display
def display_tracking_window(traceable_object_list, exitKey = "q"):
	"""
		Given a list of iterables, track all objects in that list.
		Press exitKey to quit the window
	"""
	
	while(True):

		tracker.track_objects(tracklist)
		cv2.waitKey(1)

		if cv2.waitKey(1) & 0xFF == ord(exitKey):
			break 
	cv2.destroyAllWindows()

# Team Calibration Routine
def get_team_offsets(bots, traceable_object, traceable_color):
	offsets = []
	
	for bot in bots:
		print "Im about to calibrate direction"
		offset = calibrate_bot_direction(bot,  traceable_blue, [0, 0, 255], tracker, True)
		offsets.append(offset)
		proceed = raw_input("'q' to quit, else continue")
		
		if proceed == "q":
			break
		else:
			continue
	return offsets

def bot_to_point(bot, offset,
				 targetX, targetY, 
				 TIMEOUT=800,
				 trace_object=traceable_blue, trace_color=TRACEABLE_COLOR, 
				 tracker=tracker, MAX_SECONDS=10, stopRadius=5):
	"""
		Currently makes use of a few implicit globals for simplicity
		specifically traceable_blue, traceable_color
		Maybe set stop radius  based on pixel size
		
		Wiggles because aiming for direct path / precision
		
		Constrast to "RUSH TO POINT IN STRAIGHT LINE"
		
		Really would work better with a bigger field
		
		Maybe we can push lighter things?
		
		Or boost speed when within range: pause and then burst
	"""
	currentX, currentY = get_bot_position(bot, trace_object, tracker)

	# Basic closed loop controller
	startTime = time.time()
	
	# Angle to distance
	deltaX = targetX - currentX
	deltaY = targetY - currentY
	angle = math.degrees(math.atan2(deltaY, deltaX))
	distance = math.sqrt(deltaX * deltaX + deltaY * deltaY)
	
	print("Get from {},{} to {},{}| Distance {} / {}").format(currentX, currentY, 
														 targetX, targetY, distance, angle)
	bot.set_motion_timeout(TIMEOUT)

	# REPLACE SOMEDAY WITH TRUE PID CONTROLLER
	while distance > stopRadius and (((time.time() - startTime ) < MAX_SECONDS)):
		# these should be tuned based on how many pixels 1 ball is.
		
		if distance < 60:
			print("SUPER CLOSE")
			outSpeed = 33
		elif distance < 100:
			outSpeed = 40
		elif distance < 250:
			outSpeed = 60
		else:
			time.sleep(0.3)
			outSpeed = 70

		print("Dist {} outSpeed {} at {} degrees: {},{}"\
			  .format(distance, outSpeed, angle, currentX, currentY))
		
		SpheroTeam.roll_sphero(bot, outSpeed, -angle, offset)
		
		time.sleep(TIMEOUT/1000.0)
		time.sleep(.3) # give camera time to catch up

		currentX , currentY = get_bot_position(bot, trace_object, tracker)

		# Repeat waypointing calculation
		deltaX = targetX - currentX
		deltaY = targetY - currentY
		
		angle = math.degrees(math.atan2(deltaY, deltaX))
		distance = math.sqrt(deltaX * deltaX + deltaY * deltaY)

	print("Stopped at {},{}, with dist {}").format(currentX, currentY, distance)


if __name__ == "__main__":
	main()