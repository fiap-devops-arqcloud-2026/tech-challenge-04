variable "github_token" {
 type = string
 sensitive = true
 default = ""
}
resource "terraform_data" "repo" {
 count = var.github_token != "" ? 1 : 0
 input = "dummy-public-value"
}
