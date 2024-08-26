from pulumi_gcp import secretmanager

class SecretsManagerOperations:
    def __init__(self):
        pass

    def create_secret(self, name, secret_data):
        secret = secretmanager.Secret(name, secret_data=secret_data)
        return secret

    def get_secret(self, secret_id):
        secret = secretmanager.Secret.get(secret_id)
        return secret

    def delete_secret(self, secret_id):
        secret = secretmanager.Secret.get(secret_id)
        return secret.delete()
