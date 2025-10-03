variable "vm_master_count" {
  default = 3
}

variable "vm_worker_count" {
  default = 1
}

variable "vm_infra_count" {
  default = 0
}

variable "vm_template" {
  default = "ubuntu"
}

variable "vm_storage" {
  default = "local-lvm"
}

variable "vm_network" {
  default = "vmbr0"
}

variable "vm_cpu_master" {
  default = 2
}

variable "vm_ram_master" {
  default = 6144
}

variable "vm_disk_master" {
  default = "40G"
}

variable "vm_cpu_worker" {
  default = 2
}

variable "vm_ram_worker" {
  default = 6144
}

variable "vm_disk_worker" {
  default = "40G"
}

