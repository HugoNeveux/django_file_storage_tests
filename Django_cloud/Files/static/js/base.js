$(function() {    
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
})
