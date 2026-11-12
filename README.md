# Laboratorio 11 - Infraestructura Big Data como Código (Terraform + Floci)

Curso: Business Intelligence and Big Data - Universidad César Vallejo
Autor: César Alexander Rojas Sinche

## Qué hace este proyecto
Crea con Terraform una plataforma de datos local (AWS emulado con Floci):
- Un Data Lake en S3 (`ucv-data-platform`) con dominios `sales`, `customers`, `products`
  y capas `bronze`, `silver`, `gold`.
- Una base de datos de Glue Data Catalog por dominio (`sales_domain`, `customers_domain`, `products_domain`).

## Requisitos
Docker Desktop, Terraform >= 1.6, AWS CLI v2, Git.

## Cómo usarlo
```bash
docker compose up -d
cd terraform
terraform init
terraform validate
terraform plan
terraform apply
```

Verificar:
```bash
aws --endpoint-url http://localhost:4566 s3 ls s3://ucv-data-platform/ --recursive
aws --endpoint-url http://localhost:4566 glue get-databases
```

Eliminar todo:
```bash
terraform destroy
```

## Notas
- No se sube `terraform.tfstate`, `.terraform/` ni `data/` (ver `.gitignore`).
- Las credenciales `test/test` son ficticias; no se usa ninguna cuenta AWS real.
