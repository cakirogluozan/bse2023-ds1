import numpy as np
from matplotlib import pyplot as plt
from config import cfg

def data_check(data):
    valid = True
    missing_values = data.isnull().sum() 
    print("Missing values:\n", missing_values)
    if missing_values.sum() > 0:
        valid = False

    mixed_types_cols = []
    for column in data.columns:
        if data[column].apply(type).nunique() > 1:
            mixed_types_cols.append(column)
    if len(mixed_types_cols) == 0:
        print("Columns only have one unique type of object (int, str, etc.)")
    else:
        print(f'Following columns does not have unique values {mixed_types_cols}')
        valid=False


    if valid:
        print('ALL GOOD. Data is clear to work on it')
    else:
        print('WARNING! Data cleaning and correcting is required')
    return 

def peek2data(data, columns_not2show=cfg.columns_not2show):
    for column in data.columns:
        print('-'*50)
        print(f'{column} has {len(data[column].unique())} unique values')
        if column not in columns_not2show:
            print(f'unique values: {data[column].unique()}')
        else:
            print('not printed due to large unique values:')
    return

def convert_cols(data, cfg=cfg):#cfg.columns2convert):
    # mapping_data = dict(enumerate(converted_column.cat.categories))
    data['job_title_cat'] = data['job_title'].astype('category').cat.codes
    data['salary_currency_cat'] = data['salary_currency'].astype('category').cat.codes
    data['employee_residence_cat'] = data['employee_residence'].astype('category').cat.codes
    data['company_location_cat'] = data['company_location'].astype('category').cat.codes
    data['experience_level_cat'] = data['experience_level'].map(cfg.exp_lvl_map)
    data['employment_type_cat'] = data['employment_type'].map(cfg.emp_type_map)
    data['company_size_cat'] = data['company_size'].map(cfg.comp_size_map)
    return data


def avg_salary_by_job(data, font_size=cfg.font_size):
    plt.rcParams.update({'font.size': font_size})
    avg_salary_by_job = data.groupby('job_title')['salary_in_usd'].mean()
    plt.figure(figsize=(10, 8))
    avg_salary_by_job.sort_values().plot(kind='barh')
    plt.xlabel('Average Salary (USD)')
    plt.ylabel('Job Title')
    plt.title('Average Salary by Job Title')
    plt.show()

    return

def multiple_bar(data, values='salary_in_usd', groupby='work_year', compared_col='experience_level', width=0.2, y_label='SALARY $', x_label='YEARS', font_size=cfg.font_size):
    plt.rcParams.update({'font.size': font_size})

    multiplier = 0
    x = np.arange(len(data[groupby].unique()))  # the label locations
    _, ax = plt.subplots(layout='constrained')
    xmax = 0
    for col in data[compared_col].unique():
        salary_by_year = data[data[compared_col]==col].groupby(groupby)[values].mean().sort_index()
        if salary_by_year.shape[0] != len(data[groupby].unique()):
            print(f'{col} will not be added to bar chart due to lack of info for {len(data[groupby].unique())-salary_by_year.shape[0]} years')
            continue
        if np.amax(salary_by_year) > xmax:
            xmax = np.amax(salary_by_year)
        offset = width * multiplier
        rects = ax.bar(x + offset, salary_by_year.astype(int), width, label=col, align='center')
        ax.bar_label(rects, padding=1)
        multiplier += 1

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(x + width, sorted(data[groupby].unique()))
    ax.set_title(f'{values} change of per {compared_col} over {groupby}')
    ax.legend(loc='upper left', ncols=multiplier)
    ax.set_ylim(0, int(xmax*5/4))

    plt.show()
    return


def total_vals_over_gr(data, groupby='work_year', compared_col='experience_level', width=0.2, y_label='COUNT', x_label='YEARS', font_size=cfg.font_size):
    
    plt.rcParams.update({'font.size': font_size})

    multiplier = 0
    x = np.arange(len(data[groupby].unique()))
    _, ax = plt.subplots(layout='constrained')
    xmax = 0
    for col in data[compared_col].unique():
        salary_by_year = data[data[compared_col]==col].groupby(groupby).size().sort_index()
        if np.amax(salary_by_year) > xmax:
            xmax = np.amax(salary_by_year)
        offset = width * multiplier
        rects = ax.bar(x + offset, salary_by_year.astype(int), width, label=col, align='center')
        ax.bar_label(rects, padding=1)
        multiplier += 1

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(x + width, sorted(data[groupby].unique()))
    ax.set_title(f'Distribution of {compared_col} over {groupby}')
    ax.legend(loc='upper left', ncols=multiplier)
    ax.set_ylim(0, int(xmax*5/4))

    plt.show()

    return


def avg_salary_over_focus(data):
    for df_ind in data.index:
        focus = data.job_title.loc[df_ind].split(' ')[-1]
        if focus in ['Data', 'Science', 'Learning']:
            focus = data.job_title.loc[df_ind].split(' ')[0]
        data.loc[df_ind, 'focus'] = focus
    data.groupby('focus').salary_in_usd.mean().plot(kind='pie', autopct='%1.1f%%')
    plt.ylabel('')
    
    return

def split_data_by_time(data, shuffle=True):
    train_data = data[data['work_year'] != 2023]
    test_data = data[data['work_year'] == 2023]
    print(f'training data shape {train_data.shape}')
    print(f'testing data shape {test_data.shape}')
    y_train = train_data['salary_in_usd']
    x_train = train_data.drop(columns=['job_title', 'salary_currency', 'employee_residence', 'company_location', 'experience_level', 'employment_type', 'company_size', 'focus'])

    y_test = test_data['salary_in_usd']
    x_test = test_data.drop(columns=['job_title', 'salary_currency', 'employee_residence', 'company_location', 'experience_level', 'employment_type', 'company_size', 'focus']) # , 'focus'])

    if shuffle:
        shuf_ind = np.random.permutation(len(x_train))
        x_train = x_train.iloc[shuf_ind]
        y_train = y_train.iloc[shuf_ind]

    return x_train, y_train, x_test, y_test

