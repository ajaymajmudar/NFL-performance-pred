import pandas as pd
import numpy as np
import json


player_stats = pd.read_csv("../merge_with_average.csv") # read in dataset with all the combine data for the players

# fill in empty values
# not all players have all their combine stats, so in order to fill in the gaps and remove nans, we found the position average for that combine data, and placed that as their values
visited_positions = {} # track all positions that have been visited

index = 0
for _, row in player_stats.iterrows():
	position = row["position"]
	# below is some cleaning to consolidate position data...Some positions were labeled more exactly than others, so we wanted to find averages of the larger dataset of people for
	# a player with a more exactly named position...An ILB is still a LB, but there are way more labeled LB than ILB in the dataset, so we used that average
	if position.startswith("E-"):
		position = position[2:]
	if position.startswith("QB"):
		position = "QB"
	if position == "ILB" or position == "OLB" or position.startswith("LB"):
		position = "LB"
	if position == "CB" or position == "SS" or position == "FS" or position == "S" or position.startswith("WB") or position.startswith("DB"):
		position = "DB"
	if position == "OT" or position == "OL" or position.startswith("T"):
		position = "T"
	if position == "OG" or position.startswith("G"):
		position = "G"
	if position.startswith("C"):
		position = "C"
	if position.startswith("HB") or position.startswith("RB"):
		position = "RB"
	if position.startswith("WR") or position.startswith("PR"):
		position = "WR"
	if position.startswith("TE") or position.startswith("TB") or position.startswith("LS"):
		position = "TE"
	if position.startswith("FB"):
		position = "FB"
	if position == "DL" or position.startswith("DE") or position.startswith("DT") or position.startswith("NT") or position.startswith("BB") or position.startswith("B") or position.startswith("E"):
		position = "DE"
	player_stats.iloc[index, 5] = position;
	index = index + 1

player_stats.to_csv("merge_with_average.csv") # print out the data to a csv