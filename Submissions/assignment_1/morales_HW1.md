# David Morales, 1/24/2022, HW1

## Challenge Responses:
1. I repeated the process for both a homogenous and heterogenous system although I only submitted a model for the heterogenous system; it was unclear if I needed to submit two separate sheets demonstrating each system.
2. Beneath the *Direct Solution for Flux* box, I added my own calculations for **q** and **Keq** using the corresponding values obtained from the direct calculations above; I believe that's what was meant by the directions to "show that the steady state flux agrees with the direct calculation based on the harmonic mean average K."

    As for the equation for flux, it is: q = Keq(dH/dL)

3. In the graph below, three different K-values are expressed in the column:
   - Node 1-5: K = 0.005
   - Node 6-9: K = 0.0004
   - Node 10-13: K = 0.01
  
   ![picture 1](../../images/60a3a035768a8802e06694ef8af97cb77c35d578e118dafc1ab6075750b86502.png)  

4. Looking at the head profile, we see two steep portions bookending a long, shallow middle (the quality of the slope is relative to your perspective). These two end portions represent the layers of the column with relatively high K-values compared to the "lower" of the K-values. In fact, very little head is lost as water travels through the ends of the column as indicated by their steepness. Thus, in order account for the set Type 1 boundary conditions, the equivalent K-value must reflect the "difficulty" which water experiences as it travels through the column.

## Discussion Responses:
1. What are boundary conditions?  Answer this both conceptually and mathematically.
   
   Boundary conditions are set values that limit the model to operate within certain states. Whether they relate to the specified head (type 1) or specified flux (type 2), they determine the response of the model to the set parameters.
   In this model, we use a specified head (100 top, 0 bottom) that requires the model to respond to the parameters by acquiring a flux through the cells that satisfies the boundary conditions.

2. What are model parameters?  How do they (and don't they) represent the actual subsurface?

    Model parameters are inputs that characterize the conditions of the model in order to generate a representative simulation of the physical system. They represent the subsurface through such qualities as hydraulic conductivity, layer thickness, porosity, recharge, etc. A challenge of parameter selection is understanding which parameters are relevant to the system and which are not.

3. What are steady state conditions and how can they be identified from the Excel model results?
   
    Steady state conditions names a system that experiences no change in storage or energy with time anywhere in the domain. In our initial model, steady state can be identified by the constant value of flux for every node along the column of water.

4. Can you imagine how the model inputs could be stored in separate files rather than other spreadsheet cells?  Describe the flow of information from a file that describes the other files that contain model-specific information about the system.
   
   A separate-file model could have one file that contains the parameter values and another file would contain the equations that represent the physical system. This second file would reference the parameter file for the parameter values necessary to simulate the system. In this manner, outputs are easily modified without needing to change anything in the equations.

5. What is an iterative solution?  Can you explain it to a hydrologist who is not a modeler?  Can you describe (or imagine) how Excel finds the solution?
   
   An iterative solutions starts with an initial value and calculates successive iterations of the problem until it converges to a limit of the solution. Excel probably references other cells whose value changes after each iteration. If a certain cell breaks down, every cell connected to that cell via a reference also breaks down. 

6. What is a direct solution?  What are its (dis)advantages compared to an iterative (numerical) solution?
   
   Direct solutions have finite steps depending on the amount of inputs needed to calculate the answer. Once the inputs are entered, there is only one value that it can calculate; new values will not appear in the calculation. Its disadvantage is that it cannot be used in non-linear systems where the states of two or more conditions are mutually dependent.