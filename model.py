import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv("processed_backup.csv")
X = df.drop(columns=["placement"])
y = df["placement"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=20
)
regr = RandomForestRegressor(
    n_estimators=200,
    max_depth=None,       
    random_state=20,
    n_jobs=-1              
)
regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)
y_pred_rounded = np.round(y_pred)
print("MSE:", mean_squared_error(y_test, y_pred))
print("R²:", r2_score(y_test, y_pred))

importances = regr.feature_importances_
indices = np.argsort(importances)[::-1]

print("\nTop 10 features by importance:")
for i in range(min(10, len(indices))):
    print(f"{X.columns[indices[i]]}: {importances[indices[i]]:.4f}")

# ---- Visualizations ----

# Scatter plot: Actual vs Predicted
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.6, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Placement')
plt.ylabel('Predicted Placement (Rounded)')
plt.title('Actual vs Predicted Placement')
plt.grid(True)
plt.show()


plt.hist(y_pred_rounded, bins=int(y_pred_rounded.max() - y_pred_rounded.min() + 1),
         alpha=0.7, label='Predicted')
plt.hist(y_test, bins=int(y_test.max() - y_test.min() + 1),
         alpha=0.5, label='Actual')
plt.xlabel("Placement (rounded)")
plt.ylabel("Count")
plt.title("Distribution of Actual vs Predicted")
plt.legend()
plt.show()


def prepare_features(new_df, reference_columns):
    for col in reference_columns:
        if col not in new_df:
            new_df[col] = 0
    return new_df[reference_columns]


new_df = pd.read_csv("processed.csv")
X_new = prepare_features(new_df, X.columns)
y_new_pred = regr.predict(X_new)
y_new_pred_rounded = np.round(y_new_pred)
y_new_actual = new_df["placement"]
print(y_new_pred)
print(y_new_actual.tolist())
