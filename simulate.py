import argparse
from datetime import datetime, timedelta
import calendar

def add_months(date, months):
    """Add months to a date, handling month boundaries properly"""
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return date.replace(year=year, month=month, day=day)

def simulate_strategy(balance, annual_interest_rate, monthly_payment, custom_payment, total_months, mode, payment_day=1):
    monthly_interest = annual_interest_rate / 12
    remaining_balance = balance
    month_count = 0
    total_interest = 0.0
    schedule = []
    
    # Start from next month's payment day
    today = datetime.today()
    if today.day <= payment_day:
        # If we haven't passed this month's payment day, start from this month
        current_date = today.replace(day=payment_day)
    else:
        # If we've passed this month's payment day, start from next month
        current_date = add_months(today.replace(day=payment_day), 1)
    
    # Calculate constant overpayment for reduce_payment strategy
    constant_overpayment = custom_payment - monthly_payment if mode == "reduce_payment" else 0

    while remaining_balance > 0:
        interest = remaining_balance * monthly_interest

        if mode == "mix":
            # Mix strategy: recalculate payment each month to maintain same total payment amount
            remaining_term = max(total_months - month_count, 1)
            payment = (monthly_interest * remaining_balance * ((1 + monthly_interest) ** remaining_term)) / (((1 + monthly_interest) ** remaining_term) - 1)
            overpayment = max(custom_payment - payment, 0)
        elif mode == "reduce_payment":
            # Pure reduce payment strategy: constant overpayment, but recalculate base payment based on current balance
            remaining_term = max(total_months - month_count, 1)
            # Calculate what the payment should be for current balance and remaining term
            base_payment = (monthly_interest * remaining_balance * ((1 + monthly_interest) ** remaining_term)) / (((1 + monthly_interest) ** remaining_term) - 1)
            payment = base_payment
            overpayment = constant_overpayment
        else:  # reduce_term
            # Reduce term strategy: constant payment, maximize overpayment
            payment = monthly_payment
            overpayment = max(custom_payment - payment, 0)

        principal = payment - interest
        total_payment = payment + overpayment
        
        # Ensure we don't pay more than remaining balance + interest
        if remaining_balance + interest < total_payment:
            total_payment = remaining_balance + interest
            overpayment = total_payment - payment
            if overpayment < 0:
                payment = total_payment
                overpayment = 0
                principal = payment - interest
        
        remaining_balance -= (principal + overpayment)
        total_interest += interest

        schedule.append({
            "Month": current_date.strftime("%Y-%m"),
            "Payment": round(payment, 2),
            "Overpayment": round(overpayment, 2),
            "Interest": round(interest, 2),
            "Principal": round(principal, 2),
            "Remaining Balance": round(max(remaining_balance, 0), 2)
        })

        current_date = add_months(current_date, 1)
        month_count += 1

    return schedule, total_interest, month_count

def print_schedule(schedule, label):
    print(f"\n--- {label} ---")
    print(f"{'Month':<10} {'Payment':>10} {'Overpayment':>12} {'Interest':>10} {'Principal':>10} {'Remaining':>14}")
    for row in schedule:
        print(f"{row['Month']:<10} {row['Payment']:>10.2f} {row['Overpayment']:>12.2f} {row['Interest']:>10.2f} {row['Principal']:>10.2f} {row['Remaining Balance']:>14.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mortgage repayment simulation.")
    parser.add_argument("--balance", type=float, required=True, help="Remaining loan balance")
    parser.add_argument("--interest", type=float, required=True, help="Annual interest rate (e.g. 7.84 for 7.84%)")
    parser.add_argument("--payment", type=float, required=True, help="Current monthly payment")
    parser.add_argument("--max", type=float, required=True, help="Maximum monthly amount you can pay")
    parser.add_argument("--months", type=int, required=True, help="Remaining number of months until the original end date")
    parser.add_argument("--day", type=int, default=1, help="Payment day of month (1-28, default: 1)")
    parser.add_argument("--currency", type=str, default="PLN", help="Currency symbol (default: PLN)")

    args = parser.parse_args()

    # Validate payment day
    if args.day < 1 or args.day > 28:
        print("Error: Payment day must be between 1 and 28")
        exit(1)

    # Strategy 1: Mix strategy (formerly reduce_payment)
    schedule1, interest1, months1 = simulate_strategy(
        balance=args.balance,
        annual_interest_rate=args.interest / 100,
        monthly_payment=args.payment,
        custom_payment=args.max,
        total_months=args.months,
        mode="mix",
        payment_day=args.day
    )

    # Strategy 2: Pure reduce payment strategy
    schedule2, interest2, months2 = simulate_strategy(
        balance=args.balance,
        annual_interest_rate=args.interest / 100,
        monthly_payment=args.payment,
        custom_payment=args.max,
        total_months=args.months,
        mode="reduce_payment",
        payment_day=args.day
    )

    # Strategy 3: Reduce term strategy
    schedule3, interest3, months3 = simulate_strategy(
        balance=args.balance,
        annual_interest_rate=args.interest / 100,
        monthly_payment=args.payment,
        custom_payment=args.max,
        total_months=args.months,
        mode="reduce_term",
        payment_day=args.day
    )

    print_schedule(schedule1, "Strategy 1: Mix Strategy")
    print(f"\nTotal interest paid: {interest1:.2f} {args.currency}, total months: {months1}")

    print_schedule(schedule2, "Strategy 2: Reduce Payment")
    print(f"\nTotal interest paid: {interest2:.2f} {args.currency}, total months: {months2}")

    print_schedule(schedule3, "Strategy 3: Reduce Term")
    print(f"\nTotal interest paid: {interest3:.2f} {args.currency}, total months: {months3}")

    print(f"\n--- Comparison ---")
    print(f"Mix Strategy:        {interest1:.2f} {args.currency} interest, {months1} months")
    print(f"Reduce Payment:      {interest2:.2f} {args.currency} interest, {months2} months")
    print(f"Reduce Term:         {interest3:.2f} {args.currency} interest, {months3} months")
    
    best_interest = min(interest1, interest2, interest3)
    if interest1 == best_interest:
        best_strategy = "Mix Strategy"
    elif interest2 == best_interest:
        best_strategy = "Reduce Payment"
    else:
        best_strategy = "Reduce Term"
    
    print(f"\nBest strategy for interest savings: {best_strategy}")

    # Cost Reduction Summary
    print(f"\n{'='*60}")
    print(f"{'COST REDUCTION SUMMARY':^60}")
    print(f"{'='*60}")
    
    # Calculate savings compared to no overpayment scenario
    # Simulate what would happen with just the original payment
    original_schedule, original_interest, original_months = simulate_strategy(
        balance=args.balance,
        annual_interest_rate=args.interest / 100,
        monthly_payment=args.payment,
        custom_payment=args.payment,  # No overpayment
        total_months=args.months,
        mode="reduce_term",
        payment_day=args.day
    )
    
    savings1 = original_interest - interest1
    savings2 = original_interest - interest2
    savings3 = original_interest - interest3
    
    time_saved1 = original_months - months1
    time_saved2 = original_months - months2
    time_saved3 = original_months - months3
    
    print(f"\nOriginal scenario (no overpayment):")
    print(f"  Interest: {original_interest:.2f} {args.currency}, Duration: {original_months} months")
    print(f"\nSavings compared to original:")
    print(f"  Mix Strategy:     {savings1:>8.2f} {args.currency} saved, {time_saved1:>2} months shorter")
    print(f"  Reduce Payment:   {savings2:>8.2f} {args.currency} saved, {time_saved2:>2} months shorter")
    print(f"  Reduce Term:      {savings3:>8.2f} {args.currency} saved, {time_saved3:>2} months shorter")
    
    # ASCII Visualization
    print(f"\n{'='*60}")
    print(f"{'INTEREST COST COMPARISON':^60}")
    print(f"{'='*60}")
    
    # Normalize values for visualization (scale to 50 characters max)
    max_interest = max(original_interest, interest1, interest2, interest3)
    scale = 50 / max_interest
    
    def create_bar(value, max_width=50):
        width = int(value * scale)
        return '█' * width + '░' * (max_width - width)
    
    print(f"\nInterest Cost Comparison (each █ ≈ {max_interest/50:.0f} {args.currency}):")
    print(f"Original (no overpay): {create_bar(original_interest)} {original_interest:.0f} {args.currency}")
    print(f"Mix Strategy:          {create_bar(interest1)} {interest1:.0f} {args.currency}")
    print(f"Reduce Payment:        {create_bar(interest2)} {interest2:.0f} {args.currency}")
    print(f"Reduce Term:           {create_bar(interest3)} {interest3:.0f} {args.currency}")
    
    # Time comparison
    print(f"\nLoan Duration Comparison (each █ ≈ {original_months/50:.1f} months):")
    time_scale = 50 / original_months
    
    def create_time_bar(value, max_width=50):
        width = int(value * time_scale)
        return '█' * width + '░' * (max_width - width)
    
    print(f"Original (no overpay): {create_time_bar(original_months)} {original_months} months")
    print(f"Mix Strategy:          {create_time_bar(months1)} {months1} months")
    print(f"Reduce Payment:        {create_time_bar(months2)} {months2} months")
    print(f"Reduce Term:           {create_time_bar(months3)} {months3} months")
    
    # Summary box
    max_savings = max(savings1, savings2, savings3)
    max_time_saved = max(time_saved1, time_saved2, time_saved3)
    
    box_width = 56
    
    print(f"\n┌{'─'*box_width}┐")
    print(f"│{'RECOMMENDATION':^{box_width}}│")
    print(f"├{'─'*box_width}┤")
    
    # Line 1: Best strategy
    line1_text = f" Best for MAXIMUM SAVINGS: {best_strategy}"
    line1_spaces = box_width - len(line1_text) - 1
    print(f"│{line1_text}{' ' * line1_spaces} │")
    
    # Line 2: Savings amount
    line2_text = f" Saves: {max_savings:.0f} {args.currency} vs original scenario"
    line2_spaces = box_width - len(line2_text) - 1
    print(f"│{line2_text}{' ' * line2_spaces} │")
    
    # Line 3: Time reduction
    line3_text = f" Reduces loan by: {max_time_saved} months"
    line3_spaces = box_width - len(line3_text) - 1
    print(f"│{line3_text}{' ' * line3_spaces} │")
    
    print(f"└{'─'*box_width}┘")

