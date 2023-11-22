console.log("network.js is running");

document.addEventListener('DOMContentLoaded', function() {
    const followBtn = document.getElementById('follow-btn');
    if (followBtn) {
        console.log('Follow button found, adding event listener');
        followBtn.addEventListener('click', () => follow_unfollow(followBtn));
    }
    else {
        console.log('Follow button not found');
    }
});

function follow_unfollow(followBtn) {
    console.log("button is clicked");
    const userId = followBtn.getAttribute('data-user-id');
    let isFollow = followBtn.getAttribute('data-follow') === 'true';
    const csrfToken = followBtn.getAttribute('data-csrf-token');
    console.log("isFollow == ", isFollow);

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
        }
    })
    .catch(error => console.error('Error:', error));
}