import numpy as np
import pandas as pd
from google.cloud import bigquery  # noqa
from datetime import datetime as dt

pd.set_option('display.max_columns', 500)


def get_receipts():
    client = bigquery.Client()
    QUERY = "SELECT * FROM `edm-network-development.NWK_FIN_MART.receipts`"
    return client.query(QUERY).result().to_dataframe()

def get_invoices():
    client = bigquery.Client()
    QUERY = "SELECT * FROM `edm-network-development.NWK_FIN_MART.invoices`"
    return client.query(QUERY).result().to_dataframe()

def get_sponsor_names():
    client = bigquery.Client()
    QUERY = "SELECT * FROM `edm-network-development.NWK_FIN_MART.sponsor_invoices_names`"
    return client.query(QUERY).result().to_dataframe()


day_sales = 3
up_to_month = 9- day_sales
num_days = day_sales * 30

df_pay = get_receipts()
df_all = get_invoices()
df_names = get_sponsor_names()

df_names.columns = ["SPONSOR_NUMBER","CUSTOMER_TRX_ID","TRX_NUMBER","SHIP_TO_CUSTOMER_ID","CUST_ACCOUNT_ID","SPONSOR_NAME"]
df_sponsors = df_names[["SPONSOR_NUMBER","TRX_NUMBER","SPONSOR_NAME"]]

df_all_inv = df_all.loc[df_all['CLASS'] == "INV"]
df_all_pmt = df_all.loc[df_all['CLASS'] == "PMT"]

df_pay_m = df_pay[["TRX_NUMBER","RECEIPT_NUMBER","APPLY_DATE","AMOUNT","RECEIPT_DATE"]]

df_all_left_over = pd.merge(df_all_inv, df_pay_m, left_on=["TRX_NUMBER"], right_on=["TRX_NUMBER"],how="left")

df_all_left_over = pd.merge(df_all_left_over, df_sponsors, left_on=["TRX_NUMBER"], right_on=["TRX_NUMBER"],how="left")

df_all_left_over["RECEIPT_NUMBER"] = df_all_left_over.RECEIPT_NUMBER.fillna('not_paid')
df_all_left_over["ACCOUNT_NAME"] = df_all_left_over.ACCOUNT_NAME.fillna('no_agency')
df_all_left_over["SPONSOR_NAME"] = df_all_left_over.SPONSOR_NAME.fillna('no_sponsor_name')
df_all_left_over = df_all_left_over.drop_duplicates().reset_index(drop=True)


df_all_not_paid = df_all_left_over.loc[df_all_left_over["RECEIPT_NUMBER"] == 'not_paid']
df_all_not_paid = df_all_not_paid.loc[df_all_not_paid['AMOUNT_DUE_REMAINING'] > 0]

#df_all_not_paid['TRX_DATE'] = pd.to_datetime(df_all_not_paid['TRX_DATE'], format = '%d-%b-%y', errors = 'coerce')
#df_all_not_paid['DUE_DATE'] = pd.to_datetime(df_all_not_paid['DUE_DATE'], format = '%d-%b-%y', errors = 'coerce')

df_all_not_paid["MONTH"] = df_all_not_paid['TRX_DATE'].dt.month
df_all_not_paid["DAY"] = df_all_not_paid['TRX_DATE'].dt.day
df_all_not_paid["YEAR"] = df_all_not_paid['TRX_DATE'].dt.year

df_all_not_paid["MONTH_D"] = df_all_not_paid['DUE_DATE'].dt.month
df_all_not_paid["DAY_D"] = df_all_not_paid['DUE_DATE'].dt.day
df_all_not_paid["YEAR_D"] = df_all_not_paid['DUE_DATE'].dt.year

df_all_not_paid = df_all_not_paid.loc[df_all_not_paid['YEAR'] > 2017]

df_all_left_over['TRX_DATE'] = pd.to_datetime(df_all_left_over['TRX_DATE'], format = '%d-%b-%y', errors = 'coerce')

df_all_left_over["MONTH"] = df_all_left_over['TRX_DATE'].dt.month
df_all_left_over["DAY"] = df_all_left_over['TRX_DATE'].dt.day
df_all_left_over["YEAR"] = df_all_left_over['TRX_DATE'].dt.year
print("Number 4")
print(df_all_left_over.head())
df_all_left_over = df_all_left_over.loc[df_all_left_over['YEAR'] > 2018]
print("Number 5")
print(df_all_left_over.head())
# df_all_not_paid = left over accounts receivable
#cleared_df.groupby(["agency", "client"])["not_cleared"].agg("sum").reset_index()
df_AR = df_all_not_paid.groupby(["ACCOUNT_NAME","PARTY_SITE_NUMBER","MONTH","YEAR"])["AMOUNT_DUE_ORIGINAL"].agg("sum").reset_index()
df_AR2 = df_all_not_paid.sort_values(["ACCOUNT_NAME","PARTY_SITE_NUMBER","MONTH","YEAR"],ascending=False).groupby(["ACCOUNT_NAME","PARTY_SITE_NUMBER","MONTH","YEAR"])["AMOUNT_DUE_ORIGINAL"].agg("sum").reset_index()
df_AR2.columns = ["ACCOUNT_NAME","PARTY_SITE_NUMBER","MONTH","YEAR","OUTSTANDING"]
df_AR2.to_csv("AR_sorted.csv",index = False)

df_AR_Agency_Sponsor = df_all_not_paid.sort_values(["ACCOUNT_NAME","PARTY_SITE_NUMBER","SPONSOR_NAME","SPONSOR_NUMBER","MONTH","YEAR"],ascending=False).groupby(["ACCOUNT_NAME","PARTY_SITE_NUMBER","SPONSOR_NAME","SPONSOR_NUMBER","MONTH","YEAR"])["AMOUNT_DUE_ORIGINAL"].agg("sum").reset_index()
df_AR_Agency_Sponsor.columns = ["ACCOUNT_NAME","PARTY_SITE_NUMBER","SPONSOR_NAME","SPONSOR_NUMBER","MONTH","YEAR","OUTSTANDING"]
##check ok

########################### DSO report Agency Level #####################################
df_all_sales = df_all_left_over.sort_values(["ACCOUNT_NAME","PARTY_SITE_NUMBER","MONTH","YEAR"],ascending=False).groupby(["ACCOUNT_NAME","PARTY_SITE_NUMBER","MONTH","YEAR"])["AMOUNT_DUE_ORIGINAL"].agg("sum").reset_index()
df_all_sales.columns = ["ACCOUNT_NAME","PARTY_SITE_NUMBER","MONTH","YEAR","SALES"]
df_all_sales.to_csv("all_sales.csv", index = False)

dso1 = pd.merge(df_all_sales, df_AR2, left_on=["ACCOUNT_NAME","PARTY_SITE_NUMBER","MONTH","YEAR"], right_on=["ACCOUNT_NAME","PARTY_SITE_NUMBER","MONTH","YEAR"],how="left")
dso1_3m = dso1.loc[dso1['MONTH'] > up_to_month]
dso3m = dso1_3m.groupby(['ACCOUNT_NAME','PARTY_SITE_NUMBER']).agg({'SALES':'sum'}).reset_index()
dsoOutstanding = dso1.groupby(['ACCOUNT_NAME','PARTY_SITE_NUMBER']).agg({'OUTSTANDING':'sum'}).reset_index()
dso3m = pd.merge(dsoOutstanding, dso3m, left_on=["ACCOUNT_NAME","PARTY_SITE_NUMBER"], right_on=["ACCOUNT_NAME","PARTY_SITE_NUMBER"],how="left")
dso3m["DSO"] = dso3m["OUTSTANDING"] / dso3m["SALES"] * num_days

dso1.to_csv("dso1_sales.csv", index = False)
dso3m.to_csv("dso3m.csv", index = False)

########################### DSO report Sponsor-Agency Level #####################################

df_all_sales_AS = df_all_left_over.sort_values(["ACCOUNT_NAME","PARTY_SITE_NUMBER","SPONSOR_NAME","SPONSOR_NUMBER","MONTH","YEAR"],ascending=False).groupby(["ACCOUNT_NAME","PARTY_SITE_NUMBER","SPONSOR_NAME","SPONSOR_NUMBER","MONTH","YEAR"])["AMOUNT_DUE_ORIGINAL"].agg("sum").reset_index()
df_all_sales_AS.columns = ["ACCOUNT_NAME","PARTY_SITE_NUMBER","SPONSOR_NAME","SPONSOR_NUMBER","MONTH","YEAR","SALES"]
df_all_sales_AS.to_csv("all_sales_AS.csv", index = False)

dso1_AS = pd.merge(df_all_sales_AS, df_AR_Agency_Sponsor, left_on=["ACCOUNT_NAME","PARTY_SITE_NUMBER","SPONSOR_NAME","SPONSOR_NUMBER","MONTH","YEAR"], right_on=["ACCOUNT_NAME","PARTY_SITE_NUMBER","SPONSOR_NAME","SPONSOR_NUMBER","MONTH","YEAR"],how="left")
dso3m_AS = dso1_AS.loc[dso1_AS['MONTH'] > up_to_month]
dso3m_AS = dso3m_AS.groupby(["ACCOUNT_NAME","PARTY_SITE_NUMBER","SPONSOR_NAME","SPONSOR_NUMBER"]).agg({'SALES':'sum'}).reset_index()
dsoOutstanding_AS = dso1_AS.groupby(["ACCOUNT_NAME","PARTY_SITE_NUMBER","SPONSOR_NAME","SPONSOR_NUMBER"]).agg({'OUTSTANDING':'sum'}).reset_index()
dso3m_AS= pd.merge(dsoOutstanding_AS, dso3m_AS, left_on=["ACCOUNT_NAME","PARTY_SITE_NUMBER","SPONSOR_NAME","SPONSOR_NUMBER"], right_on=["ACCOUNT_NAME","PARTY_SITE_NUMBER","SPONSOR_NAME","SPONSOR_NUMBER"],how="left")
dso3m_AS["DSO"] = dso3m_AS["OUTSTANDING"] / dso3m_AS["SALES"] * num_days

dso1_AS.to_csv("/Users/fcruz1022/Desktop/work/test_outputs/dso1_sales.csv", index = False)
dso3m_AS.to_csv("/Users/fcruz1022/Desktop/work/test_outputs/dso3m_AS.csv", index = False)


#################### Percent Deliquent Agency Level################################
