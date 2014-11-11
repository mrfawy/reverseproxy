import readline
import os
import re
import argparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)
   finally:
      readline.set_startup_hook()

def read_acceptance():
    while True:
        choice=input("Do you accept this modification?[Y|S]")
        if choice.lower()=="y":
            return True
        if choice.lower()=="s":
            return False

def prompt_line_Change(pre_line,post_lines):
    print("Current Matching Line :\n "+pre_line)
    print("Suggested Modification:\n")
    for post_line in post_lines:
        print (post_line)
    accept=read_acceptance()
    if not accept:
        post_lines=pre_line
    #while not accept:
          #post_line=rlinput("Please Edit :\n",post_lines)
          #accept=read_acceptance()
    return post_lines

def get_buffered_lines_indexes(lines,pos,window=5):
    if pos<0 or pos>len(lines):
        return null

    start_index=pos-((window-1)/2)
    if start_index<0:
       start_index=0
    end_index=pos+((window-1)/2)
    if end_index>len(lines):
       end_index=len(lines)
    return int(start_index),int(end_index)

def draw_file_contents(filepath,lines,pos):
    os.system('clear')
    print("File Contents:"+filepath)
    print("---------------")
    start_index,end_index=get_buffered_lines_indexes(lines,pos,5)
    for index in range(start_index,end_index):
        if index==pos:
           print (bcolors.WARNING+lines[index]+bcolors.ENDC)
        else:
            print(lines[index])
    print("=======================================================================================================================")

def is_matching_line(line,patterns):
    for pattern in patterns :
        if  re.search(pattern, line.lower(),re.IGNORECASE):
            return pattern
    return False

def get_suggested_line(line,matched_pattern,count=1):

    startIndex=line.find(matched_pattern)
    if(startIndex!=-1):
        endIndex=line.find('"',startIndex)
        leadingSpacesNo=len(line) - len(line.lstrip())
        leadingSpacesTxt=" ".join(" " for i in range(0,leadingSpacesNo*4))
        convTemplate="""<cfinvoke component="NBP.NetBiosProxyHelper" method="getTemplatePathForACWithEncryptedValue" fileName="{1}" returnvariable="{0}" />"""
        replaceToken="#encryptedValue"+str(count)+"#"
        textToBeReplaced=line[startIndex:endIndex]
        convLine=convTemplate.format(replaceToken,textToBeReplaced)
        new_line=line[0:startIndex]+replaceToken+line[endIndex:len(line)]
        convLine=leadingSpacesTxt+convLine
        return [convLine,leadingSpacesTxt+"<cfoutput>",new_line,leadingSpacesTxt+"</cfoutput>"]
    else:
        raise Exception("invalid processing ")

def edit_file(patterns,filepath):
    print ("Editing File :"+filepath)
    old_lines=open(filepath,"r").readlines()
    new_lines=[]
    count=1 #counter for current changes in file
    for pos in range(len(old_lines)):
        line=old_lines[pos]
        matched_pattern=is_matching_line(line,patterns)
        if matched_pattern != False:
            draw_file_contents(filepath,old_lines,pos)
            pre_line=line
            post_lines=get_suggested_line(pre_line,matched_pattern,count)
            post_lines=prompt_line_Change(pre_line,post_lines)
            new_lines.extend(post_lines)
            count+=1
        else:
         new_lines.append(line+"\n")
    output=open(filepath+"_new","w")
    output.write("\n".join(new_lines))


def process_Files(patterns,full_file_paths):
    print ("Starting Python processing")
    for filepath in full_file_paths:
        edit_file(patterns,filepath)


def get_filepaths(directory,skip_pattern):

    file_paths = []  # List which will store all of the full filepaths.
    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            if not skip_pattern  in filepath:
                file_paths.append(filepath)
    return file_paths

# Start of the Script
parser = argparse.ArgumentParser()
parser.add_argument("path", help="directory path to start scanning ")
parser.add_argument("-p","--pattern",nargs = '*' , help="list of pattern(s) to match ,please refer to Python Regex documentation .Default:'/download/' '/manuals' '/HelpDoc' '/reports/'",action="append",default=[["/download/","/manuals","/HelpDoc","/reports/"]])


args = parser.parse_args()
DIR_PATH=args.path
PATTERNS=args.pattern
full_file_paths = get_filepaths(DIR_PATH,".git")
print(full_file_paths)
process_Files(PATTERNS[-1],full_file_paths) # -1  to always get the last , as if parm is submitted it's appended
print ("DONE")
