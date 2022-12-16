import pandas as pd
import numpy as np
import json

dataset_profiles = pd.read_json(path_or_buf = "profiles.json") # read in dataset that contains player names and player ids for the dataset of game data

# remove all the unecessary columns in the profiles dataset that we will not use
dataset_profiles_simplified = dataset_profiles.drop(labels = ["height", "weight", "current_team", "birth_date", "birth_place", "death_date", "college", "high_school", "draft_team", "draft_round", "draft_position", "draft_year", "current_salary", "hof_induction_year"], axis = 1, inplace = False)

dataset_combine = pd.read_csv("combine.csv") # read in dataset with all the combine data for the players
player_game_stats = pd.read_csv("games_data.csv") # read in the dataset with all the individual game info for the players


# relate the ids between the two datasets...The combine and game data set describe the same players with different ids
# ids are easier to associate with than names, so we are looping through the names and determining the id in each dataset for a single player
# and then combining that info
new_player_ids = []
for index, row in dataset_profiles_simplified.iterrows(): # loop through rows of profiles dataset
	name = row["name"]
	right_row = dataset_combine[dataset_combine["nameFull"] == name] # find all rows that match the given name
	if right_row.empty: # if there is no name match, make a not this player does not exist in the combine dataset
		new_player_ids.append(-1)
	else:
		if right_row.shape[0] > 1: # if there is more than one match (multiple players with same name), try to find the right match by comparing colleges they went to
			college = (dataset_profiles["college"])[index] # below is doing some cleaning on college names because they are not the same format in each dataset
			if college.endswith("St."):
				college = college.replace("St.", "State")
			if college.endswith("Col."):
				college = college.replace(" Col.", "")
			if college.endswith(";"):
				college = college.replace(";", "")
			value_set = False
			for index, row in right_row.iterrows(): # loop through the rows that matched and compare colleges
				even_righter_row = right_row[right_row["college"] == college]
				if even_righter_row.empty: # if not match for college
					pass
				elif even_righter_row.shape[0] > 1: # if multiple matches for college (this case was no encountered except for when the same player was duplicated in the dataset)
					new_player_ids.append((even_righter_row["playerId"]).iloc[0])
					value_set = True
					break
				else: # if found match
					new_player_ids.append(even_righter_row["playerId"].item())
					value_set = True
					break
			if not value_set: # if unable to find match
				new_player_ids.append(-1)
		else: # add the id if a single match
			new_player_ids.append(right_row["playerId"].item())

dataset_profiles_simplified["combine_player_ids"] = new_player_ids # set the ids for combine players as these new player ids

arr = np.array(new_player_ids)
indices = np.where(arr == -1)
not_present = indices[0].tolist()# eliminate any rows with players that don't exist in both dataset
dataset_profiles_simplified.drop(labels = not_present, axis = 0, inplace = True) # drop these rows from the dataset


# add the cumulative and average player career data (average per game) to the dataset
total_players = len(dataset_profiles_simplified.index)
col_names = ["passing_attempts", "passing_completions", "passing_yards", "passing_rating", "passing_touchdowns", "passing_interceptions", "passing_sacks", "passing_sacks_yards_lost", "rushing_attempts", 
             "rushing_yards", "rushing_touchdowns", "receiving targets", "receiving_receptions", "receiving_yards", "receiving_touchdowns", "kick_return_attempts", "kick_return_yards", "kick_return_touchdowns", "punt_return_attempts",
             "punt_return_yards", "punt_return_touchdowns", "defense_sacks", "defense_tackles", "defense_tackle_assists", "defense_interceptions", "defense_interception_yards", "defense_interception_touchdowns",
             "defense_safeties", "point_after_attempts", "point_after_makes", "field_goal_attempts", "field_goal_makes", "punting_attempts", "punting_yards", "punting_blocked"]

# add the columns as empty columns to the dataset
dataset_profiles_simplified["season_played"] = [0] * total_players
for col in col_names:
	dataset_profiles_simplified[col] = [0] * total_players
for col in col_names:
	average_col_name = col + "_average"
	dataset_profiles_simplified[average_col_name] = [0] * total_players

index = 0 # loop through every row
for _, row in dataset_profiles_simplified.iterrows():
	player_id = row["player_id"]
	player_games_rows = player_game_stats[player_game_stats["player_id"] == player_id] # find all individual games where the player id info matches the player under investigation
	if not player_games_rows.empty: # if games found
		games_played = len(player_games_rows.index)
		games_played_years = player_games_rows["year"]
		years_played = max(games_played_years) - min(games_played_years) + 1 # determine years played from earliest and latest single game data
		dataset_profiles_simplified.iloc[index, 4] = years_played # set the years played at that row
		player_cumulative_stats = player_games_rows.sum(axis = 0) # determine the cumulative career stats
		player_average_stats = player_cumulative_stats[12:47]/games_played # find the per game average of the cumulative game stats
		for number in range(5, 40): # for each of the cumulative career stats, place them in their appropriate column in the dataset (The + and - terms are to make sure the right columns are referenced in both lists)
			dataset_profiles_simplified.iloc[index, number] = player_cumulative_stats.iloc[number + 7]
			dataset_profiles_simplified.iloc[index, number + 35] = player_average_stats.iloc[number - 5]
	index = index + 1


# get the combine data for this dataset
heights = []
weights = [] 
hands = []
age = []
arm = []
fortyyddash = []
vertical = []
bench = []
shuttle = []
broad = []
threeseccone = []
sixtysecshuttle = []
wonderlic = [] 

for index, row in dataset_profiles_simplified.iterrows(): # loop through the rows for each player, and set the combine data for each player from the combine dataset
	player_id = row["combine_player_ids"]
	player_id = int(player_id)
	player_combine_row = dataset_combine[dataset_combine["playerId"] == player_id]
	if not player_combine_row.empty:
		heights.append(player_combine_row.iloc[0, 4])
		weights.append(player_combine_row.iloc[0, 5]) 
		hands.append(player_combine_row.iloc[0, 6])
		age.append(player_combine_row.iloc[0, 17])
		arm.append(player_combine_row.iloc[0, 26])
		fortyyddash.append(player_combine_row.iloc[0, 27])
		vertical.append(player_combine_row.iloc[0, 28])
		bench.append(player_combine_row.iloc[0, 29])
		shuttle.append(player_combine_row.iloc[0, 30])
		broad.append(player_combine_row.iloc[0, 31])
		threeseccone.append(player_combine_row.iloc[0, 32])
		sixtysecshuttle.append(player_combine_row.iloc[0, 33])
		wonderlic.append(player_combine_row.iloc[0, 34])

# after collecting a list of all the combine info in order per player, add these lists to the dataset under the respective columns
dataset_profiles_simplified["heights"] = heights
dataset_profiles_simplified["weights"] = weights
dataset_profiles_simplified["hands"] = hands
dataset_profiles_simplified["age"] = age
dataset_profiles_simplified["arm"] = arm
dataset_profiles_simplified["40_dash"] = fortyyddash
dataset_profiles_simplified["vertical"] = vertical
dataset_profiles_simplified["bench"] = bench
dataset_profiles_simplified["shuttle"] = shuttle
dataset_profiles_simplified["broad"] = broad
dataset_profiles_simplified["3_cone"] = threeseccone
dataset_profiles_simplified["60_shuttle"] = sixtysecshuttle
dataset_profiles_simplified["wonderlic"] = wonderlic


# fill in empty values
# not all players have all their combine stats, so in order to fill in the gaps and remove nans, we found the position average for that combine data, and placed that as their values
visited_positions = {} # track all positions that have been visited

index = 0
for _, row in dataset_profiles_simplified.iterrows():
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
	if not position in list(visited_positions.keys()):# if the position has not had an average value for each combine data determined yet
		position_rows = dataset_profiles_simplified[dataset_profiles_simplified["position"] == position] # find all the rows of players with the given position
		row_averages = position_rows.mean(axis = 0) # .mean() ignores the nan values
		visited_positions[position] = row_averages # find their average and set as their value
	row_vals = visited_positions[position]
	for col in range(74, 87): # if a column in nan in the row, set that value with the position average
		if pd.isna(dataset_profiles_simplified.iloc[index, col]):
			dataset_profiles_simplified.iloc[index, col] = row_vals[col-2]
	index = index + 1


# go through and add the year players were drafted to the dataset
dataset_profiles_simplified["draft_year"] = [0] * total_players

index = 0
for _, row in dataset_profiles_simplified.iterrows(): # loop through rows
	player_id = row["combine_player_ids"]
	right_row = dataset_combine[dataset_combine["playerId"] == player_id]
	draft_year = right_row["combineYear"]
	draft_year = draft_year.values # get the players draft year from their id in the combine dataset
	if len(draft_year) > 1: # this happened in one case where someone's combine year was [2016 2016], so this line accounts for this edge case
		draft_year = draft_year[0]
	dataset_profiles_simplified.iloc[index, 88] = draft_year # set the players draft year
	index = index + 1

dataset_profiles_simplified.to_csv("Player_Data_Final.csv") # print out the data to a csv