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
		UCONST_Pi = 3.1415926
		URotation180 = float(32768)
		URotationToRadians = UCONST_Pi / URotation180 
	
		inputs = [None] * 39
	
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

		# Rotations
		bluePitch = float(gameTickPacket.gamecars[blueIndex].Rotation.Pitch)
		blueYaw = float(gameTickPacket.gamecars[blueIndex].Rotation.Yaw)
		blueRoll = float(gameTickPacket.gamecars[blueIndex].Rotation.Roll)
		orngPitch = float(gameTickPacket.gamecars[orngIndex].Rotation.Pitch)
		orngYaw = float(gameTickPacket.gamecars[orngIndex].Rotation.Yaw)
		orngRoll = float(gameTickPacket.gamecars[orngIndex].Rotation.Roll)
		
		# Blue rotations
		inputs[20] = math.cos(bluePitch * URotationToRadians) * math.cos(blueYaw * URotationToRadians) # Rot 1
		inputs[21] = math.sin(blueRoll * URotationToRadians) * math.sin(bluePitch * URotationToRadians) * math.cos(blueYaw * URotationToRadians) - math.cos(blueRoll * URotationToRadians) * math.sin(blueYaw * URotationToRadians) # Rot2
		inputs[22] = -1 * math.cos(blueRoll * URotationToRadians) * math.sin(bluePitch * URotationToRadians) * math.cos(blueYaw * URotationToRadians) + math.sin(blueRoll * URotationToRadians) * math.sin(blueYaw * URotationToRadians)  # Rot 3
		inputs[23] = math.cos(bluePitch * URotationToRadians) * math.sin(blueYaw * URotationToRadians) # Rot 4
		inputs[24] = math.sin(blueRoll * URotationToRadians) * math.sin(bluePitch * URotationToRadians) * math.sin(blueYaw * URotationToRadians) + math.cos(blueRoll * URotationToRadians) * math.cos(blueYaw * URotationToRadians) # Rot5
		inputs[25] = math.cos(blueYaw * URotationToRadians) * math.sin(blueRoll * URotationToRadians) - math.cos(blueRoll * URotationToRadians) * math.sin(bluePitch * URotationToRadians) * math.sin(blueYaw * URotationToRadians) # Rot 6
		inputs[26] = math.sin(bluePitch * URotationToRadians) # Rot 7
		inputs[27] = -1 * math.sin(blueRoll * URotationToRadians) * math.cos(bluePitch * URotationToRadians) # Rot 8
		inputs[28] = math.cos(blueRoll * URotationToRadians) * math.cos(bluePitch * URotationToRadians) # Rot 9
		
		# Orange rot
		inputs[29] = math.cos(orngPitch * URotationToRadians) * math.cos(orngYaw * URotationToRadians) # Rot 1
		inputs[30] = math.sin(orngRoll * URotationToRadians) * math.sin(orngPitch * URotationToRadians) * math.cos(orngYaw * URotationToRadians) - math.cos(orngRoll * URotationToRadians) * math.sin(orngYaw * URotationToRadians) # Rot2
		inputs[31] = -1 * math.cos(orngRoll * URotationToRadians) * math.sin(orngPitch * URotationToRadians) * math.cos(orngYaw * URotationToRadians) + math.sin(orngRoll * URotationToRadians) * math.sin(orngYaw * URotationToRadians)  # Rot 3
		inputs[32] = math.cos(orngPitch * URotationToRadians) * math.sin(orngYaw * URotationToRadians) # Rot 4
		inputs[33] = math.sin(orngRoll * URotationToRadians) * math.sin(orngPitch * URotationToRadians) * math.sin(orngYaw * URotationToRadians) + math.cos(orngRoll * URotationToRadians) * math.cos(orngYaw * URotationToRadians) # Rot5
		inputs[34] = math.cos(orngYaw * URotationToRadians) * math.sin(orngRoll * URotationToRadians) - math.cos(orngRoll * URotationToRadians) * math.sin(orngPitch * URotationToRadians) * math.sin(orngYaw * URotationToRadians) # Rot 6
		inputs[35] = math.sin(orngPitch * URotationToRadians) # Rot 7
		inputs[36] = -1 * math.sin(orngRoll * URotationToRadians) * math.cos(orngPitch * URotationToRadians) # Rot 8
		inputs[37] = math.cos(orngRoll * URotationToRadians) * math.cos(orngPitch * URotationToRadians) # Rot 9

		# Teams
		if (self.team == "blue"):
			inputs[38] = 1
		else:
			inputs[38] = 2 
		
		return inputs