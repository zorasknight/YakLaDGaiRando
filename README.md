<p align="center">
  <img src="Assets/icon.ico" width="200" />
</p>

<div align="center">
     <h1> Like a Dragon Gaiden: <br> The Man Who Erased His Name Randomizer (AP) </h1>
</div>

Archipelago (multiworld) item randomization for Yakuza/Like a Dragon: Gaiden 

If you run into any issues, please reach out to me through either the AP after dark thread, or a DM on discord. 

## Required Tools

This tool should be completely OS agnostic, though the mod relies on DLL injection to function which is a very windows thing to do. Your results may vary on non Windows OS, but success has been seen by community members, so please read below if you are on linux or another OS.

This version of the tool uses the Archipelago client to create your YAML(settings) and generate your game, please set that up before continuing here.

Archipelago setup guide:
https://archipelago.gg/tutorial/Archipelago/setup_en

You will need a copy of "Like a Dragon Gaiden: The Man Who Erased His Name".
I have tested this on the Steam version of the game, and that's the only supported version, your mileage may vary with other legal sources!

This mod is installed using the Shin Ryu Mod Manager:

Nexus link:
https://www.nexusmods.com/site/mods/743?tab=description

Alternatively Github:
https://github.com/SRMM-Studio/ShinRyuModManager/releases

Please follow that link and complete the install first before attempting to run the randomizer!

## Installing the custom Yakuza Gaiden world

You can install the packaged yakuza_gaiden.ap world file through the Archipelago application's included "Install APWorld" client. You can also simply place the 
yakuza_gaiden.ap file into the custom_worlds folder at the root of your Archipelago installation.

This client is required to use the "Options Creator" client within Archipelago to make your own custom YAML(options file). This will also be the tool used for Randomizing the game as the randomizer is now included into the Archipelago text client.

## Making your own options file (YAML)

Using the "Options Creator" within Archipelago allows you to create a combination of settings to fit how you personally want your randomized experience to be. This is sepperate from everyone elses randomized settings within your multiworld, and is required even if you intend to play in a solo world.

you can find this game under Yakuza Gaiden, likely quite far down the list, and have fun setting up all forms of different options. I recomend the default for a first playthrough.

## Patching your game

The Gaiden Randomizer has now been merged into the Gaiden Client, to setup the randomizer first install the yakuza_gaiden.apworld and navigate to the "Randomizer" tab within it. There's a "Select Folder Location" button that you can use to choose a folder to install the Randomizer files to. After that, you can press the "Create or Update the Randomizer Folder" button to install the required randomizer files into that folder. When a new update drops, you can just replace the apworld in your custom worlds folder, and re-run the "Create or Update the Randomizer Folder" button to clear those folders and remake them with the newest files.

After a multiworld room has been created you will see a "Download Patch File..." option on your slot, this will download a file containing all of your settings and information for this seed. This will be unique to every run you do, so make sure to delete the old mods in your mod folder between each run!

You then need to place the resulting zip file into the "AP_PATCH" folder that was created when you made the randomizer folder from the previous steps. Once opening the Yakuza Gaiden AP World you will see a button that says "Run Randomizer" within the "Randomizer" tab pressing that will use the most recent file in the AP_PATCH folder to generate from. You will know everything is finished when you see the text "Enjoy the rando!".

When that is finished you will have a new Gaiden_Rando.zip file contained within that selected folder that can be installed using the Shin Ryu Mod Manager. Please remember to delete other seeds before starting the randomizer!

### WARNING: There is no guarentee that other mods will work with this rando! If you're having any issues, make sure other mods are deleted from your mods folder, not just deactivated!

## How to connect to the multiworld

Once you have installed the Shin Ryu Mod Manager and followed those instructions below to launch your game, you will notice a sepperate console window will open alongside Gaiden. This console will help you keep track of sent items, found locations, as well as issue commands. Alternatively, if you have the text client open and connected while booting the game through SRMM, the console will auto connect using those credentials. You can do all commands through either the text client or the console from there!

If you want to use just the game console and not use the text client the instructions to do so are below:

When the game is first started it should connect all hooks and tell you "Awaiting item interaction to find inventory..." this means that everything has successfully began. From here you need to connect to the multiworld server, and then set your specific player port (including password only if one is set).

To connect to a world you can copy paste the /connect text found on the multiworld room. You can copy that whole block into the console window. a sample of that looks like this:

/connect archipelago.gg:62189

from there you will be asked for your port, if you have not setup a password then you can ommit the password field, here's a sample:

slot Yakuza SuperRadPassword

If everything looks good after that, then you are connected! you will not recieve or send out items until you have interacted with an item in-game. This is to locate the player inventory, so don't be alarmed if you aren't receiving items right away.

When you want to stop for the night, save your game and exit normally. On the next boot, make sure to use SRMM and load your existing save. The console should try and auto connect you if it can, but if not it will give you an error to let you connect manually again (in the situation where the port may have changed for example).

The console constantly attempts to sync your progress with the AP server, using your current save and the expected items from the server as it's baseline. What that means, is even if, after a death or game crash, you see items in the overworld again, collecting them a second time will do nothing, but nothing will be lost either as the items will be re-added as soon as you interact with your inventory in some way (eating an item, collecting an item, selling an item, etc.)

## Universal Tracker

This AP World has full Universal Tracker support, including a map tracker built in to the client!

I highly recomend using the Universal Tracker with this game, this is a sepperate AP world that can be installed alongside your other custom worlds that opens a custom text client with a list of all checks in logic based on your current player and world data. This couples with the name of each location to help make it easier to find checks as a first time player of this randomizer. For a full list of instructions to set this up please reference this link here.

This AP World has YAML-less support for the Universal Tracker, which means once you connect with the text client to a slot, you should have access to the map and tracker pages automatically.

Github link:
https://github.com/FarisTheAncient/Archipelago/releases?q=Tracker

## Installing the Shin Ryu Mod Manager

### NOTE: I did not create the Shin Ryu Mod Manager, this is just a quick reference guide.

This isn't meant to replace any existing guides for the mod manager, and updates may cause this snippet to be out of date in the future.

To install the Shin Ryu Mod Manager tool, download the zip from the provided nexusmods page, extract the contents of the zip to the "media" folder of your "Like a Dragon Gaiden" install. The folder should be the one that contains your "likeadragongaiden" exe. you want the files extracted straight to this folder, do not make a new folder at this location.

Your path should look something like this:

### \steamapps\common\LikeADragonGaiden\runtime\media

From there, you should be able to just run the "ShinRyuModManager" app, which should have you ready for the steps below! 

Remember to always launch the game through the mod manager and not through Steam if you want to play the randomizer.

## Instructions:

Install the yakuza_gaiden.apworld into your custom worlds folder for your Archipelago client.

Generate a new options yaml using the "Options Generator" (Remember to restart archipelago after adding the AP world!)

Place that yaml into the players folder of whoever is generating the game (also make sure to send them the AP world file too if it isn't you!)

Use that yaml to create a new multiworld output using "Generate".

That output can be hosted on the Archipelago website

Find your slot name, and download your patch file

Using the yakuza_gaiden.apworld select a folder to install your randomizer files into

Then generate a randomizer folder using the "Create or Update the Randomizer Folder" button

Put the patch file into the existing AP_Patch folder within wherever you selected the randomizer folder to reside in.

Press the "Run Randomizer" button to generate a new gaiden_rando.zip, you will know its ready when the text changes to "Enjoy the rando!". 

You should get an output file, zipped, with a name like: "Gaiden_Rando", this is your mod file, you can install this in your copy of "Shinryu Mod Manager" like any other mod. I recomend going into your mod folder and deleting existing copies for now to ensure stability!

Start the game from the mod manager to begin the game going forward.

If you keep the text client open and connected while starting gaiden it will automatically connect your game for you on startup. If it doesn't auto connect, you can manually connect through the console using instructions above.

### *NOTE: ALWAYS START THE GAME THROUGH THE MOD MANAGER, DO NOT START THE GAME THROUGH STEAM TO PLAY THE RANDOMIZER

## Linux options

Although I can't offer 100% full linux support, a number of players have succeded in playing by utilizing these tips:

### When using SRMM with a linux OS on Steam:

"Linux and Steam Deck users may need to adjust launch options for mods to work correctly, as Wine and Proton do not always load version.dll automatically. Some games may load it on their own, but it is recommended to explicitly set it using the overrides below."
set this within your Steam Launch Options:

WINEDLLOVERRIDES="version=n,b" %command%

https://github.com/SRMM-Studio/ShinRyuModManager/wiki/Launch-Options

### Confirmed working tools:
This is not a complete list of all possibilities just ones I have heard work:

Run the randomizer itself using Lutris, And Bazzite's included Proton for running the game, and then make sure to have the Linux version of SRMM.

## Languages other than English

This mod should work on copies of the game purchased in other countries, however, you will need to set the in-game text language to English due to how the item DBs are modified per langugage.

## FAQ/Tips

### I was sent a Shop Key but the shop is still empty?

Shop Keys are currently a consumable item that can be found within your inventory. They may be mixed in with your current items so make sure to scroll through! they won't be with key items, but rather with your other consumables. After using a key you will be booted out of your inventory and the relevant shop should have their items available for sale.

### The shop still doesn't have it's items available?

Make sure it's the correct shop! there are multiple Poppo marts for example within the various cities, same goes for shogi or gambling halls.

### Why isn't the Run Randomizer button working?

Make sure that their are enough valid locations in the pool! this mod adds 119 skill books and 60 cosmetics to the pool, so without enough valid slots the randomizer will prevent you from generating a seed. 

### Why did that healing item just tank my health/heat/make me drunk?

You really gotta be careful of cheap knockoffs these days, I hear you can tell it's fake by really paying attention to the name...

### How can I tell if the Randomizer worked?

You can tell the rando is working by the first enemy tutorial saying "Show them your strength" immediately. Or by checking the abilities screen when the game allows you. (the game allows you to upgrade Kiryu's abilities after the first fight on the dock in the intro) You should see each ability dragged out and locked, rather than seeing 4 HP upgrades available. If all your stuff is locked, that's a good sign! Past that any items aquired by wire in Yokohama or the shop items in either love magic or the pawn shop should be different than vanilla. As a note, the Soccer Ball in the intro is NOT randomized.

### An item disappeared before I could grab it!

Don't worry! Gaiden has a few "Missable" items, these items are guaranteed to only contain "Junk" quality items like stamina XX or Paper Plate. Still worth grabbing them if you can as they can have plates of all qualities or armor items, but it will never be something unique like a pocket circuit part.

### I'm in town, but getting the Akame level to 3/10 is taking forever!

That's intentional! Prioritize finding your "Key" items, it's the ones needed by the people of Sotenbori that you would normally grapple early on, to get to rank 3 you will need 2 of them, to get to rank 10 for the next cutoff another 4 are required.

### I can't find any progression items, where are they?

Progression items can be hard to find, but there are 4 guaranteed items in the early game that you can get before rank 3 (the remaining 4 are all in the later parts of the game like pocket circuit or the colliseum) Make sure to check all the minigames like pool, golf, the casino, or shogi. If that doesn't work, you can go back to Yokohama at any point in the game, there are unique checks there for Shogi and the casino!

### Where's Mahjong?

Don't make me add Mahjong. Currently the only way to implement it would be through the completion list, so maybe in the future...

## Implementation

Randomization is achieved through adjusting values in the aston.db section, among others, of the games data prior to run time. The python script modifies the loose files contained within the mod folders, then utilizes a tool by Ret to convert them back to bin files, they then get compacted into a zip file that the Shin Ryu Mod Manager can convert back into pars to be injected into your game at run time. A new file is made on startup with any difficulty the player chooses, the completion goal is set by the player.

Trap healing items have been added to catch players off guard.

Skills are separated and locked behind unique items in this run, collecting the new "Skill Books" throughout the world allows the ability to purchase that skill.

All gear have had their stats randomized betwen set values, and given a random ability with a new descripton.

Most prices and costs are randomly assigned and generated on making a new seed.

### Current Items in the pool for randomization:

Sotenbori Ebisu Pawn shop  
Pocket Circuit Parts from the Pocket Circuit part exchange  
Sotenbori Coin Lockers  
Akame Network point shop  
Billiards point shop  
Sotenbori Clothing Store  
Sotenbori Shigano
Sotenbori Hiratai
Sotenbori Tsuruna (pharmacy)
Sotenbori Kukuru
Yokohama Shichiya Pawn shop  
Yokohama Love Magic shop  
Yokohama outdoor Shogi point shop  
Yokohama Smile Wagon
Yokohama Ichiban Senbei
All Poppo marts in Yokohama and Sotenbori
Sotenbori outdoor Shogi point shop  
Golf point shop  
Darts Rivals  
Yokohama Gambling Hall point shop  
Sotenbori Gambling Hall point shop  
Colosseum Gambling Hall point shop  
Colosseum Casino point shop
Colosseum Boutique
Colosseum VIP-Boutique
Mizorogi shop within Akame's house  
Akame Tasks
Substories
wire grab items in Yokohama  
wire grab items in Sotenbori  
wire grab items in the Coliseum  
quest items and story fights  
Skill Books  
Pocket Circuit Parts from Pocket Circuit Rivals  
Trap Items
and many many more...  

### Planned locations (NOT YET IN GAME):
Coin Locker Keys (the actual coin lockers currently work!)
Completion List
Colosseum Fights
restricting Akame Tasks based on item acquisition ie: battle pass, photo pass, item gift pass, rival fight 1-16 etc.
Dungeon Keys
Core agent abilities toggled off until found

### Goals:
Collecting X golden balls out of Y
Defeating Shishido
Defeating the Pocket Circuit Owner rival race

## Credits
Nick Kiley for the Randomizer Logo, Tack7800 for cleaning up the various maps for the tracker, Ret for allowing me to bundle the reARMP tool with my randomizer, Faris for the amazing Universal Tracker, and Jhrino for helping with Pattern scanning and potential scripting access. And a big thanks to the Archipelago Yakuza community for the support!