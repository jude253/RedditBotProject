#!/usr/bin/python
import praw
import pdb
import re
import os
import operator
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


stop_words_str = set(stopwords.words("english"))
stop_words_str.add("I")
stop_words_str.add(",")
stop_words_str.add(".")
stop_words_str.add("n't")
stop_words_str.add("(")
stop_words_str.add(")")
stop_words_str.add("'s")
stop_words_str.add("the")
stop_words_str.add("it")
stop_words_str.add("he")
stop_words_str.add("!")

stop_words = []
for word in stop_words_str:
    stop_words.append(word.decode("utf-8"))

words =[]
frequency = {}

post_search_string = " "
comment_search_string = ""
bot_name = "bot1"
subreddit_name = "askreddit"
posts_replied_to = []
comments_replied_to = []
limit_of_comment_replies = 10
limit_of_comments_searched = 50
limit_of_posts_searched = 2


def main():
    #post_tracking_file_opener()
    #comment_tracking_file_opener()


    reddit = praw.Reddit(bot_name)
    subreddit = reddit.subreddit(subreddit_name)


    submission_handling(subreddit)

    #print(words)
    word_frequency_finder(words)

    top_words = 0

    for key, value in sorted(frequency.iteritems(), key=operator.itemgetter(1), reverse=True):
        print(key, value)
        top_words += 1
        if top_words == 10:
            break


    #post_tracking_file_closer()
    #comment_tracking_file_closer()




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
            submission.link_flair_text != "Modpost" and\
            submission.id not in posts_replied_to and \
            re.search(post_search_string, submission.title, re.IGNORECASE):
            print("Bot in: ", submission.title)
            #do whatever
            #print(vars(submission))
            #submission.reply("hi")

            all_comments = submission.comments.list()
            comment_handling(all_comments)
            posts_replied_to.append(submission.id)
    
def comment_handling(comments):
    comments_replied_number = 0
    comments_searched = 0
    global words
  
    for comment in comments:
        if comments_searched == limit_of_comments_searched:
            print("limit of comments searched reached")
            break
         
        #search criteria, no duplicate replies, limit of replies 
        if  re.search(comment_search_string, comment.body, re.IGNORECASE) and \
            comment.id not in comments_replied_to and \
            comments_replied_number < limit_of_comment_replies:
            #do whatever

            for word in word_tokenize(comment.body):
                if word not in stop_words:
                    words.append(word)


            #comment.reply("ww says hi")
            #print(comment.body)

            #print("Bot saw on: ", comment.id)
            #comments_replied_number += 1
            comments_replied_to.append(comment.id)
        comments_searched += 1

def word_frequency_finder(word_list):
    global frequency
    
    for word in word_list:
        if word != "I":
            word = word.lower()
        if word not in frequency:
            frequency[word] = 1
        else:
            frequency[word] += 1
    return frequency

if __name__ == '__main__':
    main()