resource "kubernetes_manifest" "notes_app_namespace" {
  manifest = {
    apiVersion = "v1"
    kind       = "Namespace"
    metadata = { name = "notes-app" }
  }
}

# You can either define manifests here OR point to your existing YAML files
resource "kubernetes_manifest" "notes_deployment" {
  manifest = yamldecode(file("../kubernetes/deployment.yaml"))
  depends_on = [kubernetes_manifest.notes_app_namespace]
}