
function deleteWarning(delete_id) {
    let confirmed = confirm("Are you sure you want to delete this post?");

    if (confirmed) {
        console.log(delete_id);
        $.ajax({
            url: '/delete_announcement',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({'id':delete_id}),
        })

    }
}