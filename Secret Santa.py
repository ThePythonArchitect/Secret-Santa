"""Grabs a list of contacts from a text file,
then randomly assigns names uniquely to other names,
then sends out text messages!

this is for the christmas secret santa gift exchange!
"""


#imports
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


"""
usage:

client = SECRET_SANTA('zach@gmail.com', 'myGmailPassword')
client.Main()

"""


#class to handle logging into the gmail servers
#and sending texts out via email-to-text
class SMS:

    def __init__(self, email, password):

        self.carriers = {
	'att': '@txt.att.net',
	'tmobile': ' @tmomail.net',
	'verizon': '@vtext.com',
	'sprint': '@page.nextel.com',
        'email': '',
        }

        #set our username and password for logging in
        self.username = email
        self.password = password

        #connect and login to the server
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login(self.username, self.password)

        return

    def send(self, to_number, carrier, message):

        """this part actually sends a SMS message
            after we're logged into the gmail servers
        """

        #verify that the to_number is a 10 character string
        assert (
            len(to_number) == 10 and
            type(to_number) == str
            ), "Phone numbers should be a 10 digit string"

        #set the actual email we'll send it to
        to_email = to_number + self.carriers[carrier]

        #forge the message so the receiving email servers
        #dont mark it as spam and block it
        send_message = MIMEMultipart('alternative')
        send_message['Subject'] = 'SMS'
        send_message['From'] = self.username
        send_message['To'] = to_email
        send_message.attach(MIMEText(message + ' ', 'plain'))

        #send the message
        self.server.sendmail(
            from_addr=self.username,
            to_addrs=to_email,
            msg=send_message.as_string())

        return


#class to store the info on each person
class PERSON:

    def __init__(self):

        #set our variables with empty values to help
        #debug if necessary
        self.name = 'no name'
        self.phone = 'no number'
        self.carrier = 'no carrier'
        self.buying_for = 'no one'

        return


#class with all the drawing names logic
class SECRET_SANTA:

    def __init__(self, email, password):

        self.people = []
        #populate this list with couples
        #such as self.couples = {'Zach': 'Rosie',
        #                        'Rosie': 'Zach'}
        #in order to prevent couples for buying for each other
        #since they will get gifts for each other anyway
        #you can also leave this empty!
        self.couples = {}

        return

    def Read_Contacts(self):

        #get the raw data from the txt file
        with open("contacts.txt", "r") as file:
            lines = file.readlines()

        #clean the data and place it in self.people
        for x in lines:

            #create an object to store our data for the person on this line
            person = PERSON()

            #get the index of the commas in this line so we can
            #parse the data correctly
            first_comma_index = x.index(',')
            second_comma_index = x.index(',', first_comma_index+1)

            #collect the data
            person.name = x[:first_comma_index]
            person.phone = x[first_comma_index+1:second_comma_index].lstrip()
            person.carrier = x[second_comma_index+1:]
            #remove the \n character from the carrier if necessary
            if person.carrier[-1] == '\n':
                person.carrier = person.carrier[:-1]
            person.carrier = person.carrier.lstrip().rstrip()

            #append the person object to self.people for later use
            self.people.append(person)

        return

    def Draw_Names(self):

        #this should only be called after Read_Contacts() has been called
        #we have a list of each person in self.people
        #we will loop through our list and assign each person uniquely
        #and randomly to another

        #mark whos name has already been drawn
        already_drawn = []

        #define how many people are being drawn for
        #this must be at least 2 people
        assert len(self.people) > 1, "More people are required"

        #loop through everyone and assign names
        for x in self.people:

            #continue to randomly choice people until we come
            #across someone who hasn't been chosen already
            #someone who isn't buying for themselves or
            #someone who isn't buying for their spouse
            while True:
                chosen_persons_name = random.choice(self.people).name
                if (
                    chosen_persons_name not in already_drawn and
                    x.name != chosen_persons_name
                    ):
                    if x.name in self.couples:
                        if self.couples[x.name] == chosen_persons_name:
                            continue
                    
                    already_drawn.append(chosen_persons_name)
                    x.buying_for = chosen_persons_name
                    break
        return

    def Notify_Everyone(self):

        client = SMS(email, password)

        for x in self.people:

            client.send(
                x.phone, x.carrier,
                        'For the Christmas Gift Exchange, '+
                        f'you are buying for {x.buying_for}'
                )
            print(f'Sent a text to {x.name}.')

        return

    def Test(self):
        
        print('Reading contacts from text file.')
        self.Read_Contacts()
        print('Drawing names.')
        self.Draw_Names()
        print('Display calculated results...')

        for x in self.people:

            print(f'{x.name} is buying for {x.buying_for}')

        print('Done.')
        

    def Main(self):

        print('Reading contacts from text file.')
        self.Read_Contacts()
        print('Drawing names.')
        self.Draw_Names()
        print('Sending out notifications to everyone.')
        self.Notify_Everyone()
        print('Complete.')

        return















