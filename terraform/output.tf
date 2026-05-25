output "cluster_name" {
  value = aws_eks_cluster.main.name
}

output "cluster_endpoint" {
  value = aws_eks_cluster.main.endpoint
}

output "ecr_inventory_url" {
  value = aws_ecr_repository.inventory.repository_url
}

output "ecr_cart_url" {
  value = aws_ecr_repository.cart.repository_url
}

output "ecr_payment_url" {
  value = aws_ecr_repository.payment.repository_url
}

output "bastion_public_ip" {
  value = aws_instance.bastion.public_ip
}