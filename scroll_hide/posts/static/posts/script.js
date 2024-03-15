let counter = 1; // Start with first post
const quantity = 20; // Load posts 20 at a time
document.addEventListener('DOMContentLoaded', load); // When DOM content has loaded, call the "load" function to render the first 20 posts.

window.onscroll = () => {  // If scrolled to bottom, load the next 20 posts.
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load();
    }
};

function load() { // Load next set of posts.
    // Set start and end post numbers, and update counter.
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;

    // Get new posts and add posts.
    fetch(`/posts?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        data.posts.forEach(add_post);
    })
};

function add_post(contents) {  // Add a new post with given contents to DOM.
    // Create new post.
    const post = document.createElement('div');
    post.className = 'post';
    post.innerHTML = `${contents} <button class="hide">Hide</button>`;

    document.querySelector('#posts').append(post);  // Add post to DOM.
};

// Here is the DOM to be clicked, so we don't need to include the following code inside of 
// "document.addEventListener('DOMContentLoaded', <the_following_function>)".
document.addEventListener('click', event => {
    const element = event.target; // Find what was clicked on. The ".target" property returns the element where the event occured, and it is read-only.

    if (element.className === 'hide') {     // Check if the user clicked on a hide button.
        element.parentElement.style.animationPlayState = 'running'; // The ".parentElement" property returns the parent element of the specified element.
        element.parentElement.addEventListener('animationend', () => {  // The "animationend" event occurs when a CSS animation has completed.
            element.parentElement.remove();     // The "".remove()"" method removes an element (or node) from the document.
        });
    }
    
});