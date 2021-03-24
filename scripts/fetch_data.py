from foresee.foresee import update_csat, fetch_foresee_data_for_services
from google_analytics.analytics_helpers import initialize_analyticsreporting, get_totals_from_report, \
    sort_tools_by_transactions, get_total_from_report, write_report_to_csv
from utils.calculation_utils import calculate_trend
from google_analytics.ga_requests import get_all_transactions_request, get_last_month_users_request, \
    get_transactions_for_tools_request, get_total_logged_in_users_request, \
    get_logged_in_users_per_month_request
from ruamel import yaml
from tenacity import retry, wait_fixed, stop_after_attempt
import os
import logging


@retry(wait=wait_fixed(10), stop=stop_after_attempt(5))
def get_ga_report(analytics_service, request):
    response = analytics_service.reports().batchGet(
        body={
            'reportRequests': [
                request
            ],
            "useResourceQuotas": False
        }
    ).execute()

    return response['reports'][0]


def fetch_transactions_for_tool(analytics_service, tool):
    report = get_ga_report(analytics_service, get_transactions_for_tools_request(tool))
    return {
        "title": tool["title"],
        "transactions": get_total_from_report(report)
    }


def fetch_ga_data_for_service(analytics_service, service):
    print("Getting data for '%s'" % service["title"])

    report = get_ga_report(analytics_service, get_last_month_users_request(service["page_path_filter"]))
    users_total, previous_total = get_totals_from_report(report)
    users_trend = round(calculate_trend(previous_total, users_total), 1)

    tools = [
        fetch_transactions_for_tool(analytics_service, tool)
        for tool in service["tools"]
    ]

    sort_tools_by_transactions(tools)

    service_data = {
        "title": service["title"],
        "users_total": users_total,
        "users_trend": users_trend,
        "tools": tools
    }

    return service_data


def add_csat_data_to_counts(counts, services):
    logging.info("Getting csat data from foresee...")

    csat_scores_by_service = fetch_foresee_data_for_services(services)
    for service in counts["services"]:
        service.update(csat_scores_by_service[service['title']])

    counts["csat_total"] = str(update_csat()) + '%'


def main():
    analytics_service = initialize_analyticsreporting()

    logging.info("Writing transactions data...")
    transactions_report = get_ga_report(analytics_service, get_all_transactions_request())
    write_report_to_csv(transactions_report, "all_transactions.csv")

    logging.info("Writing users data...")
    total_users_report = get_ga_report(analytics_service, get_total_logged_in_users_request())
    monthly_users_report = get_ga_report(analytics_service, get_logged_in_users_per_month_request())
    write_report_to_csv(monthly_users_report, "all_logged_in_users_per_month.csv")

    counts = {
        "transactions_total": get_total_from_report(transactions_report),
        "users_total": get_total_from_report(total_users_report)
    }

    services_file_path = os.path.join(os.environ['CONFIG_DIR'], 'services.yml')
    with open(services_file_path, 'r') as services_file:
        services_input = yaml.load(services_file, yaml.RoundTripLoader)
        services = services_input["services"]

    counts["services"] = []

    for service in services:
        service_data = fetch_ga_data_for_service(analytics_service, service)
        counts["services"].append(service_data)

    add_csat_data_to_counts(counts, services)

    output_file = os.path.join(os.environ['DATA_DIR'], 'counts.yml')
    with open(output_file, 'w') as output:
        yaml.dump(counts, output, default_flow_style=False)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    main()
