import io
from datetime import datetime, timedelta

import pandas as pd

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def df_auto_traffic_parser(df_auto_traffic_orig):
    df = df_auto_traffic_orig.iloc[::3, :].reset_index(drop=True)
    return df


def df_auto_traffic_promo_extract(df_in):
    df = df_in
    df["ns1:EventNote"] = df["ns1:EventNote"].astype(str)
    df = df_in[df_in["ns1:EventNote"].str.contains("Promo")].reset_index(drop=True)
    dfo = df[
        [
            "ns1:AlternateId",
            "ns1:Name",
            "ns1:SmpteTimeCode6",
            "ns1:SmpteTimeCode7",
            "ns1:EventNote",
        ]
    ]
    dfo["type"] = "traffic"
    return dfo


def df_coe_parser(df_coe_orig):
    df = df_coe_orig
    df.drop(["BIN"], axis=1, inplace=True)
    df.rename(columns={"Unnamed: 16": "Bin"}, inplace=True)

    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    df["Date"] = df["Date"].astype(str)
    df["Day"] = df["Day"].astype(str)

    df["show"] = ""

    show = ""
    for i in df.index:
        if (df.loc[i, "Date"] == "nan") & (df.loc[i, "Day"] != "nan"):
            show = df.loc[i, "Day"]
        df.at[i, "show"] = show

    df = df[df.Date != "nan"].reset_index(drop=True)
    df["show"] = df["show"].fillna("")
    df["show"] = df["show"].astype(str)
    df["Dur. (s)"] = df["Dur. (s)"].fillna(0)
    df["Dur. (s)"] = df["Dur. (s)"].astype(float)
    df["Dur. (s)"] = df["Dur. (s)"].astype(int)
    df["show"] = df["show"].str.replace("#(.*)", "", regex=True).str.strip()
    df["show"] = (
        df["show"]
        .str.replace("YOUNG AND RESTLESS", "YOUNG AND THE RESTLESS", regex=True)
        .str.strip()
    )
    df["show"] = (
        df["show"]
        .str.replace("BOLD & BEAUTIFUL", "BOLD AND THE BEAUTIFUL", regex=True)
        .str.strip()
    )
    df["show"] = (
        df["show"]
        .str.replace("PRICE IS RIGHT", "THE PRICE IS RIGHT", regex=True)
        .str.strip()
    )
    df["show"] = (
        df["show"]
        .str.replace("NCIS NEW ORLEANS", "NCIS: NEW ORLEANS", regex=True)
        .str.strip()
    )
    df["show"] = (
        df["show"]
        .str.replace("LATE LATE SHOW", "LATE LATE SHOW WITH JAMES CORDEN", regex=True)
        .str.strip()
    )

    return df


def df_ipro_parser(df_ipro_orig):
    df = df_ipro_orig

    df.rename(columns={"Unnamed: 0": "avail_code"}, inplace=True)
    df.rename(columns={"Unnamed: 3": "avail_dur"}, inplace=True)
    df.rename(columns={"Unnamed: 5": "show"}, inplace=True)
    df.rename(columns={"Unnamed: 7": "promo_dur"}, inplace=True)
    df.rename(columns={"Unnamed: 10": "promo_pres_event_title"}, inplace=True)
    df.rename(columns={"Unnamed: 14": "ISCI"}, inplace=True)
    df.rename(columns={"Unnamed: 17": "tx_element_cat"}, inplace=True)
    df.rename(columns={"Unnamed: 19": "BIN"}, inplace=True)

    df["avail_code"] = pd.Series(df["avail_code"]).fillna(method="ffill")
    df["avail_dur"] = pd.Series(df["avail_dur"]).fillna(method="ffill")
    df["show"] = pd.Series(df["show"]).fillna(method="ffill")
    df["show_time"] = ""
    show_time = ""
    times = df["avail_code"].str.contains("AM|PM", regex=True)

    for i in times.index:
        if times[i]:
            show_time = df.loc[i, "avail_code"]
        df.at[i, "show_time"] = show_time

    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    df["promo_dur"] = df["promo_dur"].astype(str)
    df = df[df.promo_dur != "nan"].reset_index(drop=True)

    df["show"] = df["show"].fillna("")
    df["show"] = df["show"].astype(str)
    df["show"] = df["show"].str.replace("- O", "", regex=True).str.strip()

    df["promo_dur"] = df["promo_dur"].astype(float)
    df["promo_dur"] = df["promo_dur"].astype(int)

    return df


def df_email_parser():
    raise NotImplementedError


def consolidate_promo_feeds(df_auto_traffic_orig, df_coe_orig, df_ipro_orig):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")

    df_coe = df_coe_parser(df_coe_orig)
    df_coe = df_coe.add_suffix("_coe")
    df_ipro = df_ipro_parser(df_ipro_orig)
    df_ipro = df_ipro.add_suffix("_pro")

    c1o = pd.merge(
        df_ipro,
        df_coe,
        left_on=["ISCI_pro", "BIN_pro", "promo_dur_pro"],
        right_on=["ISCI_coe", "Bin_coe", "Dur. (s)_coe"],
        how="outer",
    )

    c1o["type"] = ""
    c1o["show_time_pro"] = c1o["show_time_pro"].fillna("notime")
    c1o["show_time_pro"] = c1o["show_time_pro"].astype(str)
    c1o["show_time_pro_24"] = pd.to_datetime(
        c1o["show_time_pro"], format="%I:%M %p", errors="coerce"
    ).dt.time
    c1o["show_time_pro_24"] = c1o["show_time_pro_24"].fillna("notime")
    c1o["show_time_pro_24"] = c1o["show_time_pro_24"].astype(str)

    c1o["Start Time_coe"] = c1o["Start Time_coe"].astype(str)
    c1o["day_order"] = 1

    for i in c1o.index:
        if c1o.loc[i, "Start Time_coe"][0:2] == "1.":
            c1o.at[i, "Start Time_coe"] = c1o.at[i, "Start Time_coe"][2:]
            c1o.at[i, "day_order"] = 2

    c1o["Start Time_coe"] = pd.to_datetime(
        c1o["Start Time_coe"], format="%H:%M:%S", errors="coerce"
    ).dt.time

    for i in c1o.index:
        if c1o.loc[i, "show_coe"] == "LET'S MAKE A DEAL":
            t = c1o.loc[i, "Start Time_coe"]
            c1o.at[i, "Start Time_coe"] = (
                datetime.combine(datetime(1, 1, 1), t) - timedelta(hours=5)
            ).time()

    c1o["Start Time_coe"] = c1o["Start Time_coe"].fillna("notime")
    c1o["Start Time_coe"] = c1o["Start Time_coe"].astype(str)
    c1o["Sponsor_coe"] = c1o["Sponsor_coe"].fillna(c1o["promo_pres_event_title_pro"])

    for i in c1o.index:
        pro_val = c1o.loc[i, "show_time_pro_24"]
        coe_val = c1o.loc[i, "Start Time_coe"]
        if coe_val == "notime":
            c1o.at[i, "type"] = "pro"
            c1o.at[i, "Start Time_coe"] = pro_val
        elif pro_val == "notime":
            c1o.at[i, "type"] = "coe"
        else:
            c1o.at[i, "type"] = "pro_coe"

    c1o.to_excel(writer, sheet_name="Sheet 1", index=False)

    writer.close()
    output.seek(0)

    return output.getvalue()
