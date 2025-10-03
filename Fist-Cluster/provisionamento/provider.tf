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
