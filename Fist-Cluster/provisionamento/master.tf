resource "proxmox_vm_qemu" "master" {
  count       = var.vm_master_count
  name        = "okd-master-${count.index + 1}"
  target_node = "pve"
  clone       = var.vm_template

  cores       = var.vm_cpu_master
  memory      = var.vm_ram_master
  scsihw      = "virtio-scsi-pci"

  disk {
    size = var.vm_disk_master
    type = "scsi"
    storage = var.vm_storage
  }

  network {
    model  = "virtio"
    bridge = var.vm_network
  }

  agent = 1
}

