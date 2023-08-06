import re
from typing import Any

import pandas as pd

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def parse_coe_file(coe_file: Any) -> pd.DataFrame:
    coe_df = pd.read_excel(coe_file, skiprows=3)
    coe_df["BIN"] = coe_df["Unnamed: 16"]
    coe_df["show_name"] = coe_df["Day"].replace(DAYS, None).fillna(method="ffill")
    coe_df = coe_df.iloc[:, ~coe_df.columns.str.contains("^Unnamed", case=False)]
    coe_df = coe_df.dropna(subset=["Date"])

    coe_df.columns = coe_df.columns.str.lower()
    coe_df.rename(columns={"dur. (s)": "duration"}, inplace=True)
    coe_df.reset_index(inplace=True, drop=True)
    coe_df.rename(columns={"start time": "airing_time"}, inplace=True)
    coe_df["position"] = coe_df["position"].fillna("")
    coe_df["date"] = pd.to_datetime(coe_df["date"])

    return coe_df


def parse_ipro_file(ipro_file: Any) -> pd.DataFrame:
    ipro_raw_df = pd.read_excel(ipro_file)
    report_date = ipro_raw_df.iloc[3][~ipro_raw_df.iloc[3].isnull()][0]

    ipro_raw_df["Unnamed: 5"] = ipro_raw_df["Unnamed: 5"].fillna(method="ffill")
    ipro_raw_df["Unnamed: 0"] = ipro_raw_df["Unnamed: 0"].fillna(method="ffill")

    shows = []
    for show in ipro_raw_df["Unnamed: 5"].dropna().unique().tolist():
        temp_df = ipro_raw_df[ipro_raw_df["Unnamed: 5"] == show].copy()
        show_time = temp_df.iloc[0][0]
        temp_df["Unnamed: 8"] = temp_df["Unnamed: 8"].fillna(temp_df["Unnamed: 7"])
        temp_df["Unnamed: 9"] = temp_df["Unnamed: 9"].fillna(temp_df["Unnamed: 10"])
        temp_df["Unnamed: 13"] = temp_df["Unnamed: 13"].fillna(temp_df["Unnamed: 14"])
        temp_df["Unnamed: 20"] = temp_df["Unnamed: 20"].fillna(temp_df["Unnamed: 19"])
        temp_df.columns = temp_df.iloc[1]
        temp_df = temp_df.iloc[2:].copy()
        temp_df = temp_df.iloc[:, [0, 7, 9, 13, 17, 20]]
        temp_df = temp_df.dropna(subset=["ISCI"])
        temp_df.columns = [
            "position",
            "duration",
            "promo_title",
            "isci",
            "tx_element_cat",
            "bin",
        ]
        temp_df["show_name"] = show
        temp_df["scheduled_date"] = report_date
        temp_df["scheduled_time"] = show_time
        shows.append(temp_df)

    ipro_df = pd.concat(shows)
    ipro_df["tx_element_cat"] = ipro_df["tx_element_cat"].fillna("")
    ipro_df["date"] = pd.to_datetime(ipro_df["scheduled_date"])
    return ipro_df.reset_index(drop=True)


def format_position(pos: str) -> str:

    if len(pos) <= 3:
        return pos

    parts = re.split("(\\d+)", pos)

    if len(parts) == 1:
        return pos

    if len(parts[1]) >= 2:
        return parts[0][0] + parts[1]

    if parts[0] == "NTID":
        return "NI" + parts[1]

    return pos


def define_airing_schedule(row: dict) -> str:
    if str(row["airing_time"]) == "nan":
        return "SCHEDULED_AND_NOT_AIRED"
    if str(row["airing_time"]) != "nan" and str(row["scheduled_time"]) == "nan":
        return "AIRED_AND_NOT_SCHEDULED"
    if str(row["airing_time"]) != "nan" and str(row["scheduled_time"]) != "nan":
        return "AIRED_AND_SCHEDULED"


def asrun_network(coe_df: pd.DataFrame, ipro_df: pd.DataFrame) -> pd.DataFrame:
    ipro_df["position"] = ipro_df["position"].apply(lambda x: format_position(x))
    coe_report = coe_df.merge(
        ipro_df, how="left", on=["isci", "position", "date"], suffixes=("_coe", "_ipro")
    )
    ipro_report = ipro_df.merge(
        coe_df, how="left", on=["isci", "position", "date"], suffixes=("_ipro", "_coe")
    )
    combined_df = pd.concat([coe_report, ipro_report]).drop_duplicates()
    combined_df["show_name_coe"] = combined_df["show_name_coe"].fillna(
        combined_df["show_name_ipro"]
    )
    combined_df["duration_coe"] = combined_df["duration_coe"].fillna(
        combined_df["duration_ipro"]
    )
    combined_df["sponsor"] = combined_df["sponsor"].fillna(combined_df["promo_title"])

    combined_df = combined_df[
        [
            "date",
            "airing_time",
            "type",
            "position",
            "duration_coe",
            "isci",
            "sponsor",
            "show_name_coe",
            "tx_element_cat",
            "scheduled_time",
        ]
    ]

    combined_df.rename(
        columns={
            "duration_coe": "duration",
            "sponsor": "promotion_title",
            "show_name_coe": "show_name",
        },
        inplace=True,
    )

    combined_df["airing_status"] = combined_df[["airing_time", "scheduled_time"]].apply(
        define_airing_schedule, axis=1
    )
    combined_df.fillna("", inplace=True)

    return combined_df
