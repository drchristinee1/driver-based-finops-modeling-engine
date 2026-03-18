import json


def load_json_file(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


def calculate_costs(drivers_data, rates_data, business_data, scenario_data):
    drivers = drivers_data["drivers"]
    rates = rates_data["rates"]
    metrics = business_data["business_metrics"]

    # Drivers
    ec2_hours = drivers["compute"]["instance_hours"]
    rds_hours = drivers["database"]["db_hours"]
    s3_gb = drivers["storage"]["storage_gb"]

    # Rates
    ec2_rate = rates["compute"]["ec2_per_hour"]
    rds_rate = rates["database"]["rds_per_hour"]
    s3_rate = rates["storage"]["s3_per_gb"]

    # Costs
    compute_cost = ec2_hours * ec2_rate
    database_cost = rds_hours * rds_rate
    storage_cost = s3_gb * s3_rate
    total_cost = compute_cost + database_cost + storage_cost

    # Business metrics
    transactions = metrics["transactions"]
    orders_completed = metrics["orders_completed"]
    active_users = metrics["active_users"]

    # Unit economics
    cost_per_transaction = total_cost / transactions if transactions else 0
    cost_per_order = total_cost / orders_completed if orders_completed else 0
    cost_per_user = total_cost / active_users if active_users else 0

    # Scenario inputs
    scenario_name = scenario_data["scenario_name"]
    transaction_growth_percent = scenario_data["transaction_growth_percent"]
    compute_growth_percent = scenario_data["compute_growth_percent"]
    database_growth_percent = scenario_data["database_growth_percent"]
    storage_growth_percent = scenario_data["storage_growth_percent"]

    # Scenario projections
    projected_transactions = transactions * (1 + transaction_growth_percent / 100)
    projected_compute_hours = ec2_hours * (1 + compute_growth_percent / 100)
    projected_database_hours = rds_hours * (1 + database_growth_percent / 100)
    projected_storage_gb = s3_gb * (1 + storage_growth_percent / 100)

    projected_compute_cost = projected_compute_hours * ec2_rate
    projected_database_cost = projected_database_hours * rds_rate
    projected_storage_cost = projected_storage_gb * s3_rate
    projected_total_cost = (
        projected_compute_cost + projected_database_cost + projected_storage_cost
    )

    projected_cost_per_transaction = (
        projected_total_cost / projected_transactions if projected_transactions else 0
    )

    # Report
    report = {
        "service": drivers_data["service"],

        "driver_usage": {
            "compute_hours": ec2_hours,
            "database_hours": rds_hours,
            "storage_gb": s3_gb
        },

        "rates_used": {
            "compute_rate_per_hour": ec2_rate,
            "database_rate_per_hour": rds_rate,
            "storage_rate_per_gb": s3_rate
        },

        "cost_breakdown": {
            "compute_cost": round(compute_cost, 2),
            "database_cost": round(database_cost, 2),
            "storage_cost": round(storage_cost, 2),
            "total_cost": round(total_cost, 2)
        },

        "cost_distribution": {
            "compute_percent": round((compute_cost / total_cost) * 100, 2) if total_cost else 0,
            "database_percent": round((database_cost / total_cost) * 100, 2) if total_cost else 0,
            "storage_percent": round((storage_cost / total_cost) * 100, 2) if total_cost else 0
        },

        "business_metrics": {
            "transactions": transactions,
            "orders_completed": orders_completed,
            "active_users": active_users
        },

        "unit_economics": {
            "cost_per_transaction": round(cost_per_transaction, 4),
            "cost_per_order": round(cost_per_order, 4),
            "cost_per_user": round(cost_per_user, 4)
        },

        "scenario_analysis": {
            "scenario_name": scenario_name,

            "growth_assumptions": {
                "transaction_growth_percent": transaction_growth_percent,
                "compute_growth_percent": compute_growth_percent,
                "database_growth_percent": database_growth_percent,
                "storage_growth_percent": storage_growth_percent
            },

            "projected_driver_usage": {
                "projected_compute_hours": round(projected_compute_hours, 2),
                "projected_database_hours": round(projected_database_hours, 2),
                "projected_storage_gb": round(projected_storage_gb, 2)
            },

            "projected_cost_breakdown": {
                "projected_compute_cost": round(projected_compute_cost, 2),
                "projected_database_cost": round(projected_database_cost, 2),
                "projected_storage_cost": round(projected_storage_cost, 2),
                "projected_total_cost": round(projected_total_cost, 2)
            },

            "projected_business_metrics": {
                "projected_transactions": round(projected_transactions, 2)
            },

            "projected_unit_economics": {
                "projected_cost_per_transaction": round(projected_cost_per_transaction, 4)
            }
        }
    }

    return report


def save_report(report, output_path):
    with open(output_path, "w") as file:
        json.dump(report, file, indent=4)


def main():
    drivers_path = "data/drivers.json"
    rates_path = "data/rates.json"
    business_path = "data/business_metrics.json"
    scenario_path = "data/scenario.json"
    output_path = "output/unit_economics_report.json"

    drivers_data = load_json_file(drivers_path)
    rates_data = load_json_file(rates_path)
    business_data = load_json_file(business_path)
    scenario_data = load_json_file(scenario_path)

    report = calculate_costs(drivers_data, rates_data, business_data, scenario_data)
    save_report(report, output_path)

    print("\n✅ Unit economics report generated successfully.")
    print(f"📄 Output saved to: {output_path}")
    print("\nSummary:")
    print(json.dumps(report, indent=4))


if __name__ == "__main__":
    main()