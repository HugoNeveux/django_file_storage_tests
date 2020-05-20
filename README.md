# django_file_storage

![Django CI](https://github.com/HugoNeveux/django_file_storage/workflows/Django%20CI/badge.svg)

A multi-user cloud app for file storage, using the Django framework for python and boostrap 4.

## To-do list

### Urgent bugs that needs to be solved

- [x] files are not deleted when their folder is deleted
- [ ] Need to refresh page to see uploaded files


### Important features

- [x] User directories gestion
  - [x] Add user directory on user creation
  - [x] User directories privacy protection
- [x] Directory creation and deletion
- [x] **Add storage restrictions**
  - [ ] Fix storage restrictions (negative)
  - [x] Edit user model
  - [x] Show used space / allocated space
- [x] Front-end improvments
  - [x] Using boostrap
- [x] **User profile managment**
  - [x] Username / password changes
  - [x] Username and password reset
- [x] **File sharing**
  - [x] File sharing implementation
- [x] Files and folders managment
  - [x] Folder creation
  - [x] Moving files
    - [x] Moving files view
    - [x] Moving files front-end
  - [x] File deletion
- [x] Add files / folders icons
- [ ] Add 403, 404 and 500 html templates
- [ ] Add files with js on upload to avoid page reload
- [ ] Add upload button
- [ ] Add cancel upload button
- [ ] Allow color changes
- [ ] Importation from google drive

### Improvements
- [ ] API Creation
- [x] Use dropzone.js

### Secondary features

- [ ] Bug report feature
- [ ] Credits
- [x] Theme settings
- [x] Favorite files / folders
    - [x] File model creation (association with FileSystemStorage)
    - [x] Favorite files view

### Rewrite

- [x] File upload, share, settings, etc.
- [ ] Folder share & folder favorite
- [ ] Rewrite tests
- [ ] Completely remove UserFile model  
