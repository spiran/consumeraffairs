Django Project

This project contains the eye service, an application that collect events from other applications.

Using Django-rest-framework + APIView to collect post events.

Events with same session_id are stored in the same session, with key=session_id. Events in a session are list items. 
Τhe list is being converted with json and stored as session value.

Events in a Session are sequential and ordered by the time they occurred. Τhis is achieved by comparing the events timestamp and inserting the event in the corresponding position in the list by descending order. 

Using TokenAuthentication applications will be recognized as "trusted clients" to "The Eye".

Using atomic API to avoid race conditions and control database transactions.

eye app files:

 views.py

 functions

-collector: This is the main function. Αll processes take place in this function.
 
 url: http://yourdomain.com/eye/collector

-getSession: Return specific session by session_id.
 
 url: http://yourdomain.com/eye/event

-catEvents: Return events by specific category.
 
 url: http://yourdomain.com/eye/category-events

-timeRangeEvents: Return events between time range.
 
 url: http://yourdomain.com/eye/range-events

-invalidTimestamp: Return events with invalid timestamp.
 
 url: http://yourdomain.com/eye/invalid-time
  
Usage:

Visit django admin and create user. A Token will be created.

username: consaffair

password: cons1984

Send requests for example with Postman.

Request method: POST

Body:

{
  "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25424",
  "category": "form interaction",
  "name": "submit",
  "data": {
    "host": "www.consumeraffairs.com",
    "path": "/",
    "form": {
      "first_name": "George",
      "last_name": "Doe"
    }
  },
  "timestamp": "2022-01-09 09:15:27.243860"
}

Headers:

Add: Authorization Token 'your_token'


Query events:
You can query events easily using Session model.
Use getSession, catEvents, timeRangeEvents, invalidTimestamp as example.











