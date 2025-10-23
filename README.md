#  Air Quality Prediction System  

##  Project Overview  
This project develops a comprehensive air quality prediction system using machine learning and time series forecasting models. The system analyzes historical air pollutant data to predict future pollution levels, helping in environmental monitoring and smart city applications.  

---

##  Dataset Information  

###  Original Dataset (`AirQuality.csv`)  
**Source:** UCI Machine Learning Repository via Kaggle  
**Format:** Semicolon-delimited CSV with European decimal notation (comma)  
**Raw Shape:** 9,471 rows × 1 column (improperly parsed)  

**Issues:**  
- All data merged into a single column due to delimiter mismatch  
- 2,556 missing values marked as -200  
- 4,529 duplicate records  
- Inconsistent time formatting  

###  Cleaned Dataset (`AirQuality_cleaned.csv`)  
**Shape:** 827 rows × 14 columns  
**Quality:** Zero missing values, zero duplicates  
**Features:** 14 properly structured columns including datetime index and pollutant measurements  

---

##  Data Transformation Pipeline  

###  Milestone 1: Data Cleaning and Exploratory Data Analysis  

####  What Changed in the Dataset:

1. **Proper Data Parsing**  
   - Applied correct delimiter (;) and decimal separator (,) to parse the raw file  
   - Converted single malformed column into 14 properly structured feature columns  
   - **Impact:** Transformed unusable data into a structured, analysis-ready format  

2. **Handling Missing Values**  
   - Identified placeholder values (-200) indicating sensor errors or missing readings  
   - Replaced invalid values with NaN  
   - Filled missing numeric values with column means  
   - Filled missing categorical values with mode  
   - **Impact:** Ensured data completeness and statistical validity  

3. **Duplicate Removal**  
   - Detected and removed 4,529 duplicate rows (47.8% of original data)  
   - **Impact:** Eliminated redundancy and improved data quality  

4. **DateTime Processing**  
   - Fixed time format (converted 18.00.00 to 18:00:00)  
   - Merged separate Date and Time columns into a unified Datetime column  
   - Set Datetime as the dataframe index for time series operations  
   - **Impact:** Enabled proper temporal analysis and forecasting  

5. **Column Cleanup**  
   - Removed the last two empty/unnamed columns  
   - Dropped original Date and Time columns after combining  
   - **Impact:** Streamlined dataset structure  

6. **Feature Engineering**  
   - Extracted Year and Month from datetime for temporal analysis  
   - Maintained all 13 pollutant and environmental sensor readings  
   - **Impact:** Enhanced temporal pattern recognition  

7. **Data Type Conversion**  
   - Converted all numeric columns from string to proper numeric types  
   - Handled European decimal format (comma to period conversion)  
   - **Impact:** Ensured mathematical operations work correctly  

####  EDA Visualizations Created:
- **Univariate Analysis:** Distribution plots and boxplots for sensor readings  
- **Bivariate Analysis:** Scatter plots and correlation heatmap  
- **Temporal Analysis:** Records distribution by year  
- **Outlier Detection:** Boxplots for anomaly identification  

**Result:**  
- Original: 9,471 rows × 1 column (malformed)  
- After Milestone 1: 827 rows × 14 columns (clean, structured, complete)  
- **Data Reduction:** 91.3% of rows removed (duplicates + invalid entries)  
- **Quality Improvement:** 100% complete data with no missing values  

---

###  Milestone 2: Time Series Forecasting and Model Training  

####  What Changed in the Dataset:
1. **Advanced Data Preprocessing**  
   - Re-applied all Milestone 1 cleaning steps with refined approach  
   - Stricter handling: Dropped all rows with any NaN values instead of imputing  
   - **Impact:** Ensured only complete, reliable records used for forecasting  

2. **Time Series Resampling**  
   - Resampled data to hourly intervals using `.resample('H').mean()`  
   - Applied forward-fill for any gaps after resampling  
   - **Impact:** Created consistent temporal intervals required for ARIMA and Prophet  

3. **Feature Engineering for ML Models**  
   - Created lag features (previous 3 time steps) to capture temporal dependencies  
   - Generated training sequences for LSTM (sliding windows of 3 timesteps)  
   - **Impact:** Provided historical context to models for better predictions  

4. **Data Normalization**  
   - Applied MinMaxScaler to scale values between 0 and 1 for LSTM  
   - Preserved original scale for other models  
   - **Impact:** Improved LSTM convergence and training stability  

5. **Train-Test Split**  
   - Split data into 80% training and 20% testing sets  
   - Maintained temporal order (no random shuffling) to preserve time series properties  
   - **Impact:** Enabled proper model validation on unseen future data  

6. **Target Variable Selection**  
   - Focused on CO(GT) (Carbon Monoxide) as the primary prediction target  
   - Maintained all other features as potential predictors  
   - **Impact:** Simplified forecasting task while retaining model flexibility  

####  Models Trained:
- **ARIMA (3,1,2):** Classical statistical time series model  
- **Prophet:** Facebook's robust forecasting tool with seasonality handling  
- **LSTM:** Deep learning sequential model (50 units, 50 epochs)  
- **XGBoost:** Gradient boosting with lag features (100 estimators)  

####  Evaluation Metrics:
- **Mean Absolute Error (MAE)**  
- **Root Mean Squared Error (RMSE)**  

 Best model selected based on **lowest RMSE**  

**Result:**  
- **Input:** 827 clean records from Milestone 1  
- **Output:** Trained forecasting models with 24-hour ahead predictions  
- **Visualization:** Comparative plots showing ARIMA, Prophet, LSTM, and XGBoost forecasts vs actual values  

---

##  Key Dataset Features  

| Feature | Description | Unit |
|----------|-------------|------|
| Datetime | Combined date and time index | ISO Format |
| CO(GT) | True Carbon Monoxide concentration | mg/m³ |
| PT08.S1(CO) | Metal oxide sensor response to CO | Arbitrary |
| NMHC(GT) | Non-Methane Hydrocarbons concentration | μg/m³ |
| C6H6(GT) | Benzene concentration | μg/m³ |
| PT08.S2(NMHC) | Metal oxide sensor response to NMHC | Arbitrary |
| NOx(GT) | Nitrogen Oxides concentration | ppb |
| PT08.S3(NOx) | Metal oxide sensor response to NOx | Arbitrary |
| NO2(GT) | Nitrogen Dioxide concentration | μg/m³ |
| PT08.S4(NO2) | Metal oxide sensor response to NO2 | Arbitrary |
| PT08.S5(O3) | Metal oxide sensor response to Ozone | Arbitrary |
| T | Temperature | °C |
| RH | Relative Humidity | % |
| AH | Absolute Humidity | g/m³ |

---

##  Technical Stack  

**Libraries Used:**  
 Data Processing: `pandas`, `numpy`  
 Visualization: `matplotlib`, `seaborn`  
 Machine Learning: `scikit-learn`, `xgboost`  
 Deep Learning: `tensorflow`, `keras`  
 Time Series: `statsmodels` (ARIMA), `prophet`  
 Data Acquisition: `kaggle`  

**Requirements:**  
pandas
numpy
matplotlib
seaborn
scikit-learn
xgboost
tensorflow
statsmodels
prophet
kaggle

---

##  Project Structure  
├── AirQuality.csv # Original raw dataset
├── AirQuality_cleaned.csv # Cleaned dataset after Milestone 1
├── milestone_1.py # Data cleaning, EDA, and preprocessing
├── milestone_2.py # Time series modeling and forecasting
└── README.md # Project documentation

---

##  Usage Instructions  

### Step 1: ⚙️ Setup Kaggle API  
```python
# Install Kaggle
!pip install kaggle -q

# Upload kaggle.json
from google.colab import files
files.upload()

# Configure Kaggle
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

# Download dataset
!kaggle datasets download -d fedesoriano/air-quality-data-set --unzip
Step 2:  Run Milestone 1 (Data Cleaning)
python milestone_1.py


Output: AirQuality_cleaned.csv with complete, structured data

Step 3:  Run Milestone 2 (Model Training)
python milestone_2.py


Output: Trained models and forecast visualizations
 Model Performance Summary

All models evaluated using:

MAE (Mean Absolute Error): Average prediction error magnitude

RMSE (Root Mean Squared Error): Penalizes large errors more heavily

 The best-performing model is automatically saved for deployment.

 Key Insights

Data Quality Transformation: 91.3% data reduction through removal of duplicates and invalid entries

100% completeness achieved (zero missing values)

Proper temporal structure enabled forecasting capabilities

 Why These Changes Matter:

Parsing errors corrected → Models can access individual features

Missing values handled → Statistical calculations are valid

Duplicates removed → Models learn true patterns, not repetitions

Datetime structured → Time series analysis becomes possible

Lag features added → Models capture temporal dependencies

Normalization applied → Deep learning converges faster

 Future Enhancements

 Multi-pollutant simultaneous prediction
 Integration of external weather data
 Real-time prediction API
 Spatial analysis across multiple monitoring stations
 Deep learning architecture optimization

Platform: Google Colab

Tools: Python ecosystem for data science and machine learning


