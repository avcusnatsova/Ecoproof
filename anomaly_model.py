import pandas as pd

def detect_anomalies(df):
    numeric_cols = ['pm2_5', 'pm10', 'so2_level', 'no2_level', 'aqi']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['anomaly_flag'] = False
    df['anomaly_severity'] = 'Normal'

    moderate_mask = (
        (df['pm2_5'].between(186, 269)) |
        (df['pm10'].between(239, 350)) |
        (df['so2_level'].between(87, 125)) |
        (df['no2_level'].between(121, 177)) |
        (df['aqi'].between(178, 223))
    )
    df.loc[moderate_mask, ['anomaly_flag', 'anomaly_severity']] = [True, 'Moderate']

    high_mask = (
        (df['pm2_5'].between(269, 341)) |
        (df['pm10'].between(350, 430)) |
        (df['so2_level'].between(125, 152)) |
        (df['no2_level'].between(177, 217)) |
        (df['aqi'].between(223, 263))
    )
    df.loc[high_mask, ['anomaly_flag', 'anomaly_severity']] = [True, 'High']

    violation_mask = (
        (df['pm2_5'].between(341, 372)) |
        (df['pm10'].between(430, 464)) |
        (df['so2_level'].between(152, 167)) |
        (df['no2_level'].between(217, 234)) |
        (df['aqi'].between(263, 291))
    )
    df.loc[violation_mask, ['anomaly_flag', 'anomaly_severity']] = [True, 'Violation']

    severe_mask = (
        (df['pm2_5'] > 372) |
        (df['pm10'] > 464) |
        (df['so2_level'] > 167) |
        (df['no2_level'] > 234) |
        (df['aqi'] > 291)
    )
    df.loc[severe_mask, ['anomaly_flag', 'anomaly_severity']] = [True, 'Severe']

    return df