# RedditMon

RedditMon is a dumb and janky little package I threw together so that I could learn how to package a python project.

## Installation

1. `pip install redditmon`
1. ????
1. Profit!!!

## Usage

To use this module (assuming you have it installed), create a config file in your home directory with the name `redditmon.config.ini` that contains the details of your reddit API account. Look at [this example](https://github.com/cummings-chris/redditmon/blob/main/example_redditmon.config.ini) to see how to structure the file. Once you have your config file in place, you can launch the module directly by issuing `redditmon <subredditname>`. Alternatively, you can launch it as a python module using `python3 -m redditmon <subredditname>`. Use `redditmon --help` for more information.
