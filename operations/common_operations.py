import pulumi
from pulumi_gcp import compute, storage, secretmanager
import logging

class CommonOperations:
    def __init__(self):
        pass

    def get_resources(self):
        instances = compute.Instance.get_all()
        buckets = storage.Bucket.get_all()
        return instances, buckets

    def stop_all_instances(self):
        instances, _ = self.get_resources()
        stopped_instances = []
        for instance in instances:
            instance.stop()
            stopped_instances.append(instance)
        return stopped_instances

    def delete_all_resources(self):
        instances, buckets = self.get_resources()
        deleted_resources = []

        for bucket in buckets:
            action = input(f"Delete bucket {bucket.name}? (yes/no): ")
            if action.lower() in ["yes", "y"]:
                bucket.delete()
                deleted_resources.append(f"Bucket {bucket.name} deleted")

        for instance in instances:
            action = input(f"Delete instance {instance.name}? (yes/no): ")
            if action.lower() in ["yes", "y"]:
                instance.delete()
                deleted_resources.append(f"Instance {instance.name} deleted")

        return deleted_resources

    def query_all_resources(self, output_file=None):
        instances, buckets = self.get_resources()
        report = f"Instances: {len(instances)}\nBuckets: {len(buckets)}"
        print(report)

        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)

        return report
