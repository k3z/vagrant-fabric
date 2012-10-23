# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  # All Vagrant configuration is done here. 

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "debian-squeeze-64"

  # The url from where the 'config.vm.box' box will be fetched if it
  config.vm.box_url = "http://puppetlabs.s3.amazonaws.com/pub/squeeze64.box"

  # Forward a port from the guest to the host, which allows for outside
  # computers to access the VM, whereas host only networking does not.
  config.vm.forward_port 80, 8080
  config.vm.forward_port 3306, 3307

  # Share an additional folder to the guest VM. The first argument is
  # an identifier, the second is the path on the guest to mount the
  # folder, and the third is the path on the host to the actual folder.
  config.vm.share_folder "v-www", "/vagrant_www", "../vagrant_www"

end
