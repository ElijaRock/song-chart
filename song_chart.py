# cython: language_level=3
import codecs
import os.path
import time
from selenium import webdriver
from selenium.webdriver import Keys  # can be used for scroll down if needed
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.firefox.options import Options as ff_options
import matplotlib.pyplot as plt
import numpy as np


# Can use to make the checkmark thing: https://blog.finxter.com/how-to-overwrite-the-previous-print-to-stdout-in-python/

def scroll_down():
    SCROLL_PAUSE_TIME = 2

    # hardcoded scroll len
    for rand in range(1000):
        driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(SCROLL_PAUSE_TIME)


print("Please enter a youtube link: ", end="")
url = input()
print("")

try:
    print("Trying Chrome...", end="")

    options = chrome_options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
except:
    print("\u2717")
    time.sleep(0.4)
    print("\nTrying Firefox...", end="")
    options = ff_options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

print("\u2713")
time.sleep(0.4)
print("\nLoading webpage (will take longer for larger playlists)...", end="")
driver.get(url)

scroll_down()

print("\u2713")
time.sleep(0.4)
print("\nDownloading list of artists...", end="")

artists_dup = [channel.text for channel in driver.find_elements(By.CLASS_NAME, "ytd-channel-name")]
playlist_title = driver.title.split(" - ")[0]

driver.quit()

# solution for removing duplicates (there are 3 of each)
chunks = [artists_dup[x:x + 3] for x in range(0, len(artists_dup), 5)]
artists = []
for i in range(len(chunks)):
    artist = chunks[i][0]
    if artist != "":
        artists.append(chunks[i][0])

# print(*chunks, sep="\n")

artists_dict = {key: None for key in artists}

artists_len = len(artists)

print("\u2713" + " (" + str(artists_len) + " songs)")
time.sleep(0.4)

choice = "y"
if os.path.isfile("./" + playlist_title + ".txt"):
    print("\nFile already exists, would you like to generate a new one?")
    choice = str(input())

if "y" in choice.lower():
    with codecs.open(playlist_title + ".txt", "w", encoding="utf-8") as file:
        for key in artists_dict:
            file.write(str(key) + "\n")
        file.close()

print("\nPlease check the file that has just been generated: \"" + playlist_title + ".txt\" and change the artists' "
                                                                                    "names as needed", end="")

print("\nEnter \"continue\" when finished: ", end="")
input()

file = codecs.open(playlist_title + ".txt", "r", encoding="utf-8")
names = file.readlines()
for key, name in zip(artists_dict, names):
    artists_dict[key] = name.strip()

fnames_dict = {key: 0 for key in artists_dict.values()}

for artist in artists:
    fname = artists_dict[artist]
    fnames_dict[fname] += 1

sorted_fnames = dict(sorted(fnames_dict.items(), key=lambda x: x[1], reverse=True))

# TODO: ask user for top x but for now it's 5
top_artists = [x[1] for x in sorted_fnames.items()][:5]
labels = [x[0] for x in sorted_fnames.items()][:5]
colors = ["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4", "#9467bd", "#7f7f7f"]

others_sum = artists_len - sum(top_artists)
top_artists.append(others_sum)
labels.append("Other")

chart = np.array(top_artists)

plt.pie(chart, labels=labels, colors=colors)
plt.show()
