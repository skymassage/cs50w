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
            e.preventDefault();   // To prevent from redirection, use "preventDefault" before "load_comment".
            load_comment(a_tag.id, click_check);
        });
    });
});

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