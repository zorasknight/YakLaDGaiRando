# YakLaDGaiRando
First implementation for a LaD Gaiden Randomizer


Randomization is achieved through adjusting values in the aston.db section, among others, of the games data prior to run time. The python script modifies the loose files contained within the mod folders before running the shinryu modloader to compact them back into pars and package them as a proper mod that can be ran through the shinryu modloader. A new file is made on startup with any difficulty the player chooses, the completion goal is set by the player.

Skills are sepperated and locked behind unique items in this run, collecting the new "Skill Books" throughout the world allows the ability to purchase that skill.

Current Items in the pool for randomization:
94 Pocket Circuit Parts from the Pocket Circuit part exchange
14 Pocket Circuit Parts from Pocket Circuit Rivals
18 items from the Sotenbori Ebisu Pawn shop
26 items from the Akame Network point shop
11 items from the Billiards point shop
13 items from the Golf point shop
11 items from the Collisuem Gambler Hall point shop
15 items from the Collisuem Casino point shop
15 items from the Collisuem Boutique shop
11 items from the Collisuem VIP Boutique shop
5 items from the Mizorogi Armor shop
121 items from Wire Grabs
119 Skill Books
50 items from the Sotenbori Coin Lockers


Planned locations:
Coin Locker Keys
Cosmetic Shops
Other minigame point stores
Completion List
Substories
Akane Tasks
Colliseum
restricting part time jobs based on item aquisition ie: battle pass, photo pass, item gift pass, rival fight 1-16 etc.

Goals:
Collecting 7 golden balls and finishing the substory for Shen
Beating X Pocket Circuit Rivals
Completing X Substories
Reach X Akane Rank

The goal set will unlock the win conditions below:
Defeat Shin Amon in the final substory
Defeat Robot Amon in the colliseum
Defeat the Final Golden Samurai for Akame
Defeat the Courstar owner in pocket circuit
Finish the Finale Act

Logic is used to avoid hiding items behind themself, for example the A1 key cannot be stored within the A1 locker, likewise the Colliseum unlocks (colored tigers) cannot be hidden behind a later colliseum. This game is light on logic at the moment, but if we can get proper hooks we would like to randomize progression for substory unlocks.

Currently this is built as a local only proof of concept as until we have a way to hook in to the game, linking this to archipelago will be impossible.
