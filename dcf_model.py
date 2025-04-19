def dcf_valuation(fcf, growth_rate, discount_rate, years, terminal_growth):
    fcf = float(fcf)
    total_value = 0

    for year in range(1, years + 1):
        projected_fcf = fcf * ((1 + growth_rate) ** year)
        discounted_fcf = projected_fcf / ((1 + discount_rate) ** year)
        total_value += discounted_fcf

    terminal_fcf = fcf * ((1 + growth_rate) ** years)
    terminal_value = terminal_fcf * (1 + terminal_growth) / (discount_rate - terminal_growth)
    terminal_value_discounted = terminal_value / ((1 + discount_rate) ** years)

    total_value += terminal_value_discounted
    return total_value
