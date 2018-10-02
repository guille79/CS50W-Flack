document.addEventListener('DOMContentLoaded', () => {
    // By default, submit button is disabled
    document.querySelector('#submit').disabled = true;

    // Enable button only if there is text in the input field
    document.querySelector('#field').onkeyup = () => {
        if (document.querySelector('#field').value.length > 0)
            document.querySelector('#submit').disabled = false;
        else
            document.querySelector('#submit').disabled = true;
    };
});
