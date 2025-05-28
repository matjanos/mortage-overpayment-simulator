# Mortgage Overpayment Simulator

A Python simulation tool that compares three mortgage overpayment strategies to help you optimize your loan repayment.

## Purpose

This program simulates mortgage repayment using three different overpayment strategies:

1. **Mix Strategy** - Each overpayment reduces your monthly payment while maintaining the same total payment amount, providing flexibility and improved creditworthiness.

2. **Reduce Payment** - Maintains a constant overpayment amount while recalculating the base monthly payment based on the current balance, resulting in decreasing monthly payments over time.

3. **Reduce Term** - Each overpayment shortens the loan term while keeping monthly payments constant, maximizing interest savings.

## Usage

Run the simulation with required parameters:

```bash
python simulate.py --balance 196964 --interest 7.84 --payment 3873.80 --max 10000 --months 62
```

### Parameters

| Flag | Description | Example |
|------|-------------|---------|
| `--balance` | Remaining loan balance (PLN) | 196964 |
| `--interest` | Annual interest rate (%) | 7.84 |
| `--payment` | Current monthly payment (PLN) | 3873.80 |
| `--max` | Maximum monthly amount you can pay (PLN) | 10000 |
| `--months` | Remaining months until original end date | 62 |

## Output

The program generates:

- **Detailed payment schedules** for all three strategies showing monthly breakdown of payments, overpayments, interest, principal, and remaining balance
- **Summary statistics** including total interest paid and loan duration for each strategy
- **Comprehensive comparison** between all three approaches with the best strategy recommendation

## Example Output

```
--- Strategy 1: Mix Strategy ---
Month      Payment  Overpayment   Interest  Principal     Remaining
2025-06    3873.80      6126.20    1286.83    2586.97     188250.83
2025-07    3654.32      6345.68    1230.45    2423.87     179481.28
2025-08    ...

Total interest paid: 14569.43 PLN, total months: 22

--- Strategy 2: Reduce Payment ---
Month      Payment  Overpayment   Interest  Principal     Remaining
2025-06    3873.80      6126.20    1286.83    2586.97     188250.83
2025-07    3654.32      6126.20    1230.45    2423.87     179500.76
2025-08    ...

Total interest paid: 16303.77 PLN, total months: 26

--- Strategy 3: Reduce Term ---
Month      Payment  Overpayment   Interest  Principal     Remaining
2025-06    3873.80      6126.20    1286.83    2586.97     188250.83
2025-07    3873.80      6126.20    1230.45    2643.35     179481.28
2025-08    ...

Total interest paid: 14569.43 PLN, total months: 22

--- Comparison ---
Mix Strategy:        14569.43 PLN interest, 22 months
Reduce Payment:      16303.77 PLN interest, 26 months
Reduce Term:         14569.43 PLN interest, 22 months

Best strategy for interest savings: Mix Strategy

============================================================
                    COST REDUCTION SUMMARY                    
============================================================

Original scenario (no overpayment):
  Interest: 43211.61 PLN, Duration: 63 months

Savings compared to original:
  Mix Strategy:     28642.18 PLN saved, 41 months shorter
  Reduce Payment:   26907.84 PLN saved, 37 months shorter
  Reduce Term:      28642.18 PLN saved, 41 months shorter

============================================================
                 INTEREST COST COMPARISON                 
============================================================

Interest Cost Comparison (each █ ≈ 864 PLN):
Original (no overpay): ██████████████████████████████████████████████████ 43212 PLN
Mix Strategy:          ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 14569 PLN
Reduce Payment:        ███████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 16304 PLN
Reduce Term:           ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 14569 PLN

Loan Duration Comparison (each █ ≈ 1.3 months):
Original (no overpay): ██████████████████████████████████████████████████ 63 months
Mix Strategy:          █████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 22 months
Reduce Payment:        ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 26 months
Reduce Term:           █████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 22 months

┌────────────────────────────────────────────────────────┐
│                    RECOMMENDATION                      │
├────────────────────────────────────────────────────────┤
│ Best for MAXIMUM SAVINGS: Mix Strategy                 │
│ Saves: 28642 PLN vs original scenario                  │
│ Reduces loan by: 41 months                             │
└────────────────────────────────────────────────────────┘
```

## Benefits

This tool helps you:
- Understand the financial impact of mortgage overpayments
- Compare flexible vs. aggressive repayment strategies
- Calculate potential interest savings in both time and money
- View detailed month-by-month payment schedules
- Identify the optimal strategy for your financial situation

## Strategy Details

### Mix Strategy
- Recalculates monthly payment each month to maintain the same total payment amount
- Provides maximum flexibility as monthly payments decrease over time
- Good for improving creditworthiness while maintaining consistent cash flow

### Reduce Payment Strategy  
- Maintains constant overpayment amount throughout the loan
- Recalculates base payment based on current balance and remaining term
- Results in decreasing monthly payments over time
- Balances flexibility with consistent overpayment discipline

### Reduce Term Strategy
- Keeps monthly payment constant at the original amount
- Maximizes overpayment each month
- Provides maximum interest savings and shortest loan term
- Best for those who can maintain higher payments consistently