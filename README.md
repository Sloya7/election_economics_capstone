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


importance features:
tested and found that not surprisingly, the finacial information was the most influencial of if the year was a "gain'. removing those columns the imporance went to an array of zeros. 
while this is an answer, I wanted to dive deeper into if the specific year leading up to, during or following an election had a pattern to if the year was a gain. created a loop sorting data into the election cycles