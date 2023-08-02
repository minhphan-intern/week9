Vagrant.configure("2") do |config|
    config.hostmanager.enabled = true 
    config.hostmanager.manage_host = true
    config.vm.define "db" do |db|
        db.vm.box = "ubuntu/focal64"
        db.vm.network "private_network", ip: "192.168.56.11"
        db.vm.provision "shell", path: "db.sh"
    end
    config.vm.define "host1" do |host1|
        host1.vm.box = "ubuntu/focal64"
        host1.vm.network "private_network", ip: "192.168.56.10"
        host1.vm.provider "virtualbox" do |vb|
            vb.memory = "2048"
            vb.cpus = 2
        end 
        host1.vm.provision "shell", path: "server.sh"
    end
    config.vm.define "host2" do |host2|
        host2.vm.box = "ubuntu/focal64"
        host2.vm.network "private_network", ip: "192.168.56.12"
        host2.vm.provider "virtualbox" do |vb|
            vb.memory = "2048"
            vb.cpus = 2
        end
        host2.vm.provision "shell", path: "host.sh"
    end
  end