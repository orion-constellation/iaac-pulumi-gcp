from pulumi_gcp import cloudrun, cloudbuild, clouddeploy

class CloudRunOperations:
    def __init__(self):
        pass

    def create_cloud_run_service(self, name, region, image):
        service = cloudrun.Service(name,
                                   location=region,
                                   template=cloudrun.ServiceTemplateArgs(
                                       spec=cloudrun.ServiceTemplateSpecArgs(
                                           containers=[cloudrun.ServiceTemplateSpecContainerArgs(
                                               image=image,
                                           )]
                                       )
                                   ))
        return service

    def create_cloud_build_trigger(self, name, repo_name, branch_name):
        trigger = cloudbuild.Trigger(name,
                                     github=cloudbuild.TriggerGithubArgs(
                                         name=repo_name,
                                         owner="your-github-username",
                                         push=cloudbuild.TriggerGithubPushArgs(
                                             branch=branch_name
                                         )
                                     ))
        return trigger

    def deploy_cloud(self, name, region, image):
        deployment = clouddeploy.DeliveryPipeline(name,
                                                  location=region,
                                                  project="your-gcp-project",
                                                  default_target_id="default",
                                                  render_args=clouddeploy.RenderArgs(
                                                      substitutions={
                                                          "IMAGE_NAME": image,
                                                      }
                                                  ))
        return deployment
