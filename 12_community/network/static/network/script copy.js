/* In general, the steps for a browser to load a website:
   1. Parse HTML
   2. Load style(.css) and JavaScript(.js)
   3. Parse and execute JavaScript
   4. DOM tree rendering is completed (The "DOMContentLoaded" event is triggered)
   5. Load external files such as images
   6. The page is loaded (The "load" event is triggered) */

document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.comment_link').forEach(a_tag => {
        a_tag.addEventListener('click', e => {
            /* Note that the second argument of "addEventListener" should be a function, 
               and this function has only one parameter which is the event.
               If you don't want to submit the form or redirection.
               First, prevent redirection using "preventDefault" before "load_comment".
               Then, use another function to complete main work. 
               So you can't pass the function to "addEventListener" to do the job and prevent redirection meanwhile. */
            e.preventDefault();
            load_comment(a_tag.id.slice(15));
        });
    });

    document.querySelectorAll('.comment_submit_btn').forEach(btn => {
        btn.addEventListener('click', e => {
            e.preventDefault();

            // Prevent the send the blank comment.
            if (document.querySelector(`#leave_comment_postId_${btn.value}`).value) {
                comment(btn.value);
                document.querySelector(`.card-footer.comment.postId_${btn.value}`).style.display = 'block';
            }
        });
    });
    
    document.querySelectorAll('.edit_btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelector(`#content_postId_${btn.value}`).style.display = "none";
            document.querySelector(`#edit_postId_${btn.value}`).style.display = "block";
        });
    });

    document.querySelectorAll('.submit_edit_btn').forEach(btn => {
        btn.addEventListener('click', e => {
            e.preventDefault();
            edit(btn.value);
            document.querySelector(`#content_postId_${btn.value}`).style.display = "block";
            document.querySelector(`#edit_postId_${btn.value}`).style.display = "none";
        });
    });

    document.querySelectorAll('.cancel_edit_btn').forEach(btn => {
        btn.addEventListener('click', e => {
            e.preventDefault();
            document.querySelector(`#content_postId_${btn.value}`).style.display = "block";
            document.querySelector(`#edit_postId_${btn.value}`).style.display = "none";
        });
    });


    document.querySelectorAll(".post-ratings-container").forEach(post => {
        const ratings = post.querySelectorAll(".post-rating");
        const likeRating = ratings[0];
    
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
    
                const likeOrDislike = likeRating === rating ? "like" : "dislike";
                // const response = await fetch(`/posts/${postId}/${likeOrDislike}`);
                const response = await fetch(`/rate`, {
                    method: 'PUT',
                    headers: {
                        "Content-type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: json.stringify({
                        post_id: 1,
                        user_id: 2,
                        like: false,
                        dislike: true
                    })
                });
                const body = await response.json();
            });
        });
    });
});



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

function edit(post_id) {
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
            content: document.querySelector(`#edit_content_${post_id}`).value
        })
    })
    .then(response => response.json())
    .then(result => {
        document.querySelector(`#content_text_postId_${postId}`).innerHTML = result.content;
    });
}


function comment(post_id) {
    fetch('/comment', {
        method: 'POST',
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            post_id: post_id,
            comment_content: document.querySelector(`#leave_comment_postId_${post_id}`).value
        })
    })
    .then(response => response.json())
    .then(comments => {
        document.querySelector(`#leave_comment_postId_${post_id}`).value = '';
        document.querySelector(`.card-footer.comment.postId_${post_id}`).style.display = 'none'; 
        load_comment(post_id);
    });
}


function load_comment(post_id) {
    /* In JS, we can select all tags with the "card-footer comment postId_{{ post.id }}" class name using
       ".card-footer.comment" this part without considering postId_<post_id>,
       where the whitespace of "card-footer comment" is replaceed by "."
       And we can access the single tag using ".card-footer.comment.postId_<post_id>",
       where we use "postId_<post_id>" to specify the tag. */
    let comment_div = document.querySelector(`.card-footer.comment.postId_${post_id}`);  
    let comment_content_div = document.querySelector(`#comment_content_postId_${post_id}`);

    comment_content_div.innerHTML = '';

    if (comment_div.style.display == 'none') {
        fetch(`/show_comment/${post_id}`)
        .then(response => response.json())
        .then(comments => {
            /* Note that we cannot assign the elements of the array to variables in this way 
            to let the elements change as the variables change. */
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