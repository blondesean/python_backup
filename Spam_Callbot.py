# Download the library from twilio.com/docs/libraries
from twilio.rest import Client

#Send call or text
textorcall = "Text"

# Get these credentials from http://twilio.com/user/account
account_sid = "AC971502147e6c342b91ea2f38bea1fd5b"
auth_token = "3634d60647507a239ad8eb3d9f5027ab"
client = Client(account_sid, auth_token)

#Send a Text
while (textorcall == "Text"):
  client.messages.create(
      to="+12404772332"
      ,from_="+12406541592"
      ,body="This is a test text.")
      #,media_url="https://c1.staticflickr.com/3/2899/14341091933_1e92e62d12_b.jpg"


#Make the call
if (textorcall == "Call"):
  call = client.api.account.calls\
      .create(to="+12404772332",  # Any phone number
              from_="+12406541592", # Must be a valid Twilio number
              url='http://demo.twilio.com/docs/voice.xml')
  print(call.sid)