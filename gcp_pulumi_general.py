
import pulumi
from pulumi_gcp import compute, storage
import logging


resources = [instances, vpc, build, run, deploy, dns, artifact_reg, vertex_ai] #Options include buckets etc @TODO Implement command line tool.

def get_resources(resources: list):
    instances = compute.Instance.get_all()
    buckets = storage.Bucket.get_all()
    return instances, buckets

def stop_all():
    stopped_instances = []
    instances = get_resources()

    # Stop all instances
    for instance in instances:
        instance.stop()
        stopped_instances.append(instance)

    return print("Stopped:\n {}")


def delete_all():
    instances, buckets = get_resources()
    deleted_instance=[]
    deleted_buckets=[]
    
    for bucket in buckets:
        action = input(f"Delete: {bucket}?")
        if action == "yes" or "y":
            bucket.delete()
            deleted_buckets.append(f"{bucket} deleted")
            print(f"{bucket} deleted")
        else:
            continue
    
    for instance in instances:
        action = input(f"Delete: {instance}?")
        if action == "yes" or "y":
            instance.delete()
            deleted_buckets.append(f"{instance} deleted")
            print(f"{bucket} deleted")
        else:
            continue
    
    