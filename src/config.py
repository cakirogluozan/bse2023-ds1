from pathlib import Path

from pydantic import BaseSettings
'''
job_title             object
salary                 int64
salary_currency       object
salary_in_usd          int64
employee_residence    object
remote_ratio           int64
company_location      object
company_size          object
'''
# Define your dictionary mapping of objects to integers for ordinal data
EXP_LVL_MAP = {'EN': 1, 'MI': 2, 'SE': 3, 'EX': 4}
EMP_TYPE_MAP = {'CT': 1, 'FL': 2, 'PT': 3, 'FT': 4}
COMP_SIZE_MAP = {'S': 1, 'M': 2, 'L': 3}

# Convert the column to integers using the dictionary mapping
exp_lvl_dict = {}
class Settings(BaseSettings):
    data_path: Path = Path("../data/ds_salaries.csv")
    font_size: int = int(7)
    columns_not2show: list = list(['job_title', 'salary', 'salary_in_usd'])
    exp_lvl_map: dict = EXP_LVL_MAP
    emp_type_map: dict = EMP_TYPE_MAP
    comp_size_map: dict = COMP_SIZE_MAP
cfg = Settings()
