# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
	config.vm.box = "debian-7.5.0-amd64"
	config.vm.box_url = "http://hub.takeflight.net.au/files/debian-7.5.0-amd64.box"

	config.vm.network :forwarded_port,
		id: "http",
		guest: 1100,
		host: 1100
	config.vm.network :forwarded_port,
		id: "ssh",
		guest: 22,
		host: 1101

	config.vm.provision :shell,
		:path => "setup/install.sh"

	if File.exist? "Vagrantfile.local"
		instance_eval File.read("Vagrantfile.local"), "Vagrantfile.local"
	end
end