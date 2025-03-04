if task_to_perform == 2:
    reg_str = eval('month_word')+"|Employee_name"
    data = data.filter(regex=reg_str)

    # For each employee's timesheet, we need to add a status column after each week
    for index, row in data.iterrows():
        period_dates = row[1:].values  # All the dates except the 'Employee_name'
        status_list = []

        # Loop through periods and determine status (dummy logic, replace with actual extraction logic)
        for period in period_dates:
            # Assuming we can get status from the period (this logic needs adjustment)
            # If we had a column "Status" somewhere in the line or data, use it to determine the status.
            # Example: Add status based on some external logic or status of the task
            if "Approved" in period:  # Check if it's approved (example logic)
                status_list.append("Approved")
            elif "Submitted" in period:  # Check if it's submitted
                status_list.append("Submitted")
            else:  # Default to Pending
                status_list.append("Pending")
        
        # After collecting status for the periods, insert them into the DataFrame as new columns
        for i, status in enumerate(status_list):
            status_column_name = f"Status_{i + 1}"  # Create unique column names for each week
            data.insert(i * 2 + 1, status_column_name, status)  # Insert after each week

    # Now save the updated DataFrame with statuses to Excel
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    data.to_excel(download_path + '/' + month_word + '_' + current_time + '.xlsx')
    print("\n..DONE..")
