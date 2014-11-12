<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">





<html>


<head>


	<title>Agent Center</title>


</head>


<link rel="stylesheet" type="text/css" href="../templates/agentcenter.css"><body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">


<cfset title = "Welcome to Allied General Agency!">


<cfinclude template="topFrame.cfm">


          <span class="svshead">Agency Agreement & Agency Questionnaire</span>


              


                <table width="212" height="70" border="0" align="right"  cellpadding="0" cellspacing="0"><br>


			<tr>


                    <td align="right" valign="top"><div align="right"><img src="allied_logo.jpg" width="200" height="72"></div></td>


				  </tr>


					</table>


                <br><br>Thank you for your interest in Allied General Agency.<br><br>


				We can quote but AGA can't bind any business for your agency until we receive your completed Agency Agreement, Agency Questionnaire and W-9.<br><br>


				If you would like an original document returned to you please sign and forward two signed contracts otherwise fax the completed and signed documents as indicated below. A copy of the executed documents will be sent to you.<br><br>


	 	 	 	<cfinvoke component="NBP.NetBiosProxyHelper" method="getTemplatePathForACWithEncryptedValue" fileName="/download/Forms/AGA/ACGAGRE.pdf" returnvariable="#encryptedValue1#" />
	 	 	 	<cfoutput>
				<a href="#encryptedValue1#" target="_blank">AGA Agency Agreement</a><br>

	 	 	 	</cfoutput>
	 	 	 	<cfinvoke component="NBP.NetBiosProxyHelper" method="getTemplatePathForACWithEncryptedValue" fileName="/download/Forms/AGA/AGENCY QUESTIONNAIRE.pdf" returnvariable="#encryptedValue2#" />
	 	 	 	<cfoutput>
				<a href="#encryptedValue2#" target="_blank">Agency Questionnaire</a><br>

	 	 	 	</cfoutput>
	 	 	 	<cfinvoke component="NBP.NetBiosProxyHelper" method="getTemplatePathForACWithEncryptedValue" fileName="/download/Forms/AGA/w9.pdf" returnvariable="#encryptedValue3#" />
	 	 	 	<cfoutput>
				<a href="#encryptedValue3#" target="_blank">Tax Form W-9</a><br>

	 	 	 	</cfoutput>
				<br>


				Allied General Agency<br>


				1100 Locust St. Dept 2002<br>


				Des Moines, IA. 50391-2002<br>    


				FAX 866-433-4331<br><br>


				If you have any questions please call us at 888-364-3434 or E-mail us at <a href="mailto:AlliedGA@nationwide.com">AlliedGA@nationwide.com</a> 


 





              <blockquote>


  <p>&nbsp;</p></blockquote>


            </blockquote>


				</td>


					</tr>








<cfinclude template="bottomFrame.cfm">


</body>


</html>

