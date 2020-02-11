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
        e.dataTransfer.files;
    })
    .on('dragend dragleave drop', function(e) {
        $form.removeClass('is-dragover');
    });
}
