from datetime import datetime, timedelta

import pandas as pd
from fuzzywuzzy import process as pfuzz

# df_auto_traffic_orig = pd.read_excel(f1)
# df_coe_orig = pd.read_excel(f2, skiprows=3)
# df_ipro_orig = pd.read_excel(f3)
# df_phoenix_orig = pd.read_excel(f4)

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def fuzzy_names_coe(dfin, df_ipro, column_name):

    dfipro = df_ipro_parser(df_ipro)
    show_names = dfipro.show.unique()

    for i in dfin.index:
        cname = dfin.loc[i, column_name]
        tup = pfuzz.extractOne(cname, show_names)

        if tup[1] > 80:
            dfin.at[i, column_name] = pfuzz.extractOne(cname, show_names)[0]

    return dfin


def fuzzy_names_cams(dfin, df_ipro, column_name):

    dfipro = df_ipro_parser(df_ipro)
    show_names = dfipro.show.unique()

    for i in dfin.index:
        cname = dfin.loc[i, column_name]
        tup = pfuzz.extractOne(cname, show_names)

        if tup[1] > 80:
            dfin.at[i, column_name] = pfuzz.extractOne(cname, show_names)[0]

    return dfin


def read_cams(f_in):
    df_ratings = pd.read_excel(f_in, skiprows=3)
    df_ratings = df_ratings[
        [
            "Days",
            "Date",
            "Pgm St Time",
            "Program Title",
            "Duration",
            "LIVE+SD HH %",
            "% Coverage",
        ]
    ]

    df_ratings.rename(
        columns={"Played Duration": "Duration", "gm St Time": "Start Time"},
        inplace=True,
    )
    return df_ratings


def read_in_sports(f_in):
    df_name = list(pd.read_excel(f_in))[0]
    df_sports = pd.read_excel(f_in, skiprows=1)
    df_sports["game_name"] = df_name
    first_ad = datetime.strptime(df_sports.loc[1, "Time"], "%H:%M:%S:%f").time()
    first_ad_time = first_ad.hour + first_ad.minute / 60
    if first_ad_time < 15:
        df_sports["Show"] = "1PM"
    else:
        df_sports["Show"] = "4PM"
    return df_sports


def read_in_sports_nfl(f_in):
    df_name = list(pd.read_excel(f_in))[0]
    df_sports = pd.read_excel(f_in, skiprows=1)
    df_sports["game_name"] = df_name
    first_ad = datetime.strptime(df_sports.loc[1, "Time"], "%H:%M:%S:%f").time()
    first_ad_time = first_ad.hour + first_ad.minute / 60
    if first_ad_time < 15:
        df_sports["Show"] = "1PM"
    else:
        df_sports["Show"] = "4PM"
    return df_sports


def read_in_sports_ncaa(f_in):
    df_name = list(pd.read_excel(f_in))[0]
    df_sports = pd.read_excel(f_in, skiprows=1)
    df_sports["game_name"] = df_name
    df_sports["Show"] = "NCAA"


def df_sports_concat(files_in):
    appended_data = []
    for infile in files_in:
        data = read_in_sports(infile)
        appended_data.append(data)
    if not files_in:
        df_out = []
    else:
        df_out = pd.concat(appended_data).reset_index(drop=True)

    return df_out


def df_sports_nfl_process(dfin):
    dfout = dfin[dfin["Type"] == "PRO"].reset_index()

    mask_pregame = dfout["Break Id"].str.contains("PREGAME")
    dfout.loc[mask_pregame, "Show"] = "THE NFL TODAY PRESENTED"

    mask_postgun = dfout["Break Id"].str.contains("POSTGUN")
    dfout.loc[mask_postgun, "Show"] = "NFL NATIONAL POSTGUN"

    mask_postgun = dfout["Break Id"].str.contains("BREAK END BREAK")
    dfout.loc[mask_postgun, "Show"] = "NFL REGIONAL POSTGUN"

    dfout = dfout[
        [
            "Channel",
            "Position",
            "Date",
            "Isci",
            "Bin",
            "Sponsor",
            "Played Duration",
            "Time",
            "Show",
            "game_name",
        ]
    ]

    dfout.rename(
        columns={
            "Played Duration": "Duration",
            "Time": "Start Time",
            "Isci": "ISCI",
            "game_name": "type",
        },
        inplace=True,
    )

    dfout["Duration"] = pd.to_datetime(
        dfout["Duration"], format="%H:%M:%S:%f", errors="coerce"
    ).dt.second
    dfout["Start Time"] = pd.to_datetime(
        dfout["Start Time"], format="%H:%M:%S:%f", errors="coerce"
    ).dt.round(freq="S")
    dfout["Start Time"] = dfout["Start Time"].dt.time
    dfout = dfout.reset_index(drop=True)
    # g = ['ISCI', 'Duration', 'Start Time', 'Date', 'Bin', 'Position','Sponsor']
    g = ["ISCI", "Duration", "Date", "Bin", "Position", "Sponsor", "Show"]
    dfo = dfout.groupby(g)["type"].apply(lambda x: ", ".join(x)).reset_index()
    dftime = dfout.groupby(g)["Start Time"].min().reset_index()

    dfo = pd.merge(dfo, dftime, on=g, how="left")

    # print(list(dfo))
    # dfo = dfout.groupby(g).agg(lambda x: ', '.join(x)).reset_index()
    dfo["day_order"] = 1
    return dfo


def df_auto_traffic_parser(df_auto_traffic_orig):
    df = df_auto_traffic_orig.iloc[::3, :].reset_index(drop=True)
    return df


def get_traffic_show_list(df):
    terms = ["CBS", "LSA", "LSB"]

    # df1 = df_in[df_in['ns1:EventNote'].str.contains('|'.join(terms))].reset_index(drop=True)
    # print(list(df))

    dfo = df[df["ns1:Name4"].str.contains("|".join(terms), na=False)]
    dfo = dfo[["ns1:Name", "broadcastDate", "ns1:SmpteTimeCode6"]]

    dfo.rename(columns={"ns1:Name": "show", "ns1:SmpteTimeCode6": "time"}, inplace=True)

    dfo["time"] = pd.to_datetime(
        dfo["time"], format="%H:%M:%S:%f", errors="coerce"
    ).dt.time
    dfo["date"] = pd.to_datetime(
        dfo["broadcastDate"], format="%m:%d:%y %H:%M:%S", errors="coerce"
    ).dt.date

    for i in dfo.index:
        td = dfo.loc[i, "date"]
        tt = dfo.loc[i, "time"]
        dfo.at[i, "combo_time"] = datetime.combine(td, tt)

    dfo = dfo.iloc[::3, :].reset_index(drop=True)
    dfo.to_csv("df_local_shows.csv", index=False)
    return dfo


def df_auto_traffic_promo_extract(df_in):

    df = df_in
    dfshows = get_traffic_show_list(df_in)

    df["ns1:EventNote"] = df["ns1:EventNote"].astype(str)
    terms = ["tease", "Tease", "TEASE"]

    # dfShow = get_traffic_show_list(df_in)

    df1 = df_in[df_in["ns1:EventNote"].str.contains("|".join(terms))].reset_index(
        drop=True
    )
    df1 = df1[
        [
            "scheduleStart",
            "ns1:AlternateId",
            "broadcastDate",
            "ns1:Name",
            "ns1:SmpteTimeCode6",
            "ns1:SmpteTimeCode7",
            "ns1:EventNote",
        ]
    ]

    df2 = df_in[df_in["ns1:AlternateId"].str.match("[1-2][1-9][a-zA-Z]{1}.*", na=False)]
    df2 = df2[df2["ns1:Status"] != "Did not air"]

    df2 = df2[
        [
            "scheduleStart",
            "ns1:AlternateId",
            "broadcastDate",
            "ns1:Name",
            "ns1:SmpteTimeCode6",
            "ns1:SmpteTimeCode7",
            "ns1:EventNote",
        ]
    ]
    dfo = pd.concat([df1, df2])
    dfo = dfo[pd.notnull(dfo["ns1:AlternateId"])]

    dfo["Duration"] = pd.to_datetime(
        dfo["ns1:SmpteTimeCode7"], format="%H:%M:%S:%f", errors="coerce"
    ).dt.second
    dfo["time"] = pd.to_datetime(
        dfo["ns1:SmpteTimeCode6"], format="%H:%M:%S:%f", errors="coerce"
    ).dt.time
    dfo["date"] = pd.to_datetime(
        dfo["broadcastDate"], format="%m:%d:%y %H:%M:%S", errors="coerce"
    ).dt.date

    for i in dfo.index:
        td = dfo.loc[i, "date"]
        tt = dfo.loc[i, "time"]
        dfo.at[i, "temp_date_time"] = datetime.combine(td, tt)

    for i in dfo.index:
        d = dfo.loc[i, "date"]
        t = dfo.loc[i, "time"]
        dfo.at[i, "DT"] = (datetime.combine(d, t) - timedelta(hours=5)).replace(
            microsecond=0
        )

    dfo["Start Time"] = dfo["DT"].dt.time
    dfo = dfo.sort_values(by=["temp_date_time"])

    dfo["Show"] = ""
    for i in dfo.index:
        curr_dt = dfo.loc[i, "temp_date_time"]
        for j in dfshows.index:
            if (curr_dt > dfshows.loc[j, "combo_time"]) & (
                curr_dt < dfshows.loc[j + 1, "combo_time"]
            ):
                dfo.at[i, "Show"] = dfshows.loc[j, "show"]
                break

    dfo["Date"] = pd.to_datetime(
        dfo["scheduleStart"], format="%m:%d:%y %H:%M:%S", errors="coerce"
    ).dt.date
    dfo.rename(columns={"ns1:AlternateId": "ISCI", "ns1:Name": "Sponsor"}, inplace=True)

    dfo = dfo[["Start Time", "Date", "ISCI", "Sponsor", "Duration", "Show"]]

    dfo["Position"] = ""
    dfo["Bin"] = ""

    dfo["type"] = "nyc"
    dfo["day_order"] = 1

    dfo.to_csv("df_local_regex.csv", index=False)

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
        df["show"].str.replace("(1ST HALF HOUR)", "10:30AM", regex=True).str.strip()
    )
    df["show"] = (
        df["show"].str.replace("(2ND HALF HOUR)", "11:00AM", regex=True).str.strip()
    )
    return df


def df_ipro_parser(df_ipro_orig):
    df = df_ipro_orig
    pro_date = df.iloc[3, 11]
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
    df["show"] = df["show"].str.replace("- P", "", regex=True).str.strip()
    df["show"] = df["show"].str.replace("- SP", "", regex=True).str.strip()
    df["promo_dur"] = df["promo_dur"].astype(float)
    df["promo_dur"] = df["promo_dur"].astype(int)
    # df = df[df.Date != 'nan'].reset_index(drop = True)
    # pd.to_datetime(dfo['ns1:SmpteTimeCode6'], format = '%H:%M:%S:%f', errors = 'coerce').dt.time
    POSITIONS = {"PP": "P", "SH": "S"}
    df["avail_code"] = df["avail_code"].replace("NTID", "NI", regex=True)
    df["avail_code"] = df["avail_code"].replace("POS", "PO", regex=True)

    mask1 = df["avail_code"].str.contains("PP") & (df["avail_code"].str.len() > 3)
    df.loc[mask1, "avail_code"] = df.loc[mask1, "avail_code"].replace(
        "PP", "P", regex=True
    )

    mask1 = df["avail_code"].str.contains("SH") & (df["avail_code"].str.len() > 3)
    df.loc[mask1, "avail_code"] = df.loc[mask1, "avail_code"].replace(
        "SH", "S", regex=True
    )
    df.to_csv("debug_ipro.csv")
    df["date"] = datetime.strptime(pro_date, "%A, %B %d, %Y").date()

    return df


def df_email_parser():
    return 0


def df_merge_pro_sports(dfpro, dfsports):

    c1o = pd.merge(
        dfpro,
        dfsports,
        left_on=["ISCI_pro", "promo_dur_pro", "avail_code_pro"],
        right_on=["ISCI", "Duration", "Position"],
        how="outer",
    )
    c1o["show_time_pro"] = c1o["show_time_pro"].fillna("notime")
    c1o["show_time_pro"] = c1o["show_time_pro"].astype(str)
    c1o["show_time_pro_24"] = pd.to_datetime(
        c1o["show_time_pro"], format="%I:%M %p", errors="coerce"
    ).dt.time
    c1o["day_order"] = 1

    c1o.to_csv("merge_pro_sports.csv", index=False)

    return 0


def consolidate_promo_feeds_discrepancy(
    df_auto_traffic_orig, df_coe_orig, df_ipro_orig, f_sports_file
):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")

    df1 = df_auto_traffic_promo_extract(df_auto_traffic_parser(df_auto_traffic_orig))

    df_coe = fuzzy_names_coe(df_coe_parser(df_coe_orig), df_ipro_orig, "show")
    df_coe = df_coe.add_suffix("_coe")

    df_ipro = df_ipro_parser(df_ipro_orig)
    df_ipro = df_ipro.add_suffix("_pro")

    # c1 = pd.merge(
    #     df_ipro,
    #     df_coe,
    #     left_on=["ISCI_pro", "BIN_pro"],
    #     right_on=["ISCI_coe", "Bin_coe"],
    #     how="left",
    # )
    c1o = pd.merge(
        df_ipro,
        df_coe,
        left_on=["ISCI_pro", "show_pro", "promo_dur_pro", "avail_code_pro"],
        right_on=["ISCI_coe", "show_coe", "Dur. (s)_coe", "Position_coe"],
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

    c1o["Sponsor_coe"] = c1o["Sponsor_coe"].fillna(c1o["promo_pres_event_title_pro"])
    c1o["show_coe"] = c1o["show_coe"].fillna(c1o["show_pro"])
    c1o["Bin_coe"] = c1o["Bin_coe"].fillna(c1o["BIN_pro"])
    c1o["ISCI_coe"] = c1o["ISCI_coe"].fillna(c1o["ISCI_pro"])
    c1o["Dur. (s)_coe"] = c1o["Dur. (s)_coe"].fillna(c1o["avail_dur_pro"])
    c1o["Date_coe"] = c1o["Date_coe"].fillna(c1o["date_pro"])

    c1o = c1o.sort_values(by=["day_order", "Start Time_coe"])

    c1o.drop_duplicates(inplace=True)

    c1o.to_csv("c1o.csv", index=False)

    c1oo = c1o[
        [
            "Date_coe",
            "Start Time_coe",
            "avail_code_pro",
            "Position_coe",
            "Dur. (s)_coe",
            "ISCI_coe",
            "Bin_coe",
            "Sponsor_coe",
            "show_coe",
            "tx_element_cat_pro",
            "type",
            "day_order",
        ]
    ]
    c1oo.rename(
        columns={
            "Date_coe": "Date",
            "Start Time_coe": "Start Time",
            "avail_code_pro": "Position Pro",
            "Position_coe": "Position",
            "Dur. (s)_coe": "Duration",
            "ISCI_coe": "ISCI",
            "Bin_coe": "Bin",
            "tx_element_cat_pro": "tx_element_cat",
            "Sponsor_coe": "Sponsor",
            "show_coe": "Show",
        },
        inplace=True,
    )

    c1oo["Start Time"] = pd.to_datetime(
        c1oo["Start Time"], format="%H:%M:%S", errors="coerce"
    ).dt.time
    if not f_sports_file:
        c2o = pd.concat([c1oo, df1])
    else:
        # df_sport = df_sports_process(df_sports_concat(f_sports_file))
        df_merge_pro_sports(df_ipro, df_sport)
        c2o = pd.concat([c1oo, df1, df_sport])

    c2o = c2o.sort_values(by=["day_order", "Start Time"])
    # c2o.to_csv("discrepancy" + out_date + ".csv", index=False)


def consolidate_promo_feeds_asrun(df_auto_traffic_orig, df_coe_orig, f_sports):
    df1 = df_auto_traffic_promo_extract(df_auto_traffic_parser(df_auto_traffic_orig))
    get_traffic_show_list(df_auto_traffic_orig)

    df_coe = df_coe_parser(df_coe_orig)
    df_coe = df_coe.add_suffix("_coe")

    df_coe["type"] = "coe"
    df_coe["day_order"] = 1
    for i in df_coe.index:
        if df_coe.loc[i, "Start Time_coe"][0:2] == "1.":
            df_coe.at[i, "Start Time_coe"] = df_coe.at[i, "Start Time_coe"][2:]
            df_coe.at[i, "day_order"] = 2

    df_coe["Start Time_coe"] = pd.to_datetime(
        df_coe["Start Time_coe"], format="%H:%M:%S", errors="coerce"
    ).dt.time

    coe = df_coe[
        [
            "Date_coe",
            "Start Time_coe",
            "Position_coe",
            "Dur. (s)_coe",
            "ISCI_coe",
            "Bin_coe",
            "Sponsor_coe",
            "show_coe",
            "type",
            "day_order",
        ]
    ]
    coe.rename(
        columns={
            "Date_coe": "Date",
            "Start Time_coe": "Start Time",
            "Position_coe": "Position",
            "Dur. (s)_coe": "Duration",
            "ISCI_coe": "ISCI",
            "Bin_coe": "Bin",
            "Sponsor_coe": "Sponsor",
            "show_coe": "Show",
        },
        inplace=True,
    )
    if not f_sports:
        co = pd.concat([coe, df1])
    else:
        df_sport = df_sports_process(df_sports_concat(f_sports))
        co = pd.concat([coe, df1, df_sport])

    co = co.sort_values(by=["day_order", "Start Time"])
    co.to_csv("asrun_" + out_date + ".csv", index=False)

    writer.close()
    output.seek(0)
    return output.getvalue()


# consolidate_promo_feeds_discrepancy(df_auto_traffic_orig, df_coe_orig, df_ipro_orig,f_sports)
# consolidate_promo_feeds_asrun(df_auto_traffic_orig, pd.read_excel(f2, skiprows = 3), f_sports)
# print("--- %s seconds ---" % (time.time() - start_time))
