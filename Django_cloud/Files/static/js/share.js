$('.action_file_share').on('click', function (e) {
    /* Makes a request to the server when user clicks on "share" button */
    let file_path = $(e.target).attr('fpath');    // Gets file path
    $.getJSON(`/Share/create/${file_path}`, function (data) {   // gets json from server
        $('#copy-input').attr('value', `${window.location.origin}/Share/s/${data.link}`);
        $('#shareModal').modal('show'); // Show modal with link
    });
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip(); // Tooltip for copy button
});

function tempCopyMsg(msg) {
    $('#copy-button').attr('data-original-title', msg);
    $('#copy-button').tooltip('show');
    $('#copy-button').attr('data-original-title', 'Copier');
}

// Change tooltip if the user copied the link successfuly
$('#copy-button').on('click', function(e) {
    let link = $('#copy-input').attr('value');
    $('#copy-input').select();
    try {
        let success = document.execCommand('copy');
        if (success) {
            tempCopyMsg('Copié !');
        } else {
            tempCopyMsg('Échec de la copie.');
        }
    }
    catch (err) {
        tempCopyMsg('Échec de la copie.');
    }
});
