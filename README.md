# Checkout FinOps Model

A simple prototype showing how driver-based cloud cost modeling connects infrastructure usage to business unit economics.

## What it does

This project:
- models cloud infrastructure drivers for an e-commerce checkout API
- calculates infrastructure cost
- translates cloud spend into cost per transaction, cost per order, and cost per user

## Files

- `data/drivers.json` → infrastructure usage drivers
- `data/rates.json` → cloud unit rates
- `data/business_metrics.json` → business output metrics
- `main.py` → cost and unit economics calculator
- `output/unit_economics_report.json` → generated report

## Run

```bash
python3 main.py