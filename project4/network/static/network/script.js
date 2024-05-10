/* In general, the steps for a browser to load a website:
   1. Parse HTML
   2. Load style(.css) and JavaScript(.js)
   3. Parse and execute JavaScript
   4. DOM tree rendering is completed (The "DOMContentLoaded" event is triggered)
   5. Load external files such as images
   6. The page is loaded (The "load" event is triggered) */

document.addEventListener('DOMContentLoaded', function() {
        
    /* In JS, we can select all tags with the "post card" class name using ".post.card",
       where the whitespace of "post card" is replaceed by "." */
    document.querySelectorAll('.post.card').forEach(post => {
        var postId = post.id.slice(7);

        /* Element also has the ".querySelector" method to select elements within itself,
           so we don't need "document.querySelector" to select the element in the whole DOM. */
        post.querySelector('.comment_link').addEventListener('click', e => {
            /* Note that the second argument of "addEventListener" should be a function, 
               and this function has only one parameter which is the event.
               If you don't want to submit the form or redirection.
               First, prevent redirection using "preventDefault" before "load_comment".
               Then, use another function to complete main task. 
               So you can't pass the function to "addEventListener" to do the job and prevent redirection meanwhile. */
            e.preventDefault();
            load_comment(post, postId);
        });

        if (post.querySelector('.comment_submit_btn')) {
            post.querySelector('.comment_submit_btn').addEventListener('click', e => {
                e.preventDefault();
                if (post.querySelector('.comment_field').value) { // Prevent the send the blank comment.
                    comment(post, postId);
                }
            });
        }

        if (post.querySelector('.edit_btn')) {
            post.querySelector('.edit_btn').addEventListener('click', e => {
                e.preventDefault();
                post.querySelector('.content').style.display = "none";
                post.querySelector('.edit').style.display = "block";
            });

            post.querySelector('.cancel_edit_btn').addEventListener('click', e => {
                e.preventDefault();
                post.querySelector('.content').style.display = "block";
                post.querySelector('.edit').style.display = "none";
            });

            post.querySelector('.submit_edit_btn').addEventListener('click', e => {
                e.preventDefault();
                edit(post, postId);
            });
        }
        
        // post.querySelector('.post-ratings-container').forEach();
        //////////////////
        const ratings = post.querySelectorAll(".post-rating");    
        ratings.forEach(rating => {
            const button = rating.querySelector(".logined.post-rating-button");
            const count = rating.querySelector(".post-rating-count");
    
            button.addEventListener("click", async () => {
                if (rating.classList.contains("post-rating-selected")) {
                    return;
                }
    
                count.textContent = Number(count.textContent) + 1;
    
                ratings.forEach(rating => {
                    if (rating.classList.contains("post-rating-selected")) {
                        const count = rating.querySelector(".post-rating-count");
    
                        count.textContent = Math.max(0, Number(count.textContent) - 1);
                        rating.classList.remove("post-rating-selected");
                    }
                });
    
                rating.classList.add("post-rating-selected");
            });
        });


        ////////////////////////////////////
    });
});


function edit(post, post_id) {
    fetch('/edit', {
        method: 'POST',
        // HTTP "headers" let the client and the server pass additional information with an HTTP request or response.
        headers: {
            /* The "content-type" of "headers" tells the browser what format of data is sent, 
               and the browser handles different types of data in different ways. 
               JSON format is often used for front-end and back-end data interaction because it is readable, 
               concise and convenient. So set "content-type" to "application/json". */ 
            "Content-type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            post_id: post_id,
            content: post.querySelector('.edit_field').value
        })
    })
    .then(response => response.json())
    .then(result => {
        post.querySelector('.content_text').innerText = result.content;
        post.querySelector('.content').style.display = "block";
        post.querySelector('.edit').style.display = "none";
    });
}


function comment(post, post_id) {
    fetch('/comment', {
        method: 'POST',
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            post_id: post_id,
            comment_content: post.querySelector('.comment_field').value
        })
    })
    .then(response => response.json())
    .then(result => {
        post.querySelector('.comment_field').value = '';
        post.querySelector('.comment').style.display = 'none'; 
        load_comment(post, post_id);
    });
}


function load_comment(post, post_id) {
    let comment_div = post.querySelector('.comment');
    let comment_content_div = post.querySelector('.comment_content');

    comment_content_div.innerHTML = '';

    if (comment_div.style.display == 'none') {
        fetch(`/show_comment/${post_id}`)
        .then(response => response.json())
        .then(comments => {
            if (comment_div.style.display == 'none') {
                comment_div.style.display = 'block';

                comments.forEach(comment => {
                    /* If we declare the rendering content as a string,
                       the results displayed on the page will have many tags (i.e., many '<', '>', '/', etc),
                       because this is a string not an HTML object.
                       We can declare a <div> and have its "innerHTML" attribute be the rendering content. */
                    let each_comment = document.createElement('div');
                    each_comment.innerHTML = `
                        <div class="d-flex justify-content-between">
                            <div class="text-start">
                                <a class="text-dark" href="/profile/${comment.author}"><strong>${comment.author}</strong></a>
                            </div>  
                            <div class="text-end">${comment.timestamp}</div>
                        </div>
                        <p>${comment.message}</p>
                    `;
                    /* In JS, don't use {% url ... %} like <a class="text-dark" href="{% url 'profile' username=comment.author %}">.
                    URL paths should be hardcoded in JS like <a class="text-dark" href="/profile/${comment.author}"> above. */
        
                    comment_content_div.append(each_comment);
                });
                comment_div.append(comment_content_div);
            } 
        });
    } else if (comment_div.style.display == 'block') {
        comment_div.style.display = 'none';
    }
}


/* Django prevent Cross Site Request Forgery (CSRF) through the "django.middleware.csrf.CsrfViewMiddleware" middleware in "setting.py".
   When Django responds to a request from a client, it will randomly generate a random string 
   as a token on the server side and put this token in the cookie.
   Before processing the POST request, the server performs CSRF token validation, i.e., 
   comparing the token value in the request with the csrftoken value in the cookie.
   If not, the request may come from someone else's CSRF attack, and a 403 error will be returned.
   Therefore, when performing POST submission, we need to add "X-CSRFTOKEN" to the "headers" of the request, 
   and obtain the "csrftoken" value in the cookie as the value of the "X-CSRFTOKEN" key. */

/* This funcion is used to retrieve "csrftoken" from cookie which may contain many key-value pairs. */
function getCookie(name){
    /* ".split()" splits a string into the new array of substrings and returns this new array (doesn't change the original string).
       ".pop()" removes (pops) the last element of an array (changes the original array) and returns this removed element. 
       ".shift()" removes the first elemnt of an array (changes the original array) and returns this removed element. */
    
    /* Access cookies through "document.cookie", and a cookie look likes '<key1>=<value1>; <key2>=<value2>...'.
       Here Django autimatically create the cookie for us, which is csrftoken=<csrftoken>. */

    // If document.cookie is 'csrftoken=<csrftoken>; <key1>=<value1>; <key2>=<value2>; ...'
    const value = `; ${document.cookie}`;    // '; csrftoken=<csrftoken>; <key1>=<value1>; <key2>=<value2>; ...'
    const parts = value.split(`; ${name}=`); // ['', '<csrftoken>; <key1>=<value1>; <key2>=<value2>; ...']    
    if(parts.length == 2) return parts.pop().split(';').shift();
    /* parts.pop()                           // ''<csrftoken>; <key1>=<value1>; <key2>=<value2>; ...'
       parts.pop().split(';')                // ['<csrftoken>', ' <key1>=<value1>', ' <key2>=<value2>', ...]
       parts.pop().split(';').shift()        // '<csrftoken>'                                                   */
}