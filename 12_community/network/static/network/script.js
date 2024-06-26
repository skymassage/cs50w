/* In general, the steps for a browser to load a website:
   1. Parse HTML
   2. Load style(.css) and JavaScript(.js)
   3. Parse and execute JavaScript
   4. DOM tree rendering is completed (The "DOMContentLoaded" event is triggered)
   5. Load external files such as images
   6. The page is loaded (The "load" event is triggered) */

/* In the DOM, everything is a node. A node can be an element, attribute, text, comment, document, 
   or any other type of DOM object. Nodes are organized in a tree-like structure, 
   with the document node at the top and all other nodes branching off from it. 
   Nodes have properties and methods that allow you to manipulate them and their child nodes. 
   For example, you can use the appendChild() method to add a child node to an existing node.
   
   Elements are a specific type of node that represents an HTML element. Elements have all the properties and methods of a node, 
   but they also have additional properties and methods that are specific to elements. 
   For example, elements have a tagName property that specifies the name of the element, such as "div" or "span". 
   
   The main difference between Element and Node is that Element is a specific type of Node that represents an HTML or XML element.
   While all Elements are Nodes, not all Nodes are Elements. 
   Some methods and properties behave differently depending on whether they are called on an Element or a Node. */

/* ".innerHTML" returns the text content of the element, including all spacing and inner HTML tags.
   ".innerText" just returns the text content of the element and all its children, without CSS hidden text spacing and tags, except <script> and <style> elements.
   ".textContent" returns the text content of the element and all descendaces, with spacing and CSS hidden text, but without tags. */

document.addEventListener('DOMContentLoaded', function() {
    
    /* In JS, we can select all tags with the "post card" class name using ".post.card",
       where the whitespace of "post card" is replaceed by "." */
    document.querySelectorAll('.post.card').forEach(post => {
        var postId = post.id.slice(7);

        /* Element also has the ".querySelector" method to select elements within itself,
           so we don't need "document.querySelector" to select the element in the whole DOM. */
        post.querySelector('.comment_link').onclick = function () {
            load_comment(post, postId);
            return false;  // Method 1: "return false" prevent submission.
        };
        if (post.querySelector('.comment_submit_btn')) {
            post.querySelector('.comment_submit_btn').addEventListener('click', e => {
                /* Note that the second argument of "addEventListener" should be a function, 
                   and this function has only one parameter which is the event.
                   If you don't want to submit the form or redirection.
                   First, prevent redirection using "preventDefault" before "load_comment".
                   Then, use another function to complete main task. 
                   So you can't pass the function to "addEventListener" to do the job and prevent redirection meanwhile. */
                e.preventDefault(); // Method 2: "e.preventDefault()" prevents submission.
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


        // Note that the element with the "userId" class is in the layout.html.
        if (document.querySelector('.userId')) {
            var userId = document.querySelector('.userId').id.slice(7);
            const ratings = post.querySelectorAll(".post-rating");
            const likeRating = ratings[0]; 
            ratings.forEach(rating => {
                const button = rating.querySelector(".logined.post-rating-button");
                const count = rating.querySelector(".post-rating-count");
        
                button.addEventListener("click", async () => {
                    /* "<element>.classList" returns a DOMTokenList (an array-like object with some properties and method) 
                       containing the classnames of <element>. 
                       ".add()" adds one or more tokens to the list and ".remove()" removes one or more tokens from the list.
                       For example: "<div id="ex" class="first second third">" in HTML.
                                    In JS, "document.querySelector('#ex').classList" returns "['first', 'second', 'third']",
                                    and "document.querySelector('#ex').classList.remove('second', 'third')" leads to "<div id="ex" class="first">" in HTML. 
                      "<node_1>.contains(<node_2>)" returns true if <node_2> is a descendant of a <node_1>. */
                    if (rating.classList.contains("post-rating-selected")) {
                        count.textContent = Number(count.textContent) - 1;
                        rating.classList.remove("post-rating-selected");

                        const response = await fetch('/rate', {
                            method: 'POST',
                            headers: {
                                "Content-type": "application/json",
                                "X-CSRFToken": getCookie("csrftoken")
                            },
                            body: JSON.stringify({
                                post_id: postId,
                                user_id: userId,
                                like: false,
                                dislike: false
                            })
                        });

                        return;
                    }

                    count.textContent = Number(count.textContent) + 1;
                    ratings.forEach(rating => {
                        if (rating.classList.contains("post-rating-selected")) {
                            const count = rating.querySelector(".post-rating-count");
                            /* "Math.max()" returns the largest of the numbers given as input parameters, 
                               or "-Infinity" if there are no parameters. 
                               For example: Math.max(0, 150, 30, 20, 38); // 150 */
                            count.textContent = Math.max(0, Number(count.textContent) - 1);
                            rating.classList.remove("post-rating-selected");
                        }
                    });
                    rating.classList.add("post-rating-selected");

                    const likeOrDislike = likeRating === rating ? 'like' : 'dislike';

                    const response = await fetch('/rate', {
                        method: 'POST',
                        headers: {
                            "Content-type": "application/json",
                            "X-CSRFToken": getCookie("csrftoken")
                        },
                        body: JSON.stringify({
                            post_id: postId,
                            user_id: userId,
                            like: likeOrDislike === 'like' ? true : false,
                            dislike: likeOrDislike === 'dislike' ? true : false
                        })
                    });
                });
            });
        }        
    });


    if (document.querySelector('#follow_btn')) {
        /* Note that changing "document.querySelector('#follower_num > strong').innerText" 
           doesn't change the "document.querySelector('#follower_num > strong')" element.
           Use "document.querySelector('#follower_num > strong')" and access its ".innerText" property to change it. */
        let follower_ele = document.querySelector('#follower_num > strong'); // Use '>' to specify the child element.
        document.querySelector('#follow_btn > button').onclick = function () {
            follow(this.value, true);
            document.querySelector('#follow_btn').style.display = 'none';
            document.querySelector('#following_btn').style.display = 'inline-block';
            document.querySelector('#unfollow_btn').style.display = 'inline-block';
            follower_ele.innerText = Number(follower_ele.innerText) + 1; // "Number()" converts a value to a number. If the value cannot be converted, NaN is returned.
            return false;
        };
    }
    if (document.querySelector('#unfollow_btn')) {
        let follower_ele = document.querySelector('#follower_num > strong');
        document.querySelector('#unfollow_btn > button').onclick = function () {
            follow(this.value, false);
            document.querySelector('#follow_btn').style.display = 'inline-block';
            document.querySelector('#following_btn').style.display = 'none';
            document.querySelector('#unfollow_btn').style.display = 'none';
            follower_ele.innerText = Number(follower_ele.innerText) - 1;
            return false;
        };
    }


    /* The history object contains the URLs visited by the user (the browser's history.). 
       The history object is a property of the window object, and be accessed with "window.history" or just "history".
       "history.replaceState(data, title, url)" and "history.pushState(data, title, url)" are similar but still different.
       data: Information (in ket-value format) passed to the target URL, can be empty.
       title: There are historical reasons for this argument. Currently, all browsers do not support it. Just fill in the blank string.
       url: Target URL, doesn't check if it exists. And the first argument "data" can be passed here by refering to keys.
            Be careful not to cross domains. For example, it can't cross from Google (https://www.google.com) to Facebook (https://www.facebook.com/).
       Similarities: We can modify the URL without refreshing. Neither supports cross-domain.
       Differences: ".replaceState" will modify the current URL without leaving a record in the history.
                    Whether a record will be left means that after changing the URL, 
                    whether it can be reversed through the back arrow button of the browser.
                    "pushState" can be reversed because it leaves a record.
                    "replaceState" cannot be reversed because no record is left. */
    /* The location object contains information about the current URL.
       The location object is a property of the window object, and cen be accessed with "window.location" or just "location".
       The ".pathname" property of the location object sets or returns the pathname of a URL (page). */
       history.replaceState({}, "", location.pathname); // Prevent URL changes when using paginator.
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


function edit(post, post_id) {
    fetch('/edit', {
        method: 'PUT',
        // HTTP "headers" let the client and the server pass additional information with an HTTP request or response.
        headers: {
            /* The "content-type" of "headers" tells the browser what format of data is sent, 
               and the browser handles different types of data in different ways. 
               JSON format is often used for front-end and back-end data interaction because it is readable, 
               concise and convenient. So set "content-type" to "application/json". */ 
            'Content-type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
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
            'Content-type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
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


function follow(user_id, if_follow) {
    fetch('/follow', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            user_id: user_id,
            if_follow: if_follow
        })
    });
    /* Note that here it will be an error if using "response.json()".
       Because the status code of the JSON object returned by the backend is "204 No Content",
       this means that the request has been successfully processed, but is not returning any content.
       Therefore no response object is returned, and "".json()" cannot be used. */
}