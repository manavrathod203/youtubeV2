# DO NOT TOUCH!!
"""
1. Total number of comments analyzed
2. No. of positive, neutral and negative and neutral comments out of total comments
3. Pie chart of sentiment analysis
4. seperate positive, negative and neutral comments and show them in three different tables 

SAVES EVERYTHING 
pie chart : sentiment_pie_chart.png
Dataframes in csv files : positive_comments.csv , negative_comments.csv , neutral_comments.csv

"""
import os
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd
from youtube_comment_downloader import *
import sys
import emoji
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from PIL import Image, ImageDraw
import math

script_directory = os.path.dirname(os.path.abspath(__file__))


def get_comments(url):
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_POPULAR)
    text_comments = [[comment['text']] for comment in comments]
    return text_comments


# Define lists of positive and negative emojis
emoji_positive_list = [
    "😀", "😃", "😄", "😁", "😆", "🥹", "😅", "😂", "🤣", "😊", "😇", "🙂", "😉", "😌", "😍", "🥰", "😘", "😙", "😚", "😋", "😝", "😜", 
    "🤓", "😎", "🤩", "🥳", "😏", "🥺", "🥵", "😳", "🤯", "🤗", "🫣", "🤭", "🫠", "🤤", "🤑", "🤠", "😺", "😸", "😹", "😻", "😼", "😽", 
    "🫶", "🫶🏻", "🫶🏼", "🫶🏽", "🫶🏾", "🫶🏿", "🙌", "🙌🏻", "🙌🏼", "🙌🏽", "🙌🏾", "🙌🏿", "👏", "👏🏻", "👏🏼", "👏🏽", "👏🏾", "👏🏿", "🤝", "👍", "👍🏻", "👍🏼", 
    "👍🏽", "👍🏾", "👍🏿", "🤞", "🤞🏻", "🤞🏼", "🤞🏽", "🤞🏾", "🤞🏿", "✌", "✌🏻", "✌🏼", "✌🏽", "✌🏾", "✌🏿", "🫰", "🫰🏻", "🫰🏼", "🫰🏽", "🫰🏾", "🫰🏿", "🤟", 
    "🤟🏻", "🤟🏼", "🤟🏽", "🤟🏾", "🤟🏿", "🤘", "🤘🏻", "🤘🏼", "🤘🏽", "🤘🏾", "🤘🏿", "👌", "👌🏻", "👌🏼", "👌🏽", "👌🏾", "👌🏿", "🤌", "🤌🏻", "🤌🏼", "🤌🏽", "🤌🏾", 
    "🤌🏿", "🤙", "🤙🏻", "🤙🏼", "🤙🏽", "🤙🏾", "🤙🏿", "🙏", "🙏🏻", "🙏🏼", "🙏🏽", "🙏🏾", "🙏🏿", "💋", "🫂", "👸", "🫅", "🦸", "🧚", "👼", "💁", "💃", 
    "🕺", "👯", "👫", "👭", "👬", "💑", "💏", "🎓", "👑", "💍", "🐶", "🐱", "🐻", "🐼", "🐨", "🐯", "🦁", "🐸", "🐧", "🐤", "🐥", "🐣", 
    "🦄", "🦋", "🐞", "🐬", "🐅", "🐕", "🐩", "🦮", "🐈", "🪽", "🦚", "🦢", "🐇", "🐿", "🐾", "🎄", "🌲", "🌳", "🌴", "🍀", "🍃", "🍂", 
    "🍁", "🌾", "💐", "🌷", "🌹", "🪻", "🪷", "🌺", "🌸", "🌼", "🌻", "🌞", "🌝", "🌛", "🌜", "🌕", "🌗", "🌖", "🌘", "🌒", "🌓", "🌔",
    "🌍", "🌙", "🌏", "🌎", "💫", "⭐", "✨", "🌟", "⚡", "☄", "💥", "🔥", "🌈", "🫧", "⛅", "⛄", "🍏", "🍎", "🍐", "🍊", "🍋", "🍌", 
    "🍒", "🍆", "🌽", "🥕", "🥔", "🥦", "🥬", "🥒", "🥞", "🧇", "🥓", "🥩", "🍖", "🍗", "🍟", "🍕", "🌮", "🍤", "🎂", "🍰", "🥧", "🧁", 
    "🍦", "🍨", "🍧", "🍮", "🍭", "🍬", "🍫", "🍿", "🍩", "🍯", "🍼", "🥛", "☕", "🍵", "🍶", "🥂", "🍻", "🍺", "🍷", "🥃", "🍸", "🍹", 
    "🍾", "🍴", "🥄", "🥢", "⚽", "🏀", "🎾", "🏐", "🏓", "🏸", "🏏", "🥅", "⛳", "🧘‍♀", "🧘🏻‍♀", "🧘🏼‍♀", "🧘🏽‍♀", "🧘🏾‍♀", "🧘🏿‍♀", "🧘‍♂", "🧘🏻‍♂", "🧘🏼‍♂", 
    "🧘🏽‍♂", "🧘🏾‍♂", "🧘🏿‍♂", "🏆", "🥇", "🥈", "🥉", "🏅", "🎼", "🥁", "🎷", "🎺", "🎸", "🎻", "🎤", "🎯", "🎰", "🚀", "🚲", "🎡", "🎢", "🎠", 
    "🎇", "🎆", "🌠", "🌄", "🌅", "🎑", "🌃", "🌌", "🌉", "🌁", "🌆", "🌇", "🪔", "💎", "🧿", "🪬", "🧸", "🎁", "🎈", "🎀", "🪄", "🪅", 
    "🎊", "🎉", "💌", "🩷", "❤", "🧡", "💛", "💚", "🩵", "💙", "💜", "🩶", "🤍", "🤎", "❤‍🔥", "💕", "💞", "💓", "💗", "💖", "💘", "💝", 
    "💟", "💯", "✅", "🆒", "🎵", "🎶", "🔊", "🔔"
    ]

emoji_negative_list = [
    "😔", "😞", "😣", "😢", "😭", "😰", "😩", "🥺","😫", "😨", "😡", "😠", "😤", "😥", "😪", "😷", "🤒", "🤕", "🤢", "🤮", "🤧", "🥴", 
    "🤯", "😳","😖", "😬", "😟", "🙁", "☹️", "😾", "😿", "🙀","😼", "👎", "👿", "💔", "💣", "💀", "👻", "💩","🙈", "🙉", "🙊", "💀", 
    "🦠", "🧟‍♀️", "🧟‍♂️","🧛‍♀️", "🧛‍♂️", "🕷️", "🦂", "🦇", "🐍", "🐺","🐃", "🦃", "🐔", "🐓", "🐣", "🐤", "🐥", "🐦","🐧", "🦆", "🦢", "🕊️", 
    "🦉", "🦚", "🦜", "🦩","🦔", "🦝", "🦙", "🦘", "🐪", "🐫", "🦫", "🦡","🐿️", "🦨", "🐖", "🦑", "🦞", "🦀", "🐡", "🐠","🐟", "🐬", 
    "🐳", "🐋", "🦈", "🦭", "🐊", "🐅","🐆", "🦓", "🦍", "🦧", "🦣", "🐘", "🦛", "🦏","🐪", "🐫", "🦫", "🦡", "🐾", "🦔", "🦝", "🦢",
    "🐜", "🐛", "🐝", "🦗", "🕸️", "🐌", "🐚", "🐞","🦋", "🦇", "🐙", "🦑", "🦐", "🦀", "🦞", "🦂","🐢", "🦕", "🦖","🥲","🙃","🤪","😒",
    "😞","😔","😟","😕","🙁","😣","😖","😫","😩","😢","😭","😤","😠","😡","🤬","😱","😨","😰","😥","😓","🤥","😐","🫤","😑","🫨","😬",
    "🙄","😦","😧","🥱","😴","😪","😵","😵‍💫","🥴","🤢","🤮","🤧","😷","🤕","😈","👿","👹","👺","🤡","💩","👻","💀","😼","😿","😾","👎",
    "👎🏻","👎🏼","👎🏽","👎🏾","👎🏿","👊","👊🏻","👊🏼","👊🏽","👊🏾","👊🏿","🖕","🖕🏻","🖕🏼","🖕🏽","🖕🏾","🖕🏿","👅","🦹‍♀","🦹‍♂","🦹🏻‍♀","🦹🏻‍♂","🧟‍♀","🧟‍♂","🙅🏻‍♀","🙅‍♀",
    "🙅‍♂","🙅🏻‍♂","🤦🏻‍♀","🤦‍♂","🤦🏻‍♂","🤦‍♀","🦊","🐷","🐽","🙈","🐵","🙉","🙊","🐒","🐔","🐗","🐛","🐌","🐜","🪰","🐢","🐍","🦀","🦞","🦍","🦧",
    "🐊","🐖","🥀","💦","💧","🔪","🪓","🧨","💣","🚬","💔","❤‍🩹","❌","📛","🚫","💢","🚷","🚯","🚳","🚱","🔞","📵","🚭","❎","🔕","🏴‍☠"
    ]


def calculate_emoji_sentiment(comment):
    positive_score = 0
    negative_score = 0

    for emoji_char in comment:
        if emoji_char in emoji_positive_list:
            positive_score += 1
        elif emoji_char in emoji_negative_list:
            negative_score += 1

    # Calculate a sentiment score based on the difference between positive and negative emojis
    sentiment_score = positive_score - negative_score
    return sentiment_score


def analyze_comments():
    text_comments = get_comments(url)

    sia = SentimentIntensityAnalyzer()

    positive_comments = []
    negative_comments = []
    neutral_comments = []

    for comment in text_comments:
        # Get the sentiment score for the text part of the comment
        text_sentiment_score = sia.polarity_scores(comment[0])['compound']

        # Calculate sentiment score based on emojis
        emoji_sentiment_score = calculate_emoji_sentiment(comment[0])

        # Combine the sentiment scores from text and emojis
        combined_sentiment_score = text_sentiment_score + emoji_sentiment_score

        if combined_sentiment_score > 0:
            positive_comments.append(comment)
        elif combined_sentiment_score < 0:
            negative_comments.append(comment)
        else:
            neutral_comments.append(comment)

    total_comments = len(text_comments)
    num_positive_comments = len(positive_comments)
    num_negative_comments = len(negative_comments)
    num_neutral_comments = len(neutral_comments)

    # print('Total number of comments analyzed:', total_comments)
    # print('Number of positive comments:', num_positive_comments)
    # print('Number of negative comments:', num_negative_comments)
    # print('Number of neutral comments:', num_neutral_comments)

    # print('\nSentiment Analysis Pie Chart:')
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [num_positive_comments,
             num_negative_comments, num_neutral_comments]
    # # sizes = [0 if np.isnan(size) else size for size in sizes]
    # colors = ['#AEE2FF', '#FF6969', '#FEFF86']

    # labels = ['Positive', 'Negative', 'Neutral']
    # sizes = [30,
    #          50, 20]
    # # sizes = [0 if np.isnan(size) else size for size in sizes]
    # colors = ['#AEE2FF', '#FF6969', '#FEFF86']




  
    # Sample data
    # sizes = [50,30,20]
    # labels = ['A', 'B', 'C']
    hex_colors = ['#AEE2FF', '#FF6969', '#FEFF86']

    # Convert hexadecimal colors to RGB tuples
    colors = [tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5)) for hex_color in hex_colors]

    # Create a blank image
    image_size = 400
    image = Image.new("RGB", (image_size, image_size), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw pie chart
    start_angle = 0
    for size, label, color in zip(sizes, labels, colors):
        angle = 360 * size / sum(sizes)
        draw.pieslice([(50, 50), (350, 350)], start_angle, start_angle + angle, fill=color, outline="black")
        start_angle += angle

    # Add legend
    # legend_start = 100
    # for label, hex_color in zip(labels, hex_colors):
    #     rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    #     draw.rectangle([(270, legend_start), (290, legend_start + 20)], fill=rgb_color, outline=None)
    #     draw.text((300, legend_start), label, fill="black")
    #     legend_start += 25

    # Save as PNG
    image.save("sentiment_pie_chart.png")


    # plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
    # plt.axis('equal')
    # plt.savefig('sentiment_pie_chart.png')
    # plt.show()
    
    # plt.pie(sizes, colors=colors, autopct='%1.1f%%', startangle=90)
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.xticks([])
    # plt.yticks([])
    # plt.savefig('sentiment_pie_chart.png', dpi=300, bbox_inches='tight', pad_inches=0.0)

   

    # Save the pie chart as a PNG image

    # display_comment_tables(
    #     positive_comments, negative_comments, neutral_comments)

    positive_df = pd.DataFrame(
        positive_comments, columns=['Positive Comments'])
    positive_df.insert(0, "#", range(1, len(positive_df) + 1))
    negative_df = pd.DataFrame(
        negative_comments, columns=['Negative Comments'])
    negative_df.insert(0, "#", range(1, len(negative_df) + 1))
    neutral_df = pd.DataFrame(neutral_comments, columns=['Neutral Comments'])
    neutral_df.insert(0, "#", range(1, len(neutral_df) + 1))

    # Save DataFrames as CSV files
    positive_df.to_csv('positive_comments.csv', index=False)
    negative_df.to_csv('negative_comments.csv', index=False)
    neutral_df.to_csv('neutral_comments.csv', index=False)

    # Read CSV files into pandas DataFrames
    df1 = pd.read_csv('positive_comments.csv')
    df2 = pd.read_csv('neutral_comments.csv')
    df3 = pd.read_csv('negative_comments.csv')
    

    # Convert DataFrames to HTML tables
    # positive_table = df1.to_html(
    #     classes='table table-bordered border border-dark border-3 table-success ', index=False)
    # neutral_table = df2.to_html(
    #     classes='table table-bordered border border-dark border-3 table-warning ', index=False)
    # negative_table = df3.to_html(
    #     classes='table table-bordered border border-dark border-3 table-danger ', index=False)
    
    positive_table = df1.to_html(
        classes='bg-[#AEE2FF] table table-bordered border border-dark border-3  ', index=False)
    neutral_table = df2.to_html(
        classes='table table-bordered border border-dark border-3 table-warning ', index=False)
    negative_table = df3.to_html(
        classes='table table-bordered border border-dark border-3 table-danger ', index=False)

    print(json.dumps({
    'positive_table': positive_table,
    'neutral_table': neutral_table,
    'negative_table': negative_table,
    'countTotal': total_comments,
    'countPositive': num_positive_comments,
    'countNeutral': num_neutral_comments,
    'countNegative': num_negative_comments,
    'positive_list': positive_comments,
    'negative_list': negative_comments,
    'neutral_list': neutral_comments,
    'allComments': text_comments,
}))



def display_comment_tables(positive_comments, negative_comments, neutral_comments):
    positive_df = pd.DataFrame(
        positive_comments, columns=['Positive Comments'])
    positive_df.insert(0, "#", range(1, len(positive_df) + 1))
    negative_df = pd.DataFrame(
        negative_comments, columns=['Negative Comments'])
    negative_df.insert(0, "#", range(1, len(negative_df) + 1))
    neutral_df = pd.DataFrame(neutral_comments, columns=['Neutral Comments'])
    neutral_df.insert(0, "#", range(1, len(neutral_df) + 1))

    # print('Positive Comments:')
    # print(positive_df)

    # print('Negative Comments:')
    # print(negative_df)

    # print('Neutral Comments:')
    # print(neutral_df)

    # Save DataFrames as CSV files
    positive_df.to_csv('positive_comments.csv', index=False)
    negative_df.to_csv('negative_comments.csv', index=False)
    neutral_df.to_csv('neutral_comments.csv', index=False)


# if len(sys.argv) != 2:
#     print("Usage: python main.py <url>")
#     sys.exit(1)

# url = sys.argv[1]
# print(url)
    
# -----------------------------
url = sys.argv[1] if len(sys.argv) > 1 else None
# ----------------------------- 
analyze_comments()
