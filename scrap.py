from requests_html import HTMLSession
import os
os.system('clear')
#  Problem with mic??
# mine?? yes, give me a monment take ur time

def url(song_name):
    list_ = song_name.split()
    list_.append("lyrics")
    name = "+".join(list_)
    # print(name)
    return "https://www.google.com/search?safe=active&sxsrf=ALeKk03EbjukJL_bDCCTT_keRhTcYUFBBw%3A1585116544851&ei=gPV6XobMM4r2rQHMoqWgCg&q="+ name + "&oq="+ name + "+&gs_l=psy-ab.3.0.0i20i263j0l8j0i20i263.356254.360799..361918...0.1..0.396.4843.0j5j8j6......0....1..gws-wiz.......0i71j35i39j0i67.Hqqc8FjDoP0"

session = HTMLSession()
r = session.get(url("tera ban jaunga"))
singer = r.html.find("div[class='wwUB2c PZPZlf'] span a", first=True)
name = r.html.find(".gsmt span", first=True)
print("\n\n\n")
# [class='kno-ecr-pt PZPZlf gsmt i8lZMc']
print("Song Name: ", name.text, "\n")

print("Singer Name: ", singer.text)
print("\n\n\n")
print("Lyrics")
lyrics = r.html.find("span[jsname='YS01Ge']")
for l in lyrics:
  print(l.text)