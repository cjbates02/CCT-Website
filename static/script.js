
function deleteWarning(delete_id) {
    let confirmed = confirm("Are you sure you want to delete this announcement. this will not be recoverable?");

    if (confirmed) {
        console.log(delete_id);
        $.ajax({
            url: '/delete_announcement',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({'id':delete_id}),
        })
        location.reload();
    }
}


function deleteChangeLogWarning(delete_id) {
    let confirmed = confirm("Are you sure you want to delete this change log, this will not be recoverable?");

    if (confirmed) {
        console.log(delete_id);
        $.ajax({
            url: '/delete_change_log',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({'id':delete_id}),
        })
        location.reload();
    }
}