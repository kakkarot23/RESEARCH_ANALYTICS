# 📊 Power BI Dashboard & Star-Schema Data Model

This directory contains the complete **Power BI Analytics Dashboard Assets** for the TellCo Telecommunication Due Diligence & Subscriber Intelligence application.

---

## 📁 Included Files & Data Models

| File Name | Description | Power BI Use Case |
| :--- | :--- | :--- |
| `PowerBI_TellCo_Analytics_Model.xlsx` | Multi-sheet Excel Data Model | **1-Click Import**: Direct data source for Power BI Desktop |
| `Fact_Subscriber_Sessions.csv` | Fact Table | Granular xDR subscriber sessions & application traffic |
| `Dim_Handset_Device.csv` | Dimension Table | Handset type & manufacturer device catalog |
| `Dim_User_Analytics_Summary.csv` | Dimension Table | Aggregated metrics, engagement, and experience scores |
| `dax_measures.dax` | DAX Measures Library | Pre-written DAX formulas for KPIs, traffic shares, and ML scores |
| `powerbi_report_config.json` | Report Layout Schema | JSON layout structure for visuals, cards, and page layout |
| `power_bi_data_exporter.py` | Python Exporter | Pipeline script to regenerate Power BI datasets from raw data |

---

## ⚡ 1-Minute Setup Guide (Power BI Desktop)

1. **Open Power BI Desktop**.
2. Click **Get Data** -> **Excel Workbook**.
3. Select `PowerBI_TellCo_Analytics_Model.xlsx`.
4. Check all sheets (`User_Aggregates`, `Handset_Catalog`, `Fact_Subscriber_Sessions_Sample`) and click **Load**.
5. Import DAX measures from `dax_measures.dax` into your dataset.
6. Design executive visual pages using the layout guidelines defined in `powerbi_report_config.json`.

---

## 📐 Star-Schema Data Model Diagram

```
[Dim_Handset_Device]  <--- (Handset_Type) --->  [Fact_Subscriber_Sessions]  <--- (MSISDN_Number) --->  [Dim_User_Analytics_Summary]
```

---

## 📈 Key DAX Measures

* **Total Active Subscribers**: `DISTINCTCOUNT(Fact_Subscriber_Sessions[MSISDN_Number])`
* **Gaming Traffic Share %**: `DIVIDE([Gaming Data Traffic (GB)], [Total Data Traffic (GB)], 0)`
* **Average Throughput (kbps)**: `AVERAGE(Fact_Subscriber_Sessions[Avg_Bearer_TP_DL_kbps])`
* **Satisfaction Score**: `AVERAGE(Dim_User_Analytics_Summary[Satisfaction_Score])`
