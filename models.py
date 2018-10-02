from datetime import datetime 
        
class Channel:
    channels = []
    counter = 0
    
    def __init__(self, name, creator):
        self.id = Channel.counter
        self.name = name
        self.creator = creator
        self.messages =  []
        Channel.counter += 1
        Channel.channels.append(self)        
        
    def send_message(self, new_message):
        self.messages.append(new_message)   
        while len(self.messages) > 100:
            self.messages.remove(self.messages[0]) 
            # are we deleting wholefully the old messages?

        
class Message:

    def __init__(self, text, author):
        self.text = text
        self.author = author
        self.timestamp = datetime.utcnow().timestamp() 
        

