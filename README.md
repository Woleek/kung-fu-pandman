<p align="center"># ![pandman](https://github.com/Woleek/kung-fu-pandman/assets/84938240/73506f5f-ab74-4af0-acb5-e4aa2eaa0b3b) kung-fu-pandman</p>
   
Game made with PyGame module to explore threading usage in Python. It's a modified game of Pacman, that has some of it's original functionalities and same new ones....and it looks like Kung Fu Panda.   
   
### Prerequisites   
```
pygame==2.1.2
```
   
### Run game   
Game can be launched by running `main.py` from terminal.
```
> python src/main.py
```
   
### Modify game settings
All settings can be modified from `settings.py` file by changing coresponding variables values
```
> notepad src/settings.py
```
   
Most important settings:   
`SCREEN_WIDTH` / `SCREEN_HEIGHT` - display size   
`BLOCK_SIZE` - size of ingame objects   
`BLOCKS_DENSITY` - random factor for block spawn density   
`JOMBIE_AIM` - random factor for jombie move direction change (1 is perfect aim - never miss)   
`NUM_JOMBIES` - number of jombies spawned   
`NOODLE_REST` - time to respawn noodle   
`LIFE` - starting life points   
