function pathJoin(parts, sep){
   let separator = sep || '/';
   let replace   = new RegExp(separator+'{1,}', 'g');
   return parts.join(separator).replace(replace, separator);
}

$(function() {
    $("#new_folder").on('click', function() {
        let name = prompt("Veuillez entrer le nom du dossier à créer");
        let path_to_dir = "";
        if (name != null) {
            if ((name.indexOf("/") <= -1) && name.length <= 100) {
                if (current_dir == "") {
                    path_to_dir = name;
                } else {
                    path_to_dir = pathJoin([current_dir, name]);
                }
                window.location = `/Files/create_dir/${path_to_dir}?next=${current_dir}`;
            } else if (name.length > 100) {
                alert("Le nom de votre dossier est trop long. Il ne peut pas dépasser 100 caractères.");
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
})
