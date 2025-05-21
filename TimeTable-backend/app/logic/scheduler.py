def generate_schedule_matrix(years, days, hours):
    return {
        year.id: {day: {hour: None for hour in hours} for day in days}
        for year in years
    }