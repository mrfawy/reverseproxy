import re

#Only handles <a href="simpletext" /> in CF files
class SimpleColdFusionLinkProcessor:

    def __init__(self,OS_IS_WIN):
        self.OS_IS_WIN=OS_IS_WIN

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
            endIndex=line.find('"',startIndex)
            leadingSpacesNo=len(line) - len(line.lstrip())
            if self.OS_IS_WIN:
                leadingSpacesTxt=" ".join(" " for i in range(0,leadingSpacesNo))
            else:
                leadingSpacesTxt=" ".join("\t" for i in range(0,leadingSpacesNo))
            convTemplate="""<cfinvoke component="NBP.NetBiosProxyHelper" method="getTemplatePathForACWithEncryptedValue" fileName="{1}" returnvariable="{0}" />"""
            replaceToken="#encryptedValue"+str(count)+"#"
            textToBeReplaced=line[startIndex:endIndex]
            convLine=convTemplate.format(replaceToken,textToBeReplaced)
            new_line=line[0:startIndex]+replaceToken+line[endIndex:len(line)]
            convLine=leadingSpacesTxt+convLine
            return [convLine,leadingSpacesTxt+"<cfoutput>",new_line,leadingSpacesTxt+"</cfoutput>"]
        else:
            print ("invalid processing ")
            return ["ERROR!! : unable to retreive this line suggesstions!!"]

#Implement similar processors
"""
    class SimpleJavascript:

    def accepts(line):
    if "window.open" in line.lower()
    return True
    def get_suggested_modification(line):
    return line

"""
