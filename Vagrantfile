# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/vivid64"

  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.network "forwarded_port", guest: 8080, host: 8080

  config.vm.synced_folder ".", "/app"

  config.vm.provision "shell", inline:
    "curl -sSL https://get.docker.com/ | sh
     curl -L https://github.com/docker/compose/releases/download/1.4.2/docker-compose-`uname -s`-`uname -m` > docker-compose
     mv docker-compose /bin/docker-compose
     chmod +x /bin/docker-compose
     chmod 777 /var/run/docker.sock
     curl -sSL https://shipyard-project.com/deploy | bash"
end
