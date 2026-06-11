# Like a Dragon Gaiden: The Man Who Erased His Name Randomizer
First implementation for a Like A Dragon Gaiden Item Randomizer

## Required Tools

Shin Ryu Mod Manager:
https://www.nexusmods.com/site/mods/743?tab=description

Like a Dragon Gaiden: The Man Who Erased His Name
I use the Steam version, and that's the only officially supported version, your mileage may vary!

## Instructions:

Unzip the folder to wherever you like (desktop with all your other folders....).

Run the Gaiden_Randomizer.exe from within that folder

You should get an output file, zipped, with a name like: "Gaiden_Rando_061026", this is your mod file, you can drag and drop this into your "Shinryu Mod Manager" window like any other mod

Start the game, make a new save at your desired difficulty and enjoy!

## FAQ/Tips

### How can I tell if the Randomizer worked?

You can tell the rando is working by checking the abilities screen when the game allows you. (the game allows you to upgrade Kiryu's abilities after the first fight on the dock in the intro) You should see each ability dragged out and locked, rather than seeing 4 HP upgrades available. If all your stuff is locked, that's a good sign! The real rando begins in chapter 2, so hold out until then, cutscene skip is your friend!

### An item disappeared before I could grab it!

Don't worry! Gaiden has a few "Missable" items, these items are guaranteed to only contain "Junk" quality items like stamina XX or Paper Plate. Still worth grabbing them if you can as they can have plates of all qualities or armor items, but it will never be something unique like a pocket circuit part.

### I'm in town, but getting the Akame level to 3/10 is taking forever!

That's intentional! Prioritize finding your "Key" items, it's the ones needed by the people of Sotenbori that you would normally grapple early on, to get to rank 3 you will need 2 of them, to get to rank 10 is another 4 required.

### I can't find any progression items, where are they?

Progression items can be hard to find, but there are 4 guaranteed items in the early game that you can get before rank 3 (the remaining 4 are all in the later parts of the game like pocket circuit or the colliseum) Make sure to check all the minigames like pool, golf, the casino, or shogi!

### I hate shogi, why is it on?

Settings will come soon! right now everything is on by default...

### Where's Mahjong?

Don't make me add Mahjong.

## implementation

Randomization is achieved through adjusting values in the aston.db section, among others, of the games data prior to run time. The python script modifies the loose files contained within the mod folders before running the shinryu modloader to compact them back into pars and package them as a proper mod that can be run through the shinryu modloader. A new file is made on startup with any difficulty the player chooses, the completion goal is set by the player.

Skills are separated and locked behind unique items in this run, collecting the new "Skill Books" throughout the world allows the ability to purchase that skill.

### Current Items in the pool for randomization:
94 Pocket Circuit Parts from the Pocket Circuit part exchange
14 Pocket Circuit Parts from Pocket Circuit Rivals
18 items from the Sotenbori Ebisu Pawn shop
26 items from the Akame Network point shop
11 items from the Billiards point shop
13 items from the Golf point shop
11 items from the Coliseum Gambler Hall point shop
15 items from the Coliseum Casino point shop
15 items from the Coliseum Boutique shop
11 items from the Coliseum VIP Boutique shop
5 items from the Mizorogi Armor shop
121 items from Wire Grabs
119 Skill Books
50 items from the Sotenbori Coin Lockers


### Planned locations:
Coin Locker Keys
Cosmetic Shops
Other minigame point stores
Completion List
Substories
Akane Tasks
Coliseum
restricting part time jobs based on item acquisition ie: battle pass, photo pass, item gift pass, rival fight 1-16 etc.

### Goals:
Collecting 7 golden balls and finishing the substory for Shen
Beating X Pocket Circuit Rivals
Completing X Substories
Reach X Akane Rank

### Win Conditions:
Defeat Shin Amon in the final substory
Defeat Robot Amon in the Coliseum
Defeat the Final Golden Samurai for Akame
Defeat the Courstar owner in pocket circuit
Finish the Finale Act

Logic is used to avoid hiding items behind themself, for example the A1 key cannot be stored within the A1 locker, likewise the Coliseum unlocks (colored tigers) cannot be hidden behind a later colliseum. This game is light on logic at the moment, but if we can get proper hooks we would like to randomize progression for substory unlocks.

Currently this is built as a local only proof of concept as until we have a way to hook into the game, linking this to archipelago will be impossible.

## Credits
Ret for building a ton of infrastructure for Yakuza modding, and allowing me to bundle the reARMP tool with my randomizer.