
function deleteWarning(delete_id) {
    let confirmed = confirm("Are you sure you want to delete this announcement? this will not be recoverable.");

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
    let confirmed = confirm("Are you sure you want to delete this change log? this will not be recoverable.");

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

function deleteBlueStack(delete_id, stack) {
    let confirmed = confirm("Are you sure you want to delete this item? This will not be recoverable.")
    console.log(stack)
    if (confirmed) {
        console.log(delete_id)
        $.ajax({
            url: '/delete_doc',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                'id': delete_id,
                'stack' : stack
            }),
        })
        location.reload();
    }

}

// document.getElementById('delete-doc').addEventListener('click', () => {
//     delete_id = document.getElementById
// })