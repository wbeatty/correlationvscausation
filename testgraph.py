import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("AMZN_2012-05-19_2025-04-17.csv")
cd = df[["date", "adj_close"]]
cd["date"] = pd.to_datetime(cd["date"], utc=True)
cd.set_index("date", inplace=True)

start_date = "2012-05-21"
end_date = "2020-11-04"

sp = pd.read_csv("SPX.csv")
sp.rename(columns={"Date": "date", "Adj Close": "adj_close"}, inplace=True)
sp.drop(columns=["Open", "High", "Low", "Close", "Volume"], inplace=True)
sp["date"] = pd.to_datetime(sp["date"], utc=True)
sp.set_index("date", inplace=True)


sp["adj_close_normalized"] = (sp["adj_close"] - sp["adj_close"].min()) / (
    sp["adj_close"].max() - sp["adj_close"].min()
)
cd["adj_close_normalized"] = (cd["adj_close"] - cd["adj_close"].min()) / (
    cd["adj_close"].max() - cd["adj_close"].min()
)

cd_filtered = cd.loc["2012-05-21":"2020-11-04"]
sp_filtered = sp.loc["2012-05-21":"2020-11-04"]


cd_filtered["first_derivative"] = cd_filtered["adj_close_normalized"].diff()
cd_filtered["second_derivative"] = cd_filtered["first_derivative"].diff()

sp_filtered["first_derivative"] = sp_filtered["adj_close_normalized"].diff()
sp_filtered["second_derivative"] = sp_filtered["first_derivative"].diff()

merged_second_derivatives = pd.concat(
    [
        cd_filtered["second_derivative"].rename("AMZN_second_derivative"),
        sp_filtered["second_derivative"].rename("SPX_second_derivative"),
    ],
    axis=1,
)

merged_second_derivatives.dropna(inplace=True)


MSE = np.square(
    np.subtract(
        merged_second_derivatives["AMZN_second_derivative"],
        merged_second_derivatives["SPX_second_derivative"],
    )
).mean()

print("Mean Squared Error between AMZN and SPX second derivatives:", MSE)

plt.figure(figsize=(10, 6))
plt.plot(
    cd_filtered.index,
    cd_filtered["second_derivative"],
    label="Second Derivative of AMZN",
)

plt.plot(
    sp_filtered.index,
    sp_filtered["second_derivative"],
    label="Second Derivative of SPX",
)

plt.title("Second Derivative of AMZN and SPX")
plt.xlabel("Date")
plt.ylabel("Second Derivative")
plt.legend()
plt.show()

# cd.loc["2012-05-21":"2020-11-04"]
# sp.loc["2012-05-21":"2020-11-04"]
# 2012-05-21 : 2020-11-04
