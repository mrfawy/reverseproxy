#import readline
import http.client, urllib
import os
import re
import argparse
import lineProcessors

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
            choice=input("Do you accept this modification?[Y|N]")
            if choice.lower()=="y":
                return True
            if choice.lower()=="n":
                return False

    def prompt_line_Change(self,pre_line,post_lines,isValidSuggestion):
        print("Current Matching Line :\n "+pre_line)
        print("Suggested Modification:\n")

        for post_line in post_lines:
            print (post_line)
        resultLines=[pre_line]
        if not isValidSuggestion:
            choice=input("Skipping forward,press any key to continue ,...")
            self.skippedRecords.append(self.getCurrentProcessedRecord())
        else:
            accept=self.read_acceptance()
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

        lineProcessorList=[ lineProcessors.SimpleColdFusionLinkProcessor(OS_IS_WIN),lineProcessors.CFJSOpenNeWWindowLinkProcessor(OS_IS_WIN),lineProcessors.CFJSOpenNeWWindowCFSETProcessor(OS_IS_WIN)]
        matchedLineProcessorsNum=0
        for lineProcessor in lineProcessorList:
            if lineProcessor.accepts(line,matched_pattern,self.currentProcessedFilePath):
                lastMatchedLineProcessor=lineProcessor
                matchedLineProcessorsNum+=1
        #more than a match with line processors , they should be disjoint
        if matchedLineProcessorsNum>1:
                print("Error: multiple line seggesion matches , please check your acceptance criteria")
                return {"successFlag":False,"postLines":[]}
        # no matched line processors
        if matchedLineProcessorsNum == 0:
                print("Error : can't match suggestion for this line,no suggestions available !!")
                return {"successFlag":False,"postLines":[]}
        else:
            return lastMatchedLineProcessor.get_suggested_modification(line,matched_pattern,count)

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
                resultMap=self.get_suggested_line(pre_line,matched_pattern,count)
                post_lines=self.prompt_line_Change(pre_line,resultMap["postLines"],resultMap["successFlag"])
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
parser.add_argument("-f","--file" ,help="file path to start scanning ")
parser.add_argument("-d","--dir", help="directory path to start scanning ")
parser.add_argument("-t","--pattern",nargs = '*' , help="list of pattern(s) to match ,please refer to Python Regex documentation .Default:'/download/' '/manuals' '/HelpDoc' '/reports/'",action="append",default=[["/download/","/manuals","/HelpDoc","/reports/"]])

args = parser.parse_args()
DIR_PATH=args.dir
FILE_PATH=args.file
if DIR_PATH ==None and FILE_PATH == None:
    print("Missing arguments, please specify at least a file with -f argument , or a dir in - p argument")
    exit(1)
PATTERNS=args.pattern
if "nt" in os.name:
    print ("Detected Windows like OS")
    OS_IS_WIN=True
full_file_paths=[]
if DIR_PATH :
    full_file_paths = get_filepaths(DIR_PATH,[".cfm","cfc"],[".svn",".git"])
if FILE_PATH :
    full_file_paths.append(FILE_PATH)
processor=FileProcessor(full_file_paths,PATTERNS[-1])  # -1  to always get the last , as if parm is submitted it's appended
processor.process_Files()
processor.printSkippedRecords()
processor.printModifiedRecords()
print ("DONE")


