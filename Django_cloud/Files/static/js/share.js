$('.action_file_share').on('click', function (e) {
    let file_id = $(e.target).attr('fid');
    $.getJSON(`/Share/create/${file_id}`, function (data) {
        $('#copy-input').attr('value', `${window.location.origin}/Share/s/${data.link}`);
        $('#shareModal').modal('show');
    });
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

function tempCopyMsg(msg) {
    $('#copy-button').attr('data-original-title', msg);
    $('#copy-button').tooltip('show');
    $('#copy-button').attr('data-original-title', 'Copier');
}

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
