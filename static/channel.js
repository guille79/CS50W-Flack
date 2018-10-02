document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure input form
    socket.on('connect', () => {
     
        // By default, submit button is disabled
        document.querySelector('#submit').disabled = true;

        // Enable button only if there is text in the input field
        document.querySelector('#message').onkeyup = () => {
            if (document.querySelector('#message').value.length > 0)
                document.querySelector('#submit').disabled = false;
            else
                document.querySelector('#submit').disabled = true;
        }; 
    
        document.querySelector('#new-message').onsubmit = () => {
      
            // submit text of new message to server
            const text = document.querySelector('#message').value;
            socket.emit('submit message', {'text': text});
            
            // Clear input field and disable button again
            document.querySelector('#message').value = '';
            document.querySelector('#submit').disabled = true;

            // Stop form from submitting
            return false;
        };
    
    });

    // When a new vote is announced, add to the unordered list
    socket.on('publish message', msg => {
        const li = document.createElement('li');
        li.innerHTML = `${msg.author}: ${msg.text}, ${msg.time}`;
        document.querySelector('#messages').append(li);
    });    
});

