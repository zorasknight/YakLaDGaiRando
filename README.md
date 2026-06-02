# YakLaDGaiRando
First implementation for a LaD Gaiden Randomizer


Randomization is achieved through adjusting values in the aston.db section, among others, of the games data prior to run time. The python script modifies the loose files contained within the mod folders before running the shinryu modloader to compact them back into pars and package them as a proper mod that can be ran through the shinryu modloader. Currently a save is provided that is modified to work with the rando. In the future a new save could work the same.

Current Items in the pool for randomization:
94 Pocket Circuit Parts from the Pocket Circuit part exchange
5 unique items from the Sotenbori Ebisu Pawn shop
50 items from the Sotenbori Coin Lockers


Planned locations:
Akane Point Shop
Items found by Wire
Coin Locker Keys
Cosmetic Shops
Billiard point store
Other minigame point stores
Completion List
Substories
Akane Tasks
Colliseum

Goals:
Collecting 7 golden balls and finishing the substory for Shen
Beating X Pocket Circuit Rivals
Completing X Substories
Reach X Akane Rank

The goal set will unlock the win conditions below:
Defeat Shin Amon in the final substory
Defeat Robot Amon in the colliseum
Defeat the Courstar owner in pocket circuit
Finish the Finale Act

Logic is used to avoid hiding items behind themself, for example the A1 key cannot be stored within the A1 locker, likewise the Colliseum unlocks (colored tigers) cannot be hidden behind a later colliseum. This game is light on logic at the moment, but if we can get proper hooks we would like to randomize progression for substory unlocks.

Currently this is built as a local only proof of concept as until we have a way to hook in to the game, linking this to archipelago will be impossible.
