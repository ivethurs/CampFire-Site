// sending the like post request 
function likePost(postId) {
    fetch("/like_unlike_post", {
        method: "POST",
        body: JSON.stringify({postId: postId})
    }).then((res) => {
        window.location.href="/"
    })
}

// sending the delete post request 
function deletePost(postId) {
    fetch("/deletePost", {
        method: "POST",
        body: JSON.stringify({postId: postId})
    }).then((res) => {
        window.location.href = "/"
    })
}
// sending the follower user reqest
function followUser(userId) {
    fetch("/follow", {
        method: "POST",
        body: JSON.stringify({userId: userId})
    }).then((res) => {
        window.location.href = `/profile/${userId}`
    })
}
// sending the unfollower user request
function unfollowUser(userId) {
    fetch("/unfollow", {
        method: "POST",
        body: JSON.stringify({userId: userId})
    }).then((res) => {
        window.location.href = `/profile/${userId}`
    })
}

function fileUpload() {
    document.getElementById("upload_post_image").click()
}