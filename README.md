# snl-expander-cleaner
![image](https://github.com/msnejad/snl-expander-cleaner/assets/111385244/c44804bc-c210-4bb3-9d65-b1939c61dd99)

The Screener/Data Wizard in S&P Capital IQ Pro Excel Addon makes retrieving insurance statutory filings much easier. However, if you try to download a large panel, particularly when you need the same data for several quarters or years, you reach the download limit:

![image](https://github.com/msnejad/snl-expander-cleaner/assets/111385244/ca434bd0-525c-474d-817f-94cd639e67ad)

A workaround is to use Excel formulas rather than the Wizard. "snl_expander.xlsm" is equipped with a VBA macro that generates these formulas and downloads the data in one query for you. Once you have downloaded the data, you can clean it and transform it into a tidy format using the "snl_cleaner.py" Python script.

# How to use snl_expander.xlsm
Use the wizard and choose all the data fields you need for only one period. For example, if you need Net Total Assets for 2005Q1 to 2022Q4, only choose one period, for instance, 2005Q1. Run the screener and export the data to the Excel sheet named "Original". Make sure to select cell A1 in the sheet before export. Now click the "Run SNL Expander" button and follow the instructions. The macro will ask you the period you want, whether to save results in CSV/XLSX formats, and saves outputs in the same folder.

