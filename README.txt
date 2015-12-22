Jack Linden #3704293
CS1571 Artificial Intelligence
12-11-15
Flappy Bird Q Learning Agent

Description: 
	Implementation of unsupervised Q learning algorithm for Flappy Bird. 
	Bird can get 10+ pipes consecutively on average with ~ 4-5 hours of 
	training.


Files:
	- flappybird.py —> game driver module
	- q_learner.py  —> Q array, Agent, State, and Actions classes needed 
			         for Q Learning algorithm
	- Q_arr             —> File containing the serialized Q array

Run:
	- python flappybird.py Q_arr       —> runs with the pre-trained Q array
	- python flappybird.py 	         —> runs with brand new Q array
	
Notes:
	- Pressing pause will save the Q array to the Q_arr file
	- When pressing pause, wait 5-10 seconds for file to write before exiting the program
		- Failure to do so may corrupt the Q_arr file	

Q Learning/Training Implementation:
	
	State Representation
		- I chose to represent my state with five criteria
			- delta x = ( pipeX+pipeWidth - birdX )
			- delta y = ( windowHeight - bottomPipeHeight - birdY )
			- bird is dead = True/False 
			- bird is jumping = True/False
			- pipe window section - (which third of the Y-axis the pipe is in) =  0,1, or 2
				- this value helped the bird most with high and low pipes by preventing him
				  from flying off the top or falling off the bottom
	Actions
		- I had my agent choose an action (i.e. jump or idle) and learn every frame so long as the transition
		  produced a new state
		- If a state had equal Q values for both actions, then I decided to bias the bird towards 
		  jumping if his position was lower than the pipe and to remain idle if he’s above it
			-This helped to prevent a lot of “bad” deaths where the bird would fly off the top
			 or fall off the bottom
		- Otherwise an action was chosen based which action had the higher Q exploration value
			- Max ( Q(s,jump) + 5/N-jump, Q(s,idle) + 5/N-idle ) returns Action associated with the max
		- This function allows for more exploration of infrequent actions in the earlier stages of learning
	Q Array
		- The Q array was represented by an object that encapsulated a python dictionary where the key
		  was a State object and the value was an ActionSet object containing the Q values for each action
		  at that state
		  
	Learning
		- alpha was set to be constant at 0.9 because it appeared to produce the best results		- gamma was set to be constant at 0.8 
		- After a state transition that produces a new state, I updated the Q(s,a) (i.e. the previous state,action)
		 using the following equation
			- Q(s,a) = Q(s,a) + alpha*( reward + max( Q(s’,a’jump, Q(s’,a’idle) ) - Q(s,a) )
			- where Q(s,a) was the previous state and action that lead to:
			- Q(s’,a’) the new state that produces “reward”
		Reward System
			- Action produced state where bird is DEAD
				- If caused by flying off top or falling off bottom
					r = -11000
				- If caused by pipe collision 
					r = - (3000 + Euclidian distance from pipe window ) (see code)
			- Action produced state where bird is ALIVE
				- If bird passed through a pipe
					r = 8000
				- Else
					r = 1 + 15/(Euclidian distance from pipe window)
	Game Speed
		- In order to speed up learning, I managed to increase the game speed by a factor of 10
		 by multiplying various speed constants by 10
		- If you want to run my program at this speed, you must change the variable OVERALL_SPEED
		  to 10 and FPS to 60
		- I found that training my bird in this manner had some ramifications on running the program at
		  normal speed. Because of how the game was implemented, I had to scale the frame rate down
		  by the factor of speed at which I trained him at. Therefore, to run the bird at normal speed, the
		  FPS variable must be set to be 6 (which it is defaulted to in the program)
		- While this makes the game look choppy, it shouldn’t really matter because his ability to get 20+ pipes
		  demonstrates that the learning algorithm was successful. 
		 
	
Resources used:
	- http://sarvagyavaish.github.io/FlappyBirdRL/
	- http://pygame.org/hifi.html
	- Artificial Intelligence: A Modern Approach, Russel and Norvig
	- Discussed state representations with Ethan Welsh, Justin Rushin, Shelley Goldberg, and Chris Boehm

		
		
	

	


	
	
	
	