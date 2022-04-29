import pandas as pd
import numpy as np

# Import whole list, clean it, and sort by number held
whole_list = pd.read_csv("snapshot.csv")
whole_list.rename(columns={'address': 'wallet'}, inplace=True)
whole_list['wallet'] = whole_list['wallet'].str.lower()
whole_list.dropna(axis=0, how='all', inplace=True)
whole_list.sort_values(by=['num_held'], inplace=True, ascending=False)

# First 30 addresses are whales
whale_list = whole_list.head(31)
# print(whale_list)
# whale_list.to_csv("whale_list.csv", encoding='utf-8', index=False)

# Remove whales from the rest of the pool
whales_removed_list = pd.concat(
    [whole_list, whale_list, whale_list]).drop_duplicates(keep=False)

# Give one entry for each MEV owned
l = []
for index, row in whales_removed_list.iterrows():
    l.extend([row['wallet'] for i in range(row['num_held'])])

general_draw = pd.DataFrame(l, columns=['wallet'])

# print(general_draw)
# general_draw.to_csv("general_draw.csv", encoding='utf-8', index=False)


# Read and clean quest 1 list
q1_list = pd.read_csv("../addresses_csv/q1_subs.csv")
q1_list['wallet'] = q1_list['wallet'].str.lower()
q1_list.drop_duplicates(subset="wallet",
                        inplace=True)
# Read and clean quest 2 list
q2_list = pd.read_csv("../addresses_csv/q2_subs.csv")
q2_list['wallet'] = q2_list['wallet'].str.lower()
q2_list.drop_duplicates(subset="wallet",
                        inplace=True)
# Concatinate all entries together
frames = [q1_list, q2_list]
quest_list = pd.concat(frames)
# print(quest_list)

# Remove the whales from the quest list
quests_whales_removed = quest_list[~quest_list["wallet"].isin(
    whale_list["wallet"])]

print(quests_whales_removed)

# Commented out: Remove non-holdrs from quest pool
# quest_list.drop_duplicates(subset="wallet",
#                            inplace=True)
# print(quest_list)
# print(quest_list[quest_list["wallet"].isin(whole_list["wallet"])])
