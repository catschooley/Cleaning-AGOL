# Cleaning-AGOL

This is a simple code that runs through AGOL and checks to see if layers owned by a certain user is being used in any web maps. A csv is created with the name and url for each unused layer. This code can be modified to search through a specific amount of each feature service and search through a specific amount of web maps (default is set to 10,000 for both). 

The code is currently written to require a lot of user input. This is an attempt to keep it generic, but also so it can easily be used by those hesitant to editing\writing code. There is also a print function written to show each service that is being searched for that layer. This is unnecessary but can be helpful to those unfamiliar to trust that the code is working. 
