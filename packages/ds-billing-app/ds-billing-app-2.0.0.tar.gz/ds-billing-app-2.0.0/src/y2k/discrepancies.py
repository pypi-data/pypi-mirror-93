import io

import numpy as np
import pandas as pd
from google.cloud import bigquery

from y2k.bq_client import initalize_bq_client
from y2k.query_statements import BILLING_AE_QUERY

MONTH_LOOKUP = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "eptember": "09",
    "october": "10",
    "november": "11",
    "december": "12",
}

EXCLUCION_AGENCIES = ["(0282)", "(0606)"]


def read_files_as_dataframes(clearence_report, atb_report):
    clearence_df, inverse = read_clearance_file(clearence_report)
    atb_df = pd.read_excel(atb_report, skiprows=15)
    return clearence_df, atb_df, inverse


def transform_publicis_clearance(file_name):
    xls = pd.ExcelFile(file_name)
    df = pd.DataFrame(columns=list(xls.parse(xls.sheet_names[0])))

    for sheet_name in xls.sheet_names:
        df = df.append(xls.parse(sheet_name)).reset_index(drop=True)

    df_out = df[["INV NUM", "NET INV AMT"]]
    df_out["INV NUM"] = df_out["INV NUM"].str.replace(
        "[a-zA-Z][a-zA-Z][a-zA-Z][0-9][0-9]", "", regex=True
    )
    df_out["INV NUM"] = df_out["INV NUM"].str.replace("[a-zA-Z]{1,}", "", regex=True)
    df_out["INV NUM"] = df_out["INV NUM"].str.strip()

    df_out.columns = ["invoice_number", "net"]
    return df_out


def read_clearance_file(clearance_rep):
    if not clearance_rep:
        return
    inverse = 0
    clear_df = pd.read_excel(clearance_rep, header=None)
    clear_df_out = clear_df.copy()
    if clear_df.iloc[0, 0][0:6] == "Contra":
        header = clear_df.iloc[0]
        clear_df_out = clear_df[1:]
        clear_df_out.rename(columns=header, inplace=True)
    elif clear_df.iloc[0, 0][0:6] == "Accoun":
        header = clear_df.iloc[1]
        clear_df_out = clear_df[2:]
        clear_df_out.rename(columns=header, inplace=True)
    elif clear_df.iloc[0, 0][0:6] == "Client":
        header = clear_df.iloc[0]
        clear_df_out = clear_df[1:]
        clear_df_out.rename(columns=header, inplace=True)
        clear_df_out = transform_hor_clearance(clear_df_out)
        inverse = 1
    elif clear_df.iloc[0, 0][0:3] == "MOS":
        clear_df_out = transform_publicis_clearance(clearance_rep)
    return clear_df_out, inverse


def transform_hor_clearance(df_hor):
    df_out = df_hor[["Inv#", "SchGross"]]
    df_out["SchGross"] = df_out["SchGross"] * 0.85
    df_out["Inv#"] = df_out["Inv#"].str.replace("/", "-", regex=True)
    df_out["Inv#"] = df_out["Inv#"].str.extract("(.*?)(?=-2[0-9][0-9][0-9])")
    df_out["Inv#"] = df_out["Inv#"].str.strip()
    df_out.columns = ["invoice_number", "net"]
    return df_out


def get_ae_info():
    PROJECT_ID = "edm-network-development"
    client = initalize_bq_client()
    return client.query(BILLING_AE_QUERY).result().to_dataframe()
    # # credentials = service_account.Credentials.from_service_account_file(SA_BQ)
    # # client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    # # QUERY = "SELECT * FROM `edm-network-development.NWK_SLS_MART.billing_ae_invoice`"
    # # return client.query(QUERY).result().to_dataframe()
    # return pd.read_csv("tests/data/ae_info.csv")


def process_clearence_report(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("\n", "_")
        .str.replace("#", "number")
    )
    agg_df = df.groupby(["invoice_number"])["net"].agg("sum").reset_index()
    agg_df.columns = ["invoice_number", "cleared"]
    agg_df["invoice_number"] = agg_df["invoice_number"].astype(str)
    return agg_df


def process_atb_report(df):
    df.columns = [
        x.strip().lower().replace(" ", "_").replace("\n", "_").replace("#", "number")
        for x in df.columns
    ]

    df["invoice_number"] = (
        df["invoice_number"].str.replace("/[0-9][0-9]", "", regex=True).str.strip()
    )
    df["invoice_number"] = df["invoice_number"].astype(str)
    df = df[~df.invoice_number.str.match(".*-7[0-9][0-9][0-9]")]
    df = df[~df.invoice_number.str.match(".*-8[0-9][0-9][0-9]")]
    df = df[~df.invoice_number.str.match(".*-66-.*")]
    df = df[~df.invoice_number.str.match(".*-67-.*")]
    return df


def process_ae_invoices_df(df):
    df.drop(
        [
            "deal_version_key",
            "deal_key",
            "gross_amount",
            "total_gross_amount",
            "billing_start_date",
            "billing_end_date",
        ],
        inplace=True,
        axis=1,
    )
    df.columns = ["invoice_number", "A/E"]
    df.drop_duplicates(keep="last", inplace=True)
    return df


def merge_files(clearence_df, atb_df, inverse):
    clearence_df = process_clearence_report(clearence_df)
    atb_df = process_atb_report(atb_df)
    ae_invoices_df = process_ae_invoices_df(get_ae_info())

    cleared_df = pd.merge(atb_df, ae_invoices_df, on="invoice_number", how="left")
    cleared_df = pd.merge(cleared_df, clearence_df, on="invoice_number", how="left")

    cleared_df["invoice_number"] = (
        cleared_df["invoice_number"].str.replace("nan", "", regex=True).str.strip()
    )

    if inverse == 1:
        cleared_df["cleared"] = cleared_df.apply(
            lambda x: x["total_a/r_beg_of_month"]
            if (x["invoice_number"] != "" and np.isnan(x["cleared"]))
            else 0,
            axis=1,
        )
    else:
        cleared_df["cleared"] = cleared_df.apply(
            lambda x: 0
            if (x["invoice_number"] != "" and np.isnan(x["cleared"]))
            else x["cleared"],
            axis=1,
        )

    cleared_df["not_cleared"] = (
        cleared_df["total_a/r_beg_of_month"] - cleared_df["cleared"]
    )

    month_texts = list(cleared_df)[7].replace("_billings", "")
    month_numbers = MONTH_LOOKUP[month_texts]
    cleared_df = cleared_df[
        cleared_df["invoice_number"].str.contains(month_numbers + "-")
    ]

    cleared_df = cleared_df[
        (abs(cleared_df.not_cleared) > 5) | (cleared_df.not_cleared.isnull())
    ]

    drop_columns = [
        "customer_number",
        "invoice_date",
        "`1-30",
        "31-60",
        "61-90",
        "91-120",
        "120+",
        "total_a/r_beg_of_month",
        "pmt_current",
        "pmt_past_due",
        "balance_due",
        "month_to_date_collections",
    ]

    cleared_df.drop(drop_columns, inplace=True, axis=1)

    client_total = (
        cleared_df.groupby(["agency", "client"])["not_cleared"].agg("sum").reset_index()
    )

    client_total["agency"] = client_total["agency"].astype(str)
    client_total["client"] = client_total["client"].astype(str) + " subtotal"

    agency_total = (
        cleared_df.groupby(["agency"])["not_cleared"].agg("sum").reset_index()
    )
    agency_total.columns = ["agency", "not_cleared"]
    agency_total["agency"] = agency_total["agency"].astype(str) + " subtotal"

    agg_agency_total = (
        cleared_df.groupby(["agency_group"])["not_cleared"].agg("sum").reset_index()
    )
    agg_agency_total.columns = ["agency_group", "not_cleared"]
    agg_agency_total["agency_group"] = (
        agg_agency_total["agency_group"].astype(str) + " subtotal"
    )

    agg_ae_invoices_df = (
        cleared_df.groupby(["A/E"])["not_cleared"].agg("sum").reset_index()
    )
    agg_ae_invoices_df.columns = ["A/E", "not_cleared"]

    final_df = (
        cleared_df.append(client_total)
        .append(agency_total)
        .set_index(["agency", "client"])
        .sort_index()
    )

    final_df.reset_index(inplace=True)

    final_df["agency"] = final_df["agency"].astype(str)
    final_df["client"] = final_df["client"].astype(str)
    final_df["agency"] = final_df.apply(
        lambda x: "" if "subtotal" in x["client"] else x["agency"], axis=1
    )
    final_df["client"] = final_df.apply(
        lambda x: "" if x["client"] == "nan" else x["client"], axis=1
    )
    final_df = final_df.append(pd.Series(), ignore_index=True)

    final_df = final_df.append(agg_agency_total)

    col_order = [
        "agency_group",
        "agency",
        # "customer_number",
        "client",
        "invoice_number",
        # "invoice_date",
        "sonumber",
        f"{month_texts}_billings",
        "A/E",
        "cleared",
        "not_cleared",
    ]

    final_df = final_df.append(pd.Series(), ignore_index=True)
    final_df = final_df.append(agg_ae_invoices_df)

    final_df = final_df[col_order]
    final_df.columns = [
        "Agency Group",
        "Agency",
        #"Customer Number"
        "Client",
        "Invoice #",
        #"Invoice Date",
        "SO#",
        f"{month_texts.title()} Billings",
        "A/E",
        "CLEARED",
        "NOT CLEARED",
    ]

    shifts_done = 0
    final_df = final_df.reset_index(drop=True)
    final_table_spaces = final_df

    for idx, line in final_df.iterrows():
        if ("subtotal" in str(final_df.loc[idx, "Client"])) | (
            "subtotal" in str(final_df.loc[idx, "Agency"])
        ):
            line_1 = pd.DataFrame(pd.Series(), index=[idx + shifts_done + 0.5])
            final_table_spaces = final_table_spaces.append(line_1, ignore_index=False)
            final_table_spaces = final_table_spaces.sort_index().reset_index(drop=True)
            shifts_done += 1

    final_df = final_table_spaces.drop([0], axis=1)
    final_df = final_df[
        [
            "Agency Group",
            "Agency",
            #"Customer Number",
            "Client",
            "Invoice #",
            #"Invoice Date",
            "SO#",
            f"{month_texts.title()} Billings",
            "A/E",
            "CLEARED",
            "NOT CLEARED",
        ]
    ]

    return final_df, cleared_df, agency_total, client_total, agg_ae_invoices_df


def get_col_widths(df):
    idx_max = max([len(str(s)) for s in df.index.values] + [len(str(df.index.name))])
    return [idx_max] + [
        max([len(str(s)) for s in df[col].values] + [len(col)]) for col in df.columns
    ]


def set_col_widths(df, ws):
    for idx, col in enumerate(df):
        series = df[col]
        max_len = max((series.astype(str).map(len).max(), len(str(series.name)))) + 2
        ws.set_column(idx, idx, max_len)


def prepare_and_format_excel(final_df, agency_total, client_total, agg_ae_invoices_df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    final_df.to_excel(writer, sheet_name="Summary", index=False)
    client_total.to_excel(writer, sheet_name="Client", index=False)
    agency_total.to_excel(writer, sheet_name="Agency", index=False)
    agg_ae_invoices_df.to_excel(writer, sheet_name="AE", index=False)
    workbook = writer.book
    worksheet = writer.sheets["Summary"]
    money_fmt = workbook.add_format({"align": "right", "num_format": "#,##0.00"})
    workbook.add_format({"border": 1})
    bold_fmt = workbook.add_format({"bold": True})
    format1 = workbook.add_format()
    format1.set_num_format("@")
    completed_fmt = workbook.add_format(  # noqa: F841
        {
            "bold": False,
            "border": 6,
            "align": "center",
            "valign": "vcenter",
            "bg_color": "#D7E4BC",
        }
    )
    worksheet.set_column("F:P", 18, money_fmt)
    number_rows = len(final_df.index) + 1  # noqa: F841
    worksheet.conditional_format(
        "A2:P1000",
        {
            "type": "formula",
            "criteria": 'OR(RIGHT($B2, 8) = "subtotal", RIGHT($C2, 8) = "subtotal")',
            "format": bold_fmt,
        },
    )

    writer.sheets["Client"].set_column("C:C", 18, money_fmt)
    writer.sheets["Agency"].set_column("B:B", 18, money_fmt)
    writer.sheets["AE"].set_column("B:B", 18, money_fmt)

    set_col_widths(final_df, writer.sheets["Summary"])
    set_col_widths(client_total, writer.sheets["Client"])
    set_col_widths(agency_total, writer.sheets["Agency"])
    set_col_widths(agg_ae_invoices_df, writer.sheets["AE"])

    writer.close()
    output.seek(0)

    # return output.getvalue()

    df = pd.read_excel(output)
    df.to_excel("outputFile.xlsx")
