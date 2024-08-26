from pulumi_gcp import compute

class ComputeOperations:
    def __init__(self):
        pass

    def create_instance(self, name, zone, machine_type="f1-micro", boot_disk_size_gb=10):
        instance = compute.Instance(name,
            machine_type=machine_type,
            zone=zone,
            boot_disk=compute.InstanceBootDiskArgs(
                initialize_params=compute.InstanceBootDiskInitializeParamsArgs(
                    image="debian-cloud/debian-9",
                    size=boot_disk_size_gb
                )
            ),
            network_interfaces=[compute.InstanceNetworkInterfaceArgs(
                network="default",
                access_configs=[compute.InstanceNetworkInterfaceAccessConfigArgs()],
            )]
        )
        return instance

    def start_instance(self, instance_id):
        instance = compute.Instance.get(instance_id)
        instance.start()
        return instance

    def stop_instance(self, instance_id):
        instance = compute.Instance.get(instance_id)
        instance.stop()
        return instance

    def delete_instance(self, instance_id):
        instance = compute.Instance.get(instance_id)
        instance.delete()
        return instance
