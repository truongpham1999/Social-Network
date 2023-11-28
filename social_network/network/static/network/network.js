console.log("network.js is running");

document.addEventListener('DOMContentLoaded', function() {
    // Follow & Unfollow
    const followBtn = document.getElementById('follow-btn');
    const followersCount = document.getElementById('followers-count');
    if (followBtn) {
        followBtn.addEventListener('click', () => follow_unfollow(followBtn, followersCount));
    }

    // Edit post
    document.querySelectorAll('.edit-post').forEach(function(element) {
        element.addEventListener('click', () => editPost(element.getAttribute('data-post-id')));
    });

    // Like post
    document.querySelectorAll('.like-button').forEach(function(element) {
        element.addEventListener('click', () => likePost(element.getAttribute('data-post-id')));
    });

    // Comment post
    document.querySelectorAll('.comment-link').forEach(function(element) {
        element.addEventListener('click', () => toggleComment(element.getAttribute('data-post-id')));
    });

    document.querySelectorAll('.comment-btn').forEach(function(element) {
        element.addEventListener('click', () => addComment(element.getAttribute('data-post-id')));
    });

});

function addComment(postId) {
    const commentText = document.getElementById(`comment-text-${postId}`).value;
    console.log("commentText == ", commentText);
    fetch(`/add_comment/${postId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({
            'content': commentText
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server response:", data);
        if (data.success) {
            document.getElementById(`comment-text-${postId}`).value = '';
            loadComments(postId);
        }
    })
    .catch(error => console.error('Error:', error));
}

function toggleComment(postId) {
    const commentSection = document.getElementById(`comments-section-${postId}`);
    commentSection.style.display = commentSection.style.display === 'none' ? 'block' : 'none';
    loadComments(postId);
}

function loadComments(postId) {
    fetch(`/get_comments/${postId}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(comments => {
        console.log("Server reponse:", comments);
        const commentDiv = document.getElementById(`comments-section-${postId}`);
        commentDiv.innerHTML = '';
        comments.forEach(comment => {
            commentDiv.innerHTML += `
                <div class="comment-display">
                    <a href="/profile/${comment.commenter.id}"><strong>${comment.commenter.username}</strong></a>
                    <p class="comment-content">${comment.content}</p>
                    <p class="comment-date">${comment.date}</p>
                </div>
            `;
        });
        console.log("loading cmts successfully");
    })
    .catch(error => console.error('Error:', error));
}

function likePost(postId) {
    const likeBtn = document.querySelector(`#like-button-${postId}`);
    const likeCount = document.getElementById(`like-count-${postId}`);
    let isLike = likeBtn.getAttribute('data-like') === 'true'; // Set isLike directly as a boolean

    fetch(`/like/${postId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({
            'like': !isLike
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server response:", data);
        if (data.success) {
            isLike = !isLike;
            console.log("isLike == ", isLike);
            likeBtn.setAttribute('data-like', isLike.toString());

            // Update the like count
            if (data.like) {
                likeBtn.classList.remove("unliked")
                likeBtn.classList.add("liked")
                likeCount.textContent = parseInt(likeCount.textContent) + 1;
            }
            else {
                likeBtn.classList.remove("liked")
                likeBtn.classList.add("unliked")
                likeCount.textContent = parseInt(likeCount.textContent) - 1;
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

function editPost(postId) {
    const postDiv = document.getElementById(`post-${postId}`);
    const postContent = postDiv.querySelector('.post-content');
    const postText = postContent.innerHTML;

    // Replace postContent with a textarea
    postContent.innerHTML = `<textarea class="form-control">${postText}</textarea>`;
    postContent.innerHTML += `<button class="save-edit btn btn-primary mt-2">Save</button>`;

    // Add save functionality
    postDiv.querySelector('.save-edit').addEventListener('click', () =>
        saveEdit(postId, postContent.querySelector('textarea').value));
}

function saveEdit(postId, newText) {
    // Add AJAX call to save the edit
    fetch(`/save_post/${postId}`, {
        method: 'PUT',
        headers: {
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({
            'newText': newText
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server response:", data);
        if (data.success) {
        document.querySelector(`#post-${postId}`).querySelector('.post-content').innerHTML = newText;
        }
        else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error('Error:', error));

}

// Function to get CSRF token
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').getAttribute('content');;
}

function follow_unfollow(followBtn, followersCount) {
    console.log("button is clicked");
    const userId = followBtn.getAttribute('data-user-id');
    let isFollow = followBtn.getAttribute('data-follow') === 'true'; // Set isFollow directly as a boolean
    const csrfToken = followBtn.getAttribute('data-csrf-token');

    fetch(`/follow_unfollow/${userId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            'follow': !isFollow 
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server response:", data); // Add this line to log the server response
        if (data.success) {
            isFollow = !isFollow; // Update the isFollow variable to the new state
            console.log("isFollow == ", isFollow);
            followBtn.innerText = isFollow ? 'Unfollow' : 'Follow';
            followBtn.setAttribute('data-follow', isFollow.toString());

            // Update the followers count
            if (isFollow) {
                followersCount.textContent = parseInt(followersCount.textContent) + 1;
            } else {
                followersCount.textContent = parseInt(followersCount.textContent) - 1;
            }
        }
    })
    .catch(error => console.error('Error:', error));
}