# Pesonal GameDev Asset Tools

WARNING: Requirements and features may increase in the future

## Requirements
- Python 3.9 or above and nothing else: All of this is build on top of the stdlib
- Some features may require other programs

## Features
- Create sprite sheets using FFmpeg. Tested on Linux only but it should also work on Windows and Mac
- Recovers individual sprites (images) and sounds from a Game Maker Studio 2 project (tested only with GMS2 v2.2.5.481 projects but it should work with other versions of GMS2). Recovering a sprite with more than one frame will also try and create a sprite sheet using FFmpeg, but only if you're on Linux and have FFmpeg installed
- Convert Game Maker GMMOD 3D format files to OBJ files

## Function names
If you're on Linux, Mac or any other Unix-based system, run the following line to view all features:

`$ cat personal_gamedev_asset_tools.py |grep "# Utility"`

All safe to use functions that correspond to each feature are preceded by a comment that starts with "# Utility"
There are code examples of some features in the "examples" folder
