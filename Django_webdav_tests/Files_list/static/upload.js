let dragNDropSupport = function() {
    let div = document.createElement('div');
    return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
}();

let $form = $('.dropzone');
if (dragNDropSupport) {
    $form.addClass('has-advanced-upload');
    let droppedFiles = false;
    $form.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
    })
    .on('dragover dragenter', function() {
        $form.addClass('is-dragover');
    })
    .on('drop', function(e) {
        console.log("File sent !");
        droppedFiles = e.originalEvent.dataTransfer.files;
        $form.trigger('submit');
    })
    .on('dragend dragleave drop', function(e) {
        $form.removeClass('is-dragover');
    })
    .on('change', function(e) {
        $form.trigger('sumbit');
    });

    let ajaxData = new FormData($form.get(0));

    if (droppedFiles) {
        $.each(droppedFiled, function(i, file) {
            ajaxData.append($input.attr('name'), file);
        });
    }

    $.ajax({
        url: $form.attr('action'),
        type: $form.attr('method'),
        data: ajaxData,
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: false,
        complete: function() {
            $form.removeClass('is-uploading');
        },
        success: function(data) {
            $form.addClass(data.success == true ? 'is-success' : 'is-error');
            if (!data.success) $errorMsg.text(data.error);
        },
        error: function() {
            alert("Upload error");
        }
    });
}
