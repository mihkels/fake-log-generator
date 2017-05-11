# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "wholebits/ubuntu17.04-64"

    config.vm.provider "parallels" do |v, override|
      # override.update_guest_tools = true
      override.vm.synced_folder "./", "/vagrant", mount_options: ["share"]
      override.vm.synced_folder "../gobblin-log-storage", "/gobblin", mount_options: ["share"]
    end

  config.vm.provision "shell", inline: <<-SHELL
        apt-get update
        apt-get install vim apt-transport-https ca-certificates curl software-properties-common -y
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        apt-key fingerprint 0EBFCD88
        add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
            $(lsb_release -cs) \
            edge"
        apt-get remove docker docker-engine -y
        apt-get update
        apt-get install docker-ce -y
        apt-get install python-pip -y
        pip install --upgrade docker-compose

        groupadd docker
        gpasswd -a vagrant docker
        service docker restart
  SHELL
end
