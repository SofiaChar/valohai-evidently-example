import os
import pandas as pd
import numpy as np
import requests
import zipfile
import io
from datetime import datetime, time
from sklearn import ensemble
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, RegressionPreset


def download_and_process_data(url):
    content = requests.get(url, verify=False).content
    with zipfile.ZipFile(io.BytesIO(content)) as arc:
        raw_data = pd.read_csv(arc.open("hour.csv"), header=0, sep=',', parse_dates=['dteday'], index_col='dteday')
    raw_data.index = raw_data.apply(lambda row: datetime.combine(row.name, time(hour=int(row['hr']))), axis=1)
    return raw_data


def train_model(reference_data, numerical_features, categorical_features, target):
    regressor = ensemble.RandomForestRegressor(random_state=0, n_estimators=50)
    regressor.fit(reference_data[numerical_features + categorical_features], reference_data[target])
    return regressor


def generate_and_save_report(report_obj, current_data, reference_data, column_mapping, metrics, file_name):
    report = report_obj(metrics=metrics, options={"render": {"raw_data": True}})
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
    save_path = os.getenv('VH_OUTPUTS_DIR') + '/' + file_name
    report.save(save_path)


def main():
    # Define URL for dataset download
    url = "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip"

    # Download and process the bicycle demand dataset
    raw_data = download_and_process_data(url)

    # Define numerical and categorical features for the regression model
    target = 'cnt'
    prediction = 'prediction'
    numerical_features = ['temp', 'atemp', 'hum', 'windspeed', 'hr', 'weekday']
    categorical_features = ['season', 'holiday', 'workingday']

    # Split data into reference and current periods
    reference = raw_data.loc['2011-01-01 00:00:00':'2011-01-28 23:00:00']
    current = raw_data.loc['2011-01-29 00:00:00':'2011-02-28 23:00:00']

    # Train RandomForestRegressor
    regressor = train_model(reference, numerical_features, categorical_features, target)

    # Predictions for reference and current periods
    ref_prediction = regressor.predict(reference[numerical_features + categorical_features])
    current_prediction = regressor.predict(current[numerical_features + categorical_features])
    reference['prediction'] = ref_prediction
    current['prediction'] = current_prediction

    # Convert indices to strings to avoid JSON serialization issues
    reference.index = reference.index.astype(str)
    current.index = current.index.astype(str)

    # Define column mapping for reports
    column_mapping = ColumnMapping()
    column_mapping.target = target
    column_mapping.prediction = prediction
    column_mapping.numerical_features = numerical_features
    column_mapping.categorical_features = categorical_features

    # Generate and save reports

    # Regression Performance at Training
    generate_and_save_report(Report, reference, None, column_mapping, [RegressionPreset()],
                             file_name='regression_performance_at_training.html')

    # Week 1 Reports
    week1_current = current.loc['2011-01-29 00:00:00':'2011-02-07 23:00:00']
    generate_and_save_report(Report, week1_current, reference, column_mapping, [RegressionPreset()],
                             file_name='regression_performance_after_week1.html')
    generate_and_save_report(Report, week1_current, reference, column_mapping, [TargetDriftPreset()],
                             file_name='target_drift_after_week1.html')

    # Week 2 Reports
    week2_current = current.loc['2011-02-07 00:00:00':'2011-02-14 23:00:00']
    generate_and_save_report(Report, week2_current, reference, column_mapping, [RegressionPreset()],
                             file_name='regression_performance_after_week2.html')
    generate_and_save_report(Report, week2_current, reference, column_mapping, [TargetDriftPreset()],
                             file_name='target_drift_after_week2.html')

    # Week 3 Reports
    week3_current = current.loc['2011-02-15 00:00:00':'2011-02-21 23:00:00']
    generate_and_save_report(Report, week3_current, reference, column_mapping, [RegressionPreset()],
                             file_name='regression_performance_after_week3.html')
    generate_and_save_report(Report, week3_current, reference, column_mapping, [TargetDriftPreset()],
                             file_name='target_drift_after_week3.html')

    # Data Drift Dashboard after Week 1
    generate_and_save_report(Report, week1_current, reference, column_mapping, [DataDriftPreset()],
                             file_name='data_drift_dashboard_after_week1.html')


if __name__ == "__main__":
    main()
