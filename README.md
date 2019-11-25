# Secret-Santa
Sends out text messages to a group of people to anonymously select who is buying for whom for Christmas.


What I learned from writing this:

    • How to utilize email-to-text technology from major phone carriers
    
    • How to forge an email correctly via code so that it isn't marked as spam by email servers
    
    • Praticed writing readable, maintable code (with comments, but not too many comments)
 

Usage:

client = SECRET_SANTA('zach@gmail.com', 'myGmailPasswordHere')
client.Main()


Notes:

Create a txt file in the same directory as the Secret Santa.py file.  Fill this text file with the names, numbers, and phone carriers for each person participating in the Secret Santa gift exchange.  Format it like so:

Zach, 5025551234, verizon
John, 3305551234, att
Macayla, 9035554433, tmobile
Selena, 4435551234, sprint

There is also a section in the Secret Santa.py file where you can mark who the couples are so that couples are never chosen for each other (since they are buying gifts for each other anyway).
