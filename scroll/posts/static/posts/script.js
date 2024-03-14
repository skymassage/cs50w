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

function add_post(contents) { // Add a new post with given contents to DOM.
    // Create new post.
    const post = document.createElement('div');
    post.className = 'post';
    post.innerHTML = contents;

    document.querySelector('#posts').append(post);  // Add post to DOM.
};