    function fileExists(files, filename) {
        for (let i in files) {
            if (files[i].name == filename) {
                return true;
            }
        }
        return false;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie != '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = $.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    let csrftoken = getCookie('csrftoken');

    let pathname = window.location.pathname;
    if (pathname == '/Files/' || pathname.startsWith('/Files/tree/')) {
        Dropzone.autoDiscover = false;
        $('#multiFileUpload').dropzone({
            crossDomain: false,
            paramName: "file",
            parallelUploads: 5,
            autoProcessQueue: true,
            filesizeBase: 1024,
            maxFilesize: 1073741824,
            dictRemoveFileConfirmation: null,
            assRemoveLinks: true,
            dataType: "HTML",
            timeout: 180000,
            clickable: true,
            chunking: false,
            chunkSize: 1048576, // 1Ko
            parallelChunkUploads: true,
            retryChunks: true,
            previewsContainer: '#dropzone-previews',
            previewTemplate: '<div id="dztp" class="col text-center transition-width">\
            <div class="dz-filename">\
            <span data-dz-name=""></span>\
            </div>\
            <div class="dz-progress">\
            <span class="dz-upload text-white" data-dz-uploadprogress="">\
            <span class="progress-text"></span>\
            </span>\
            </div>\
            </div>',
            init: function() {
                myDropzone = this;
                this.on('uploadprogress', function(file, progress, bytesSent) {
                    progress = bytesSent / file.size * 100;
                    percent = Math.floor(progress);
                    if (file.previewElement) {
                        let progressElement = file.previewElement.querySelector('[data-dz-uploadprogress]');
                        if (percent <= 100) {
                            progressElement.querySelector('.progress-text').textContent = percent + "%";
                        } else {
                            progressElement.querySelector('.progress-text').textContent = '100%';
                        }
                    }
                });
                this.on('sending', function(file, xhr, formData) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    if ((fileExists(files, file.name))) {
                        if (!confirm("Voulez-vous vraiment envoyer ce fichier ?\nSi vous continuez, le fichier pré-existant sera écrasé.")) {
                            this.removeFile(file);
                        }
                    }
                });
                this.on("maxfilesexceeded", function(data) {
                    let res = eval('(' + data.xhr.responseText + ')');
                });
                this.on("error", function(file, message) {
                    if ($('#errorMsg').length > 0) {
                        $('#errorMsg').remove();
                    }
                    let msg = "";
                    for (let key in message) {
                        msg += message[key] + "<br/>";
                    }
                    $('#errorZone').append(`<span id="errorMsg">${msg}</span>`);
                    $('#errorZone').show();
                });
                this.on('complete', function(file) {
                    this.removeFile(file);
                });
                this.on('success', function(file, response) {
                    if (response.file_html) {
                        $('ul#fileList').append(response.file_html);
                    }
                    $('span#usedSpace').text(response.space_used);
                });
            },
        });
    }
    $(window).on('dragover', function(e) {
        e.preventDefault();
    });
    $(window).on('drop', function(e) {
        e.preventDefault();
    });
