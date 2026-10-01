"""
Creates Power BI PBIDS (Data Source) and PBIP (Project) files for 1-click loading into Power BI Desktop.
"""

import os
import json

def create_powerbi_project_files():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "power_bi_dashboard")
    os.makedirs(output_dir, exist_ok=True)
    
    excel_path = os.path.abspath(os.path.join(output_dir, "PowerBI_TellCo_Analytics_Model.xlsx"))
    
    # 1. Create .pbids (Power BI Data Source File)
    pbids_data = {
        "version": "0.1",
        "connections": [
            {
                "details": {
                    "protocol": "file",
                    "path": excel_path
                },
                "options": {},
                "mode": "DirectQuery"
            }
        ]
    }
    
    pbids_path = os.path.join(output_dir, "TellCo_Analytics_DataSource.pbids")
    with open(pbids_path, "w", encoding="utf-8") as f:
        json.dump(pbids_data, f, indent=2)
    print(f"Created {pbids_path}")
    
    # 2. Create PBIP Dataset Folder Structure & model.bim
    dataset_dir = os.path.join(output_dir, "TellCo_Analytics.Dataset")
    os.makedirs(dataset_dir, exist_ok=True)
    
    model_bim = {
        "name": "TellCo_Analytics_Model",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "en-US",
            "dataAccessOptions": {
                "legacyRedirects": True,
                "returnErrorValuesAsNull": True
            },
            "tables": [
                {
                    "name": "Fact_Subscriber_Sessions",
                    "columns": [
                        {"name": "MSISDN_Number", "dataType": "string", "sourceColumn": "MSISDN_Number"},
                        {"name": "Dur._ms", "dataType": "int64", "sourceColumn": "Dur._ms"},
                        {"name": "Handset_Manufacturer", "dataType": "string", "sourceColumn": "Handset_Manufacturer"},
                        {"name": "Handset_Type", "dataType": "string", "sourceColumn": "Handset_Type"},
                        {"name": "Total_Data_Bytes", "dataType": "int64", "sourceColumn": "Total_Data_Bytes"},
                        {"name": "Avg_Bearer_TP_DL_kbps", "dataType": "double", "sourceColumn": "Avg_Bearer_TP_DL_kbps"},
                        {"name": "Avg_RTT_DL_ms", "dataType": "double", "sourceColumn": "Avg_RTT_DL_ms"},
                        {"name": "Gaming_DL_Bytes", "dataType": "int64", "sourceColumn": "Gaming_DL_Bytes"},
                        {"name": "Gaming_UL_Bytes", "dataType": "int64", "sourceColumn": "Gaming_UL_Bytes"},
                        {"name": "Youtube_DL_Bytes", "dataType": "int64", "sourceColumn": "Youtube_DL_Bytes"},
                        {"name": "Netflix_DL_Bytes", "dataType": "int64", "sourceColumn": "Netflix_DL_Bytes"}
                    ],
                    "measures": [
                        {"name": "Total Active Subscribers", "expression": "DISTINCTCOUNT(Fact_Subscriber_Sessions[MSISDN_Number])"},
                        {"name": "Total Data Traffic (GB)", "expression": "SUM(Fact_Subscriber_Sessions[Total_Data_Bytes]) / (1024 * 1024 * 1024)"},
                        {"name": "Gaming Traffic Share %", "expression": "DIVIDE((SUM(Fact_Subscriber_Sessions[Gaming_DL_Bytes]) + SUM(Fact_Subscriber_Sessions[Gaming_UL_Bytes])) / (1024 * 1024 * 1024), [Total Data Traffic (GB)], 0)"},
                        {"name": "Average Throughput (kbps)", "expression": "AVERAGE(Fact_Subscriber_Sessions[Avg_Bearer_TP_DL_kbps])"},
                        {"name": "Average Latency RTT (ms)", "expression": "AVERAGE(Fact_Subscriber_Sessions[Avg_RTT_DL_ms])"}
                    ]
                },
                {
                    "name": "Dim_User_Analytics_Summary",
                    "columns": [
                        {"name": "MSISDN_Number", "dataType": "string", "sourceColumn": "MSISDN_Number"},
                        {"name": "Total_Sessions", "dataType": "int64", "sourceColumn": "Total_Sessions"},
                        {"name": "Total_Duration_ms", "dataType": "int64", "sourceColumn": "Total_Duration_ms"},
                        {"name": "Satisfaction_Score", "dataType": "double", "sourceColumn": "Satisfaction_Score"}
                    ],
                    "measures": [
                        {"name": "Avg Satisfaction Score", "expression": "AVERAGE(Dim_User_Analytics_Summary[Satisfaction_Score])"}
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "Rel_Subscriber_Sessions_Summary",
                    "fromTable": "Fact_Subscriber_Sessions",
                    "fromColumn": "MSISDN_Number",
                    "toTable": "Dim_User_Analytics_Summary",
                    "toColumn": "MSISDN_Number"
                }
            ]
        }
    }
    
    with open(os.path.join(dataset_dir, "model.bim"), "w", encoding="utf-8") as f:
        json.dump(model_bim, f, indent=2)
    print(f"Created {os.path.join(dataset_dir, 'model.bim')}")
    
    # 3. Create Report Directory & PBIR Definition
    report_dir = os.path.join(output_dir, "TellCo_Analytics.Report")
    os.makedirs(report_dir, exist_ok=True)
    
    pbir_data = {
        "version": "1.0",
        "datasetReference": {
            "byPath": {
                "path": "../TellCo_Analytics.Dataset"
            }
        }
    }
    with open(os.path.join(report_dir, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump(pbir_data, f, indent=2)
    print(f"Created {os.path.join(report_dir, 'definition.pbir')}")
    
    # Root .pbip file
    pbip_data = {
        "version": "1.0",
        "artifacts": [
            {
                "report": {
                    "path": "TellCo_Analytics.Report"
                }
            }
        ]
    }
    with open(os.path.join(output_dir, "TellCo_Analytics.pbip"), "w", encoding="utf-8") as f:
        json.dump(pbip_data, f, indent=2)
    print(f"Created {os.path.join(output_dir, 'TellCo_Analytics.pbip')}")

if __name__ == "__main__":
    create_powerbi_project_files()
