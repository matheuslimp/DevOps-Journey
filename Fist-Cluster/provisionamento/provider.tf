terraform {
  required_providers {
    proxmox = {
      source  = "Telmate/proxmox"
      version = "2.9.11" # ou a versão mais recente
    }
  }
}

provider "proxmox" {
  pm_api_url      = "[URL DA API https://X.X.X.X:8006/api2/json]"
  pm_api_token_id = "[NOME DO TOKEN (IDTOKEN)]"
  pm_api_token_secret = "[API KEY]"
  pm_tls_insecure = true
}
