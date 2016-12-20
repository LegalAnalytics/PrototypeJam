#script imports webpage content from a list of URLs, removes some extraneous information, and saves the resulting text in a .txt file.
import urllib.request

#location for text files used by program 
location="C:\\Users\\trustee\\Dropbox\\ABA Stuff\\Legal Analytics\\Hackathon 2017\\script\\"

#name and location of file containing containing names and URLs for TOS webpages
file_for_urls=location+"sites.txt"

#extracts the names and URLs from the text file and returns a dictionary
def unload_sites(file):
    sites = {}
    key = ""
    site = open(file,"r")
    while key !="end":
        key=site.readline().strip("\n")
        if key=="end": break
        else:
            url=site.readline().strip("\n")
            sites[key]=url
    site.close()
    return sites


#strips out \n tags from content
def remove_new_line(text):
    new_text=text.replace("\\n","")        
    return new_text

#strips out everything outside of <body> tags and all interal tags
def extract_body(text):
    text = text.lower() #make everything lower case
    #remove everything outside of the <body> tags
    loc1=text.find("<body")
    loc2=text.find("</body>")+7
    if loc1>0:
        new_text=text[loc1:loc2]
    else:
        new_text=text
    #remove all the other tags
    x=0
    buffer=[]
    tagless_text=[]
    while x < len(new_text):
        if new_text[x]=="<":
            buffer+=new_text[x]
            x+=1
            while new_text[x]!=">":
                if new_text[x]=="<" or x==len(new_text)-1:
                    tagless_text+=buffer
                    x-=1
                    break
                else:
                    buffer+=new_text[x]
                    x+=1
            buffer=[]
            x+=1
        else:
            tagless_text+=str(new_text[x])
            x+=1
    return remove_new_line("".join(tagless_text))



#retrieves data from TOS on web and writes body text to disk as text file. Takes a dictionary with name as a key and URL as content.
def retrieve_body(tos):
    for key in tos:
    
        try:
            #get content from web
            site=urllib.request.urlopen(tos[key])
            data=site.read()
            #process data to extract text of webpage body
            body = extract_body(str(data))
            #do something with the body - current code writes to a text file
            file = open(location+key+".txt", "w")
            file.write(body)
            file.close()
            #testing line
            print ("wrote file named "+key)
        except IOError:
            print ("failed to load file named "+key)

#get the URLs from the file and download and store the file content
locations = unload_sites(file_for_urls)
retrieve_body(locations)
print ("done")

