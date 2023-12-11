#note to self - change type speed
#I was going to make more of the rooms have more functions (especialy the cockpit) but I ran out of time because I spent so long figuring out simple things like what a hashable type was. It was entirely my fault though.

#imports here
import time
import os
import random
os.system("clr" if os.name == "nt" else "clear")

t = 0 #place holder
#These are the cordinates of the player.
xy = [0, 0]
#the players inventory
inventory = ["emptyspot"]
engine = "broken"
room_pos = [[0, 0], [0, 1], [-1, 1], [-2, 1], [-1, 0], "engine_room_locked", [-1, 2], [-1, 3]]
#had to split this variable because list is not a hashable type. other half is at bottom


#this is a naration device that outputs text at a regular rate rather than all at once.
def narrate(text, speed, wait):

  #speed setting translators
  # if speed == 3:
  speed = .004
  # elif speed == 2:
  #   speed = .07
  # elif speed == 1:
  #   speed = .2

  #wait setting translators
  if wait == "short":
    wait = .7
  elif wait == "long":
    wait = 3
  elif wait == "none":
    wait = 0
  elif wait == "norm":
    wait = 1.6

  #This is where the text is printed
  for char in text:
    print(char, end='', flush=True)
    #\/This condition is here because the new lines were taking too long to be printed in my opinion.
    if char != "\n":
      time.sleep(speed)
      #\/this is how long the delay after it has been printed will last
  time.sleep(wait)

def travel(choice):
#This function takes in player text and 
#tests it for movement comands, then it updates the player's position acordingly
  global xy
  #globalise the player's position
  moved = True

  #here I test for comands and change position, if the position is locked or doesn't exist, the program will run the out of bounds function (it prints a mesage leting them know they ran into a wall) and reset its position.
  if "north" in choice:
    xy[1] = xy[1] + 1
    if xy not in room_pos:
      moved = False
      xy[1] -= 1
      out_of_bounds()
  elif "east" in choice:
    xy[0] +=1
    if xy not in room_pos:
      moved = False
      xy[0] -=1
      out_of_bounds()
  elif "south" in choice:
    xy[1] -=1
    if xy not in room_pos:
      moved = False
      xy[1] +=1
      out_of_bounds()
  elif "west" in choice:
    xy[0] -=1
    if xy not in room_pos:
      moved = False
      xy[0] +=1
      out_of_bounds()

  #this returns the function that corisponds with the players position
  if moved == True:
    id = room_pos.index(xy)
    return room_locate[id]

def out_of_bounds():
  #This will play every time the player atempts to walk through walls.
  narrate("You ran into a wall so hard it launched you backwards!\n", 2, 'short')
  narrate("Don't ask me who put a wall there, how should I know?\n", 2, 'none')


def hibernation_room():
  #clears syestem when enter room
  os.system("clr" if os.name == "nt" else "clear")
  
#globalise player position, movement variable, and inventory
  global xy
  global t
  global inventory

  #introduction to room
  narrate("\nHIBERNATION ROOM\nYou are in a large round room filled with cylindrical chambers, near the south side there is a pile of more damaged chambers, there is a pod door on the north side, and reinforced walls near the west. It doesn't look like anyone else awoke from their hibernation.", 3, 'norm')

  #pos is used to track where a player is in a request chain
  pos = ''
  #while the room is unchanged run the player options
  while xy == [0, 0]:
    #get input
    narrate('\n\n\nwhat would you like to do?', 2, 'none')
    choose = input('\n\n')
    #set input to a more universal scale so I dont have to test for all of these as an example "The tHe thE THE the"
    choice = choose.lower()
    #here is the request chain, it tests for key words in sentences as comands, then exicutes its best guess.
    if 'check' in choice and 'room' in choice:
      #if player asked to check the room
      narrate("HIBERNATION ROOM\nYou are in a large round room filled with cylindrical chambers, the ones on the south side are knocked over, there is a pod door on the north side, and reinforced walls near the west. It doesn't look like anyone else awoke from their hibernation.", 3, 'norm')
    elif ('check' in choice or 'go' in choice) and ('chamber' in choice or 'cylind' in choice) and ('pile' in choice or 'damaged' in choice or 'broken' in choice):
      #if player asked to check the broken chambers
      os.system("clr" if os.name == "nt" else "clear")
      narrate("There are three cryochambers lying here, behind one there is a small locked pod door.", 2, 'norm')
      pos = 'broken cryochamber'
    elif 'check' in choice and ('chamber' in choice or 'cylind' in choice):
      #if player asked to check the unbroken chambers in general
      narrate("You carefuly look through the cryochambers. You only vagly recignise most people sleeping but one seems strikingly familiar, you just can't put your finger on it.\n\n You are tempted for a moment to open a chamber, before remembering that without proper training opening somone else's chamber is a death sentence for the one within.", 2, 'norm')
      pos = ''
    elif 'check' in choice and 'reinforced' in choice:
      #if player asked about the reinforced wall
      narrate("Yep, it's shure a reinforced wall. You can tell because your friend mentioned they have a dark shine to them. Who was he again?", 2, 'norm')
      pos = ''
    elif 'check' in choice and 'door' in choice:
      #if player asked about the northern door
      narrate("The northern pod door is open and through the opening you see the crew's quarters, as well as your quarters.", 2, 'norm')
      pos = 'door'

    if pos == 'door':
      #if player is at the door ask these questions
      if 'enter' in choice or "go" in choice:
        choice = 'north'
    if pos == 'broken cryochamber':
      #if player is at the broken cryochamber ask these questions
      if "unlock" in choice:
        if "engine room key placeholder" in inventory:
          narrate("You unlock the door and with the hissing of pistons it opens.", 2, "norm")
          #\/ this adds the room's position to the list of positions at the bottom of my code thus making it a valid destination.
          room_pos[5] = [0, -1]
        else:
          #you dont have the key
          narrate("You are missing the key card required to open.", 2, "norm")
      elif 'open' in choice:
        narrate("Door is locked", 2, "norm")
      elif 'enter' in choice or 'through' in choice:
        # if player says enter while near this door rather than the traditional directions, this will transelate it
        choice = 'south'


    # run the movement function
    t = travel(choice)
    #\/this function acts as a wall, the room is acsesable, just not from here.
    if t == armory_room:
      xy = [0, 0]
      out_of_bounds()
      #\/ I put this condition in because of a glitch I kept encountering, it should be fixed now, but I dont want to risk it.__doc__
  if t != hibernation_room:
    #when the while function above stops (when room changes) This makes it oficial, using the return value from the travel function it will run whatever room you are moveing to.
    t()
      

      

      
def engine_room():
  #clears syestem when enter room
  os.system("clr" if os.name == "nt" else "clear")
  
  #globalise player position, movement variable, inventory, and the engine variable which represents wether the engine is fixed or not.
  global xy
  global t
  global inventory
  global engine
  #room intro
  narrate("\nENGINE ROOM\nYou are in a cramped mecanical hallway that runs alongside the space ship's engine. Wait, the ship! That's where you are! Your memories are returning, but slowly.", 3, 'norm')

  #while room is unchanged run player options
  while xy == [0, -1]:
    narrate('\n\n\nwhat would you like to do?', 2, 'none')
    choose = input('\n\n')
    #set player options to a easyer form to test
    choice = choose.lower()
    # the folowing is the choice branches that test for key words and run the syestem responce.
    if "fix" in choice or "repair" in choice:
      #to fix an engine you must first have the tools
      if "repair tool" in inventory:
        narrate("Fixing engine dialog: Useing the tool you found in the storage room.", 2, 'norm')
        engine = 'fixed'
      else:
        narrate("You will probably need a tool for this.", 2, 'norm')
    elif "check" in choice and "engine" in choice:
      narrate("The engine apears to be damaged. It isnt beond your ability to fix, but you dont think you were a mechanic.", 2, 'norm')
    elif "check" in choice and "room" in choice:
      #alternate room discription called on by the player
      narrate("You are in a cramped mecanical hallway that runs alongside the space ship's engine. You never liked it here, luckily you were rarly needed there.", 2, 'norm')
    #test for basic movement comands via the travel function
    t = travel(choice)
    #another potential glitch avoider\/
  if t != engine_room:
    t()
    #after loop ends move to corect room from travel function



      

def servant_quarters_room():
  #clears syestem when enter room
  os.system("clr" if os.name == "nt" else "clear")
  
  #globalise player position, movement variable, and inventory.
  global xy
  global t
  global inventory
  #intro to room
  narrate('\n\n\nTHE QUARTERS\n There is a long hallway with many doors, all are locked though, and can only be unlocked through fingerprint. You find one that seems familiar and slip inside. It is fairly messy and there is a pile of laundry in the corner.', 3, 'norm')
  while xy == [0, 1]:
    narrate('\n\n\nwhat would you like to do?', 3, 'none')
    choose = input('\n\n')
    choice = choose.lower()
    if 'check' in choice and 'laundry' in choice:
      if 'engine room key placeholder' in inventory:
        narrate('You search the disgarded clothing, but find nothing there.', 2, 'norm')
      else:
        narrate("After searching through the disgarded cloths you found a passenger's key card and add it to your inventory.", 2, 'norm')
        inventory += ["engine room key placeholder"]
    elif 'check' in choice and 'room' in choice:
      narrate("You are begining to remember this place but not all is quite clear. The laundry pile in the corner should have been cleaned a long time ago. You aren't lazy, you just havent goten around to it yet.", 3, 'norm')
    t = travel(choice) 
  if t != servant_quarters_room:
    t()
      
#the folowing code will run when the player changes the room.


      
def guard_room():
  os.system("clr" if os.name == "nt" else "clear")
  
  
  global xy
  global t
  global inventory
  narrate('GUARD ROOM\nYou are in a smaller (compared to everywhere else) cubular room you think you spent alot of time in. There are suits of armor on the wall, and... are those... video games? It seems like a bit of a mismatch as the rest of the room is very militant.', 3, 'norm')
  pos = ''
  while xy == [-1, 1]:
    narrate('\n\n\nwhat would you like to do?', 2, 'none')
    choose = input('\n\n')
    choice = choose.lower()
    #insert activitys and decitions here
    if 'check' in choice and 'room' in choice:
      pass
    elif 'check' in choice and 'armor' in choice:
      narrate("You go to admire the armor hanging on the wall. You recignise one of the names etched into the armor, Deric. It's too high for you to reach though, and far too big to ware. You wonder what goliaths must have owned them.", 2, 'norm')
      pos = 'armor'
    elif 'check' in choice and 'game' in choice:
      narrate('\nYou used to have a lot of fun with these games, you always played against somone far stonger than you phisicaly. But, things were differint in a game world, there none of that mattered.', 2, 'norm')
      pos = 'games'
    t = travel(choice)
    if pos == 'games' and "take" in choice:
      narrate('You take a controller with you, its all you have left of them.', 2, 'norm')
      inventory += ["game controller"]
    elif pos == 'armor' and "take" in choice:
      narrate("Try as you might to grab the armor you just can't reach. You would jump and grab it, but you could never get it down, some things aren't up for grabs.", 2, 'norm')
  if xy != [-1, 1] and t != guard_room:
    t()

#the folowing code will run when the player changes the room.


      

      
def storage_room():
  os.system("clr" if os.name == "nt" else "clear")
  
  
  global xy
  global t
  global inventory
  narrate('\n\n\nSTORAGE ROOM\nstorage room intro here: You are in a room filled with boxes, it will probably take a few tries to find anything.', 3, 'norm')
  while xy == [-2, 1]:
    narrate('\nwhat would you like to do?', 2, 'norm')
    choose = input('\n\n')
    choice = choose.lower()
    #insert activitys and decitions here
    if 'check' in choice and 'box' in choice:
      chance = random.randint(1, 5)
      print(chance)
      if chance == 1:
        if 'repair tool' in inventory:
          narrate('You search the boxes, but find nothing there.', 2, 'norm')
        else:
          narrate("After searching through many boxes you found a repair tool and add it to your inventory.", 2, 'norm')
          inventory += ["repair tool"]
      else:
        narrate('You search the boxes, but find nothing but junk.', 2, 'norm')
    elif 'explore' in choice:
      narrate('Nothing here but boxes', 2, 'norm')
    t = travel(choice)
  if xy != [-2, 1]  and t != storage_room:
    t()
      
#the folowing code will run when the player changes the room.


      

      

def armory_room():
  os.system("clr" if os.name == "nt" else "clear")
  

  global xy
  global t
  global inventory
  global engine
  if engine != 'fixed':
    narrate("\nUNKNOWN ROOM\nThis room is filled with thick smoke. You can't see anything and leave before you cough your lungs out.\n", 3, 'long')
    xy = [-1, 1]
    guard_room()
  
  narrate("\n\n\nARMORY ROOM\nYou weren't alowed in here often, far too dangerus for somone so small. The rooms two most noticable fetures are its reinforced walls and poor desighn. I mean they put bombs right next to the engine! (Which is still smoking a little.)\n", 2, 'norm')
  while xy == [-1, 0]:
    narrate('\nwhat would you like to do?', 2, 'norm')
    choose = input('\n\n')
    choice = choose.lower()
    if 'check' in choice and 'room' in choice:
      narrate("\nARMORY ROOM\nIt is a room with reinforced walls, one of which is filled with bombs, the other is just a wall of scrap now.\n", 2, 'norm')
    if ('check' in choice or "grab" in choice) and ('wall' in choice or 'weapon' in choice or 'bomb' in choice):
      narrate('You searched the wall of wepons, and grab a bomb.', 2, 'norm')
      inventory += ["bomb"]
    t = travel(choice)
    if t == hibernation_room:
      xy = [-1, 0]
      out_of_bounds()
  if t != armory_room:
    t()
      
#the folowing code will run when the player changes the room.

      

       
def cockpit_room():
  os.system("clr" if os.name == "nt" else "clear")
  
  global xy
  global t
  global inventory
  narrate('\nCOCKPIT\nThis is it, just push the button and head home.', 3, 'norm')
  choice = ''
  while xy == [-1, 3] and ("push" not in choice or "pres" not in choice):
    narrate('\n\n\nwhat would you like to do?', 2, 'norm')
    choose = input('\n\n')
    choice = choose.lower()
    if "push" in choice or "pres" in choice:
      narrate("You pushed the button to head home, and began heading back to your sleep chamber. Then a thought struck you, 'what if the cryochamber doesn't turn back on like the others?'. But it is a risk you have to take, and enter your pod.")
    t = travel(choice)
  if xy != [-1, 0] and t != cockpit_room:
    t()
  os.system("clr" if os.name == "nt" else "clear")
  narrate("The End", 2, 'norm')
#the folowing code will run when the player changes the room.


      

    
      
def lounge_room():

  os.system("clr" if os.name == "nt" else "clear")
  
  
  global xy
  global t
  global inventory
  narrate("\nLOUNGE ROOM\nYou are in a hallway, one you recignise, like the rest of the ship, but this is different. You used to wait in this (bomb proof) and highly reflective glass hallway for your dad quite alot.", 3, 'norm')
  pos = ''
  while xy == [-1, 2]:
    narrate('\n\n\nwhat would you like to do?', 0, 'norm')
    choose = input('\n\n')
    choice = choose.lower()
    if 'place' in choice and 'bomb' in choice:
      if 'bomb' in inventory:
        narrate("You place the bomb down and run in the other direction, before setting it off.", 2, 'norm')
        narrate("\nThe bomb explodes, leaveing a hole just wide enugh to climb through.", 2, 'norm')
        pos = 'opening'
    elif 'check' in choice and 'room' in choice:
      narrate("\nLOUNGE ROOM\nYou are in a (bomb proof) glass hallway hallway that brings back many memories. At one end is the door to the control room, your goal. But first, wouldn't it be better to 'reflect' on your journy? (That is if you have found some of the story)", 3, 'norm')
    elif 'reflect' in choice:
      os.system("clr" if os.name == "nt" else "clear")
      narrate("\nOutside a milion briliant yet kind stars are visible. You stare into your reflection, and for the first time recignise your small frame.", 2, 'norm')
      narrate("\nYou are but a child, how can you ever hope to reach home on your own? This whole journy has been dificult for you, but now staring into the great infinity you are finaly truely frightened.", 2, 'norm')
      narrate("\nYou won't ever see Deric agian, nor your Mother and Father... will you? You huddle up and cry for a moment.", 1, 'long')
      narrate("\nNo.. Mother and Father weren't on this trip, where they?", 1, 'long')
      narrate("\nRight! You only recignized one face among the sleeping.", 2, 'norm')
      narrate("\n(During long distance travel the cockpit is primarily used to plot a course then the whole crew is temporarily frosen for a few days until arival. This is done to protect against 'radeation' or whatever other sifi nonsence I think up, This story is pretty improvised and I dont have any experience with writing stories)", 3, 'short')
    if pos == 'opening':
      if "enter" in choice:
        choice = 'north'
    t = travel(choice) 
  if t != lounge_room:
    t()
      
#the folowing code will run when the player changes the room.


    
#A record of where rooms are located

#6/8

room_locate = {0: hibernation_room, 1: servant_quarters_room, 2: guard_room, 3: storage_room, 4: armory_room, 5: engine_room, 6: lounge_room, 7:cockpit_room}
# had to define variable here because it must be after the rooms are defined.
def start():
  narrate("You awaken in a cold cramped glass cell.", 2, "norm")
  narrate("\nWho are you again? Ahh thats right, amnesia is a common side effect.", 2, "norm")
  narrate("\nThere isnt much you can do.\n", 2, "norm")

  narrate("\nWell!", 1, 'short')
  narrate(" No point in waiting around.\n", 2, 'norm')

  choice = ''
  
  while "check" not in choice:
    narrate("\nTry Exploring! Include the key word 'check' acompanyed by what you want to observe.", 2, 'none')
    choose = input("\n\n")
    choice = choose.lower()

  narrate("\nAfter a closer look you realise you are in a cryochamber ", 2, "none")
  narrate(" for... for.. for ", 1, "none")
  narrate(" hybernation! You hastily push the release button on the side of your chamber.\n", 2, "long")
  hibernation_room()


start()























# author: Jeremy Holley
# CSC119 Spring 2021

#import time		# used to add wait time during printing
#import sys		# used to exit the program
#import os		# used to clear the console
#from termcolor import cprint 	# print in different colors


# The first room
#def room1(inventory):
#	user_pick = None

	# describe the room
#	print("You enter room1.\n")

	# let the user continue to make choices in the room
#	while user_pick != "4":
		# wait for 1.5 seconds
#		time.sleep(1.5)
		
#		print("\nYou are in room1. (describe the room)\n")
#		cprint("Inventory:" + str(inventory), "blue", "on_white")
#		print("\nWhat would you like to do?\n1. Go left\n2. Go right\n3. Look around\n4. Quit\n")

		# allow the user to enter a choice
#		user_pick = input()

		# one of these conditions executes based on what the user chose
#		if user_pick == "1":
			# go left
#			room2(inventory)
#		elif user_pick == "4":
			# quit the game
#			sys.exit()
#		else:
#			cprint("\nThat is not a valid choice. Try again.", "red")


# The library room that has a skeleton key item for solving a puzzle
#def room2(inventory):
#	user_pick = None

	# describe the room
#	print("You enter room2.")

	# let the user continue to make choices in the room
#	while user_pick != "4":
		# wait for 1.5 seconds
#		time.sleep(1.5)

#		print("\nYou are in room2. (describe the room)")
#		cprint("\nInventory: " + str(inventory), "yellow",)
#		print("\nWhat would you like to do?\n1. Go forward\n2. Go back\n3. Look around\n4. Quit\n")

		# wait for the user's choice
#		user_pick = input()

#		if user_pick == "3" and "skeleton key" not in inventory:
#			print("\nYou look around and find a key.\n")
#			cprint("SKELETON KEY ADDED TO INVENTORY\n", "green")
#			inventory.append("skeleton key")
#		elif user_pick == "3" and "skeleton key" in inventory:
#			print()
#			cprint(" YOU FIND NOTHING OF INTEREST ", "grey", "on_white", attrs = ['bold'])




# The main method starts the game by defining variables and calling the first_room function
#def main():

#	inventory = ["shovel"]
#	room1(inventory)



#main()