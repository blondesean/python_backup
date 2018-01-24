#import the libraries we need
import urllib.request, json, requests, numpy as np
import time
 
#change the pull date for our summarized data
fromYear = 2017
fromMonth = 7
fromDay = 1
toYear = 2017
toMonth = 11
toDay = 30
 
#Other Variables
start_time = time.time()
campaign_ids = [6090752846996,6084720838796,6058485102196,6066604670996,6068736340796,6075026819796,6076358217596,6076368041996,6081079001396,6081591574996,6084829286196,6090752725196,6084876107796,6085815998596,6086019961596,6086304648796,6089276930596,6090529061196,6090529712996,6090752689596,6047532387996]
#campaign_ids = [6058485102196, 6081079001396 ]
save_loc = "\\\\chnas06\\MKT-Data\\INTERNET\\INET Admin\\Sean\\Projects\\API\\Facebook\\"
token = 'EAAUZA23pBp2UBAN1JfaEhiJEeecrXBsFSkusGpncae0EdCbgYk5AW5UmM7G9cOZCs79vo8Mq7GI9RWpxXlv51pkHxnZBj4ESWkDHmvtJWVreSKJf1ugpRh5CuIRkmZCi9GWCwm7cuFgt6i3SbHs79TA6QCua2WD8jfgTwQg6f9m1UR8tZBf5fd2G9fy5lk5oZD'
wait_time = 15 #Seconds
batch_mode = False
 
#the main portions of the URL that won't change
baseURL1 = 'https://graph.facebook.com/v2.10/'
baseURL2 = '/insights?fields=unique_actions&action_breakdowns=action_type&time_range='
endURL = '&action_attribution_window=[“1d_view”,”7d_click”]&access_token='
pull_range = str(fromYear).zfill(2) + "_" + str(fromMonth).zfill(2) + "_" + str(fromDay).zfill(2) + '-' + str(toYear).zfill(2) + "_" + str(toMonth).zfill(2) + "_" + str(toDay).zfill(2)
 
#Function to increment dates
def date_inc(day,month,year):
               #End of year
               if month == 12 and day == 31:
                              year = year + 1
                              month = 1
                              day = 1
               #Months with 31 days, vs 30 (and 28), end of month
               elif (month == 1 or month == 3 or month == 5 or
                                month == 7 or month == 8 or month == 10 or month == 12) and day == 30:
                              day = 31
               elif day >= 30:
                              month = month + 1
                              day = 1
               #Leap year corrections
               elif month == 2:
                              if ((year % 4) == 0 and day < 29) or day < 28:
                                             day = day + 1
                              else:
                                             month = 3
                                             day = 1
               else:
                              day = day + 1
               return day, month, year
 
#declare matrix for data
data = np.array([['Campaign_ID', 'Day', 'Month', 'Year', 'Comments', 'Landing_page_views', 'Link_clicks', 'Offsite_conversion', 'Complete_registration', 'Initiate_Checkout', 'View_contents', 'Page_engagements', 'Likes', 'Posts', 'Post_engagements', 'Post_reactions', 'Video_view']])
 
#Loop through days
run_again = True
while run_again:
               #Loop through campaigns
               for campaign_id in campaign_ids:
 
                              #piece together the final URL
                              if batch_mode == False:
                                             date = "{" + '"since":"' + str(fromYear).zfill(2) + "-" + str(fromMonth).zfill(2) + "-" + str(fromDay).zfill(2) + '","' + 'until":"' + str(fromYear).zfill(2) + "-" + str(fromMonth).zfill(2) + "-" + str(fromDay).zfill(2) + '"}'
                              else:
                                             date = "{" + '"since":"' + str(fromYear).zfill(2) + "-" + str(fromMonth).zfill(2) + "-" + str(fromDay).zfill(2) + '","' + 'until":"' + str(toYear).zfill(2) + "-" + str(toMonth).zfill(2) + "-" + str(toDay).zfill(2) + '"}'
                              finalURL = baseURL1 + str(campaign_id) + baseURL2 + date + endURL + token
                             
                              #grab the json file of our requested data
                              r = requests.get(url=finalURL).json()
                              obj = json.loads(json.dumps(r))
 
                              #if there is no data on the day, skip
                              if len(obj) == 1:
                                             data_returned = False
                                             print("\nSkipping Pulling Results for campaign "  + str(campaign_id) + ", Date = " + date + ".")
                                             print("Problem =", obj['error']['message'])
                              elif len(obj) == 2:
                                             data_returned = False
                                             print("\nSkipping Pulling Results for campaign "  + str(campaign_id) + ", Date = " + date + ".")
                                             print("Problem = Campaign did not exist")
                              else:
                                             data_returned = True
                                             #Built in delay
                                             time.sleep(wait_time)
 
                              #Start looking for the values of interest
                              if data_returned:
                                             print("\nPulling Results for campaign " + str(campaign_id) + ", Date = " + date + ":")
                                            
                                             #Fill in array data with data info according to pull method
                                             if batch_mode == False:
                                                            new_row = np.array([[campaign_id,fromDay,fromMonth,fromYear,0,0,0,0,0,0,0,0,0,0,0,0,0]])
                                             else:
                                                            new_row = np.array([[campaign_id,str(fromDay) + "-" + str(toDay),str(fromMonth) + "-" + str(toMonth),str(fromYear) + "-" + str(toYear),0,0,0,0,0,0,0,0,0,0,0,0,0]])
                                            
                                             #Build the array from the JSON data
                                             for actions in obj['data'][0]['unique_actions']:
                                                            if actions['action_type'] == 'comment':
                                                                           #print("Comments:", actions["value"])
                                                                           new_row[0][4] = actions["value"]
                                                            elif actions['action_type'] == 'landing_page_view':
                                                                           #print("Landing Page Views:", actions["value"])
                                                                           new_row[0][5] = actions["value"]
                                                            elif actions['action_type'] == 'link_click':
                                                                           #print("Link clicks:", actions["value"])
                                                                           new_row[0][6] = actions["value"]
                                                            elif actions['action_type'] == 'offsite_conversion':
                                                                           #print("Off-site Conversions:", actions["value"])
                                                                           new_row[0][7] = actions["value"]
                                                            elif actions['action_type'] == 'offsite_conversion.fb_pixel_complete_registration':
                                                                           #print("Complete registrations:", actions["value"])
                                                                           new_row[0][8] = actions["value"]
                                                            elif actions['action_type'] == 'offsite_conversion.fb_pixel_initiate_checkout':
                                                                           #print("Initiate checkouts:", actions["value"])
                                                                           new_row[0][9] = actions["value"]
                                                            elif actions['action_type'] == 'offsite_conversion.fb_pixel_view_content':
                                                                           #print("View contents:", actions["value"])
                                                                           new_row[0][10] = actions["value"]
                                                            elif actions['action_type'] == 'page_engagement':
                                                                           #print("Page engagements:", actions["value"])
                                                                           new_row[0][11] = actions["value"]
                                                            elif actions['action_type'] == 'like':
                                                                           #print("Likes:", actions["value"])
                                                                           new_row[0][12] = actions["value"]
                                                            elif actions['action_type'] == 'post':
                                                                           #print("Posts:", actions["value"])
                                                                           new_row[0][13] = actions["value"]
                                                            elif actions['action_type'] == 'post_engagement':
                                                                           #print("Post engagements:", actions["value"])
                                                                           new_row[0][14] = actions["value"]
                                                            elif actions['action_type'] == 'post_reaction':
                                                                           #print("Post reactions:", actions["value"])
                                                                           new_row[0][15] = actions["value"]
                                                            elif actions['action_type'] == 'video_view':
                                                                           #print("Video views:", actions["value"])
                                                                           new_row[0][16] = actions["value"]
                                                            else:
                                                                           print("Unknown Action", actions['action_type'])
 
                                             #Add the data to the matrix
                                             print(new_row)
                                             data = np.concatenate((data,new_row))
                             
               #Year supersedes month, month supersedes day, if from day (or other) > to day then end
               if batch_mode == True:
                              run_again = False
               elif fromYear < toYear :
                              run_again = True
               else:
                              if fromMonth < toMonth:
                                             run_again = True
                              else:
                                             if fromDay < toDay:
                                                            run_again = True
                                             else:
                                                            run_again = False
 
               #Increment the day, check if we need to run again
               fromDay, fromMonth, fromYear = date_inc(fromDay, fromMonth, fromYear)
 
#View the result
print('\n', data)
 
#Create a .csv from the results
if batch_mode == True:
               tag = "Facebook_BatchAPI_Pull_"
else:
               tag = "Facebook_API_Pull_"
np.savetxt(save_loc + tag + pull_range + ".csv", data, delimiter=",", fmt='%s')
 
#Done, let user know
print("\nSaved data in " + save_loc + tag + pull_range + ".csv", "\nRun took " + str(round(((time.time() - start_time)/60),2)) + " minutes to Complete.")
