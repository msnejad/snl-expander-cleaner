import numpy as np
import pandas as pd

naic_forms_variables_renaming = {
                                 'Total Assets ($000)': 'ASSETS',
                                 'Total Liabilities ($000)': 'LIAB',
                                 'Net Income ($000)': 'NI',
                                 'Net Underwriting Gains ($000)': 'NUG',
                                 'Gross Premiums Written ($000)': 'GPW',
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
                                 'Adjusted Capital ($000)': 'ADJCAP',
                                 'Auth Control Level Risk Based Capital ($000)': 'AUTH_RBC',
                                 'CAL Risk Based Capital Ratio (%)': 'CAL_RBC',
                                 'ACL Risk Based Capital Ratio (%)': 'RBC',
                                 'Surplus as Regards Policyholders ($000)': 'SURPLUS',
                                 'Loss & Loss Adj Exp Reserves ($000)': 'RESERVES',
                                 'Net Investment Income Earned ($000)': 'INV_INC',
                                 'Net Yield on Invested Assets (%)': 'INV_YIELD',
                                 'Net Adm Cash & Invested Assets ($000)': 'ADM_CASH_INVSTD_ASSETS',
                                 'Subtotal: Cash & Invested Assets ($000)': 'CASH_INVSTD_ASSETS',
                                 'Dividends Paid on Direct Business ($000)': 'DIV',
                                 'Direct Simple Loss & Loss Adj Exp Ratio (%)': 'LAE_RATIO',
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
                                 "Guidance from Latest Fncl Exam Rpt Complied with? Yes/No": "is_finexam_guidance_complied",
                                 'NAIC Group Number ': 'GCODE',
                                 'NAIC Company Code ': 'COCODE'
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
                                          "Add'n Combo: Cat Risk": "ADN_CAT_RISK",
                                          }


def organize_snl_export(csv_file_path, record_key, vars_renaming_dict=None,
                        vars_modifiers_renaming_dict=None):
    """
    In tables exported from SNL, the four rows are the following: Variable name, Variable SNL code, Date, and Variable
    modifier. Variable modifier can include line of business and state, and if it includes both they are separated by a
    colon (":").
    :param csv_file_path: path to the csv file which must have the NAIC Company Code
    :param record_key: the name of the record key column, can be either NAIC_COCODE or SNL_ENTITY_KEY. Use SNL_ENTITY_KEY
    when the observations are not at the company level
    :param vars_renaming_dict: a dictionary that matches SNL variable names to desirable variable names
    :param vars_modifiers_renaming_dict: a dictionary that matches SNL variable modifiers to desirable variable
    modifiers
    :return: This function organizes the SNL exported tables to three subtables:
        1. df_subset_no_modifier is a COCODE-VAR-DATE-VALUE table for observations with no VAR_MODIFIER
        2. df_subset_with_modifier is a COCODE-VAR-VAR_MODIFIER-DATE-VALUE table for observations with VAR_MODIFIER
        3. df_subset_with_modifier_by_state is a COCODE-VAR-VAR_MODIFIER-STATE-DATE-VALUE table for observations with
         VAR_MODIFIER and STATE
    """
    df = pd.read_csv(csv_file_path, encoding_errors='ignore', header=None, low_memory=False)  # Read the csv file
    df = df.drop(1, axis=0)  # Drop SNL variable code that is not needed
    var_names = df.iloc[0, :]  # Variable names are in the first row
    period = df.iloc[1, :]  # Period is in the second row
    modifier = df.iloc[2, :]  # Modifier is the third row
    df.columns = [var_names, modifier, period]  # Set column names
    df = df.iloc[3:, ]  # Drop the first three rows after setting them as column names
    df = df.iloc[:, 1:]  # Drop the entity name

    # Set record key to the front
    if record_key == "NAIC_COCODE":
        df = df[[('NAIC Company Code ', np.nan, np.nan)] + [c for c in df if c != (
            'NAIC Company Code ', np.nan, np.nan)]]  # Move NAIC Company Code to the front
        key_name = "COCODE"
        # drop S&P Statutory Entity Key
        df = df.drop(('S&P Statutory Entity Key ', np.nan, np.nan), axis=1)
    elif record_key == "SNL_ENTITY_KEY":
        df = df[[('S&P Statutory Entity Key ', np.nan, np.nan)] + [c for c in df if c != (
            'S&P Statutory Entity Key ', np.nan, np.nan)]]
        key_name = "SNL_ENTITY_KEY"
        # # drop NAIC Company Code if it exists
        # if ('NAIC Company Code ', np.nan, np.nan) in df.columns:
        #     df = df.drop(('NAIC Company Code ', np.nan, np.nan), axis=1)
    else:
        raise ValueError("record_key must be either NAIC_COCODE or SNL_ENTITY_KEY")

    df = df.melt(id_vars=[df.columns[0]])  # Reshape the dataframe
    df = df.iloc[2:, ]  # Clean rows without data
    df = df.reset_index(drop=True)  # Reset index
    df.columns = [key_name, 'VAR', 'VAR_MODIFIER', 'DATE', 'VALUE']
    df = df[~df[key_name].isna()]  # Drop rows without key
    df.loc[:, "VAR_MODIFIER"] = df["VAR_MODIFIER"].replace({'PY(0)': np.nan})

    if vars_renaming_dict is not None:
        df.loc[:, "VAR"] = df["VAR"].replace(vars_renaming_dict)  # Rename variables

    df_subset_no_date = df[df["DATE"].isna()].drop(columns=['DATE']).pivot(index=key_name, columns="VAR",
                                                                           values="VALUE")
    df = df[~df["DATE"].isna()]  # Drop rows without date
    df_subset_no_modifier = df[(df["VAR_MODIFIER"].isna()) & (~df["DATE"].isna())].drop(columns=['VAR_MODIFIER']).pivot(
        index=[key_name, "DATE"],
        columns="VAR",
        values="VALUE")
    df_subset_with_modifier = None
    df_subset_with_modifier_by_state = None

    if ~ df["VAR_MODIFIER"].isna().all():  # If there are observations with VAR_MODIFIER
        df[["VAR_MODIFIER", "STATE"]] = df. \
            VAR_MODIFIER.str.split("|", expand=True)  # Split VAR_MODIFIER into VAR_MODIFIER and STATE
        df["STATE"] = df["STATE"].str.split(":", expand=True)[1]  # Fix STATE column
        if vars_modifiers_renaming_dict is not None:
            df.loc[:, "VAR_MODIFIER"] = df["VAR_MODIFIER"].replace(vars_modifiers_renaming_dict)
        df["VALUE"] = df["VALUE"].str.replace(",", "")  # Remove commas from values
        if 'Q' in df.iloc[1]["DATE"]:
            # The date is quarterly
            df["DATE"] = pd.to_datetime(df["DATE"]).dt.to_period('Q').dt.end_time.dt.date
        else:
            # The date is annual
            df["DATE"] = df["DATE"].str.replace("Y", "")  # Remove Y from years
            df["DATE"] = pd.to_datetime(df["DATE"]).dt.to_period('Y').dt.end_time.dt.date

        df_subset_with_modifier = df[(~(df["VAR_MODIFIER"].isna())) & (df["STATE"].isna())]. \
            pivot(index=[key_name, "DATE"], columns=["VAR", "VAR_MODIFIER"], values="VALUE")

        df_subset_with_modifier_by_state = df[(~(df["VAR_MODIFIER"].isna())) & (~df["STATE"].isna())]. \
            pivot(index=[key_name, "DATE"], columns=["VAR", "VAR_MODIFIER", "STATE"], values="VALUE")

    # If COCODE is in df_subset_no_date, merge it with df_subset_no_modifier, df_subset_with_modifier,
    # and df_subset_with_modifier_by_state
    if "COCODE" in df_subset_no_date.columns:
        if df_subset_no_modifier is not None:
            df_subset_no_modifier = df_subset_no_modifier.merge(df_subset_no_date, on=key_name, how="left")
        if df_subset_with_modifier is not None:
            df_subset_with_modifier = df_subset_with_modifier.merge(df_subset_no_date, on=key_name, how="left")
        if df_subset_with_modifier_by_state is not None:
            df_subset_with_modifier_by_state = df_subset_with_modifier_by_state.merge(df_subset_no_date, on=key_name,
                                                                                      how="left")

    return df_subset_no_date, df_subset_no_modifier, df_subset_with_modifier, df_subset_with_modifier_by_state
