import pandas as pd
import numpy as np

import json

dataset_profiles = pd.read_json(path_or_buf = "profiles.json")
dataset_profiles_simplified = dataset_profiles.drop(labels = ["height", "weight", "current_team", "birth_date", "birth_place", "death_date", "high_school", "draft_team", "draft_round", "draft_position", "draft_year", "current_salary", "hof_induction_year"], axis = 1, inplace = False)

dataset_combine = pd.read_csv("combine.csv")
player_game_stats = pd.read_csv("games_data.csv")

new_player_ids = []
for index, row in dataset_profiles_simplified.iterrows():
	name = row["name"]
	right_row = dataset_combine[dataset_combine["nameFull"] == name]
	if right_row.empty:
		new_player_ids.append(-1)
	else:
		if right_row.shape[0] > 1:
			college = (dataset_profiles["college"])[index]
			if college.endswith("St."):
				college = college.replace("St.", "State")
			if college.endswith("Col."):
				college = college.replace(" Col.", "")
			if college.endswith(";"):
				college = college.replace(";", "")
			value_set = False
			for index, row in right_row.iterrows():
				even_righter_row = right_row[right_row["college"] == college]
				if even_righter_row.empty:
					pass
				elif even_righter_row.shape[0] > 1:
					new_player_ids.append((even_righter_row["playerId"]).iloc[0])
					value_set = True
					break
				else:
					new_player_ids.append(even_righter_row["playerId"].item())
					value_set = True
					break
			if not value_set:
				new_player_ids.append(-1)
		else:
			new_player_ids.append(right_row["playerId"].item())

dataset_profiles_simplified["combine_player_ids"] = new_player_ids

arr = np.array(new_player_ids)
indices = np.where(arr == -1)
not_present = indices[0].tolist()
dataset_profiles_simplified.drop(labels = not_present, axis = 0, inplace = True)

total_players = len(dataset_profiles_simplified.index)
col_names = ["passing_attempts", "passing_completions", "passing_yards", "passing_rating", "passing_touchdowns", "passing_interceptions", "passing_sacks", "passing_sacks_yards_lost", "rushing_attempts", 
             "rushing_yards", "rushing_touchdowns", "receiving targets", "receiving_receptions", "receiving_yards", "receiving_touchdowns", "kick_return_attempts", "kick_return_yards", "kick_return_touchdowns", "punt_return_attempts",
             "punt_return_yards", "punt_return_touchdowns", "defense_sacks", "defense_tackles", "defense_tackle_assists", "defense_interceptions", "defense_interception_yards", "defense_interception_touchdowns",
             "defense_safeties", "point_after_attempts", "point_after_makes", "field_goal_attempts", "field_goal_makes", "punting_attempts", "punting_yards", "punting_blocked"]

dataset_profiles_simplified["season_played"] = [0] * total_players
for col in col_names:
	dataset_profiles_simplified[col] = [0] * total_players
for col in col_names:
	average_col_name = col + "_average"
	dataset_profiles_simplified[average_col_name] = [0] * total_players

dataset_profiles_simplified.to_csv("Temp_Data_Set.csv")

index = 0
for _, row in dataset_profiles_simplified.iterrows():
	player_id = row["player_id"]
	player_games_rows = player_game_stats[player_game_stats["player_id"] == player_id]
	if not player_games_rows.empty:
		games_played = len(player_games_rows.index)
		games_played_years = player_games_rows["year"]
		years_played = max(games_played_years) - min(games_played_years) + 1
		dataset_profiles_simplified.iloc[index, 5] = years_played
		player_cumulative_stats = player_games_rows.sum(axis = 0)
		player_average_stats = player_cumulative_stats[12:47]/games_played
		for number in range(6, 41):
			dataset_profiles_simplified.iloc[index, number] = player_cumulative_stats.iloc[number + 6]
			dataset_profiles_simplified.iloc[index, number + 35] = player_average_stats.iloc[number - 6]
	index = index + 1

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

for index, row in dataset_profiles_simplified.iterrows():
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

dataset_profiles_simplified.to_csv("PlayerDataset_2.csv")