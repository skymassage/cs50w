/* In general, the steps for a browser to load a website:
   1. Parse HTML
   2. Load style(.css) and JavaScript(.js)
   3. Parse and execute JavaScript
   4. DOM tree rendering is completed (The "DOMContentLoaded" event is triggered)
   5. Load external files such as images
   6. The page is loaded (The "load" event is triggered) */

document.addEventListener('DOMContentLoaded', function() {
    /* We need to declare two variables for each <a class="comment_link">. 
       One is to check whether the API request to obtain the comment content has been submitted,
       and the other is to check whether the comment should be shown or hidden. 
       To access these variables in another function, we use the dictionary 
       so that we can access these variables by the keys based on the post's ID.
       Note that we should declare the variable here, because executing JavaScript is 
       before the DOM tree rendering is completed (The "DOMContentLoaded" event is triggered).
       You can access ".comment_link" after "DOMContentLoaded". */
    var click_check = {}, commentLinks = document.querySelectorAll('.comment_link');
    for (var i = 0; i < commentLinks.length; i++) {
        click_check[`clicked_${commentLinks[i].name}`] = false;
        click_check[`submitted_${commentLinks[i].name}`] = false; 
    }
    
    document.querySelectorAll('.comment_link').forEach(a_tag => {
        a_tag.addEventListener('click', (e) => {
            /* Note that the second argument of "addEventListener" should be a function, 
               and this function has only one parameter which is the event.
               If you don't want to submit the form or redirection.
               First, prevent redirection using "preventDefault" before "load_comment".
               Then, use another function to complete main work. 
               So you can't pass the function to "addEventListener" to do the job and prevent redirection meanwhile. */
            e.preventDefault();
            load_comment(a_tag.id, click_check);
        });
    });

    document.querySelectorAll('.edit_btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelector(`#content_postId_${btn.value}`).style.display = "none";
            document.querySelector(`#edit_postId_${btn.value}`).style.display = "block";
        });
    });

    document.querySelectorAll('.submit_edit_btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            edit(btn.value);
            document.querySelector(`#content_postId_${btn.value}`).style.display = "block";
            document.querySelector(`#edit_postId_${btn.value}`).style.display = "none";
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

function edit(postId) {
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
            post_id: postId,
            content: document.querySelector(`#edit_content_${postId}`).value
        })
    })
    .then(response => response.json())
    .then(result => {
        document.querySelector(`#content_text_postId_${postId}`).innerHTML = result.content;
    });
}


// var _parts = [...parts]; // or _parts = Array.from(parts);

function load_comment(comment_postId, click_check) {
    post_id = comment_postId.slice(15);

    fetch(`/comment/${post_id}`)
    .then(response => response.json())
    .then(comments => {
        /* In JS, we can select all tags with the "card-footer comment postId_{{ post.id }}" class name using
           ".card-footer.comment" this part without considering postId_<post_id>,
           where the whitespace of "card-footer comment" is replaceed by "."
           And we can access the single tag using ".card-footer.comment.postId_<post_id>",
           where we use "postId_<post_id>" to specify the tag. */
        comment_div = document.querySelector(`.card-footer.comment.postId_${post_id}`);    
        /* Note that we cannot assign the elements of the array to variables in this way 
           to let the elements change as the variables change. */
        if (!click_check[`clicked_${post_id}`]) {
            click_check[`clicked_${post_id}`] = true;
            comment_div.style = 'block';
            if (!click_check[`submitted_${post_id}`]) {
                comments.forEach(comment => {
                    /* If we declare the rendering content as a string, 
                       the results displayed on the page will have many tags
                       (i.e., many '<', '>', '/', etc). Because this is a string not an HTML object.
                       We can declare a <div> and have its "innerHTML" attribute be the rendering content. */
                    let convert_to_html = document.createElement('div');
                    convert_to_html.innerHTML = `
                        <div class="d-flex justify-content-between">
                            <div class="text-start">
                                <a class="text-dark" href="/profile/${comment.author}">${comment.author}</a>
                            </div>  
                            <div class="text-end">${comment.timestamp}</div>
                        </div>
                        <p>${comment.message}</p>
                    `;
                    /* In JS, don't use {% url ... %} like <a class="text-dark" href="{% url 'profile' username=comment.author %}">.
                       URL paths should be hardcoded in JS like <a class="text-dark" href="/profile/${comment.author}"> above. */
    
                    comment_div.append(convert_to_html);
                });

                document.querySelector(`#postId_${post_id}`).append(comment_div);
                click_check[`submitted_${post_id}`] = true;
            }
        } else {
            comment_div.style.display = 'none';
            click_check[`clicked_${post_id}`] = false;
        }
    });
}