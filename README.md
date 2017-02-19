# FullStack-Project--5

# SongCatalog

### Keypoints:

* Develop a RESTful web application using the Python framework Flask

* Implementing third-party OAuth authentication.

* Implementing CRUD (create, read, update and delete) operations.

## How to Run:

### Prerequisites

- [Python ~2.7](https://www.python.org/)  
- [Vagrant](https://www.vagrantup.com/)
- [VirtualBox](https://www.virtualbox.org/)


### Steps to follow up

For an initial set up please follow these 2 steps:

1. Download or clone the [fullstack-nanodegree-vm repository](https://github.com/udacity/fullstack-nanodegree-vm).

2. Find the *catalog* folder and replace it with the content of this current repository, by either downloading it or cloning it - [Github Link](https://github.com/iliketomatoes/tournament).


### Launch

Launch the Vagrant VM from inside the *vagrant* folder with:

`vagrant up`

`vagrant ssh`

Then move inside the catalog folder:

`cd /vagrant/catalog`

Then lift the application:

`python app.py`

After the last command you are able to browse the application at this URL:

`http://localhost:8000/`

It is important you use *localhost* instead of *0.0.0.0* inside the URL address. That will prevent OAuth from failing.
