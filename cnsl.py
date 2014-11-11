import readline
import os
import re

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
        choice=input("Do you accept this modification?[Y|N]")
        if choice.lower()=="y":
            return True
        if choice.lower()=="n":
            return False

def prompt_line_Change(pre_line,post_lines):
    print("Current Matching Line :\n "+pre_line)
    print("Suggested Modification:\n")
    for post_line in post_lines:
        print (post_line)
    accept=read_acceptance()
    while not accept:
          post_line=rlinput("Please Edit :\n",post_line)
          accept=read_acceptance()
    return post_line

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

def draw_file_contents(lines,pos):
    os.system('clear')
    print("File Contents:")
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
        convTemplate="""<cfinvoke component="NBP.NetBiosProxyHelper" method="getTemplatePathForACWithEncryptedValue" fileName="{1}" returnvariable="{0}" />"""
        replaceToken="#encryptedValue"+str(count)+"#"
        textToBeReplaced=line[startIndex:endIndex]
        convLine=convTemplate.format(replaceToken,textToBeReplaced)
        new_line=line[0:startIndex]+replaceToken+line[endIndex:len(line)]
        return [convLine,new_line]
    else:
        raise Exception("invalid processing ")


patterns=["/download/","/manuals","/HelpDoc","/reports/"]
old_lines=open("agreement.cfm","r").readlines()
new_lines=[]
count=1 #counter for current changes in file
for pos in range(len(old_lines)):
    line=old_lines[pos]
    matched_pattern=is_matching_line(line,patterns)
    if matched_pattern != False:
        draw_file_contents(old_lines,pos)
        pre_line=line
        post_line=get_suggested_line(pre_line,matched_pattern)
        post_line=prompt_line_Change(pre_line,post_line)
        new_lines.append(post_line)
        count+=1
    else:
     new_lines.append(line+"\n")
output=open("foo_tmp.txt","w")
output.write("\n".join(new_lines))



"""
before_line="before reverse proxy line !!"
after_line="after removing ,I'm new :)"
value=prompt_line_Change(before_line,after_line)
print("modified as:\n "+value)
"""
