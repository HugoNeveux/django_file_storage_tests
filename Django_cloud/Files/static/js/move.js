$('.action_file_move').on('click', function (e) {
    $li = $(e.target).closest('li.file');
    console.log($li);
    path = $li.children('.name__icon').text();
    console.log(path);
    if ($('#modalMoveUl li.folder')) {
        $('#modalMoveUl li.folder').remove();
    }
    for (dir of $('.dir')) {
        dirname = dir.text;
        from = current_dir + path;
        to = current_dir + dirname;
        $('#modalMoveUl').append(
            `<li class="folder" style="width:100%;"><a href="/Files/mv?from=${from}&to=${to}"><span class="fa fa-folder" id="icone_folder"></span>${dirname}</a></li>`
        );
    }
    $('#modalMove').modal('show');
})
