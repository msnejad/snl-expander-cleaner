import numpy as np
import pandas as pd

naic_forms_variables_renaming = {'Net Total Assets ($000)': 'ASSETS',
                                 'Total Liabilities ($000)': 'LIAB',
                                 'Net Income ($000)': 'NI',
                                 'Net Underwriting Gains ($000)': 'NUG',
                                 'Net Premiums Written ($000)': 'NPW',
                                 'Net Premiums Earned ($000)': 'NPE',
                                 'Direct Premiums Written ($000)': 'DPW',
                                 'Direct Premiums Earned ($000)': 'DPE',
                                 'Direct Losses Incurred ($000)': 'DLI',
                                 'Bonds ($000)': 'BONDS',
                                 'Common Stock ($000)': 'CSTOCKS',
                                 'Preferred Stock ($000)': 'PSTOCKS',
                                 'Bonds: Carrying Value ($000)': 'LBONDS_CV',
                                 'Bonds: Short Term and Cash Equivalent Bonds ($000)': 'SBONDS_CV',
                                 'Pref Stock: Carrying Value ($000)': 'PS_CV',
                                 'Cash Cash Equivalent and Short Term Assets ($000)': 'CASH',
                                 'Auth Control Level Risk Based Capital ($000)': 'RBC',
                                 'Adjusted Capital ($000)': 'ADJCAP',
                                 'Net Adm Cash & Invested Assets ($000)': 'ADM_CASH_INVSTD_ASSETS',
                                 'Subtotal: Cash & Invested Assets ($000)': 'CASH_INVSTD_ASSETS',
                                 'Dividends Paid on Direct Business ($000)': 'DIV',
                                 'Direct Simple Loss & Loss Adj Exp Ratio (%)': 'LAE_RATIO',
                                 'ACL Risk Based Capital Ratio (%)': 'RBC',
                                 'Cash, Equivalents and ST Inv: Gross Inv Holding ($000)': 'CASH_EQV_ST_INV',
                                 'Common Stocks: Gross Investment Holding ($000)': 'COM_STOCK',
                                 'Invested Assets: Gross Investment Holding ($000)': 'TOTAL_INV',
                                 'Long Term Bonds: Gross Investment Holding ($000)': 'LT_BOND',
                                 'Mortgage Loans: Gross Investment Holding ($000)': 'MORTGAGE',
                                 'Preferred Stocks: Gross Investment Holding ($000)': 'PREF_STOCK',
                                 'Real Estate: Gross Investment Holding ($000)': 'REAL_ESTATE',
                                 "Date of Latest Financial Exam by Regulator MM/dd/yyyy": "last_finexam_date",
                                 "Balance Sheet Date of Financial Exam by Regulator MM/dd/yyyy": "last_finexam_balance_sheet_date",
                                 "Date Last Reg Financl Exam Rpt Publicly Available MM/dd/yyyy": "last_finexam_report_date",
                                 "Adj from Last Financial Exam Shown In Fncl Stmts? Yes/No": "is_finexam_adjusted",
                                 "Guidance from Latest Fncl Exam Rpt Complied with? Yes/No": "is_finexam_guidance_complied"
                                 }

naic_forms_variable_modifiers_renaming = {'AR: Total All Lines': 'ALL_LINES',
                                          'AR: Auto Phys': 'AUTO_PHYS',
                                          "AR: Comm'l Auto Liab": "COM_AUTO_LIAB",
                                          'AR: Pvt Pass Auto Liab': "PVT_AUTO_LIAB",
                                          "Add'n Combo: Auto Liab": "ADN_AUTO_LIAB",
                                          "Add'n Combo: Auto Combined": "ADN_AUTO_COMBND",
                                          "AR: Comm'l Auto No-Fault": "COM_AUTO_NF",
                                          "AR: Comm'l Auto Phys": "COM_AUTO_PHYS",
                                          "AR: Oth Comm'l Auto Liab": "COM_AUTO_LIAB_OTH",
                                          'AR: Pvt Pass Auto No-Fault': "PVT_AUTO_NF",
                                          'AR: Pvt Pass Auto Phys Damage': "PVT_AUTO_PHYS",
                                          }


def organize_snl_export(csv_file_path, vars_renaming_dict=None, vars_modifiers_renaming_dict=None):
    """
    In tables exported from SNL, the four rows are the following: Variable name, Variable SNL code, Date, and Variable
    modifier. Variable modifier can include line of business and state, and if it includes both they are separated by a
    colon (":").
    :param csv_file_path: path to the csv file which must have the NAIC Company Code
    :param vars_renaming_dict: a dictionary that matches SNL variable names to desirable variable names
    :param vars_modifiers_renaming_dict: a dictionary that matches SNL variable modifiers to desirable variable
    modifiers
    :return: This function organizes the SNL exported tables to three subtables:
        1. df_subset_no_modifier is a COCODE-VAR-DATE-VALUE table for observations with no VAR_MODIFIER
        2. df_subset_with_modifier is a COCODE-VAR-VAR_MODIFIER-DATE-VALUE table for observations with VAR_MODIFIER
        3. df_subset_with_modifier_state is a COCODE-VAR-VAR_MODIFIER-STATE-DATE-VALUE table for observations with
         VAR_MODIFIER and STATE
    """
    df = pd.read_csv(csv_file_path, encoding_errors='ignore', header=None, low_memory=False)  # Read the csv file
    df = df.drop(1, axis=0)  # Drop SNL variable code that is not needed
    df = df.iloc[:, 2:]  # Drop entity name and S&P statutory entity key that are not needed
    var_names = df.iloc[0, :]  # Variable names are in the first row
    period = df.iloc[1, :]  # Period is the first row
    modifier = df.iloc[2, :]  # Modifier is the second row
    df.columns = [var_names, modifier, period]  # Set column names
    df = df.iloc[3:, ]  # Drop the first three rows after setting them as column names
    df = df[[('NAIC Company Code ', np.nan, np.nan)] + [c for c in df if c != (
        'NAIC Company Code ', np.nan, np.nan)]]  # Move NAIC Company Code to the front
    df = df.melt(id_vars=[df.columns[0]])  # Reshape the dataframe
    df = df.iloc[2:, ]  # Clean rows without data
    df = df.reset_index(drop=True)  # Reset index
    df.columns = ['COCODE', 'VAR', 'VAR_MODIFIER', 'DATE', 'VALUE']
    df = df[~df.COCODE.isna()]  # Drop rows with no COCODE
    df.loc[:, "VAR_MODIFIER"] = df["VAR_MODIFIER"].replace({'PY(0)': np.nan})
    df[["VAR_MODIFIER", "STATE"]] = df. \
        VAR_MODIFIER.str.split("|", expand=True)  # Split VAR_MODIFIER into VAR_MODIFIER and STATE
    df["STATE"] = df["STATE"].str.split(":", expand=True)[1]  # Fix STATE column
    if vars_renaming_dict is not None:
        df.loc[:, "VAR"] = df["VAR"].replace(vars_renaming_dict)  # Rename variables
    if vars_modifiers_renaming_dict is not None:
        df.loc[:, "VAR_MODIFIER"] = df["VAR_MODIFIER"].replace(vars_modifiers_renaming_dict)
    df["VALUE"] = df["VALUE"].str.replace(",", "")  # Remove commas from values
    if 'Q' in df.loc[1, "DATE"]:
        # The date is quarterly
        df["DATE"] = pd.to_datetime(df["DATE"]).dt.to_period('Q').dt.end_time.dt.date
    else:
        # The date is annual
        df["DATE"] = df["DATE"].str.replace("Y", "")  # Remove Y from years
        df["DATE"] = pd.to_datetime(df["DATE"]).dt.to_period('Y').dt.end_time.dt.date

    df_subset_no_modifier = df[df["VAR_MODIFIER"].isna()].drop(columns=['VAR_MODIFIER']).pivot(index=["COCODE", "DATE"],
                                                                                               columns="VAR",
                                                                                               values="VALUE")
    df_subset_with_modifier = df[(~(df["VAR_MODIFIER"].isna())) & (df["STATE"].isna())]. \
        pivot(index=["COCODE", "DATE"], columns=["VAR", "VAR_MODIFIER"], values="VALUE")
    df_subset_with_modifier_by_state = df[(~(df["VAR_MODIFIER"].isna())) & (~df["STATE"].isna())]. \
        pivot(index=["COCODE", "DATE"], columns=["VAR", "VAR_MODIFIER", "STATE"], values="VALUE")
    return df_subset_no_modifier, df_subset_with_modifier, df_subset_with_modifier_by_state
