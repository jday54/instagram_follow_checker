import json
import easygui
import os
import tkinter as tk
from tkinter import filedialog

# read in json file containing followers/followed accounts inforrmation;
# return list of usernames of followers/followed accounts
def get_usernames(json_file_name, relationship):
    username_list = []
    with open(json_file_name) as f:
        json_data = json.load(f)
        if relationship == "relationships_following":
            json_data = json_data[relationship]
        for follower in json_data:
            # print(follower['string_list_data'])
            username = follower['string_list_data'][0]['value']
            username_list.append(username)
        return username_list

# find difference between list a and list b
def find_difference(list_a, list_b):
    difference = []
    for item in list_a:
        if item not in list_b:
            difference.append(item)
    return difference

def write_to_html(difference, html_file_name):
    with open(html_file_name, 'w') as f:
        f.write("<html><body>")
        for username in difference:
            f.write("<a href=\"https://www.instagram.com/{}/\">{}</a><br>".format(username, username))
        f.write("</body></html>")


if __name__ == '__main__':
    # Ask user to select a file using GUI file explorer
    # get follower file
    output = easygui.msgbox("Select the 'followers.json' file and 'following.json' file", "NOTICE", "OK")
    root = tk.Tk()
    root.withdraw()
    followers_filepath = filedialog.askopenfilename(title="Select the 'followers.json' file")
    following_filepath = filedialog.askopenfilename(title="Select the 'following.json' file")
 
    # Get list of followers and following usernames
    followers_list = get_usernames(followers_filepath, "relationships_followers")
    following_list = get_usernames(following_filepath, "relationships_following")

    # Get list of those following accounts who are not also followers
    difference = find_difference(following_list, followers_list)
    output = easygui.msgbox(f"Number of accounts not following you back is:{len(difference)}", "NOTICE", "OK")

    # Write difference to html file where each username is hyperlinked to instagram profile
    html_file_name = "follower_differences.html"
    output = easygui.msgbox("Select the folder where you want to save the output Web HTML file", "NOTICE", "OK")
    folderpath = easygui.diropenbox(msg="Select the folder where you want to save the output Web HTML file:", title="Save as", default=html_file_name)
    filepath = os.path.join(folderpath, html_file_name)
    write_to_html(difference, filepath)
    
    root.destroy()

