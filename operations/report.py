import logging
from operations.common_operations import CommonOperations

class ReportService:
    def __init__(self):
        self.common_ops = CommonOperations()

    def generate_report(self):
        """Generates a comprehensive report on active assets and logs errors."""
        try:
            instances, buckets = self.common_ops.get_resources()

            report = f"Active Compute Instances: {len(instances)}\n" \
                     f"Active Storage Buckets: {len(buckets)}\n"

            logging.info("Generating report on active assets...")
            logging.info(report)

            with open("./tmp/log/report.txt", "w") as report_file:
                report_file.write(report)

            logging.info("Report generated successfully.")
            return report

        except Exception as e:
            logging.error(f"Error generating report: {e}")
            raise

    def list_errors(self):
        """Lists all logged errors."""
        try:
            with open("./tmp/log/error.log", "r") as error_file:
                errors = error_file.read()

            if errors:
                logging.info("Listing all errors logged:")
                logging.info(errors)
            else:
                logging.info("No errors logged.")

        except FileNotFoundError:
            logging.info("No error log found.")
        except Exception as e:
            logging.error(f"Error reading error log: {e}")
            raise