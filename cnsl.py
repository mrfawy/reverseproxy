#import readline
import http.client, urllib
import os
import re
import argparse

OS_IS_WIN=False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class Record:
    def __init__(self,file_path="",line_number="",line=""):
        self.file_path=file_path
        self.line_number=line_number
        self.line=line

class FileProcessor:

    def __init__(self,filepaths,patterns):
        self.filepaths=filepaths
        self.patterns=patterns
        self.skippedRecords=[]
        self.modifiedRecrods=[]
        self.currentProcessedFilePath=""
        self.currentProcessedLineNo=""
        self.currentProcessedLineTxt=""
        self.currentProcessedRecord=None



    def getCurrentProcessedRecord(self,skipFileDetails=False):
        if skipFileDetails:
            return Record(self.currentProcessedFilePath,"ALL","ALL")
        return Record(self.currentProcessedFilePath,self.currentProcessedLineNo,self.currentProcessedLineTxt)

# def rlinput(prompt, prefill=''):
#    readline.set_startup_hook(lambda: readline.insert_text(prefill))
#    try:
#       return input(prompt)
#    finally:
#       readline.set_startup_hook()

    def read_acceptance(self):
        while True:
            choice=input("Do you accept this modification?[Y|S]")
            if choice.lower()=="y":
                return True
            if choice.lower()=="s":
                return False

    def prompt_line_Change(self,pre_line,post_lines):
        print("Current Matching Line :\n "+pre_line)
        print("Suggested Modification:\n")
        for post_line in post_lines:
            print (post_line)
        accept=self.read_acceptance()
        resultLines=[pre_line]
        if not accept:
            self.skippedRecords.append(self.getCurrentProcessedRecord())
        #while not accept:
              #post_line=rlinput("Please Edit :\n",post_lines)
              #accept=read_acceptance()
        else:
            self.modifiedRecrods.append(self.getCurrentProcessedRecord())
            resultLines=post_lines
        return resultLines

    def get_buffered_lines_indexes(self,lines,pos,window=5):
        if pos<0 or pos>len(lines):
            return null

        start_index=pos-((window-1)/2)
        if start_index<0:
           start_index=0
        end_index=pos+((window-1)/2)
        if end_index>len(lines):
           end_index=len(lines)
        return int(start_index),int(end_index)

    def clearScr(self):
        if OS_IS_WIN:
            os.system('cls')
        else:
            os.system('clear')

    def draw_file_contents(self,filepath,lines,pos):
        self.clearScr()
        print("File Contents:"+filepath)
        print("---------------")
        start_index,end_index=self.get_buffered_lines_indexes(lines,pos,5)
        for index in range(start_index,end_index):
            if index==pos:
                if OS_IS_WIN:
                   print (lines[index])
                else:
                   print (bcolors.OKBLUE+lines[index]+bcolors.ENDC)
            else:
                print(lines[index])
        print("=======================================================================================================================")

    def is_matching_line(self,line,patterns):
        for pattern in patterns :
            if  re.search(pattern, line.lower(),re.IGNORECASE):
                return pattern
        return None

    def get_suggested_line(self,line,matched_pattern,count=1):

        startIndex=line.find(matched_pattern)
        if(startIndex!=-1):
            endIndex=line.find('"',startIndex)
            leadingSpacesNo=len(line) - len(line.lstrip())
            if OS_IS_WIN:
                leadingSpacesTxt=" ".join(" " for i in range(0,leadingSpacesNo))
            else:
                leadingSpacesTxt=" ".join("\t" for i in range(0,leadingSpacesNo))
            convTemplate="""<cfinvoke component="NBP.NetBiosProxyHelper" method="getTemplatePathForACWithEncryptedValue" fileName="{1}" returnvariable="{0}" />"""
            replaceToken="#encryptedValue"+str(count)+"#"
            textToBeReplaced=line[startIndex:endIndex]
            convLine=convTemplate.format(replaceToken,textToBeReplaced)
            new_line=line[0:startIndex]+replaceToken+line[endIndex:len(line)]
            convLine=leadingSpacesTxt+convLine
            B
            return [convLine,leadingSpacesTxt+"<cfoutput>",new_line,leadingSpacesTxt+"</cfoutput>"]
        else:
            print ("invalid processing ")
            return ["ERROR!! : unable to retreive this line suggesstions!!"]

    def is_file_contains_Patterns(self,patterns,filepath):
        lines=[]
        try:
            lines=open(filepath,"r").readlines()
        except:
            print("unable to read/parse file "+filepath)
            return False
        for line in lines:
            if self.is_matching_line(line,patterns):
                return True
        return False

    def prompt_file_Change(self,filepath):
        print("File:"+filepath)
        print("is matching with one or more patterns, it'll be edited")
        accept=self.read_acceptance()
        if accept:
            B
            return True
        return False

    def process_file(self,patterns,filepath):
        print ("Scanning File :"+filepath)
        self.currentProcessedFilePath=filepath
        isMatchingFile=self.is_file_contains_Patterns(self.patterns,filepath)
        if not isMatchingFile:
            return
        else:
            if not self.prompt_file_Change(filepath):
                self.skippedRecords.append(self.getCurrentProcessedRecord(True))
                return
        #start editing file
        old_lines=open(filepath,"r").readlines()
        new_lines=[]
        count=1 #counter for current changes in file
        for pos in range(len(old_lines)):
            line=old_lines[pos]
            self.currentProcessedLineNo=pos
            self.currentProcessedLineTxt=line
            matched_pattern=self.is_matching_line(line,self.patterns)
            if matched_pattern :
                self.draw_file_contents(filepath,old_lines,pos)
                pre_line=line
                post_lines=self.get_suggested_line(pre_line,matched_pattern,count)
                post_lines=self.prompt_line_Change(pre_line,post_lines)
                new_lines.extend(post_lines)
                count+=1
            else:
             new_lines.append(line+"\n")
        output=open(filepath,"w")
        output.write("\n".join(new_lines))


    def process_Files(self):
        print ("Starting Python processing")
        for filepath in self.filepaths:
            self.process_file(self.patterns,filepath)


    def printSkippedRecords(self):
        print ("Skipped Lines :")
        for record in self.skippedRecords:
            print ( record.file_path +"||"+str(record.line_number)+"||"+record.line[:100] )

    def printModifiedRecords(self):
        print ("Modified Lines :")
        for record in self.modifiedRecrods:
            print ( record.file_path +"||"+str(record.line_number)+"||"+record.line[:100] )


#To retreive encrypted value via Restful call
    def getEncryptedUrl(self,url):
        url=""
        params = urllib.urlencode({'@url': url})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection(url)
        conn.request("POST", "", params, headers)
        response = conn.getresponse()
        print (response.status)
        data = response.read()

def get_filepaths(directory,includePatterns,skip_patterns):
    print("building file paths recursively ... ")
    file_paths = []  # List which will store all of the full filepaths.
    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            for includePattern in includePatterns:
                if includePattern in filepath:
                    skipFlag=False
                    for skip_pattern in skip_patterns:
                        if skip_pattern  in filepath:
                            skipFlag=True
                    if not skipFlag :
                        file_paths.append(filepath)
    return file_paths

# Start of the Script
parser = argparse.ArgumentParser()
parser.add_argument("path", help="directory path to start scanning ")
parser.add_argument("-p","--pattern",nargs = '*' , help="list of pattern(s) to match ,please refer to Python Regex documentation .Default:'/download/' '/manuals' '/HelpDoc' '/reports/'",action="append",default=[["/download/","/manuals","/HelpDoc","/reports/"]])

args = parser.parse_args()
DIR_PATH=args.path
PATTERNS=args.pattern
if "nt" in os.name:
    print ("Detected Windows like OS")
    OS_IS_WIN=True

full_file_paths = get_filepaths(DIR_PATH,[".cfm","cfc"],[".svn",".git"])
processor=FileProcessor(full_file_paths,PATTERNS[-1])  # -1  to always get the last , as if parm is submitted it's appended
processor.process_Files()
processor.printSkippedRecords()
processor.printModifiedRecords()
print ("DONE")


