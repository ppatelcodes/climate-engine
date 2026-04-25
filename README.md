# Climate Risk Financial Impact Engine

This project analyzes how real-world climate events impact financial markets and company performance using event-driven analysis and scenario-based stress testing.

It combines climate data with stock market data to quantify sector-level exposure and simulate potential financial risk under future climate scenarios.

---

## Overview

Climate risk is increasingly being recognized as a financial risk factor, not just an environmental issue. This project aims to bridge that gap by linking climate events such as floods, storms, and heatwaves with stock market behavior.

The system captures how markets react before and after climate shocks and evaluates sector-level sensitivity across industries.

---

## Key Features

* Event-driven analysis linking climate events to stock returns
* Sector-level impact comparison (Energy, Metals, Cement, Banking, IT)
* Volatility and return shift analysis around event windows
* Monte Carlo-based stress testing for future climate scenarios
* Clean data pipeline integrating multiple real-world datasets

---

## Architecture & Pipeline

Climate Data → Event Timeline
                    ↓
Stock Prices → Return Calculation
                    ↓
Event Study → Impact Measurement
                    ↓
Sector Analysis → Comparative Risk
                    ↓
Stress Testing → Scenario Simulation

---

## Results & Visualizations

### Sector Impact of Climate Events

![Sector Impact](data/processed/visuals/sector_impact.png)

### Event-Type Impact Analysis

![Event Type Impact](data/processed/visuals/event_type_impact.png)

### Impact Distribution

![Impact Distribution](data/processed/visuals/impact_distribution.png)

### Sector Sensitivity Heatmap

![Heatmap](data/processed/visuals/sector_event_heatmap.png)


## Key Insights

* Climate events show measurable impact on stock returns across sectors
* Infrastructure-heavy sectors tend to exhibit higher sensitivity
* IT sector behaves relatively stable, acting as a control group
* Volatility generally increases following major climate events
* Different event types (floods, storms, heatwaves) affect sectors differently


## Methodology

* Event Study Window: ±5 trading days around each event
* Impact Calculation:
  `Impact = Average Return After Event – Average Return Before Event`
* Sector aggregation performed using mean impact across companies
* Stress testing performed using Monte Carlo simulation


## Limitations

* External macroeconomic factors are not explicitly controlled
* Climate event timing may involve approximations
* Causality cannot be fully isolated from broader market movements


## Future Improvements

* Add ESG scoring for deeper sustainability analysis
* Incorporate macroeconomic variables (GDP, inflation, rates)
* Expand analysis across multiple countries
* Build an interactive dashboard (Streamlit / Power BI)


## Tech Stack

* Python (Pandas, NumPy)
* Kite Connect API (stock data)
* Matplotlib & Seaborn (visualization)
* Excel (climate dataset processing)


## Project Structure

climate-engine/
│
├── src/                     # Core scripts
├── data/
│   ├── raw/                # Raw datasets
│   └── processed/          # Cleaned data + outputs
│
├── requirements.txt
├── README.md
└── .gitignore


## Summary

This project demonstrates how climate risk can be translated into quantifiable financial impact, enabling better understanding of sector vulnerability and portfolio-level risk under climate stress scenarios.