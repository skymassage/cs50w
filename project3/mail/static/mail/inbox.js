document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  // ".charAt(index)" returns the character at a specified <index> (position) in a string.
  // ".slice(start, end)" returns a new array selected from the start to the end (not inclusive) and doesn't change the original array.
}

/* 
"JSON.stringify" is a common use of JSON is to exchange data to/from a web server.
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
	document.getElementById("demo").innerHTML = obj.name;
*/


/* 
"fetch" sends an HTTP request and returns a promise that will be resolved as a response object.
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
Other options: mode, credentials, cache, redirect, integrity.
*/