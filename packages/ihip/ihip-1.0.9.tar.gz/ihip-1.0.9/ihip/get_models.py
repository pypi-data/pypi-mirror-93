import boto3
import pandas as pd
import io
from pandas.core.common import flatten
import scipy.stats
import h2o
from h2o.estimators.gbm import H2OGradientBoostingEstimator
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

s3_id = 'AKIAQEANRIBFMUN5KIVJ'
s3_key = 'ttziaBkx9N/n6F+JFKZfpf+dSstbiCyzgnNoa/ow'
s3 = boto3.client('s3', aws_access_key_id=s3_id, aws_secret_access_key=s3_key)


def get_available_data_sources(user_name):
    """
    This method accepts user name and returns the list of data sets available for the user
    :param user_name: user name
    :return: returns list of available data sets selected by the user
    """
    external_file_list = []
    internal_file_list = []
    output_json = {}
    external_data_path = "Data_Market/" + user_name + "/DatasetSelection/"
    internal_data_path = "AI_ML/" + user_name + "/Dataset_selection/"
    for external_obj in s3.list_objects_v2(Bucket="datainsightsplatform", Prefix=external_data_path)['Contents']:
        external_file_list.append(external_obj['Key'])
    for internal_obj in s3.list_objects_v2(Bucket="datainsightsplatform", Prefix=internal_data_path)['Contents']:
        internal_file_list.append(internal_obj['Key'])
    output_json['Internal_datasource'] = internal_file_list
    output_json['External_datasource'] = external_file_list
    print(output_json)


def read_csv_file(file_path):
    """
       This method accepts file path and returns the data frame of the file
       :param file_path: location of the file
       :return: returns data frame of the file
    """
    obj = s3.get_object(Bucket="datainsightsplatform", Key=file_path)
    initial_df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    return initial_df


def get_column_name(df):
    """
       This method accepts data frame and returns the column names of the file
       :param df: data frame of the file
       :return: returns column names from the data frame
    """
    column_names = df.columns.tolist()
    return column_names


def get_data_type(df):
    """
       This method accepts data frame and returns the column data type of the file
       :param df: data frame of the file
       :return: returns column data type from the data frame
    """
    column_data_type = df.dtypes.tolist()
    return column_data_type


def change_data_type(column_data_type):
    """
       This method accepts column data type and returns the changed column data type of the file
       :param column_data_type: column data type of the file
       :return: returns the changed data type list
    """
    data_type_list = []
    for df_type in column_data_type:
        if df_type == "object":
            change_df_type = "Text"
            data_type_list.append(change_df_type)
        elif df_type == 'datetime64[ns]':
            change_df_type = 'Timestamp'
            data_type_list.append(change_df_type)
        elif df_type == "int64" or "float64":
            change_df_type = 'Numeric'
            data_type_list.append(change_df_type)
    return data_type_list


def extract_role(column_data_type):
    """
       This method accepts column data type and returns the role of the column
       :param column_data_type: column data type of the file
       :return: returns the role type list
    """
    type_list = []
    for df_type in column_data_type:
        if df_type == "object":
            change_type = 'Not Feature'
            type_list.append(change_type)
        elif df_type == "int64" or "float64":
            change_type = 'Feature'
            type_list.append(change_type)
        elif df_type == "datetime64[ns]":
            change_type = 'Time'
            type_list.append(change_type)
    return type_list


def calculate_mean(column_name, data_type_list, df):
    """
       This method accepts column name, data type list and data frame and returns the calculated mean for the columns
       which are numeric data type
       :param column_name: name of the column
       :param data_type_list: data type of the column
       :param df: data frame of the file
       :return: returns the mean for the columns which are numeric data type
    """
    avg_list = []
    for i in column_name:
        data_type = data_type_list[column_name.index(i)]
        if data_type == 'Numeric':
            val = df[i].mean()
            avg_list.append(val)
        else:
            avg_list.append('')
    return list(flatten(avg_list))


def calculate_min(column_name, data_type_list, df):
    """
       This method accepts column name, data type list and data frame and returns the calculated min for the columns
       which are numeric data type
       :param column_name: name of the column
       :param data_type_list: data type of the column
       :param df: data frame of the file
       :return: returns the minimum for the columns which are numeric data type
    """
    min_list = []
    for i in column_name:
        data_type = data_type_list[column_name.index(i)]
        if data_type == 'Numeric':
            val = df[i].min()
            min_list.append(val)
        else:
            min_list.append('')
    return list(flatten(min_list))


def calculate_max(column_name, data_type_list, df):
    """
       This method accepts column name, data type list and data frame and returns the calculated max for the columns
       which are numeric data type
       :param column_name: name of the column
       :param data_type_list: data type of the column
       :param df: data frame of the file
       :return: returns the maximum for the columns which are numeric data type
    """
    max_list = []
    for i in column_name:
        data_type = data_type_list[column_name.index(i)]
        if data_type == 'Numeric':
            val = df[i].max()
            max_list.append(val)
        else:
            max_list.append('')
    return list(flatten(max_list))


def calculate_median(column_name, data_type_list, df):
    """
       This method accepts column name, data type list and data frame and returns the calculated median for the columns
       which are numeric data type
       :param column_name: name of the column
       :param data_type_list: data type of the column
       :param df: data frame of the file
       :return: returns the median for the columns which are numeric data type
    """
    median_list = []
    for i in column_name:
        data_type = data_type_list[column_name.index(i)]
        if data_type == 'Numeric':
            val = df[i].median()
            median_list.append(val)
        else:
            median_list.append('')
    return list(flatten(median_list))


def calculate_entropy(df):
    """
       This method accepts data frame and returns the calculated entropy for the columns
       :param column_name: name of the column
       :param data_type_list: data type of the column
       :param df: data frame of the file
       :return: returns the entropy for the columns
    """
    column_name_list = df.columns.values.tolist()
    entropy_list = []
    for column in column_name_list:
        data = df[column].values
        pandas_data = pd.Series(data).value_counts()
        entropy_data = scipy.stats.entropy(pandas_data)  # get entropy from counts
        entropy_data = round(entropy_data, 3)
        entropy_list.append(entropy_data)
    return entropy_list


def calculate_unique_count(column_name, df):
    """
       This method accepts column name and data frame and returns the calculated count for the unique columns
       :param column_name: name of the column
       :param df: data frame of the file
       :return: returns the unique count list for the columns
    """
    count_list = []
    for i in column_name:
        val = df[i].count()
        count_list.append(val)
    return list(flatten(count_list))


def category_check(unique_count_list):
    """
       This method accepts unique count list and returns the category for the columns
       which are numeric data type
       :param unique_count_list: unique count list of the columns
       :return: returns the category for the columns
    """
    find_category = []
    for find_cat in unique_count_list:
        if find_cat < 10:
            find_category.append("CATEGORY")
        else:
            find_category.append("NOT-CATEGORY")
    return list(flatten(find_category))


def missing_rate_check(column_name, df):
    """
       This method accepts column name and data frame and returns the missing rate of the columns
       :param column_name: name of the column
       :param df: data frame of the file
       :return: returns the missing rate of the columns
    """
    missing_per_list = []
    for column in column_name:
        percent_missing = df[column].isnull().sum() * 100 / len(df)
        missing_per_list.append(percent_missing)
    return list(flatten(missing_per_list))


def health_check(category_list, mean_list, median_list, entropy_list, missing_per_list, data_type_list):
    """
       This method accepts category list, mean list, median list, entropy list, missing list and data type list and
       returns the health check for the columns
       :param category_list: category list of the columns
       :param mean_list: mean list of the columns
       :param median_list: median list of the columns
       :param entropy_list: entropy list of the columns
       :param missing_per_list: missing list of the columns
       :param data_type_list: data type of the column
       :return: returns the health check for the columns
    """
    health_diagnosis_list = []
    data_health_list = []
    missing_rate_min = 0.1
    missing_rate_max = 0.3
    threshold = 0.5
    ABS_VAL = 0.6
    concerning_threshold = 0.6
    for category in range(len(category_list)):
        if data_type_list[category] == 'Numeric':
            missing_rate = missing_per_list[category]
            if category_list[category] == "NOT-CATEGORY":
                abs_val = abs(median_list[category]) - mean_list[category]
                if missing_rate >= threshold:
                    data_health = 'Alarming'
                    data_health_list.append('Alarming')
                    if abs_val >= threshold:
                        health_diagnosis = 'Data is highly skewed'
                        health_diagnosis_list.append('Data is highly skewed')
                    else:
                        health_diagnosis = missing_rate
                        health_diagnosis_list.append(
                            'The Missing rate is ' + str(missing_rate))  # 'show the missing %')
                elif missing_rate_min <= missing_rate < missing_rate_max:
                    data_health = 'Concerning'
                    data_health_list.append(data_health)
                    if abs_val >= ABS_VAL:
                        health_diagnosis = 'Data is highly skewed'
                        health_diagnosis_list.append(health_diagnosis)
                    elif abs_val < ABS_VAL:
                        health_diagnosis = 'The Missing rate is ' + str(missing_rate)  # 'show the missing %'
                        health_diagnosis_list.append(health_diagnosis)
                elif missing_rate_min < missing_rate:
                    data_health = 'Good'
                    data_health_list.append(data_health)
                    if abs_val > ABS_VAL:
                        health_diagnosis = 'Data is highly skewed'
                        health_diagnosis_list.append(health_diagnosis)
                    elif abs_val < ABS_VAL:
                        health_diagnosis = 'No problem detected'
                        health_diagnosis_list.append(health_diagnosis)
                else:
                    data_health = 'Good'
                    health_diagnosis = 'No problem detected'
                    health_diagnosis_list.append(health_diagnosis)
                    data_health_list.append(data_health)
            if category_list[category] == "CATEGORY":
                ent_val = entropy_list[category]
                if missing_rate >= threshold:
                    data_health = 'Alarming'
                    data_health_list.append(data_health)
                    if ent_val < threshold:
                        health_diagnosis = 'Data has extreme variation'
                        health_diagnosis_list.append(health_diagnosis)
                    else:
                        health_diagnosis = 'The Missing rate is ' + str(missing_rate)  # 'show the missing %'
                        health_diagnosis_list.append(health_diagnosis)
                if missing_rate >= concerning_threshold:
                    data_health = 'Concerning'
                    data_health_list.append(data_health)
                if missing_rate == 0.0:
                    data_health = 'Good'
                    health_diagnosis = 'No problem detected'
                    health_diagnosis_list.append(health_diagnosis)
                    data_health_list.append(data_health)
        else:
            health_diagnosis_list.append('No problem detected')
            data_health_list.append('Good')
    return health_diagnosis_list, data_health_list


def get_col_list(file_path):
    """
       This method accepts file name and user name and returns the column list of the file related to user
       :param file_path: path of the file
       :return: returns the column list of the file related to user
    """
    obj = s3.get_object(Bucket="datainsightsplatform", Key=file_path)
    initial_df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    col_name = initial_df.columns.values.tolist()
    return col_name


def create_json(column_name, data_type_list, role_list, health_diagnosis_list, data_health_list,
                unique_count_list, missing_per_list, mean_list, entropy_list, median_list, min_list, max_list):
    """
       This method accepts column name, data type list, role list, health diagnosis list, data health list, unique
       count list, missing list, mean list, entropy list, median list, min list and max list and returns the json based
       on the parameters
       :param column_name: name of the column
       :param data_type_list: data type list of the columns
       :param role_list: role list of the columns
       :param health_diagnosis_list: health diagnosis list of the columns
       :param data_health_list: data health list of the columns
       :param unique_count_list: unique count list of the columns
       :param missing_per_list: missing list of the columns
       :param mean_list: mean list of the columns
       :param entropy_list: entropy list of the columns
       :param median_list: median list of the columns
       :param min_list: minimum list of the columns
       :param max_list: maximum list of the columns
       :return: returns the json for the columns based on the parameters
    """
    dictionary = {
        "data": [{'Column_Name': i, 'Data_Type': j, 'Attribute': k, 'Health_Diagnosis': l, 'Column_Health': m,
                  'Unique': n, 'Missing': o, 'Mean': p, 'Std_Dev': q, 'Median': r, 'Min': s, 'Max': t}
                 for i, j, k, l, m, n, o, p, q, r, s, t in zip
                 (column_name, data_type_list, role_list, health_diagnosis_list, data_health_list,
                  unique_count_list, missing_per_list, mean_list, entropy_list, median_list, min_list, max_list)]}
    return dictionary


def get_column_metrics(file_path):
    """
       This method accepts file path and returns the column metrics of the file
       :param file_path: path of the file
       :return: returns the column metrics of the file
    """
    filename = file_path.split('/')[-1]
    user_name = file_path.split('/')[1]
    df = read_csv_file(file_path)
    column_name = get_column_name(df)
    column_data_type = get_data_type(df)
    data_type_list = change_data_type(column_data_type)
    role_list = extract_role(column_data_type)
    mean_list = calculate_mean(column_name, data_type_list, df)
    min_list = calculate_min(column_name, data_type_list, df)
    max_list = calculate_max(column_name, data_type_list, df)
    median_list = calculate_median(column_name, data_type_list, df)
    entropy_list = calculate_entropy(df)
    unique_count_list = calculate_unique_count(column_name, df)
    category_list = category_check(unique_count_list)
    missing_per_list = missing_rate_check(column_name, df)
    health = health_check(category_list, mean_list, median_list, entropy_list, missing_per_list,
                          data_type_list)
    health_diagnosis_list = health[0]
    data_health_list = health[1]
    csv_col_name = get_col_list(file_path)
    json_data = create_json(csv_col_name, data_type_list, role_list, health_diagnosis_list, data_health_list,
                            unique_count_list, missing_per_list, mean_list, entropy_list, median_list,
                            min_list, max_list)
    print(json_data)
    return json_data


def fetch_columns(file_path):
    """
       This method accepts file path and returns the column list
       :param file_path: path of the file
       :return: returns the column list of the file
    """
    try:
        obj = s3.get_object(Bucket='datainsightsplatform', Key=file_path)
        grid_sizes = pd.read_csv(obj['Body'])  # to get all csv data in pandas dataframe format
        #     print(grid_sizes)
        available_columns = grid_sizes.columns.values.tolist()  # to get availale columns in a list format
        print(available_columns)
    except Exception as e:
        print('error at the time of fetching data: ', e)


def get_h2o_credentials():
    """
       This method returns h2o user name, password and URL
       :return: returns the h2o user name, password and URL
    """
    content_object = s3.get_object(Bucket="datainsightsplatform",
                                   Key="Configuration/AI_ML_configuration/configProperties_tangent.json")
    config_file_content = content_object["Body"].read().decode()
    file_content = json.loads(config_file_content)
    h2o_user_name = file_content["h2oConfig"]['userName']
    h2o_pwd = file_content["h2oConfig"]['password']
    h2o_url = file_content["h2oConfig"]['h2oURL']
    return h2o_user_name, h2o_pwd, h2o_url


def build_gbm(file_path, feature_columns, target_column):
    """
       This method accepts file path, feature_columns and target_column
       :param file_path: path of the file
       :param feature_columns: feature columns of the file
       :param target_column: target column of the file
    """
    try:
        h2o_user_name = get_h2o_credentials()[0]
        h2o_pwd = get_h2o_credentials()[1]
        h2o_url = get_h2o_credentials()[2]
        h2o.connect(server=None, url=h2o_url, ip=None, port=None,
                    https=None, verify_ssl_certificates=None, auth=(h2o_user_name, h2o_pwd),
                    proxy=None, cookies=None, verbose=True, config=None)

        data = h2o.import_file('s3a://' + 'datainsightsplatform' + '/' + file_path)
        data['predict'] = data[target_column].asfactor()

        # split into train and testing sets
        train, test = data.split_frame(ratios=[0.8], seed=1234)

        # Build and train the model:
        pros_gbm = H2OGradientBoostingEstimator(nfolds=5,
                                                seed=1111,
                                                keep_cross_validation_predictions=True)
        pros_gbm.train(x=feature_columns, y=target_column, training_frame=train)
        gbm_perf_pred(data, pros_gbm)
        confusion_matrix(pros_gbm, train)
        k_hit_ratio(pros_gbm)
        download_mojo(pros_gbm)
    except Exception as e:
        print("error at the timeof building model: ", e)


def gbm_perf_pred(data, pros_gbm):
    """
       This method accepts data and model
       :param data: data of the file
       :param pros_gbm: model of the file
    """
    try:
        # Eval performance:
        print('*********Start of Performance***************')
        perf = pros_gbm.model_performance()
        print(perf)
        print('*********End of Performance*****************')

        # Generate predictions on a test set (if necessary):
        print('**********Start of Prediction*****************')
        pred = pros_gbm.predict(data)
        print(pred)
        print('**********End of Prediction*****************')
    except Exception as e:
        print("error at the time of metrics calculation: ", e)


def confusion_matrix(pros_gbm, train):
    """
       This method accepts pros_gbm and train and provides the confusion matrix plot
       :param pros_gbm: model of the file
       :param train: train model of the file
    """
    abc = pros_gbm.confusion_matrix(train).as_data_frame()
    for i in abc:
        for j in range(len(abc[i])):
            if type(abc[i][j]) == type(np.float64(1.0)):
                abc[i][j] = round(abc[i][j], 1)
    abc = abc.drop("Rate", axis=1)
    ax = plt.subplot()
    sns.heatmap(abc, xticklabels=abc.columns, yticklabels=False, linewidths=1, annot=True, fmt='g', ax=ax)
    ax.set_title('Confusion Matrix')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.figure(figsize=(10, 7))
    plt.show()


def k_hit_ratio(pros_gbm):
    """
       This method accepts pros_gbm and provides the k-hit ratio plot
       :param pros_gbm: model of the file
    """
    # to create the k-hit ratio
    abc = pros_gbm.hit_ratio_table().as_data_frame()
    abc['k'] = abc.k.astype(int)
    abc['hit_ratio'] = [round(num, 5) for num in abc['hit_ratio']]
    ax = plt.subplot()
    sns.heatmap(abc, xticklabels=abc.columns, yticklabels=False, linewidths=1, annot=True, fmt='g', ax=ax)
    ax.set_title('K-Hit Ratio')
    plt.show()


def download_mojo(pros_gbm):
    """
       This method accepts pros_gbm and downloads the mojo file to downloads folder
       :param pros_gbm: model of the file
    """
    try:
        path = 'Downloads/'
        my_mojo = pros_gbm.download_mojo(path)
        print('mojo_path_in_instance:', my_mojo)
        print('mojo_file_name:', my_mojo.split('/')[-1])
        return my_mojo
    except Exception as e:
        print("error at the time of downloading mojo: ", e)


def upload_mojo(mojo_file_name):
    """
       This method accepts mojo_file_name and uploads the mojo to Downloads folder
       :param mojo_file_name: mojo file
    """
    try:
        path_to_your_mojo = 'Downloads/'
        # mojo_file_name = 'GBM_model_python_1610517303782_3.zip'
        mojo_model = h2o.upload_mojo(path_to_your_mojo + mojo_file_name)

        to_be_predicted_path = 'Test/abc.csv'
        new_observations = h2o.import_file('s3a://' + 'datainsightsplatform' + '/' + to_be_predicted_path)
        predictions = mojo_model.predict(new_observations)
        print("********************start of prediction*********************")
        print(predictions)

    except Exception as e:
        print("error at the time of using of mojo from local: ", e)


def upload_mojo_s3(user, my_mojo):
    """
       This method accepts user and mojo file and upload mojo file to s3
       :param user: user name
       :param my_mojo: mojo file name
    """
    file_name = my_mojo.split('/')[-1]
    key = 'AI_ML/' + user + '/Jupyter/'
    try:
        s3.upload_file(
            my_mojo.replace('\\', '/'),
            'datainsightsplatform',
            key + file_name
        )
        print('uploaded to s3')
    except Exception as exp:
        print('error at the time of uploading mojo to s3: ', exp)


def list_models(user):
    """
       This method accepts user and provides generated models for the user
       :param user: user name
    """
    try:
        response = s3.list_objects(
            Bucket='datainsightsplatform',
            Prefix='AI_ML/' + user
        )
        for i in response['Contents']:
            if '.zip' in i['Key']:  # and 'Model_MOJO' in i['Key']:
                print(i['Key'])
    except Exception as exp:
        print('error at the time of experimenting on mojo: ', exp)


def download_file(mojo_file_path):
    """
       This method accepts mojo file path and downloads file from s3 to downloads folder
       :param mojo_file_path: mojo file path
    """
    try:
        s3.download_file('datainsightsplatform', mojo_file_path, 'Downloads/' + mojo_file_path.split('/')[-1])
        print("downloaded")

    except Exception as exp:
        print('error at the time of experimenting on mojo: ', exp)


def predict_mojo(file_name):
    """
       This method accepts mojo file name and does prediction for the mojo file
       :param file_name: mojo file name
    """
    try:
        mojo_model = h2o.upload_mojo('Downloads/' + file_name)
        to_be_predicted_path = 'Test/abc.csv'
        new_observations = h2o.import_file('s3a://' + 'datainsightsplatform' + '/' + to_be_predicted_path)
        predictions = mojo_model.predict(new_observations)
        print("********************start of prediction*********************")
        print(predictions)
        print('predicted file saved in the path')
        print('s3a://' + 'datainsightsplatform' + '/' + to_be_predicted_path)
    except Exception as exp:
        print('error at the time of experimenting on mojo: ', exp)
