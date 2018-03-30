#!/usr/bin/python
import praw
import pdb
import re
import os

post_search_string = " "
comment_search_string = " "
bot_name = "bot1"
subreddit_name = "askreddit"
posts_replied_to = []
comments_replied_to = []
limit_of_comment_replies = 10
limit_of_comments_searched = 50
limit_of_posts_searched = 10


def main():
    post_tracking_file_opener()
    comment_tracking_file_opener()


    reddit = praw.Reddit(bot_name)
    subreddit = reddit.subreddit(subreddit_name)


    submission_handling(subreddit)

    post_tracking_file_closer()
    comment_tracking_file_closer()




def post_tracking_file_opener():
    global posts_replied_to

    #setting up a file to keep track of what posts have already been commented on
    if not os.path.isfile("posts_replied_to_" + bot_name + ".txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to_" + bot_name + ".txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))

def post_tracking_file_closer():
    with open("posts_replied_to_" + bot_name + ".txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")

def comment_tracking_file_opener():
    global comments_replied_to

    #setting up a file to keep track of what comments have already been commented on
    if not os.path.isfile("comments_replied_to_" + bot_name + ".txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to_" + bot_name + ".txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))

def comment_tracking_file_closer():
    with open("comments_replied_to_" + bot_name + ".txt", "w") as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")

def submission_handling(subreddit):
    for submission in subreddit.hot(limit=limit_of_posts_searched):

        #post not archived, no duplicate replies, search criteria 
        if  not submission.archived and \
            submission.id not in posts_replied_to and \
            re.search(post_search_string, submission.title, re.IGNORECASE):
            print("Bot in: ", submission.title)
            #do whatever

            #submission.reply("hi")

            all_comments = submission.comments.list()
            comment_handling(all_comments)
            posts_replied_to.append(submission.id)
    
def comment_handling(comments):
    comments_replied_number = 0
    comments_searched = 0
    global good
    global bad

    for comment in comments:
        if comments_searched == limit_of_comments_searched:
            print("limit of comments searched reached")
            break
         
        #search criteria, no duplicate replies, limit of replies 
        if  re.search(comment_search_string, comment.body, re.IGNORECASE) and \
            comment.id not in comments_replied_to and \
            comments_replied_number < limit_of_comment_replies:
            #do whatever


            #comment.reply("ww says hi")
            #print(comment.body)

            print("Bot commented on: ", comment.id)
            comments_replied_number += 1
            comments_replied_to.append(comment.id)
        comments_searched += 1

if __name__ == '__main__':
    main()
