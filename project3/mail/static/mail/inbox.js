/* "fetch" sends an HTTP request and returns a promise that will be resolved as a response object.
   There is two ways to pass arguments to "fetch"：
   1. Accept an HTTP request object as an arugument, for example:
	const req = new Request(<URL>, { method: 'GET'});
	fetch(req);
   2. Accept the argument that conforms to construct an HTTP request object , for example:
	fetch(<URL>, { method: 'GET'});

   Construct an HTTP request, for example:
	   const req = new Request(<URL>, {method: <...> , headers: <...>, body: <...>, ...});
   The following is the options inside of the second argument in "Request":
   method：Specify the HTTP request method, such as GET, POST, PUT, etc. and default is GET.
   headers：Any Headers objects you want to add to the request and default is "{}" empty. (You can go to cs50/wk9_flask/11_birthdays/app.py to view about request headers)
   body: The information you want to send to the server. Note that GET or HEAD method requests cannot contain body information.
   Other options: mode, credentials, cache, redirect, integrity. */


/* "JSON.stringify" is a common use of JSON is to exchange data to/from a web server.
   When sending data to a web server, the data has to be a string. It can convert a JS object and arrays into a string.

   In JSON, date objects are not allowed, but "JSON.stringify" will convert any dates into strings:
	   const obj = {name: "John", today: new Date(), city : "New York"};
	   const myJSON = JSON.stringify(obj);

   In JSON, functions are not allowed as object values. "JSON.stringify" will remove any functions from a JS object, both the key and the value. So you must convert the functions into strings before running "JSON.stringify": 
	   const obj = {name: "John", age: function () {return 30;}, city: "New York"};
	   obj.age = obj.age.toString();   // convert to string
	   const myJSON = JSON.stringify(obj);

   When storing data, the data has to be a certain format, and regardless of where you choose to store it, text is always one of the legal formats. JSON makes it possible to store JS objects as text:
	   // Storing data:
	   const myObj = {name: "John", age: 31, city: "New York"};
	   const myJSON = JSON.stringify(myObj);
	   localStorage.setItem("testJSON", myJSON);

	   // Retrieving data:
	   let text = localStorage.getItem("testJSON");
	   let obj = JSON.parse(text);  // "JSON.parse" converts text into a JS object.
	   document.getElementById("demo").innerHTML = obj.name; */

document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
    document.querySelector('#compose-form').addEventListener('submit', send_email);

    // By default, load the inbox
    load_mailbox('inbox');

});


function compose_email() {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-content-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}


function send_email (e) {
    /* "preventDefault()" and "return false" are used to stop an event's default behavior. 
       "preventDefault()" is used to stop the default behavior of an event, 
       while "return false" not only prevents the default behavior but also stops event propagation to parent elements.
       If we use "return false" here, it won't load the user's sent mailbox after sending emails. */
    e.preventDefault();
    
    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: document.querySelector('#compose-recipients').value,
            subject: document.querySelector('#compose-subject').value,
            body: document.querySelector('#compose-body').value
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            load_error(result.error);
        } else {
            load_mailbox('sent');
        }
    });
}


function load_error(error) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-content-view').style.display = 'block';
    
    document.querySelector('#email-content-view').innerHTML += error;
}


function load_mailbox(mailbox) {
  
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-content-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    // ".charAt(index)" returns the character at a specified <index> (position) in a string.
    // ".slice(start, end)" returns a new array selected from the start to the end (not inclusive) and doesn't change the original array.

    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        console.log(emails);
        emails.forEach(email => {
            /* Instead of creating a <div>, we create an <a> so that when the mouse is hovering over <a>, 
               the mouse cursor will turn into a hand shape. */
            let email_entry = document.createElement('a'); 
            email_entry.setAttribute('href', '');
            email_entry.className = `list-group-item list-group-item-action ${email.read ? 'list-group-item-dark' : ''}`;
            email_entry.innerHTML = `
                <div class="d-flex justify-content-between">
                    <div class="text-start">
                        <span style="display: inline-block; width: 200px"><strong>${email.sender}</strong></span>
                        <span>${email.subject}</span>
                    </div>
                    <div class="text-end">${email.timestamp}</div>
                </div>
            `;
            
            email_entry.addEventListener('click', (e) => {
                e.preventDefault();
                load_email(email.id);
            });

            document.querySelector('#emails-view').append(email_entry);
        });
    });
}


function load_email(email_id) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-content-view').style.display = 'block';

    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
        console.log(email);

        content = document.querySelector('#email-content-view');

        email.body = email.body.replaceAll('\n', '<br/>');
        content.innerHTML = `
            <p><strong>From: </strong>${email.sender}</p>
            <p><strong>To: </strong>${email.recipients}</p>
            <p><strong>Subject: </strong>${email.subject}</p>
            <p><strong>Timestamp: </strong>${email.timestamp}</p>
            <hr>
            ${email.body}
            <br/><br/> 
        `;
        
        if (document.querySelector('#user-email-address').innerHTML != email.sender) {
            content.innerHTML += `
                <button class="btn btn-sm btn-outline-primary" id="reply" onclick="reply_email(${email.id})">Reply</button>
                <button class="btn btn-sm btn-outline-primary" id="archive" onclick="archive_email(${email.id}, ${email.archived})">${email.archived ? 'Unarchive' : 'Archive'}</button>
            `;
        }

        if (!email.read == true) {
            fetch(`/emails/${email.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true
                })
            });
        }
    });
}


function archive_email(email_id, archived) {
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !archived
        })
    })
    .then(() => {
        load_mailbox('inbox');
    })
}


function reply_email(email_id) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-content-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
        document.querySelector('#compose-recipients').value = email.sender;
        // ".substr(i, len)" extracts a substring of length len from the i-th position of the string.
        document.querySelector('#compose-subject').value = (email.subject.substr(0, 4) === 'Re: ') ? email.subject : 'Re: ' + email.subject;
        document.querySelector('#compose-body').value = '\r\n\r\n' + `------------------------------------------On ${email.timestamp} ${email.sender} wrote: `+ '\r\n' + email.body;
    });
}