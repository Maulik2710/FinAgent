from .statistics import (
    get_dataset_info,
    get_missing_values,
    get_duplicate_count,
    get_statistical_summary,
    get_date_range
)


def generate_eda_report(df):

    info = get_dataset_info(df)
    start, end = get_date_range(df)
    print("=" * 50)
    print("EDA REPORT")
    print("=" * 50)
    print(f"Rows: {info['rows']}")
    print(f"Columns: {info['columns']}")
    print(f"Date Range: {start} -> {end}")
    print("\nColumn Names")
    print(info["column_names"])
    print("\nData Types")
    print(info["dtypes"])
    print("\nMissing Values")
    print(get_missing_values(df))
    print("\nDuplicate Rows")
    print(get_duplicate_count(df))
    print("\nStatistical Summary")
    print(get_statistical_summary(df))
    print("=" * 50)