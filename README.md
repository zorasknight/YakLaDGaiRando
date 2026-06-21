<p align="center">
  <img src="Assets/icon.ico" width="600" />
</p>

<p align="center">
     <h1> Like a Dragon Gaiden: <br> The Man Who Erased His Name Randomizer </h1>
</p>
First implementation for a Like A Dragon Gaiden Item Randomizer, capable of locally generating a randomized game for you to complete. Currently supports shops, lockers, gear stats and abilities, skills, wire items, rewards and more!

## Required Tools

This mod is installed using the Shin Ryu Mod Manager:
https://www.nexusmods.com/site/mods/743?tab=description

Please follow that link and complete the install first before attempting to run the randomizer!

You will need a copy of "Like a Dragon Gaiden: The Man Who Erased His Name".
I use a purchased Steam version of the game, and that's the only officially supported version, your mileage may vary with any other ways!

## Instructions:

Unzip the LaDGaidenRandomizer folder to wherever you want the randomizer to live (desktop with all your other folders etc....).

Run the Gaiden_Randomizer.exe from within that folder
    *NOTE: if you can't run the EXE for whatever reason, the order of operations to create a rando seed is: shuffle.py, replace_items.py, convert.py. The EXE has a function that just runs those three scripts back to back. You may also be able to just run the randomizer.py as it was the earlier intent for how to set it up before the GUI was made.

A GUI should launch that allows you to make any changes to the game settings per your likes! Make sure to leave enough spots open for important checks to be placed! the randomizer will fail if there aren't enough slots available. I recomend leaving stores on.

Once you're ready click the "Run Randomizer" buttons. Everything auto saves pretty instantly on category change or closing of the app.

You should get an output file, zipped, with a name like: "Gaiden_Rando_061026", this is your mod file, you can drag and drop this into your "Shinryu Mod Manager" window like any other mod.

Start the game, make a new save at your desired difficulty and enjoy!

## FAQ/Tips

### Why did that healing item just tank my health/heat/make me drunk?

You really gotta be careful of cheap knockoffs these days, I hear you can tell it's fake by really paying attention to the name...

### How can I tell if the Randomizer worked?

You can tell the rando is working by checking the abilities screen when the game allows you. (the game allows you to upgrade Kiryu's abilities after the first fight on the dock in the intro) You should see each ability dragged out and locked, rather than seeing 4 HP upgrades available. If all your stuff is locked, that's a good sign! Past that any items aquired by wire in Yokohama or the shop items in either love magic or the pawn shop should be different than vanilla. As a note, the Soccer Ball in the intro is NOT randomized.

### An item disappeared before I could grab it!

Don't worry! Gaiden has a few "Missable" items, these items are guaranteed to only contain "Junk" quality items like stamina XX or Paper Plate. Still worth grabbing them if you can as they can have plates of all qualities or armor items, but it will never be something unique like a pocket circuit part.

### I'm in town, but getting the Akame level to 3/10 is taking forever!

That's intentional! Prioritize finding your "Key" items, it's the ones needed by the people of Sotenbori that you would normally grapple early on, to get to rank 3 you will need 2 of them, to get to rank 10 for the next cutoff another 4 are required.

### I can't find any progression items, where are they?

Progression items can be hard to find, but there are 4 guaranteed items in the early game that you can get before rank 3 (the remaining 4 are all in the later parts of the game like pocket circuit or the colliseum) Make sure to check all the minigames like pool, golf, the casino, or shogi. If that doesn't work, you can go back to Yokohama at any point in the game, there are unique checks there for Shogi and the casino!

### I hate Shogi, why is it on?

Settings will come soon! But for now, puzzle shogi is consistent and you can lookup the solutions online.

### Where's Mahjong?

Don't make me add Mahjong. Currently the only way to implement it would be through the completion list, and I don't want to test play mahjong enough to build that out.

## Implementation

Randomization is achieved through adjusting values in the aston.db section, among others, of the games data prior to run time. The python script modifies the loose files contained within the mod folders, then utilizes a tool by Rett to conver them back to bin files, they then get compacted into a zip file that the Shin Ryu Mod Manager can convert back into pars to be injected into your game at run time. A new file is made on startup with any difficulty the player chooses, the completion goal is set by the player.

Trap healing items have been added to catch players off guard.

Skills are separated and locked behind unique items in this run, collecting the new "Skill Books" throughout the world allows the ability to purchase that skill.

All gear have had their stats randomized betwen set values, and given a random ability with a new descripton.

Most prices and costs are randomly assigned and generated on making a new seed.

### Current Items in the pool for randomization:

18 items from the Sotenbori Ebisu Pawn shop
94 Pocket Circuit Parts from the Pocket Circuit part exchange
50 items from the Sotenbori Coin Lockers
26 items from the Akame Network point shop
11 items from the Billiards point shop
12 items from the Sotenbori Clothing Store
8 items from the Yokohama Shichiya Pawn shop
11 items from the Yokohama Love Magic shop
11 Items from the Yokohama outdoor Shogi point shop
11 Items from the Sotenbori outdoor Shogi point shop
13 items from the Golf point shop
11 items from the Yokohama Gambler Hall point shop
10 items from the Sotenbori Gambler Hall point shop
16 items from the Coliseum Gambler Hall point shop
15 items from the Coliseum Casino point shop
38 items from the Coliseum Boutique
10 items from Mizorogi
40 wire grab items in Yokohama
50 wire grab items in Sotenbori
30 wire grab items in the Coliseum
30 wire grab items in the Coliseum Dungeon
12 quest items
119 Skill Books
14 Pocket Circuit Parts from Pocket Circuit Rivals
32 Trap Items

### Planned locations:
Coin Locker Keys
Cosmetic Shops
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

Logic is used to avoid hiding items behind themself, for example the A1 key cannot be stored within the A1 locker, This game is light on logic at the moment, but if we can get proper hooks we would like to randomize progression for substory unlocks.

Currently this is built as a local only proof of concept as until we have a way to hook into the game, linking this to an archipelago will be impossible.

## Credits
Nick Kiley for the Randomizer Logo, Ret for allowing me to bundle the reARMP tool with my randomizer, and Jhrino for helping with hooks and potential scripting access. And a big thanks to the Archipelago Yakuza community for the support!