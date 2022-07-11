# Terraform
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

# postgres
docker volume create pgdata
docker run --name my-postgres -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres -v postgres-data:/var/lib/postgresql/data
