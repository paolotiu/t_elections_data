import os
import json
import pandas as pd


folder_path = './'
data_list = []
# Iterate through each subfolder (categorized by date)
for date_folder in os.listdir(folder_path):
    print(date_folder)

    date_folder_path = os.path.join(folder_path, date_folder)

    # Check if it's a directory
    if os.path.isdir(date_folder_path):
        # Iterate through each JSON file in the subfolder
        for file_name in os.listdir(date_folder_path):
            file_path = os.path.join(date_folder_path, file_name)

            # Check if it's a file and has a .json extension
            if os.path.isfile(file_path) and file_name.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    # Load JSON data
                    json_data = json.load(json_file)
                    tweets = json_data["data"]["search_by_raw_query"]["search_timeline"]["timeline"]["instructions"][0]["entries"]

                    # Extract relevant information (user name and tweet text)
                    for tweet in tweets:
                        user = None
                        tweet_text = None

                        if tweet["entryId"].startswith("tweet"):

                          result = tweet["content"]["itemContent"]["tweet_results"]["result"]


                          if "tweet" in result:
                              user = result["tweet"]["core"]["user_results"]["result"]["legacy"]["name"]
                              tweet_text = tweet["content"]["itemContent"]["tweet_results"]["result"]["tweet"]["legacy"]["full_text"]
                          else:
                              user = result["core"]["user_results"]["result"]["legacy"]["name"]
                              tweet_text = tweet["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["full_text"]
                              



                        # Check if 'user' is a dictionary or a string
                        if isinstance(user, dict):
                            user_name = user.get('screen_name', '')
                        elif isinstance(user, str):
                            user_name = user
                        else:
                            user_name = ''


                        # Append data to the list
                        if user_name or tweet_text:

                          data_list.append({'User Name': user_name, 'Tweet Text': tweet_text})

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data_list)

# Display the resulting DataFrame
print(df.head())