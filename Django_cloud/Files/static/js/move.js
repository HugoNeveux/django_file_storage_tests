function pathJoin(parts, sep){
   let separator = sep || '/';
   let replace   = new RegExp(separator+'{1,}', 'g');
   return parts.join(separator).replace(replace, separator);
}

$('.action_file_move').on('click', function (e) {
    let $li = $(e.target).closest('li.file');
    let path = $li.children('.name__icon').text();
    if ($('#modalMoveUl li.folder')) {
        $('#modalMoveUl li.folder').remove();
    }
    let from = pathJoin([current_dir, path]);
    from = from.replace(/(^\/+|\/+$)/mg, '');
    if (current_dir != "") {
        $('#modalMoveUl').append(
            `<li class="folder" style="width:100%;">\
            <a href="/Files/mv/?from=${from}&to=previous&redirect=${current_dir}">\
            <span class="fa fa-folder" id="icone_folder"></span>Dossier précédent</a></li>`
        );
    }
    for (dir of $('.dir')) {
        let to = pathJoin([current_dir, dir.text]);
        to = to.replace(/(^\/+|\/+$)/mg, '');
        $('#modalMoveUl').append(
            `<li class="folder" style="width:100%;">\
            <a href="/Files/mv/?from=${from}&to=${to}&redirect=${current_dir}">\
            <span class="fa fa-folder" id="icone_folder"></span>${dir.text}</a></li>`
        );
    }
    $('#modalMove').modal('show');
})
