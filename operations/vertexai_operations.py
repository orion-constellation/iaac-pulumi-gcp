from pulumi_gcp import vertexai

class VertexAIOperations:
    def __init__(self):
        pass

    def create_model(self, model_name, project_id, region):
        model = vertexai.Model(model_name,
                               project=project_id,
                               region=region,
                               display_name=model_name)
        return model

    def delete_model(self, model_id):
        model = vertexai.Model.get(model_id)
        model.delete()
        return model
