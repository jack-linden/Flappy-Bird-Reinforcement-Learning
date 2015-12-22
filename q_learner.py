#Jack Linden #3704293
#Q Learning Code


import os
import math
from random import randint,random
class ActionSet:
	#Enum values
    NOTHING = 0
    JUMP = 1

    def __init__(self):
        self.Q_JUMP = 1
        self.j_cnt = 0
        self.Q_NOTHING = 1
        self.n_cnt = 0
    
    #Returns the maximum reward associated with this state
    def max_reward(self):
        jump_r = self.Q_JUMP + 5.0/(self.j_cnt+1)
        noth_r = self.Q_NOTHING + 5.0/(self.n_cnt+1)
        return max(jump_r,noth_r)
    
    #Choose an action
    def choose_action(self,dx,dy):
        action = 0
        #If equal, jump if lower than pipe, else nothing
        if (self.Q_JUMP +5.0/(self.j_cnt+1)) == (self.Q_NOTHING +5.0/(self.n_cnt+1)):
            if dx > 30 and dy < -10:
                action = ActionSet.JUMP
            else:
                action = ActionSet.NOTHING
        elif self.Q_JUMP +5.0/(self.j_cnt+1) > self.Q_NOTHING +5.0/(self.n_cnt+1):
            action = ActionSet.JUMP
        else:
            action = ActionSet.NOTHING          
        
        return action
    def __str__(self):
        s = "Q Jump - " + str(self.Q_JUMP) + "\n" + "Q nothing - " + str(self.Q_NOTHING)
        return s
    #Return reward associated with specified action
    def get_reward(self,action):
        if action == ActionSet.JUMP:
            return self.Q_JUMP
        return self.Q_NOTHING
    
    #Update the Q value for the specified action and update counts 
    def update_reward(self,action,value):
        if action == ActionSet.JUMP:
            self.Q_JUMP = value
        else:
            self.Q_NOTHING = value
        if action == ActionSet.JUMP:
            self.j_cnt += 1
        else:
            self.n_cnt += 1  
   	
   	#.9 works pretty well
    def get_alpha(self):
        return .9
                
    
class Agent:
    
    def __init__(self):
        self.Q = Q_Array()   
             
     #Return an action
    def decide(self,state,bird):
        if not self.Q.contains(state):
            self.Q.add(state)
        actions = self.Q.get(state) 
        action = actions.choose_action(state.delt_x,state.delt_y)
        
        return action
    #Determine the immediate reward for the state transition
    def immediate_reward(self,new_state,action,pipe_cleared,pipe_collision):
        dist = math.sqrt(new_state.delt_x**2 + new_state.delt_y**2)
        
        #If bird died
        if new_state.dead:
            self.Q.get(new_state).update_reward(0,-1000)
            self.Q.get(new_state).update_reward(1,-1000)
            r = -(1000 + dist)#Base punishment
            if pipe_collision: #If collided with a pipe, slightly punish more
                  r -= 2000
            else:			   #If bird fell off map, punish heavily
                  r -= 10000;
            print("Died, punishing " + str(r))
            return r
        #Bird is alive
        else:
            r = 1.0
            r += 15.0/dist
            if pipe_cleared : #Reward for making it through a pipe
                r += 8000
            return r
  
  	#Calculates Q(s,a) = Q_old + alpha*(reward + Q_new_max - Q_old)
    def learn(self,old_state,new_state,action,pipe_cleared,pipe_collision):
        old_Q_actions = self.Q.get(old_state)
        if not self.Q.contains(new_state):
            self.Q.add(new_state)
        new_Q_actions = self.Q.get(new_state)
        r = self.immediate_reward(new_state,action, pipe_cleared,pipe_collision)
        alpha = old_Q_actions.get_alpha() #Alpha
        Q_old = old_Q_actions.get_reward(action) # old Q(s,a)
        Q_new_max = new_Q_actions.max_reward() # max Q sample
       	#Gamma constant at .8
        Q_old = Q_old + alpha*(r + .8*Q_new_max - Q_old )
        #update Q(s,a)
        old_Q_actions.update_reward(action, Q_old)

#Stores State,Action pairs
class Q_Array:
        
    def __init__(self):
        self.history = {}
    
    #Adds new state with new ActionSet 
    def add(self,state):
        if state not in self.history:
            self.history[state] = ActionSet()
    #Returns Actions associated with specified state
    def get(self,state):
        return self.history[state]
    
    #Checks if state is contained in Q array
    def contains(self,state):
        return state in self.history

#Helper function
def myround(x, base=3):
    return int(base * round(float(x)/base))

#State representation
	# delt_x - difference of right side of pipe to the bird's x position 
	# delt_y - difference of pipe window height to bird y position
	# dead - whether or not the bird is dead
	# is_jumping - whether or not the bird is rising or falling
	# py - what third of the Y axis the pipe is in (0th, 1st, 2nd)
class State:
    
    def __init__(self, delt_x, delt_y,dead, is_jumping,py):
        self.delt_x = int(myround(delt_x))
        self.delt_y = int(myround(delt_y))
        self.dead = dead
        self.is_jumping = is_jumping
        if py < 512/3:
            self.py = 0
        elif py < 512/2:
            self.py = 1
        elif py < 512:
            self.py = 2      
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        
        return self.py == other.py and self.is_jumping == other.is_jumping and self.dead == other.dead and self.delt_x == other.delt_x and self.delt_y == other.delt_y
    
    def __hash__(self):
        return hash((self.delt_x,self.delt_y,self.dead, self.is_jumping,self.py))
    
    def __str__(self):
        return str((self.delt_x,self.delt_y,self.dead, self.is_jumping,self.py))