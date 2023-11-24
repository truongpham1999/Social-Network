console.log("network.js is running");

document.addEventListener('DOMContentLoaded', function() {
    const followBtn = document.getElementById('follow-btn');
    const followersCount = document.getElementById('followers-count');
    if (followBtn) {
        console.log('Follow button found, adding event listener');
        console.log("isFollow == ", followBtn.getAttribute('data-follow'));
        followBtn.addEventListener('click', () => follow_unfollow(followBtn, followersCount));
    }
});

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