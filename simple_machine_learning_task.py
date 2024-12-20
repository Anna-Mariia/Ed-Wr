import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split,GridSearchCV,cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_error
from sklearn.preprocessing import StandardScaler,LabelEncoder
import matplotlib.pyplot as plt

my_file = "apartments_pl_2023_08.csv"
df = pd.read_csv(my_file)

df = df[["squareMeters","rooms","centreDistance","condition","price"]]

df = df.dropna()

encoder = LabelEncoder()
df["condition"] = encoder.fit_transform(df["condition"])

scaler = StandardScaler()
df[["squareMeters","rooms","centreDistance"]] = scaler.fit_transform(df[["squareMeters","rooms","centreDistance"]])

X = df[["squareMeters","rooms","centreDistance","condition"]]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#LR
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

#DT з grid
dt_params = {"max_depth": [5, 10, 15, 20],"min_samples_split": [5, 10, 20],"min_samples_leaf": [1, 5, 10]}

dt_grid = GridSearchCV(DecisionTreeRegressor(random_state=42), dt_params, cv=5, scoring="r2")
dt_grid.fit(X_train, y_train)
dt_best_model = dt_grid.best_estimator_
y_pred_dt = dt_best_model.predict(X_test)

#RF з grid
rf_params = {"n_estimators": [100, 200, 300],"max_depth": [10, 20, 30],"min_samples_split": [5, 10],"min_samples_leaf": [1, 5]}

rf_grid = GridSearchCV(RandomForestRegressor(random_state=42), rf_params, cv=5, scoring="r2")
rf_grid.fit(X_train, y_train)
rf_best_model = rf_grid.best_estimator_
y_pred_rf = rf_best_model.predict(X_test)

"""функція для оцінки моделей"""

def evaluate_model(model_name,y_true,y_pred):
    mse = mean_squared_error(y_true,y_pred)
    r2 = r2_score(y_true,y_pred)
    mae = mean_absolute_error(y_true,y_pred)
    print(f"{model_name} - mse: {mse:.2f}, R квадрат: {r2:.2f}, mae: {mae:.2f}")

print("\nОцінка моделей:")
evaluate_model("Linear Regression",y_test,y_pred_lr)
evaluate_model("Decision Tree",y_test,y_pred_dt)
evaluate_model("Random Forest",y_test,y_pred_rf)

"""зообразимо все"""

plt.figure(figsize=(12, 6))
plt.scatter(y_test, y_pred_lr,color="blue",alpha=0.5,label="Linear Regression")
plt.scatter(y_test, y_pred_dt,color="green",alpha=0.5,label="Decision Tree")
plt.scatter(y_test, y_pred_rf,color="red",alpha=0.5,label="Random Forest")
plt.plot([y_test.min(),y_test.max()],[y_test.min(),y_test.max()],color="black", linestyle="--")
plt.xlabel("Справжні значення цін")
plt.ylabel("Прогнозовані значення цін")
plt.title("Порівняння моделей: Linear Regression,Decision Tree,Random Forest")
plt.legend()
plt.show()

"""показую роботу grid з його визначенням найкращих параметрів серед тих,що я задала"""

print("\nНайкращі параметри для Decision Tree:")
print(dt_grid.best_params_)

print("\nНайкращі параметри для Random Forest:")
print(rf_grid.best_params_)
