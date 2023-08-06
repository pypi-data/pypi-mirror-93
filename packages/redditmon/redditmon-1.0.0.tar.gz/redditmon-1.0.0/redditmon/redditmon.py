"""Module for monitoring a subreddit for new posts
"""

import praw, time, os, argparse, configparser
from os.path import expanduser

class RedditDisplay:
    def __init__(self, subreddit_name, refresh_interval, config_path):
        self.subreddit = subreddit_name
        self.refresh_interval = refresh_interval
        self.config = self.load_config(config_path)
        self.reddit_client = praw.Reddit(
            client_id=self.config["API"]["client_id"],
            client_secret=self.config["API"]["client_secret"],
            user_agent=self.config["API"]["user_agent"])
        self.post = self.get_top_post()

    def load_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        try:
            config["API"]["client_id"]
        except KeyError:
            print("Error encountered when loading config file. Please create a config file\n" +
                "in the proper format, and store it in your home directory.\n" +
                "\n" +
                "The config file should looke like this and be named ~/config.ini:" +
                "\n" +
                "\n" +
                "[API]" +
                "\n" +
                "client_id = Some_Reddit_AppID\n" +
                "client_secret = Some_Reddit_App_Secret\n" +
                "user_agent = redditmon/0.1 by slash64-api\n" +
                "\n" +
                "\n" +
                "Alternatively, you can specify the location of your config file \n" +
                "with the -c flag (use --help for a hint)\n")
            exit()

        return config

    def get_top_post(self):
        post = list(self.reddit_client.subreddit(self.subreddit).hot(limit=1))[0]
        return post

    def print_post_title(self):
        print(f'The Current Top Post on /r/{self.subreddit} is:')
        print(f'"{self.post.title}" submitted by user "{self.post.author}" with {self.post.score} Upvotes')

    def print_post_body(self):
        if self.post.selftext == "":
            print(f'Click to view URL: {self.post.url}')
        else:
            print(self.post.selftext)

    def print_post_url(self):
        print(f'View This Post on Reddit at this URL: https://old.reddit.com{self.post.permalink}')

    def display_post(self):
        # Clear out the old posts from the Terminal Screen
        os.system("clear")

        # Print out the post
        self.print_post_title()
        print()
        self.print_post_body()
        print()
        self.print_post_url()

        # Hang out a bit until the refresh interval expires
        time.sleep(self.refresh_interval)
        print("Done Sleeping!")


def get_cli_args():
    user_home = expanduser("~")
    parser = argparse.ArgumentParser(description="A Janky CLI Tool to Monitor a Subreddit")
    parser.add_argument(
        'Subreddit', 
        metavar='subreddit',
        type=str, 
        help='The name of the subreddit you want to view')

    parser.add_argument(
        '-r', 
        metavar='refresh',
        type=int,
        default=10,
        help='The amount of time in seconds between refreshes (default 10)')

    parser.add_argument(
        '-c',
        metavar='config',
        type=str,
        default=f'{user_home}/redditmon.config.ini',
        help='The file path to the config file (defaults to ~/redditmon.config.ini)')

    args = parser.parse_args()

    return args

def redditmon_cli():
    args = get_cli_args()

    subreddit_name = args.Subreddit
    refresh_interval = args.r
    config_path = args.c

    display = RedditDisplay(subreddit_name, refresh_interval, config_path)

    while True:
        try:
            display.display_post()
        except KeyboardInterrupt:
            os.system("clear")
            print("Exiting RedditMon")
            time.sleep(.5)
            exit()


if __name__ == "__main__":
    redditmon_cli()
