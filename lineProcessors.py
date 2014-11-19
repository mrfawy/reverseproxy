import re


class LineProcessor:

    def __init__(self,OS_IS_WIN):
        self.OS_IS_WIN=OS_IS_WIN
    def accepts(line):
        return True

    def get_suggested_modification(self,line,matched_pattern,count=1):
        return line


"""
Only handles <a href="simpletext" /> in CF files
no Id is defined fot the tag , no java sript of any kind exists
"""

class SimpleColdFusionLinkProcessor(LineProcessor):

    def __init__(self,OS_IS_WIN):
        LineProcessor.__init__(self,OS_IS_WIN)

    def accepts(self,line,matched_pattern,filepath):
        #check if file is a coldFusion
        if not (filepath.endswith(".cfc") or filepath.endswith(".cfm")):
            return False
        #check no java script exists in the line
        if "window.open" in line.lower():
            return False
        print ("INSIDE with ")
        return True

    def get_suggested_modification(self,line,matched_pattern,count=1):
        startIndex=line.find(matched_pattern)
        if(startIndex!=-1):
            leadingSpacesNo=len(line) - len(line.lstrip())
            if self.OS_IS_WIN:
                leadingSpacesTxt=" ".join(" " for i in range(0,leadingSpacesNo))
            else:
                leadingSpacesTxt=" ".join("\t" for i in range(0,leadingSpacesNo))
            convTemplate="""<cfinvoke component="NBP.NetBiosProxyHelper" method="getTemplatePathForACWithEncryptedValue" fileName="{1}" returnvariable="{0}" />"""
            replaceToken="#encryptedValue"+str(count)+"#"
            hyberlinkTagIndex=line.find("<a")
            hrefAtrrIndex=line.find("href",hyberlinkTagIndex)
            hrefContentStartIndex=line.find("\"",hrefAtrrIndex)
            hrefContentEndIndex=line.find("\"",hrefContentStartIndex+1)
            idToken=" id=\"cfLinkId"+str(count)+"\" "
            convLine=convTemplate.format(replaceToken,line[hrefContentStartIndex+1:hrefContentEndIndex])
            new_line=line[0:hyberlinkTagIndex+2]+idToken+line[hrefAtrrIndex:hrefContentStartIndex+1]+replaceToken+line[hrefContentEndIndex:len(line)]
            convLine=leadingSpacesTxt+convLine
            return [convLine,leadingSpacesTxt+"<cfoutput>",new_line,leadingSpacesTxt+"</cfoutput>"]

        else:
            print ("invalid processing ")
            return ["ERROR!! : unable to retreive this line suggesstions!!"]

