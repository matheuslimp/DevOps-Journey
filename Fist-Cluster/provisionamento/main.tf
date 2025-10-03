terraform {
  required_providers {
    proxmox = {
      source  = "Telmate/proxmox"
      version = "2.9.11" # ou a versão mais recente
    }
  }
}

provider "proxmox" {
  pm_api_url      = "https://10.0.0.10:8006/api2/json"
  pm_api_token_id = "root@pam!root_api"
  pm_api_token_secret = "baa8c164-9cc9-419d-91c9-320fdbb601e6"
  pm_tls_insecure = true
}

resource "proxmox_vm_qemu" "vm1" {
  name        = "vm-teste"
  target_node = "pve"
  clone       = "ubuntu"
  cores       = 2
  memory      = 2048
  disk {
    size = "30G"
    type = "scsi"
    storage = "local-lvm"
  }
  network {
    model  = "virtio"
    bridge = "vmbr0"
  }
}

