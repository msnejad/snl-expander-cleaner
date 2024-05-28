import numpy as np
import pandas as pd

naic_forms_variables_renaming = {
    'Total Assets ($000)': 'ASSETS',
    'Net Total Assets ($000)': 'ADM_ASSETS',
    'Non Admitted Total Assets ($000)': 'NON_ADM_ASSETS',
    'NonAdm Write-Ins for Non-Invested Assets ($000)': 'NON_ADM_WRITE_INS_NON_INV',
    'NonAdm Write-Ins of Invested Assets ($000)': 'NON_ADM_WRITE_INS_INV',
    'Total Liabilities ($000)': 'LIAB',
    'Interest Maintenance Reserve ($000)': 'IMR',
    'Asset Valuation Reserve ($000)': 'AVR',
    'Bonds ($000)': 'BONDS',
    'Net Adm Bonds ($000)': 'ADM_BONDS',
    'Net Adm Common Stock ($000)': 'ADM_CSTOCKS',
    'Net Adm Mortgage Loans ($000)': 'ADM_MORTGAGE',
    'Net Adm Preferred Stock ($000)': 'ADM_PSTOCKS',
    'Net Adm Real Estate ($000)': 'ADM_REAL_ESTATE',
    'Net Cash Cash Equivalents and Short Term Assets ($000)': 'ADM_CASH',
    'Bonds: Weighted Avg Ratings by Bond Characteristics (actual)': 'BONDS_WAR',
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
    'Liabilities and Capital & Surplus ($000)': 'LIAB_CAP_SURPLUS',
    'Surplus as Regards Policyholders ($000)': 'SURPLUS',
    'Surplus Notes ($000)': 'SURPLUS_NOTES',
    'Capital & Surplus/ Assets (%)': 'SURPLUS_TO_ASSETS',
    'Loss & Loss Adj Exp Reserves ($000)': 'RESERVES',
    'Loss & Loss Adj Expense ($000)': 'LAE',
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
    "Financial Strength Rating ": "FSR",
    'NAIC Group Number ': 'GCODE',
    'NAIC Company Code ': 'COCODE',
    'Net Income ($000)': 'NI',
    'Total Reserves incl Separate Accounts ($000)': 'RESERVES_INCL_SEP_ACCTS',
    'Total Revenue ($000)': 'REVENUE',
    'Net Underwriting Gains ($000)': 'NUG',
    'Gross Premiums Written ($000)': 'GPW',
    'Net Premiums Written ($000)': 'NPW',
    'Net Premiums Earned ($000)': 'NPE',
    'Direct Premiums Written ($000)': 'DPW',
    'Direct Premiums Earned ($000)': 'DPE',
    'Direct Losses Incurred ($000)': 'DLI',
    'Benefits ($000)': 'BENEFITS',
    'Premiums, Consideration & Deposits ($000)': 'PREMIUMS_CONSD_DEPOSITS',
    'Surrender Benefits, Withdrawals for Life Contracts ($000)': 'SURRENDER_BENEFITS',
    'All Lines: Benefits ($000)': 'BENEFITS',
    'All Lines: Premiums, Consideration & Deposits ($000)': 'PREMIUMS_CONSD_DEPOSITS',
    'All Lines: Surrender Benefits, Withdrawals for Life Contracts ($000)': 'SURRENDER_BENEFITS',
    'General Insurance Expenses ($000)': 'GI_EXPENSES',
    'Negative Cash Flow ($000)': 'NEG_OPER_CASHFLOW',
    'Positive Cash Flow ($000)': 'POS_OPER_CASHFLOW',
    'Cash From Operations ($000)': 'NET_CASH_FROM_OPER',
    'Cash Flow: Investment Proceeds ($000)': 'INV_PROCEEDS',
    'Cash Flow: Cost of Long Term Investments ($000)': 'LT_INV_CASH_COST',
    'Cash Flow: Cash from Investments ($000)': 'NET_CASH_FROM_INV',
    'Net Cash From Financing & Misc Sources ($000)': 'CASH_FROM_FINANCING',
    'Net Chg In Cash & Short Term Investments ($000)': 'NET_CASH_CHG',
    'Cash, Cash Equivalents & Short Term Investments ($000)': 'CASH_EQV_ST_INV',
}

naic_forms_variable_modifiers_renaming = {
    "AR: Total All Lines": "ALL_LINES",
    "AR: Aircraft": "AIRCRAFT",
    "AR: Allied Lines (Sub)": "ALLIED_LINES_SUB",
    "AR: Boiler & Machinery": "BOILER_MACHINERY",
    "AR: Burglary & Theft": "BURGLARY_THEFT",
    "AR: Cllct Rnbl A&H (2021)": "CLLCT_RNBL_AH_2021",
    "AR: Cmprhsv (Hosp, Med) Grp": "CMPRHSV_HOSP_MED_GRP",
    "AR: Cmprhsv (Hosp, Med) Ind": "CMPRHSV_HOSP_MED_IND",
    "AR: Comm'l Auto No-Fault": "COM_AUTO_NF",
    "AR: Comm'l Auto Phys": "COM_AUTO_PHYS",
    "AR: Comm'l Multi Prl (Liab)": "COM_MULTI_PRL_LIAB",
    "AR: Comm'l Multi Prl (Non-Liab)": "COM_MULTI_PRL_NON_LIAB",
    "AR: Credit A&H (Grp & Ind) (2021)": "CREDIT_AH_GRP_IND_2021",
    "AR: Credit": "CREDIT",
    "AR: Dental Only": "DENTAL_ONLY",
    "AR: Disability Income": "DISABILITY_INCOME",
    "AR: Earthquake": "EARTHQUAKE",
    "AR: Excess Workers Comp": "EXCESS_WORKERS_COMP",
    "AR: Farmowners MP": "FARMOWNERS_MP",
    "AR: Fed Emp Health Ben": "FED_EMP_HEALTH_BEN",
    "AR: Federal Flood": "FEDERAL_FLOOD",
    "AR: Fidelity": "FIDELITY",
    "AR: Financial Guaranty": "FINANCIAL_GUARANTY",
    "AR: Fire": "FIRE",
    "AR: Group A&H (2021)": "GROUP_AH_2021",
    "AR: Grted Renewable A&H (2021)": "GRTED_RENEWABLE_AH_2021",
    "AR: Homeowners MP": "HO",
    "AR: Inland Marine": "INLAND_MARINE",
    "AR: International": "INTERNATIONAL",
    "AR: Long-Term Care": "LONG_TERM_CARE",
    "AR: Med Prof Liab (Claims Made)": "MED_PROF_LIAB_CLAIMS_MADE",
    "AR: Med Prof Liab (Occurrence)": "MED_PROF_LIAB_OCCURRENCE",
    "AR: Medicare Supplement": "MEDICARE_SUPPLEMENT",
    "AR: Medicare Title XVIII Tax Exempt (2021)": "MEDICARE_TITLE_XVIII_TAX_EXEMPT_2021",
    "AR: Mrtg Guaranty": "MRTG_GUARANTY",
    "AR: Multiple Peril Crop": "MULTIPLE_PERIL_CROP",
    "AR: Non-Cancelable A&H (2021)": "NON_CANCELABLE_AH_2021",
    "AR: NonRnwbl Stated Only (2021)": "NONRNWBL_STATED_ONLY_2021",
    "AR: Ocean Marine": "OCEAN_MARINE",
    "AR: Oth A&H (State) (2021)": "OTH_AH_STATE_2021",
    "AR: Oth Accident Only (2021)": "OTH_ACCIDENT_ONLY_2021",
    "AR: Oth Comm'l Auto Liab": "COM_AUTO_LIAB_OTH",
    "AR: Oth Health": "OTH_HEALTH",
    "AR: Oth Liab (Claims)": "OTH_LIAB_CLAIMS",
    "AR: Oth Liab (Occurrence)": "OTH_LIAB_OCCURRENCE",
    "AR: Oth P&C (State)": "OTH_P_AND_C_STATE",
    "AR: Oth Pvt Pass Auto Liab": "OTH_PVT_PASS_AUTO_LIAB",
    "AR: Private Crop": "PRIVATE_CROP",
    "AR: Private Flood": "PRIVATE_FLOOD",
    "AR: Prod Liab (Claims)": "PROD_LIAB_CLAIMS",
    "AR: Prod Liab (Occurrence)": "PROD_LIAB_OCCURRENCE",
    "AR: Pvt Pass Auto No-Fault": "PVT_AUTO_NF",
    "AR: Pvt Pass Auto Phys Damage": "PVT_AUTO_PHYS",
    "AR: Reins (NP Assmd Finl)": "REINS_NP_ASSMD_FINL",
    "AR: Reins (NP Assmd Liab)": "REINS_NP_ASSMD_LIAB",
    "AR: Reins (NP Assmd Prop)": "REINS_NP_ASSMD_PROP",
    "AR: Surety": "SURETY",
    "AR: Title XIX Medicaid": "TITLE_XIX_MEDICAID",
    "AR: Title XVIII Medicare": "TITLE_XVIII_MEDICARE",
    "AR: Vision Only": "VISION_ONLY",
    "AR: Warranty": "WARRANTY",
    "AR: Workers' Comp": "WORKERS_COMP",
    "Major: Accident and Health": "MAJOR_AH",
    "Major: Acc & Health (2021)": "MAJOR_AH_2021",
    "Major: Commercial": "MAJOR_COMMERCIAL",
    "Major: Personal": "MAJOR_PERSONAL",
    "Minor: Accident and Health": "MINOR_AH",
    "Minor: Acc & Health (2021)": "MINOR_AH_2021",
    "Minor: Aircraft": "MINOR_AIRCRAFT",
    "Minor: Cmbnd NP Reins": "MINOR_CMBND_NP_REINS",
    "Minor: Comm'l Auto": "MINOR_COMM_AUTO",
    "Minor: Comm'l Multi Prl": "MINOR_COMM_MULTI_PRL",
    "Minor: Fidelity & Surety": "MINOR_FIDELITY_SURETY",
    "Minor: Finl & Mrtg Grty": "MINOR_FINL_MRTG_GRTY",
    "Minor: Fire & Allied Cmbnd": "MINOR_FIRE_ALLIED_CMBND",
    "Minor: Homeowner, Farmowner": "MINOR_HOME_FARM",
    "Minor: Marine Lines Cmbnd": "MINOR_MARINE_LINES_CMBND",
    "Minor: Med Prof Liab": "MINOR_MED_PROF_LIAB",
    "Minor: Oth Comm'l": "MINOR_OTH_COMM",
    "Minor: Oth, Prod Liab Cmbnd": "MINOR_OTH_PROD_LIAB_CMBND",
    "Minor: Private Auto": "MINOR_PRIV_AUTO",
    "Minor: Workers' Comp": "MINOR_WORKERS_COMP",
    "Add'n Combo: Auto Combined": "ADN_AUTO_COMBND",
    "Add'n Combo: Auto Liab": "ADN_AUTO_LIAB",
    "Add'n Combo: Cat Risk": "ADN_CAT_RISK",
    "Add'n Combo: Fire, Allied, Home, MP": "ADN_FIRE_ALLIED_HOME_MP",
    "Add'n Combo: Multi Peril": "ADN_MULTI_PERIL",
    "Add'n Combo: Oth Liab, Prod, Med Prof Liab": "ADN_OTH_LIAB_PROD_MED_PROF_LIAB",
    "Add'n Combo: Oth Liability": "ADN_OTH_LIABILITY",
    "Add'n Combo: Prod Liability": "ADN_PROD_LIABILITY",
    "AR: Comm'l Auto Liab": "COM_AUTO_LIAB",
    "Minor: Private Auto (est)": "MIN_PRIV_AUTO_EST",
    "AR: Allied Lines": "ALLIED_LINES",
    "AR: Auto Phys": "AUTO_PHYS",
    "AR: Oth A&H": "OTH_AH",
    "AR: Oth P&C": "OTH_P_AND_C",
    "AR: Pvt Pass Auto Liab": "PVT_AUTO_LIAB"
}


def organize_snl_export(csv_file_path, record_key, vars_renaming_dict=None,
                        vars_modifiers_renaming_dict=None, convert_values_to_number=True):
    """
    This function organizes and cleans CSV files exported from SNL. The CSV file from SNL must have an identifier column
    (record key), either NAIC_COCODE or SNL_ENTITY_KEY. SNL-generated files have the following four rows at the top:
    Variable name, Variable SNL code, Date, and Variable modifier. Variable modifier can include line of business and
    state, and if it includes both they are separated by a colon (":").
    :param csv_file_path: path to the csv file
    :param record_key: the name of the record key column, which can be either NAIC_COCODE or SNL_ENTITY_KEY. Use
    SNL_ENTITY_KEY when the observations are not at the company level
    :param vars_renaming_dict: a dictionary that matches SNL variable names to desirable variable names
    :param vars_modifiers_renaming_dict: a dictionary that matches SNL variable modifiers to desirable variable
    modifiers
    :param convert_values_to_number: if True, the function will try to convert the values to numbers
    :return: This function organizes the SNL exported tables into 4 subtables:
        1. df_subset_no_date is a COCODE-VAR-VALUE table for observations with no DATE
        2. df_subset_no_modifier is a COCODE-VAR-DATE-VALUE table for observations with no VAR_MODIFIER
        3. df_subset_with_modifier is a COCODE-VAR-VAR_MODIFIER-DATE-VALUE table for observations with VAR_MODIFIER
        4. df_subset_with_modifier_by_modifier is a COCODE-VAR-VAR_MODIFIER-STATE-DATE-VALUE table for observations with
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

    # Rename the first level of columns that is "SNL Statutory Entity Key " to "S&P Statutory Entity Key "
    df.columns = df.columns.set_levels(
        df.columns.levels[0].str.replace('SNL Statutory Entity Key ', 'S&P Statutory Entity Key '), level=0)

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

    # drop the first two rows of df
    df = df.melt(id_vars=[df.columns[0]])  # Reshape the dataframe
    df = df.reset_index(drop=True)  # Reset index
    df.columns = [key_name, 'VAR', 'VAR_MODIFIER', 'DATE', 'VALUE']
    df = df[~df[key_name].isna()]  # Drop rows without key
    df.loc[:, "VAR_MODIFIER"] = df["VAR_MODIFIER"].replace({'PY(0)': np.nan})

    if vars_renaming_dict is not None:
        df.loc[:, "VAR"] = df["VAR"].replace(vars_renaming_dict)  # Rename variables

    df_subset_no_date = df[df["DATE"].isna()].drop(columns=['DATE']).pivot(index=key_name, columns="VAR",
                                                                           values="VALUE")
    df = df[~df["DATE"].isna()]  # Drop rows without date
    df_subset_no_modifier = None
    df_subset_with_modifier = None
    df_subset_with_modifier_by_modifier = None  # Two modifiers, usually VAR_MODIFIER and STATE
    if df.empty is False:
        if convert_values_to_number:
            df["VALUE"] = pd.to_numeric(df["VALUE"].str.replace(",", ""),
                                        errors="coerce")  # Remove commas from values and convert to numeric
        if 'Q' in df.iloc[1]["DATE"]:
            # The date is quarterly
            df["DATE"] = pd.to_datetime(pd.to_datetime(df["DATE"]).dt.to_period('Q').dt.end_time.dt.date)
        else:
            # The date is annual
            df["DATE"] = df["DATE"].str.replace("Y", "")  # Remove Y from years
            df["DATE"] = pd.to_datetime(pd.to_datetime(df["DATE"]).dt.to_period('Y').dt.end_time.dt.date)
        df_subset_no_modifier = df[(df["VAR_MODIFIER"].isna()) & (~df["DATE"].isna())].drop(columns=['VAR_MODIFIER']).pivot(
            index=[key_name, "DATE"],
            columns="VAR",
            values="VALUE")        
    
        if ~df["VAR_MODIFIER"].isna().all():  # If there are observations with VAR_MODIFIER
    
            # drop rows with NaN values in VAR_MODIFIER
            df = df[~df["VAR_MODIFIER"].isna()]
    
            # define df_subset_with_modifier as rows in df whose VAR_MODIFIER does not include |
            df_subset_with_modifier = df[~df["VAR_MODIFIER"].str.contains("\|")]
            df_subset_with_modifier_by_modifier = df[df["VAR_MODIFIER"].str.contains("\|")]
    
            # Fix df_subset_with_modifier
            if df_subset_with_modifier.shape[0] > 0:
                if vars_modifiers_renaming_dict is not None:
                    df_subset_with_modifier.loc[:, "VAR_MODIFIER"] = df_subset_with_modifier["VAR_MODIFIER"].replace(
                        vars_modifiers_renaming_dict)
    
                df_subset_with_modifier = df_subset_with_modifier.pivot(index=[key_name, "DATE"],
                                                                        columns=["VAR", "VAR_MODIFIER"], values="VALUE")
            # df_subset_with_modifier_by_modifier.iloc[1,:]
            # Fix df_subset_with_modifier_by_modifier
            if df_subset_with_modifier_by_modifier.shape[0] > 0:
                df_subset_with_modifier_by_modifier[
                    ["VAR_MODIFIER", "VAR_MODIFIER2"]] = df_subset_with_modifier_by_modifier. \
                    VAR_MODIFIER.str.split("|", expand=True)  # Split VAR_MODIFIER into VAR_MODIFIER and VAR_MODIFIER2
                var_modifier2_is_state = False
                if df_subset_with_modifier_by_modifier["VAR_MODIFIER2"].str.contains(":").any():
                    # The second modifier is STATE
                    var_modifier2_is_state = True
                    df_subset_with_modifier_by_modifier["VAR_MODIFIER2"] = \
                        df_subset_with_modifier_by_modifier["VAR_MODIFIER2"].str.split(":", expand=True)[
                            1]  # Fix STATE column
                if vars_modifiers_renaming_dict is not None:
                    df_subset_with_modifier_by_modifier.loc[:, "VAR_MODIFIER"] = df_subset_with_modifier_by_modifier[
                        "VAR_MODIFIER"].replace(vars_modifiers_renaming_dict)
                if var_modifier2_is_state:
                    df_subset_with_modifier_by_modifier = df_subset_with_modifier_by_modifier.rename(
                        columns={"VAR_MODIFIER2": "STATE"})
                    df_subset_with_modifier_by_modifier = df_subset_with_modifier_by_modifier.pivot(
                        index=[key_name, "DATE"],
                        columns=["VAR", "VAR_MODIFIER",
                                 "STATE"], values="VALUE")
                else:
                    df_subset_with_modifier_by_modifier = df_subset_with_modifier_by_modifier.pivot(
                        index=[key_name, "DATE"],
                        columns=["VAR", "VAR_MODIFIER",
                                 "VAR_MODIFIER2"], values="VALUE")
    
        # If key_name is in df_subset_no_date, merge it with df_subset_no_modifier, df_subset_with_modifier,
        # and df_subset_with_modifier_by_modifier
        if key_name in df_subset_no_date.columns:
            if df_subset_no_modifier is not None:
                df_subset_no_modifier = df_subset_no_modifier.merge(df_subset_no_date, on=key_name, how="left")
            if df_subset_with_modifier is not None:
                df_subset_with_modifier = df_subset_with_modifier.merge(df_subset_no_date, on=key_name, how="left")
            if df_subset_with_modifier_by_modifier is not None:
                df_subset_with_modifier_by_modifier = df_subset_with_modifier_by_modifier.merge(df_subset_no_date,
                                                                                                on=key_name,
                                                                                                how="left")

    # if column names end with a " ", remove the space
    if df_subset_no_date is not None:
        df_subset_no_date.columns = df_subset_no_date.columns.str.rstrip()
    if df_subset_no_modifier is not None:
        df_subset_no_modifier.columns = df_subset_no_modifier.columns.str.rstrip()
    if df_subset_with_modifier is not None:
        df_subset_with_modifier.columns = df_subset_with_modifier.columns.str.rstrip()
    if df_subset_with_modifier_by_modifier is not None:
        df_subset_with_modifier_by_modifier.columns = df_subset_with_modifier_by_modifier.columns.str.rstrip()
    return df_subset_no_date, df_subset_no_modifier, df_subset_with_modifier, df_subset_with_modifier_by_modifier
