# election_economics_capstone
Jupyter Notebook Project Analyzing Economics around election years

cleaning



create ml process

uses a binarizer to make the 1 and 0 columns
seperates out the gold, silver and market data so each can be evaluated independently
removes the asset name since the gold and silver are in thier own df and we don't care about the specific EFT.
uses the target column of 'ElectCycle' since we want the results to be paired with the cycle






reinteration of concept:
made the model and got feature importance including the open/close data. found that open and change were in the higher ranks of importance.
This intuitively makes sense and bring some other questions up for exploration however, to answer the original question, I decided to remove 
the open, close, loss, change data. all that data instead, serves to get to the data point of "was it a gainful year?"



feature importance:
high degree of coorelation- reduced number of variables