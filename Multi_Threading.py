#!/usr/bin/python

import thread
import time

# Define a function for the thread
def print_time( threadName, delay):
  count = 0
  while count < 30:
    time.sleep(delay)
    count += 1
    print "%s: %s" % ( threadName, time.ctime(time.time()) )
  return delay

# Create two threads as follows
try:
   thread.start_new_thread( print_time, ("Thread-1", 1, ) )
   thread.start_new_thread( print_time, ("Thread-2", 3, ) )
except:
   print "Error: unable to start thread"

while 1:
   pass