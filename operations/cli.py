import argparse
from operations.common_operations import CommonOperations
from operations.compute_operations import ComputeOperations

def main():
    parser = argparse.ArgumentParser(description="Pulumi GCP Operations CLI")
    parser.add_argument("--action", choices=["stop-all", "delete-all", "query-all", "create-instance"], required=True, help="Action to perform")
    parser.add_argument("--output", help="Optional output file for query results")

    args = parser.parse_args()

    common_ops = CommonOperations()
    compute_ops = ComputeOperations()

    if args.action == "stop-all":
        common_ops.stop_all_instances()

    elif args.action == "delete-all":
        common_ops.delete_all_resources()

    elif args.action == "query-all":
        common_ops.query_all_resources(output_file=args.output)

    elif args.action == "create-instance":
        instance = compute_ops.create_instance(name="example-instance", zone="us-central1-a")
        print(f"Created instance: {instance.name}")

if __name__ == "__main__":
    main()
