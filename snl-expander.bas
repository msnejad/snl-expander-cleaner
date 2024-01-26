Attribute VB_Name = "Module1"
Sub snl_expander()
    'Expands SNL Tables.

    'How to use?
    '1. Create a SNL Table in sheet "Original" in cell "A1", using the variables of interest but only for one point in time (a quarter or a year).
    '2. Run this code. The code expands the table to more periods, specified in user prompts, in a new sheet called "Updated".
    'Then refreshes the new table, and if user wants, exports it to a new csv or excel file (in excel file, the SNL table can be updated again).

    'PARAMETERS'''''''''''''''''''''''
    original_sheet_name = "Original"
    ''''''''''''''''''''''''''''''''''
    is_ready = (MsgBox("Create a SNL Table in sheet 'Original' in cell 'A1', using the variables of interest but only for one point in time (a quarter or a year)." & vbNewLine & "Is everything ready?", vbYesNo) = vbYes)
    If Not is_ready Then
        Exit Sub
    End If
    
    'Check if sheet Original exists
    original_sheet_exists = False
    For Each ws In ThisWorkbook.Sheets
        If ws.Name = "Original" Then
            original_sheet_exists = True
            Exit For
        End If
    Next

    If Not original_sheet_exists Then
        MsgBox "Sheet 'Original' doesn't exist. Rename the sheet the containt the SNLTable to 'Original'."
        Exit Sub
    End If

    Dim export_csv As Boolean
    Dim export_excel As Boolean

    st_y = InputBox("Enter the start year:", "Start Year")
    If Not IsNumeric(st_y) Then
        MsgBox "Please enter a valid number for the start year."
        Exit Sub
    End If

    en_y = InputBox("Enter the end year:", "End Year")
    If Not IsNumeric(en_y) Then
        MsgBox "Please enter a valid number for the end year."
        Exit Sub
    End If

    export_csv = (MsgBox("Export to CSV afer completion?", vbYesNo) = vbYes)
    If export_csv Then
        'Prompt the user for the name of the new CSV file
        csv_file_name = InputBox("Enter the name of the new CSV file:")
    End If
    
    export_excel = (MsgBox("Export to Excel after completion?", vbYesNo) = vbYes)
    If export_excel Then
        'Prompt the user for the name of the new excel file
        excel_file_name = InputBox("Enter the name of the new Excel file:")
    End If
    
        
    Dim uws As Worksheet
    Dim quarters As New Collection
    Dim years As New Collection

    For i = st_y To en_y
        years.Add CStr(i) + "Y"
        For j = 1 To 4
            quarters.Add (CStr(i) + "Q") + CStr(j)
        Next
    Next

    For Each ws In Worksheets
        If ws.Name <> original_sheet_name And ws.Visible = True Then
            Application.DisplayAlerts = False
            ws.Delete
            Application.DisplayAlerts = True
        End If
    Next

    Worksheets("Original").Copy After:=Worksheets("Original")
    Worksheets("Original (2)").Name = "Updated"

    Set uws = Worksheets("Updated")

    current_col = uws.Range("A4").End(xlToRight).Column
    Do While uws.Cells(4, current_col).Value <> ""

        If Mid(uws.Cells(4, current_col).Value, 5, 1) = "Q" Then 'quarter type
            Set iterator = quarters
        End If
        If Mid(uws.Cells(4, current_col).Value, 5, 1) = "Y" Then 'year type
            Set iterator = years
        End If

        bg_col = next_col
        counter = 0
        For Each iter In iterator
            new_col = current_col + counter
            If counter <> 0 Then
                Columns(new_col).Insert
                uws.Cells(2, new_col).Formula = uws.Cells(2, new_col - 1).Formula
                uws.Cells(3, new_col).Value = uws.Cells(3, new_col - 1).Value
                uws.Cells(5, new_col).Formula = uws.Cells(5, new_col - 1).Formula
            End If
            uws.Cells(4, new_col) = iter
            counter = counter + 1
        Next
        current_col = current_col + iterator.Count

    Loop

    'Delete the button
    Dim btn As Button
    For Each btn In uws.Buttons
        btn.Delete
    Next btn
    
    'Update table formula
    last_col_num = Cells(2, Columns.Count).End(xlToLeft).Column
    last_col_letter = Split(Cells(1, last_col_num).Address, "$")(1)
    formula_parts = Split(uws.Cells(1, 1).Formula, ",")
    formula_parts(2) = "$C$3:$" & last_col_letter & "3"
    uws.Cells(1, 1).Formula = Join(formula_parts, ",")
    
    'Refresh
    Application.Run ("SNLxlAddin.xla!RefreshActiveCells")
    
    'Export
    If export_csv Then
        Call export_to_csv(csv_file_name)
    End If
    If export_excel Then
        Call export_to_excel(excel_file_name)
    End If
    MsgBox "Done!"

End Sub

Function export_to_excel(fileName)
    'Exports "Updated" sheet generated by snl_expander() to a standalone excel file

    'Get the path of the current file
    Dim filePath As String
    filePath = Application.ActiveWorkbook.Path

    'Export the sheet "Updated" to the new Excel file
    Sheets("Updated").Copy

    'Save the new Excel file in the same directory as the current file
    ActiveWorkbook.SaveAs filePath & "\" & fileName & ".xlsx", xlOpenXMLWorkbook
    ActiveWorkbook.Close

End Function

Function export_to_csv(fileName)
    'Exports "Updated" sheet generated by snl_expander() to a standalone CSV file

    Dim currentWB As Workbook
    Set currentWB = ActiveWorkbook

    'Get the path of the current file
    Dim filePath As String
    filePath = Application.ActiveWorkbook.Path

    'Create the new CSV file
    Dim newFile As Workbook
    Set newFile = Workbooks.Add
    newFile.SaveAs filePath & "\" & fileName & ".csv", xlCSV

    'Copy the values from the current sheet
    currentWB.Sheets("Updated").UsedRange.Copy

    'Paste into the new CSV file
    newFile.Sheets(1).Range("A1").PasteSpecial
    newFile.Sheets(1).Range("A1").PasteSpecial xlPasteValues

    'Clean redundant colunms
    lastColumn = newFile.Sheets(1).Range("A2").End(xlToRight).Column + 1
    ColumnName = Split(Cells(1, lastColumn).Address, "$")(1)
    newFile.Sheets(1).Columns(ColumnName & ":" & ColumnName).Select
    newFile.Sheets(1).Range(Selection, Selection.End(xlToRight)).Select
    newFile.Sheets(1).Application.CutCopyMode = False
    Selection.Delete Shift:=xlToLeft

    'Delete the first row of the sheet
    newFile.Sheets(1).Rows(1).Delete

    'Save abd close the new CSV file
    newFile.Save
    newFile.Close

End Function

