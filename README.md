# election_economics_capstone
Jupyter Notebook Project Analyzing Economics around election years




create ml process

uses a binarizer to make the 1 and 0 columns
seperates out the gold, silver and market data so each can be evaluated independently
removes the asset name since the gold and silver are in thier own df and we don't care about the specific EFT.
uses the target column of 'ElectCycle' since we want the results to be paired with the cycle
