import io

import pandas as pd

from src.y2k.bq_client import initalize_bq_client
from src.y2k.query_statements import (
    INVOICE_NAME_QUERY,
    INVOICES_QUERY,
    RECEIPTS_QUERY,
    BANK_INFO_QUERY,
)


def get_receipts():
    client = initalize_bq_client()
    return client.query(RECEIPTS_QUERY).result().to_dataframe()


def get_invoices():
    client = initalize_bq_client()
    return client.query(INVOICES_QUERY).result().to_dataframe()


def get_sponsor_names():
    client = initalize_bq_client()
    return client.query(INVOICE_NAME_QUERY).result().to_dataframe()


def get_bank_info():
    client = initalize_bq_client()
    return client.query(BANK_INFO_QUERY).result().to_dataframe()


def process_cash_sheet(pay_month, pay_year):
    pay_month =int(pay_month)
    pay_year =int(pay_year)

    df_pay = get_receipts()
    df_all = get_invoices()
    df_names = get_sponsor_names()
    df_bank = get_bank_info()

    df_bank_info = df_bank[
        [
            "DIVISION",
            "RECEIPT_NUMBER",
            "BANK_ACCOUNT_NUM",
            "BANK_NAME",
            "BANK_BRANCH_NAME",
            "RECEIPT_DATE",
        ]
    ]

    df_names.columns = [
        "SPONSOR_NUMBER",
        "CUSTOMER_TRX_ID",
        "TRX_NUMBER",
        "SHIP_TO_CUSTOMER_ID",
        "CUST_ACCOUNT_ID",
        "SPONSOR_NAME",
    ]
    df_sponsors = df_names[["SPONSOR_NUMBER", "TRX_NUMBER", "SPONSOR_NAME"]]

    df_p = df_all[
        ["TRX_NUMBER", "PARTY_SITE_NUMBER", "CATEGORY", "GRP", "BILL_TO_FLAG"]
    ]

    df_payments_primary = pd.merge(
        df_pay,
        df_p,
        left_on=["TRX_NUMBER", "AGENCY"],
        right_on=["TRX_NUMBER", "PARTY_SITE_NUMBER"],
        how="left",
    )
    df_payments_primary = pd.merge(
        df_payments_primary,
        df_sponsors,
        left_on=["TRX_NUMBER"],
        right_on=["TRX_NUMBER"],
        how="left",
    )

    df_payments_primary = df_payments_primary.loc[
        df_payments_primary["BILL_TO_FLAG"] == "P"
    ]
    df_payments_primary["RECEIPT_DATE_2"] = df_payments_primary["RECEIPT_DATE"]
    df_payments_primary["RECEIPT_DATE_2"] = pd.to_datetime(
        df_payments_primary["RECEIPT_DATE"], errors="coerce"
    )

    df_payments_primary["MONTH_R"] = df_payments_primary["RECEIPT_DATE_2"].dt.month
    df_payments_primary["YEAR_R"] = df_payments_primary["RECEIPT_DATE_2"].dt.year

    df_payments_primary["TRX_DATE"] = pd.to_datetime(
        df_payments_primary["TRX_DATE"], errors="coerce"
    )

    df_payments_primary["MONTH"] = df_payments_primary["TRX_DATE"].dt.month
    df_payments_primary["DAY"] = df_payments_primary["TRX_DATE"].dt.day
    df_payments_primary["YEAR"] = df_payments_primary["TRX_DATE"].dt.year

    df_payments_primary = df_payments_primary.loc[
        df_payments_primary["YEAR_R"] >= pay_year
    ]
    df_payments_primary = df_payments_primary.loc[
        df_payments_primary["MONTH_R"] >= pay_month
    ]
    df_bank_info = df_bank_info.drop_duplicates().reset_index(drop=True)

    receipts_bank = pd.merge(
        df_payments_primary, df_bank_info, on="RECEIPT_NUMBER", how="left"
    )


    col_order = [
        "BANK_NAME",
        "BANK_ACCOUNT_NUM",
        "PARTY_SITE_NUMBER",
        "ACCOUNT_NAME",
        "SPONSOR_NAME",
        "CATEGORY",
        "MONTH",
        "YEAR",
        "AMOUNT",
        "AMOUNT_APPLIED",
        "RECEIPT_NUMBER",
        "RECEIPT_DATE_x",
        "STATUS",
        "TRX_NUMBER",
        "TRX_DATE",
        "APPLY_DATE",
        "TRANSACTION_GL_DATE",
        "SPONSOR",
        "AGENCY",
        "GRP",
        "BILL_TO_FLAG",
        "SPONSOR_NUMBER",
        "DAY",
        "DIVISION",
        "BANK_BRANCH_NAME",
        "RECEIPT_DATE_y",
    ]

    receipts_bank = receipts_bank[col_order]
    receipts_bank_agg = (
        receipts_bank.groupby(
            [
                "BANK_NAME",
                "BANK_ACCOUNT_NUM",
                "PARTY_SITE_NUMBER",
                "SPONSOR_NAME",
                "CATEGORY",
                "RECEIPT_NUMBER",
                "RECEIPT_DATE_x",
                "MONTH",
                "YEAR",
            ]
        )["AMOUNT_APPLIED"]
        .agg("sum")
        .reset_index()
    )
    return receipts_bank_agg


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


def format_and_process(df_rec_bank):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df_rec_bank.to_excel(writer, sheet_name="Monthly_Summary", index=False)
    workbook = writer.book
    worksheet = writer.sheets["Monthly_Summary"]

    money_fmt = workbook.add_format({"align": "right", "num_format": "#,##0.00"})
    date_int_fmt = workbook.add_format({"num_format": "#"})

    workbook.add_format({"border": 1})
    bold_fmt = workbook.add_format({"bold": True})  # noqa: F841
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

    writer.sheets["Monthly_Summary"].set_column("J:J", 18, money_fmt)
    writer.sheets["Monthly_Summary"].set_column("H:I", 18, date_int_fmt)

    set_col_widths(df_rec_bank, writer.sheets["Monthly_Summary"])
    writer.close()
    output.seek(0)

    return output.getvalue()
