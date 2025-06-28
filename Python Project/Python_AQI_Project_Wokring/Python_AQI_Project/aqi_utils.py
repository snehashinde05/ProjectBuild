# === CPCB AQI Breakpoint Formula ===
def calculate_cpcb_aqi(pollutant, concentration):
    breakpoints = {
        "pm25": [(0, 30, 0, 50), (31, 60, 51, 100), (61, 90, 101, 200), (91, 120, 201, 300),
                 (121, 250, 301, 400), (251, 500, 401, 500)],
        "pm10": [(0, 50, 0, 50), (51, 100, 51, 100), (101, 250, 101, 200), (251, 350, 201, 300),
                 (351, 430, 301, 400), (431, 500, 401, 500)],
        "no2": [(0, 40, 0, 50), (41, 80, 51, 100), (81, 180, 101, 200), (181, 280, 201, 300),
                (281, 400, 301, 400), (401, 500, 401, 500)],
        "o3": [(0, 50, 0, 50), (51, 100, 51, 100), (101, 168, 101, 200), (169, 208, 201, 300),
               (209, 748, 301, 400), (749, 1000, 401, 500)],
    }

    for bp in breakpoints.get(pollutant, []):
        Clow, Chigh, Ilow, Ihigh = bp
        if Clow <= concentration <= Chigh:
            return round(((Ihigh - Ilow) / (Chigh - Clow)) * (concentration - Clow) + Ilow)
    return None