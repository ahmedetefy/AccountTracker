# AccountTracker 


## Installation 

This project uses Vagrant for VM management. 

* Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](http://downloads.vagrantup.com/).

* Clone this repository:

        $ git clone https://github.com/ahmedetefy/AccountTracker.git
 
 ## Commands Guide
 
        (1) Make sure your local host points to 0.0.0.0 on your machine
            
            $ echo "0.0.0.0 localhost" | sudo tee --append /etc/hosts
        
        (2) You need to cd in your cloned project directory
        
            $ cd AccountTracker
            
        (3) $ vagrant up
        
        (4) $ vagrant ssh
        
        (5) $ cd /vagrant/projects
        
        (6) $ mkvirtualenv --quiet django_project
        
        (7) $ cd AccountTracker
        
        (8) $ pip install -r requirements.txt
        
        (9) $ python manage.py makemigrations main
        
        (10) $ python manage.py migrate
        
        (11) $ python manage.py runserver 0.0.0.0:8000
        
        (12) $ Visit localhost:8000 in your web browser


# And ENJOY! Hope you like it!!        


