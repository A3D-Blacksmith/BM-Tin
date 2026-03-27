import os, json
from time import strftime, localtime

#This file indexes all the assets in the current repository

repo = "A3D-Blacksmith/BM-Tin"
repo_manifest = []

def readManifest(path):

    file = "Assets/" + path + "/manifest.json"
    f = open(file, "r")
    content = json.loads(f.read())
    return content

def getFileTime(path):
    
    file = "Assets/" + path + "/Assets.zip"
    return os.path.getmtime(file) #Unix epoch

def getFileSize(path):

    file = "Assets/" + path + "/Assets.zip"
    file_stats = os.stat(file)
    return(str(file_stats.st_size)) #Kilobytes

def getDescription(path):

    file = "Assets/" + path + "/description.md"
    f = open(file, "r")
    return str(f.read())

def getThumbnailUrl(path):

    if os.path.isfile("Assets/" + path + "/thumbnail.gif"):
        return "Assets/" + path + "/thumbnail.gif"
    elif os.path.isfile("Assets/" + path + "/thumbnail.jpg"):
        return "Assets/" + path + "/thumbnail.jpg"
    else:
        return "Assets/" + path + "/thumbnail.png"

#Todo, check if exists
for name in os.listdir("Assets"):

    asset = {}

    asset["name"] = name
    asset["repo"] = repo
    asset["manifest"] = readManifest(name)
    asset["creator"] = asset["manifest"]["creator"]
    asset["tags"] = asset["manifest"]["tags"]
    asset["realname"] = asset["manifest"]["name"]
    asset["category"] = asset["manifest"]["category"]
    asset["date"] = getFileTime(name)
    asset["size"] = getFileSize(name)
    asset["thumbnail"] = getThumbnailUrl(name)
    asset["description"] = getDescription(name)
    

    repo_manifest.append(asset)

#print(repo_manifest[0])

json_object = json.dumps(repo_manifest, indent=4)

with open('bm_repo_index.json', 'w') as outfile:
    outfile.write(json_object)