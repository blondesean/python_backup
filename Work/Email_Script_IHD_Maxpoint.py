
import smtplib
import mimetypes
import os
import openpyxl
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

''' ------------ CHECK THE INPUTS BELOW THIS LINE ------------'''

#Login information for email server
emailfrom = "sduncan@geico.com"
password = "Qwerty12"
fromName = "Sean Duncan"

#Address the emails, seperate by commas, if only GFR type "GFR Only", if no CC type "No CC"
emailTo = "GFR Only"
ccEmails = "swise@geico.com, kegreen@geico.com, kjowaisas@geico.com"

#Invoice Recipients
invIHD = "Sarah Wise"
invSM = "Kevin Green"

#Import information to include
dueDate = "July 10, 2017"

#Construct file location string 1 Performance 2 IHD 3 Shared Mail 4 Maxpoint
fileLocation1 = "\\\\chnas06\\MKT-Data\\GFR\\GFR Internet\\DISPLAY\\Invoices\\Metrics\\"
fileLocation2 = "\\\\chnas06\\MKT-Data\\GFR\\GFR Advertising\\Invoice Tracking\\Display\\Invoices\\"
fileLocation3 = "\\\\chnas06\\MKT-Data\\GFR\\GFR Advertising\\Invoice Tracking\\Inserts\\"
fileYear = "2017"
fileMonth = "6"

#Send files
send1 = False
send2 = False
send3 = True

''' ------------ CHECK THE INPUTS ABOVE THIS LINE ------------'''

''' ------------ FOR DEV TESTING BELOW THIS LINE ------------'''

testing = True
emailLimit = 5
testEmail = "sduncan@geico.com"

''' ------------ FOR DEV TESTING ABOVE THIS LINE ------------'''

''' =========================================================='''

#The Body message 
def body_header(firstName, timePeriod):
    html =      "<html>\
                  <head></head>\
                  <body>\
                    <p>Good Afternoon " + firstName + ",</p>\
                    <p>This email contains various performance and invoice information for " + timePeriod + \
                    ". There should be a file for Display Performance (Display Performance), an In House Display Invoice (IHD) and a Shared Mail Invoice (SM Inv). If you were expecting one of these files and did not receive it, please reachout to your coordinator.</p?"
    return html

#Performance Body
def body_file1(sending):
    html = "        <p></p>\
                    <p><strong><u>DISPLAY PERFORMANCE:</u></strong></p>\
                    Definitions:\
                    <br />&mdash;&nbsp; <strong>Impressions</strong>: generally, when an ad is viewed. Clicking or not is not taken into account for this metric.\
                    <br />&mdash;&nbsp; <strong>Clicks</strong>: when a user clicks on your ad.\
                    <br />&mdash;&nbsp; <strong>Spend</strong>: the total cost of that advertising. In display, spend is on an impression basis.\
                    <br />&mdash;&nbsp; <strong>CTR</strong>: or Click Through Rate. This measures the percentage of users who saw and clicked on your ad. CTR = Clicks / Impressions. During our 3-month in-house display test, we saw an average of <strong>0.13%</strong> CTR. Typically, the mobile CTR is higher than desktop. Anything above 0.06% is good, but the higher CTR, the better!\
                    <br />&mdash;&nbsp; <strong>CPM</strong>: or Cost Per Mille. This is a cost per thousand impressions, or how much your advertising spent per 1,000 impressions. CPM = Spend / Impressions X 1,000. During our in-house test, we saw an average CPM of <strong>$1.93</strong>. CPMs will increase with more specific targeting, such as targeting specific websites, and will likely vary by location. Generally, we&rsquo;re aiming for around a $2.50 or less CPM.\
                    <br />&mdash;&nbsp; <strong>CPC</strong>: or Cost Per Click. This is the average a click cost for your advertising. CPC = Spend / Clicks. During our test, we saw an average CPC of <strong>$1.47</strong>. Generally, we&rsquo;re aiming for around a $3 or less CPC.</p>\
                    <br /><u>Reporting discrepancies</u>\
                    <br />You may notice that the numbers in the chart with your creative information doesn&rsquo;t match the device type or monthly metrics. Reporting discrepancies are normal, as multiple systems and platforms are used to measure these data sets.\
                    <br />&mdash;&nbsp; The result by creative chart uses the ad serving system, which collects information when an ad is served. False impressions could be recorded here.\
                    <br />&mdash;&nbsp; Monthly and by device results use the bid manager platform, which contains more information about your campaigns. This platform will automatically back out false impressions and clicks. Invalid or false impressions or clicks may be from bots or other spam-like behavior."
    if (sending):
        return html
    else:
        return ""

#IHD Body
def body_file2(geico_contact, due_date, otherBody, sending):
    if otherBody:
        html = body_spacer()
    else:
        html = ""

    html = html + \
           "        <p><strong><u>IN HOUSE DISPLAY INVOICE:</u></strong></p>\
                    <p>Attached is your invoice for your In-House Display campaign. Payment is due by " + due_date + ". Please write your check out to GEICO and send payments to:&nbsp;</p>\
                    <p>GEICO Marketing<br />Attn: " + geico_contact + " <br /> 5260 Western Ave <br /> ChevyChase, MD 20815</p>"

    if (sending):
        return html
    else:
        return ""

#IHD Body
def body_file3(geico_contact, due_date, otherBody, sending):
    if otherBody:
        html = body_spacer()
    else:
        html = ""
        
    html = html + \
           "        <p></p>\
                    <strong><u>SHARED MAIL INVOICE:</u></strong>\
                    <p>Attached is your invoice for your Shared Mail Display campaign. Payment is due by " + due_date + ". Please write your check out to GEICO and send payments to:&nbsp;</p>\
                    <p>GEICO Marketing<br />Attn: " + geico_contact + " <br /> 5260 Western Ave <br /> ChevyChase, MD 20815</p>"

    if (sending):
        return html
    else:
        return ""

#The Body Footer
def body_footer(whoFrom):
    html = body_spacer()
    html =          "<p>Please reach out to your coordinator if you have any questions.</p>\
                    <p>Thank you,<br />" + whoFrom + "</p>\
                  </body>\
                </html>"
    return html

#The Body Footer
def body_spacer():
    html =          "<p></p>"
    return html

#This function will recurisively find the position of a substring in a string
def find_nth(word, substring, iteration, i = 0):
    i = word.find(substring, i)
    if iteration == 1 or i == -1:
        return i 
    else:
        return find_nth(word, substring, iteration - 1, i + len(substring))

#Formats the attachment fed into the 
def prep_attachment(file):
        ctype, encoding = mimetypes.guess_type(file)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(file)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(file, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(file, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(file, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)

        #Format attachment and return
        attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(fileToSend))
        return attachment

def zone_check(df, fname, lname):
    zone_iterator = df.iterrows()
    for i, row in zone_iterator:
        if row.Fname == fname and row.Lname == lname:
            return str(int(row.Zone))
            break

def attn_check(df, fname, lname):
    attn_iterator = df.iterrows()
    for i, row in attn_iterator:
        if row.Fname == fname and row.Lname == lname:
            if row.Mkt_Coordinator == "Matt":
                return "Matthew Block"
            elif row.Mkt_Coordinator == "Kevin":
                return "Kevin Green"
            elif row.Mkt_Coordinator == "Jacob":
                return "Jacob Cash"
            elif row.Mkt_Coordinator == "Sarah":
                return "Sarah Wise"
            else:
                return row.Mkt_Coordinator
            break

def email_check(df, fname, lname):
    email_iterator = df.iterrows()
    for i, row in email_iterator:
        if row.Fname == fname and row.Lname == lname:
            return row.GFR_E_mail_Addr
            break

def zoneMan_check(df, fname, lname):
    zonMan_iterator = df.iterrows()
    for i, row in zonMan_iterator:
        if row.Fname == fname and row.Lname == lname:
            return row.ZM

def zoneMan_email(df, lname):
    zonMan_iterator = df.iterrows()
    for i, row in zonMan_iterator:
        if row.Lname == lname:
            return row.Email

def month_check(month_number):
    if month_number == "1":
        temp = "January"
    elif month_number == "2":
        temp = "February"
    elif month_number == "3":
        return "March"
    elif month_number == "4":
        return "April"
    elif month_number == "5":
        return "May"
    elif month_number == "6":
        return "June"
    elif month_number == "7":
        return "July"
    elif month_number == "8":
        return "August"
    elif month_number == "9":
        return "September"
    elif month_number == "10":
        return "October"
    elif month_number == "11":
        return "November"
    elif month_number == "12":
        return "December"
    else:
        return "Unknown"

''' =========================================================='''

###Cycle through GFRs, send them an email with all available attachements
#Change the directory to the performance metrics file
#os.chdir("\\\\chnas06\\MKT-Data\\GFR\\GFR Internet\\DISPLAY\\Invoices\\Metrics\\" + fileYear + "_" + fileMonth)

#Open the contact database, eliminate useless rows, format as panda data frame
contactDB = pd.read_excel('\\\\chnas06\\MKT-Data\\GFR\\GFR Contact\\GFR Contact Database.xlsm', sheetname = "GFR", skiprows = 2)
contactDB = contactDB[contactDB.Count.notnull()]
contactDB = contactDB[contactDB.Lname.notnull()]
contactDB = contactDB[contactDB.Lname != "<<"]
contactDB.columns = [c.replace(' ', '_') for c in contactDB.columns]
contactDB.columns = [c.replace('-', '_') for c in contactDB.columns]

#Open the zone manager database, eliminate useless rows, format as panda data frome
zoneManDB = pd.read_excel('\\\\chnas06\\MKT-Data\\GFR\\GFR Contact\\GFR Contact Database.xlsm', sheetname = "ZM", skiprows = 6)
zoneManDB = zoneManDB[zoneManDB.Lname.notnull()]
zoneManDB = zoneManDB[zoneManDB.Lname != "<<"]
zoneManDB.columns = [c.replace(' ', '_') for c in zoneManDB.columns]
zoneManDB.columns = [c.replace('-', '_') for c in zoneManDB.columns]
zoneManDB.columns = [c.replace('&', '_') for c in zoneManDB.columns]
zoneManDB.columns = [c.replace('#', '_') for c in zoneManDB.columns]
zoneManDB.columns = [c.replace('___', '_') for c in zoneManDB.columns]

#Incase format for month is long
if len(fileMonth) == 1:
    longFileMonth = "0" + fileMonth
else:
    longFileMonth = fileMonth

#Log in to the cavemail server
server = smtplib.SMTP("Cavemail.geico.net")
server.starttls()
server.login(emailfrom,password)

#Print where are we checking for these files?
print("--------------------------------------------------")
print("Display Performance Location: " + fileLocation1)
print("IHD Invoice Location:         " + fileLocation2)
print("Shared Mail Invoice Location: " + fileLocation3)
print("--------------------------------------------------")

#iterate through our GFRs and send the 3 files if they have them
GFR_iterator = contactDB.iterrows()
for i, row in GFR_iterator:
    #For testing set i <= the amount of emails you wish to send
    if (i <= emailLimit or not testing):
        #Assume no files need to be sent
        worthSending = False

        #Get the name of the next GFR
        fileGFR = row.Fname + " " + row.Lname
        print("--- Now sending email for " + fileGFR + " ---")

        #Get the name of the attn
        attn = attn_check(contactDB, row.Fname, row.Lname)
        
        #Get the GFR zone
        zone = zone_check(contactDB, row.Fname, row.Lname)
        #Formatting for pathnames with Zone
        if len(str(zone)) == 1:
            longZone = "0" + zone
        else:
            longZone = zone

        #get the GFR email
        gfr_Email = email_check(contactDB, row.Fname, row.Lname)

        #Zone Manager info
        zoneMan = zoneMan_check(contactDB, row.Fname, row.Lname)
        zoneManEmail = zoneMan_email(zoneManDB, zoneMan)

        #do we have the correct information?
        print(i," The GEICO contact is " + attn + ', the zone is ' + zone + ', their email is ' + gfr_Email)

        #Who is receiving this?
        if emailTo == "GFR Only":
            emailTo = gfr_Email 
        else:
            emailTo = gfr_Email + ', ' + emailTo

        if ccEmails == "No CC":
            ccEmails = zoneManEmail
        else:
            ccEmails = zoneManEmail + ', ' + ccEmails
        
         #Create list to deliver to  
        receiving = (emailTo + ", " + ccEmails).split(', ')

        #Construct email for next GFR
        #Declare the email and fill out basic information
        msg = MIMEMultipart()
        msg["From"] = emailfrom 
        msg["To"] = emailTo
        msg["CC"] = ccEmails

        #msg["CC"] = zoneManger_Email
        msg["Subject"] = "Test GFR Monthly Results"
        msg.preamble = "Sent from Python, Uses MIME formatting standards"

        #Start message body
        html = body_header(row.Fname, month_check(fileMonth) + " " + fileYear)

        #Add the performance metrics to the file
        fileToSend = fileLocation1 + fileYear + "_" + fileMonth + "\\" + fileYear + " " + fileMonth + " " + fileGFR + " Display Performance.xlsx"
        if (os.path.isfile(fileToSend) and send1):
            attachment = prep_attachment(fileToSend)
            msg.attach(attachment)
            print("    Attached Performance Metrics File = " + fileToSend[len(fileLocation1)-1:])
            worthSending = True
            html = html + body_file1(send1)
        elif (not send1):
            print("    NSF: Performance Metrics File = " + fileToSend[len(fileLocation1)-1:])
        else:
            print("    DNE: Performance Metrics File = " + fileToSend[len(fileLocation1)-1:])

        #Add IHD Invoice 
        fileToSend = fileLocation2 + fileYear + "\\" + longFileMonth + " " + month_check(fileMonth) + " " + fileYear + "\\" + longZone + "\\IHD " + month_check(fileMonth) + " " + fileYear + " " + row.Lname + " " + row.Fname + " " + row.ST + ".xls"
        if (os.path.isfile(fileToSend) and send2):
            attachment = prep_attachment(fileToSend)
            msg.attach(attachment)
            print("    Attached Invoice = " + fileToSend[len(fileLocation2)-1:])
            html = html + body_file2(invIHD, dueDate, worthSending, send2)
            worthSending = True
        elif (not send2):
            print("    NSF: Invoice = " + fileToSend[len(fileLocation2)-1:])
        else:
            print("    DNE: Invoice = " + fileToSend[len(fileLocation2)-1:])

        #Add Sharedmail Invoice 
        fileToSend = fileLocation3 + fileYear + " Shared Mail Invoices\\" + month_check(fileMonth) + "\\" + zone + " - " + zoneMan + "\\" + row.Lname + " " + row.Fname + " SM Inv " + month_check(fileMonth)[:3] + " " + fileYear + " " + row.ST + ".xls"
        if (os.path.isfile(fileToSend) and send3):
            attachment = prep_attachment(fileToSend)
            msg.attach(attachment)
            print("    Attached Invoice = " + fileToSend[len(fileLocation3)-1:])
            html = html + body_file3(invSM, dueDate, worthSending, send3)
            worthSending = True
        elif (not send3):
            print("    NSF: Invoice = " + fileToSend[len(fileLocation3)-1:])
        else:
            print("    DNE: Invoice = " + fileToSend[len(fileLocation3)-1:])

        #Add Email Footer
        html = html + body_footer(fromName)

        #Convert to MIME format
        htmlBody = MIMEText(html, 'html')

        #Attach the created text
        msg.attach(htmlBody)

        #Send the email
        if (worthSending and not testing):
            server.sendmail(emailfrom, receiving, msg.as_string())
            print("--- Email Sent to " + ', '.join(receiving) + " ---")
            print("--- TO: " + emailTo + " | CC: " + ccEmails)
        elif (worthSending and testing):
            server.sendmail(emailfrom, testEmail, msg.as_string())
            print("--- Email Sent to " + testEmail + " ---")
        else:
            print("--- No Email Sent ---")

#Logout to end
server.quit()


