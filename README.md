# Flight-Deconfliction with Monte Carlo Tree Search

**Liza Mozolyuk, Talia Novack, Rhys Chambers**

**Software and Hardware Requirements**

- **Imports needed:**  
  - Numpy  
  - Python 3.10.7 or higher  

**Links to Any Data Sources**

- Created our own data as seen in DummyData.py.  

**Motivation for Your Project**

All three of us have to fly to get to school every semester, and because of this have experienced the lovely delays that occur at Reagan National Airport (DCA). We wanted to model the deconfliction of multiple airplanes taking off or landing around the same time in order to make our flight travels more efficient. By designing a schedule for these flights, we will be able to help airports and airplanes work efficiently.  

As it stands, air traffic controllers still decide with their brains what plane gets to land. We want to simulate this to alleviate the pressures that lay on these poor workers’ shoulders.  

**Explanation of What You Accomplished**

We were able to model the decisions that the air traffic controllers make using a Monte Carlo Tree Search.  

At a given time step, there is always a single action taken.  

- The action in our model is the choice of which plane to land.  
- The action in our model is the landing of the plane with the most optimal fuel and distance to airport levels per time step.  

By using a transition function, we then iterated to our next state based on the previous action (which plane landed).  

**How You Measured Your Success (or Failure)**

- Run the command `python MCTSV2.py`.  
- The output measures the success of our algorithm.  
- We could then measure success by printing out the fuel and distance levels of the plane landed at each time step and making sure they were trending in the correct direction. (The correct direction being lower fuel levels and lower distances).
