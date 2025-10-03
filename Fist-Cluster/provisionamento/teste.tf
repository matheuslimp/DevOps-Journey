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
  pm_user         = "root@pam"
  pm_password     = "Ff0975483$"
  pm_tls_insecure = true
}

resource "proxmox_vm_qemu" "vm1" {
  name        = "vm-teste"
  target_node = "pve"
  clone       = "template-ubuntu"
  cores       = 2
  memory      = 2048
  disk {
    size = "10G"
    type = "scsi"
    storage = "local-lvm"
  }
  network {
    model  = "virtio"
    bridge = "vmbr0"
  }
}

