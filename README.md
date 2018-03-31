# RedditBotProject
I'm working on making some reddit bots and using NLTK

Make sure you have praw installed so in the terminal dl praw:

pip install praw

or

sudo pip install praw

This is a very helpful wrapper for the reddit api

The praw.ini file stores your reddit login credentials and
you need to configure that first to run this, and keep it 
in the same directory as the bot.py file.

more details here:
http://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html

Also edit the search criteria for posts at the top, and 
limit the number of post to be searched, comments to be searched,
comments to respond to, what sub reddit etc.

The bot goes through a subreddit and finds posts based a string in
their title and goes through the comments and finds comments based
on a string in the comment.  However, if you read through the praw
documentations there's literally endless things you can use to 
identify posts and comments, so this bot is like the most basic 
possible.

Also this bot stores the posts and comments already searched commented
on so that it will not spam post.  If you just wanna read comments and
posts, feel free to comment out the tracker parts in the main() function.
