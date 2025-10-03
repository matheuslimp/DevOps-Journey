resource "proxmox_vm_qemu" "worker" {
  count       = var.vm_worker_count
  name        = "okd-worker-${count.index + 1}"
  target_node = "pve"
  clone       = var.vm_template

  cores       = var.vm_cpu_worker
  memory      = var.vm_ram_worker
  scsihw      = "virtio-scsi-pci"

  disk {
    size = var.vm_disk_worker
    type = "scsi"
    storage = var.vm_storage
  }

  network {
    model  = "virtio"
    bridge = var.vm_network
  }

  agent = 1
}

