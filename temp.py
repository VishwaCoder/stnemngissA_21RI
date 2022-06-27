import urllib.request
import re
import webbrowser

def fun():
    l=[]
    s=input("Enter Any Query:-\n")
    search_keyword="WITSolapur-ProfessionalLearningCommunity "+s
    search_keyword = search_keyword.replace(" ", "%20")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    print(video_ids)
    for i in range(0,len(video_ids)):
        lab="https://www.youtube.com/watch?v=" + video_ids[i]
        l.append(lab)
    #print(l)
    l=list(set(l))
    l.sort()
    for x in l:
        print(x)
    for i in range(0,5):
        webbrowser.open(l[i], new=5)

    
        
fun()
