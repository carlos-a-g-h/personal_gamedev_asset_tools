# Pesonal GameDev Asset Tools

## Requirements (may change in the future)
- Python 3.9 or above and nothing else: All of this is build on top of the stdlib
- Some features may require other programs

## Features (more will be added)
- Create sprite sheets using FFmpeg. Tested on Linux only but it should also work on Windows and Mac
- Recovers individual sprites (images) and sounds from a Game Maker Studio 2 project (tested only with GMS2 v2.2.5.481 projects). Recovering a sprite with more than one frame will also try and create a sprite sheet with using FFmpeg but only if you're on Linux and have FFmpeg installed
