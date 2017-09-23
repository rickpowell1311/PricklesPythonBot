import json
import math
import numpy as np
import time
from websocket import create_connection

BOT_NAME = "Prickle's NET BOT"

class agent:
	def __init__(self, team):
		self.team = team # use self.team to determine what team you are. I will set to "blue" or "orange"
		self.ws = create_connection("ws://localhost:12345/", timeout=30000)
		
	def get_output_vector(self, sharedValue):
		new_input = self.convert_new_input_to_old_input(sharedValue)
		self.ws.send_binary(json.dumps(new_input))
		response = self.ws.recv()
		output = json.loads(response)
		print(output)
		return output

	def convert_new_input_to_old_input(self, sharedValue):
	
		UU_TO_GAMEVALUES = 50
	
		inputs = [None] * 20
	
		gameTickPacket = sharedValue.GameTickPacket
		
		numCars = gameTickPacket.numCars
		numBoosts = gameTickPacket.numBoosts
		
		team1Blue = (gameTickPacket.gamecars[0].Team == 0)
		
		if team1Blue:
			blueIndex = 0
			orngIndex = 1
		else:
			blueIndex = 1
			orngIndex = 0
		
		# -------------------------------
		# First convert ball info
		# -------------------------------
		
		# Ball positions
		inputs[0] = gameTickPacket.gameball.Location.Y / UU_TO_GAMEVALUES
		inputs[1] = gameTickPacket.gameball.Location.X / UU_TO_GAMEVALUES
		inputs[2] = gameTickPacket.gameball.Location.Z / UU_TO_GAMEVALUES
		
		# Ball velocities
		inputs[3] = gameTickPacket.gameball.Velocity.X  / UU_TO_GAMEVALUES
		inputs[4] = gameTickPacket.gameball.Velocity.Z  / UU_TO_GAMEVALUES
		inputs[5] = gameTickPacket.gameball.Velocity.Y  / UU_TO_GAMEVALUES
			
		# -------------------------------
		# Now do all car values
		# -------------------------------
		
		# Blue pos
		inputs[6] = gameTickPacket.gamecars[blueIndex].Location.Y / UU_TO_GAMEVALUES
		inputs[7] = gameTickPacket.gamecars[blueIndex].Location.X / UU_TO_GAMEVALUES
		inputs[8] = gameTickPacket.gamecars[blueIndex].Location.Z / UU_TO_GAMEVALUES
		
		# Orange pos
		inputs[9] = gameTickPacket.gamecars[orngIndex].Location.Y / UU_TO_GAMEVALUES
		inputs[10] = gameTickPacket.gamecars[orngIndex].Location.X / UU_TO_GAMEVALUES
		inputs[11] = gameTickPacket.gamecars[orngIndex].Location.Z / UU_TO_GAMEVALUES
		
		# Blue velocity
		inputs[12] = gameTickPacket.gamecars[blueIndex].Velocity.X / UU_TO_GAMEVALUES
		inputs[13] = gameTickPacket.gamecars[blueIndex].Velocity.Z / UU_TO_GAMEVALUES
		inputs[14] = gameTickPacket.gamecars[blueIndex].Velocity.Y / UU_TO_GAMEVALUES
		
		# Orange velocity
		inputs[15] = gameTickPacket.gamecars[orngIndex].Velocity.X / UU_TO_GAMEVALUES
		inputs[16] = gameTickPacket.gamecars[orngIndex].Velocity.Z / UU_TO_GAMEVALUES
		inputs[17] = gameTickPacket.gamecars[orngIndex].Velocity.Y / UU_TO_GAMEVALUES
		
		# Boost
		inputs[18] = gameTickPacket.gamecars[blueIndex].Boost
		inputs[19] = gameTickPacket.gamecars[orngIndex].Boost
		
		return inputs