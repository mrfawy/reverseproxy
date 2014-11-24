import re


class LineProcessor:

    def __init__(self,OS_IS_WIN):
        self.OS_IS_WIN=OS_IS_WIN
    def accepts(line):
        return True

# return a map {SuccessFlag:"True when suggestions exist",PostLins:[array of new lines]}
    def get_suggested_modification(self,line,matched_pattern,count=1):
        return line


"""
handles <a href="simpletext" /> in CF files
no Id is defined for the tag , no java sript of any kind exists
"""

class SimpleColdFusionLinkProcessor(LineProcessor):

    def __init__(self,OS_IS_WIN):
        LineProcessor.__init__(self,OS_IS_WIN)

    def accepts(self,line,matched_pattern,filepath):
        #check if file is a coldFusion
        if not (filepath.endswith(".cfc") or filepath.endswith(".cfm")):
            return False
        if "href" not in line.lower():
            return False
        #check no java script exists in the line
        if "window" in line.lower():
            return False
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
            return {"successFlag":True,"postLines":[convLine,leadingSpacesTxt+"<cfoutput>",new_line,leadingSpacesTxt+"</cfoutput>"]}
        else:
            print ("ERROR!! : unable to retreive this line suggesstions!!")
            return {"successFlag":False,"postlines":[]}


"""
handles <a id="47_1" href="javascript:openNewWindow('/download/tutorials/Application_Submit_viewlet_swf.html','','');">
FileType :CF:
link exist in a CF file ,Id can exist

"""

class CFJSOpenNeWWindowLinkProcessor(LineProcessor):

    def __init__(self,OS_IS_WIN):
        LineProcessor.__init__(self,OS_IS_WIN)

    def lineHasId(self,line):
        if "id=" in line:
            return True
        return False


    def accepts(self,line,matched_pattern,filepath):
        #check if file is a coldFusion
        if not (filepath.endswith(".cfc") or filepath.endswith(".cfm")):
            return False

        if "href" not in line.lower():
            return False
        #check javascript:openWindow or open new window exists in the line
        if re.match("javascript:open(New)?Window",line):
            return False
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
            replaceToken="encryptedValue"+str(count)
            hyberlinkTagIndex=line.find("<a")
            hrefAtrrIndex=line.find("href",hyberlinkTagIndex)
            hrefEqualSignIndex=line.find("=",hrefAtrrIndex)
            hrefOpeningQtIndex=line.find("\"",hrefAtrrIndex)
            hrefClosingQtIndex=line.find("\"",hrefOpeningQtIndex)
            jsopenIndex=line.find("javascript:open",hyberlinkTagIndex)
            hrefContentStartIndex=line.find("'",jsopenIndex)
            hrefContentEndIndex=line.find("'",hrefContentStartIndex+1)
            filepath=line[hrefContentStartIndex+1:hrefContentEndIndex]
            jsEndIndex=line.find(";",hrefContentEndIndex)#js ends with ';'
            idToken=""
            # if not self.lineHasId(line):
            #     idToken=" id=\"cfLinkId"+str(count)+"\" "
            #     new_line=line[0:hyberlinkTagIndex+2]+idToken+line[hrefAtrrIndex:hrefContentStartIndex+1]+"#"+replaceToken+"#"+line[jsEndIndex:len(line)]
            convLine=convTemplate.format(replaceToken,filepath)
            new_line=line[0:hrefEqualSignIndex+2]+"#"+replaceToken+"#"+line[jsEndIndex+1:len(line)]
            convLine=leadingSpacesTxt+convLine
            return {"successFlag":True,"postLines":[convLine,leadingSpacesTxt+"<cfoutput>",new_line,leadingSpacesTxt+"</cfoutput>"]}

        else:
            print ("ERROR!! : unable to retreive this line suggesstions!!")
            return {"successFlag":False,"postLines":[]}

