# 🏨 Vietnam Coastal Hotel Market Analysis and Forecasting System
## 📝 Introduction
This project focuses on researching the accommodation market in popular coastal tourist cities and island districts in Vietnam. The main objectives include building a clean, structured dataset from real-world data sources and applying machine learning models to solve two key problems: predicting room rates and analyzing factors influencing customer satisfaction.

**Executing member**
- Huỳnh Phát Đạt - ISE-UIT
- Bùi Quốc Bảo - ISE-UIT
- Lê Minh Khôi - ISE-UIT

## 📖 Data
- Data Source: Collected directly from the Booking.com booking platform using Selenium.
- Collection Method: Dynamic web scraping techniques using the Selenium library in Python were employed to extract data from dynamically loaded structured websites.
- Scale: Nearly 300,000 raw records (Bronze tier) were collected and refined to approximately 4,000 clean records for model training.
- Key Features: Hotel name, location, type of accommodation, star rating, room rate, rating, amenities (pool, airport shuttle), distance to center/beach, room details, etc.

## 🛠️ Method
The system applies a Medallion tiered data architecture for managing and processing in-depth data:

### 1. Data Processing (Bronze ➔ Silver ➔ Gold)
- Normalization: Converts date formats, converts distance units (km), processes currency, and extracts features from text strings.
- Cleaning: Removes noise, handles missing values ​​(NaN), and removes duplicate records.
- Feature Techniques: Uses Ordinal Encoding for ordinal ratings and One-hot Encoding for categorical variables.

### 2. Statistical Analysis and EDA
- Two-sample t-test: Evaluates the impact of binary utilities (pool, sea view, etc.) on price and rating.
- ANOVA & Post-hoc (Tukey's HSD): Identify differences between complex taxonomic groups such as accommodation type or location to perform optimal clustering.
- Multicollinearity control: Use variance inflation factors (VIF > 10) to remove independent variables that are too strongly correlated.

## 📊 Experiment and Results
### 1. In-depth analysis of customer satisfaction with the hotel

| Variable         | coef    | t       | P >\|t\||
|------------------|---------|---------|-------|
| Dist_DownTown    | 0.0238  | 2.546   | 0.011 |
| Dist_Beach       | -0.0001 | -0.015  | 0.988 |
| Price            | -0.0073 | -0.987  | 0.324 |
| Stars            | -0.0558 | -7.025  | 0.000 |
| Rates_Quantity   | 0.0157  | 2.122   | 0.034 |
| eaves            | 0.0519  | 3.693   | 0.000 |
| pool             | -0.0034 | -0.217  | 0.828 |
| bar              | -0.0217 | -0.956  | 0.339 |
| Fitness_center   | 0.0031  | 0.142   | 0.887 |
| tourist_spot     | 0.0684  | 3.993   | 0.000 |
| eat_drink_spot   | 0.0075  | 1.009   | 0.313 |
| beachs           | -0.0144 | -1.610  | 0.108 |
| clean            | 0.7164  | 61.988  | 0.000 |
| destination      | 0.2011  | 16.566  | 0.000 |
| da nang          | -0.0360 | -0.706  | 0.479 |
| dao cat ba       | 0.1535  | 2.542   | 0.011 |
| dong hoi         | 0.0580  | 0.713   | 0.476 |
| ha long          | 0.0517  | 1.029   | 0.304 |
| hoi an           | 0.1184  | 2.411   | 0.016 |
| mui ne           | 0.1065  | 1.654   | 0.098 |
| nha trang        | -0.0697 | -1.374  | 0.170 |
| phu quoc         | 0.1254  | 2.202   | 0.028 |
| quy nhon         | 0.0663  | 1.167   | 0.243 |
| vung tau         | -0.0004 | -0.008  | 0.994 |
| Accom_Group_B    | -0.0818 | -3.649  | 0.000 |
| Accom_Group_C    | 0.0331  | 1.361   | 0.174 |
| Accom_Group_D    | -0.0612 | -1.779  | 0.075 |


The t-test results on the regression coefficients revealed the following specific effects:
- The strongest positive effect: Cleanliness had the largest positive coefficient (coef = 0.7164), confirming that hygiene is a top priority for customers.
- Other positive factors: Hotel location, distance to the city center, number of tourist spots, and number of ratings were all directly proportional to satisfaction.
- An unexpected negative effect: The variable Stars (number of stars) had a negative coefficient (coef = -0.0558, p < 0.001). This suggests that customers often have very high expectations for multi-star hotels, leading to disappointment if the actual experience does not match.
- Factors with minimal influence: In this model, price, distance to beach, and certain amenities such as a bar or gym do not show a significant impact.

### 2. Room Price Prediction
- Our team implemented regression models to predict prices from input characteristics: Models: Linear, Ridge, Lasso Regression, and Random Forest Regressor.
- Results: Random Forest Regressor achieved superior performance with: MAE: ~95K VND, Adjusted R2: 0.96 (explaining 96% of price variation).

| **Model** | **Train** | **Test** | **Test<br>(fine-tuned model)** |
|:---------:|:---------:|:--------:|:----------------------:|
| Linear Regression | 0.54877 | 0.55327 | 0.55327 |
| Lasso Regression  | 0.549116 | 0.55467 | 0.55466 |
| Ridge Regression  | 0.549128 | 0.554678 | 0.5546779 |
| Random Forest Regressor | **0.95419** | **0.95869** | **0.95846** |


## 🚀 Conclusion & Future Development
### 1. Conclusion
- The project has successfully built a rich dataset that accurately reflects the reality of Vietnam's coastal accommodation market.
- The meticulous investment in preprocessing and the application of the Medallion architecture have helped the models achieve high accuracy and practical applicability.

### 2. Future Development
- Expanding data sources: Collect more data from other platforms such as Agoda and Traveloka to avoid bias from a single source.
- Diversifying context: Add seasonal data (peak/off-peak) and expand the geographical scope to other tourist areas.
- Technical improvements: Upgrade the data scraping system to optimize speed and reduce reliance on the web interface structure.
