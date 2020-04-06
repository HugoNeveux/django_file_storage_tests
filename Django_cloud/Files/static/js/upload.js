jQuery(document).ready(function($){
    // Correcting boostrap conflicts issues
    // $.noConflict();


    // Checks if file exists
    function fileExists(files, filename) {
        for (i in files) {
            if (files[i].fields.name == filename) {
                return true;
            }
        }
        return false;
    }


    // Checks for drag and drop browser support
    let dragNDropSupport = function() {
        let div = document.createElement('div');
        return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
    }();

    // Sends file with AJAX
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
        .on('dragend dragleave drop', function(e) {
            $form.removeClass('is-dragover');
        })
        .on('drop', function(e) {
            droppedFiles = e.originalEvent.dataTransfer.files;
            for (var file of droppedFiles) {
                if (file.size <= space_available) {
                    if (!(fileExists(files, file.name))) {
                        ajax_file_upload(file);
                    } else if (confirm("Voulez-vous vraiment envoyer ce fichier ?\nSi vous continuez, le fichier pré-existant sera écrasé.")){
                        ajax_file_upload(file);
                    }
                } else {
                    $("#file_too_big_error").show()
                }
            }
        })
        .on('change', function(e) {
        });

        function ajax_file_upload(file_obj) {
            if (file_obj != undefined) {
                let form_data = new FormData();
                form_data.append('file', file_obj);
                $.ajax({
                    type: 'POST',
                    url: '',
                    headers: {'X-CSRFToken': csrf_token},
                    contentType: false,
                    processData: false,
                    sequentialUploads: true,
                    data: form_data,
                    beforeSend: function(e) {
                        $("#modal-progress").modal("show");
                    },
                    xhr: function () {
                        let xhr = $.ajaxSettings.xhr();
                        xhr.upload.addEventListener('progress', function (e) {
                            let percent = 0;
                            let position = e.loaded || e.position;
                            let total = e.total;
                            if (e.lengthComputable) {
                                percent = Math.ceil(position / total * 100);
                            }
                            let strProgress = percent + "%";
                            $(".progress-bar").width(strProgress);
                            $(".progress-bar").text(strProgress);
                        }, true);
                        return xhr;
                    },
                    success: function(response) {
                        $("#modal-progress").modal("hide");
                        $('#file').val('');
                        location.reload();
                    }
                });
            }
        }

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    }

    $("#new_folder").on('click', function() {
        let name = prompt("Veuillez entrer le nom du dossier à créer");
        if (name != null) {
            if (!(name.indexOf("/") > -1)) {
                window.location = `/Files/create_dir/${current_dir}?dirname=${name}`;
            } else {
                alert("Le nom de votre dossier est invalide ! Il ne peut pas contenir le caractère '\/'");
            }
        }
    });

    $(".action_dir_delete").on('click', function() {
        return confirm("Voulez-vous vraiment supprimer ce dossier ? Son contenu sera définitivement effacé.");
    });

    $(".action_file_delete").on('click', function() {
        return confirm("Voulez-vous vraiment supprimer ce fichier ? Il sera définitivement effacé.");
    });
});
