from prophet import Prophet

def forecast_cashflow(df):
    df = df.rename(columns={"date": "ds", "cashflow": "y"})
    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    return {
        "3_month": float(forecast.iloc[-90]["yhat"]),
        "6_month": float(forecast.iloc[-180]["yhat"]),
        "12_month": float(forecast.iloc[-365]["yhat"])
    }
