from pandas.tseries.offsets import BMonthEnd
import re
import pandas as pd
from datetime import datetime, timedelta, date
import time
import sys
import pdfplumber

# Function to get dates between two dates
def date_range(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


def missing_date_range(prev, curr):
    date1 = datetime.strptime(prev, '%d-%b-%y') + timedelta(1)
    date2 = datetime.strptime(curr, '%d-%b-%y') + timedelta(-1)
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


# Applies regex to the string passed and returns matched groups as a list
def get_data(line):
    rows = r"(\d+\d+) (\d+\d+) (\d+\d+) (\d+\d+) (\d+\d+) (\d+.\d+) (\de.\d+)"
    rows_i = re.search(rows, line)
    if rows_i is None:
        rows = r"(\d+\d+) (\d+\d+) (\d+\d+) (\d+\d+) (\de.\d+) (\de.\d+) (\d+.\d+)"
        rows_i = re.search(rows, line)
        rows_i = [float(x) for x in rows_i.groups()]
        return rows_i
    else:
        rows_i = [float(x) for x in rows_i.groups()]
        return rows_i


# Get the month-end date for the provided month
def get_month_end(month):
    current_month = datetime.now().strftime('%m')
    if current_month == '01':
        passed_month = datetime(date.today().year - 1, month, 1)
    else:
        passed_month = datetime(date.today().year, month, 1)
    offset = BMonthEnd()
    month_end = offset.rollforward(passed_month)
    month_end = month_end.strftime('%d-%b-%y').upper()

    return month_end


def cmp_prev_n_curr_date(prev, curr):
    date1 = datetime.strptime(prev, '%d-%b-%y')
    date2 = datetime.strptime(curr, '%d-%b-%y')
    delta = date2 - date1
    return delta.days


# Execution starts here
month = int(input("1. January\n2. February\n3. March\n4. April"
                  "\n5. May \n6. June\n7. July\n8. August \n9. September"
                  "\n10. October\n11. November\n12. December"
                  "\n\n Select month from above (Enter number): \n"))
if month <= 0 | month > 12:
    raise Exception("Input is expected between 1 and 12 where number corresponds to a month")

task_to_perform = int(input("\nSelect the task you want to perform:\n"
                            "1. Get the NOT APPROVED timesheet details.\n"
                            "2. Generate excel.\n"
                            "3. Employee Count.\n\nEnter selection (1, 2, or 3): "))

if task_to_perform not in [1, 2, 3]:
    raise Exception("Allowed values are only 1, 2, or 3")
month_end = get_month_end(month)

month_list = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
month_word = month_list[month - 1]

# Open PDF
file_path = r"C:\Users\ta\mergedfilesoutput.pdf"
download_path = r"Downloads\ppm"

pdf = pdfplumber.open(file_path)
total_pages = len(pdf.pages)
print("\nTotal pages in PDF:", total_pages)

data = pd.DataFrame()
emp_name_list = []
list_per_emp = []
date_list = []
emp_page_count = 1
prev_fetch_dict = {}
emp_count = 0
name1 = ""
period_new = ""

for i in range(0, total_pages):
    page = pdf.pages[i]
    content = page.extract_text()
    lines = content.split("\n")
    line_count = 0
    temp_list = []
    name_change_flag = False
    name = ""
    name_count = 0
    total_hours = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ext_count = 0
    task_count = 0

    if task_to_perform == 3:
        for line in lines:
            if (line.startswith("Employee Name")):
                line_s = line.split("Name ")
                name = line_s[1]
                if name1 != name:
                    emp_count += 1
                    name1 = name
                    break

    if task_to_perform == 1:
        not_approved_count = 0
        for line in lines:
            if (line.startswith("Employee Name")):
                line_s = line.split("Name ")
                name = line_s[1]

            if line.startswith("Period"):
                line_s = line.split("Period")
                period = line_s[1]
                if period == period_new:
                    print("\n", "Duplicate data exists for employee :", name, " : ", period)
                else:
                    period_new = period

            if line.startswith("Status"):
                line_s = line.split("Status")
                status = line_s[1]
                if status != "Approved":
                    not_approved_count += 1
                    print("\n", name, " : ", period, " - ", status)
                break

    if task_to_perform == 2:
        for line in lines:
            line_count += 1
            if line.startswith("SUB-IN") or line.startswith("PRJ-IN"):
                task_count += 1

        for line in lines:
            ext_count += 1

            if (line.startswith("Employee Name")):
                line_s = line.split("Name ")
                name = line_s[1]
                print("\n", name)
                if ((name not in emp_name_list)):
                    emp_name_list.append(name)
                    name_count += 1

                    if (month_end not in temp_list and (len(emp_name_list) != 0)):
                        list_per_emp.insert(0, emp_name_list[name_count - 1])
                        date_list.insert(0, "Employee_name")
                        df = pd.DataFrame([list_per_emp], columns=date_list)
                        df.set_index = 'Employee_name'
                        data = pd.concat([data, df], axis=0)
                    list_per_emp = []
                    date_list = []
                    emp_page_count = 1
                    prev_fetch_dict = {}

            if (line.startswith("Period")):
                line_s = line.split("Period")
                period = line_s[1]
                print(period)

                period_s = period.split(' to ')
                date1 = datetime.strptime(period_s[0].strip(), '%d-%b-%Y')
                date2 = datetime.strptime(period_s[0].strip(), '%d-%b-%Y')
                try:
                    if (prev_fetch_dict[period] == name):
                        print("Duplicate data exists-----------------------------------------------------")
                        sys.exit("Duplicate data exists")
                        break
                except:
                    print("")

                prev_fetch_dict[period] = name
                for dt in date_range(date1, date2):
                    temp_list.append(dt.strftime('%d-%b-%Y').upper())
                if (temp_list[0] not in date_list):
                    if emp_page_count > 1:
                        diff = cmp_prev_n_curr_date(date_list[(len(date_list) - 1)], temp_list[0])
                        if (diff > 1):
                            for dt in missing_date_range(date_list[(len(date_list) - 1)], temp_list[0]):
                                date_list.append(dt.strftime('%d-%b-%Y').upper())
                                list_per_emp.append(0.0)
                    for i in temp_list:
                        date_list.append(i)

            if ((line.startswith("SUB-IN") or line.startswith("PRJ-IN")) and "Absent" not in line):
                rows_i = get_data(line)
                if (task_count > 1):
                    total_hours = [x + y for (x, y) in zip(total_hours, rows_i)]
                else:
                    total_hours = rows_i

            if (((line.startswith("SUB-IN") or line.startswith("PRJ-IN")) and (task_count == 1) and ("Absent" in line))):
                total_hours = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            if (ext_count == line_count):
                for i in total_hours:
                    list_per_emp.append(i)
                    print("append done")
                    print(name)

        emp_page_count = emp_page_count + 1
        print(month_end)

        if (month_end in temp_list and ext_count == line_count):
            list_per_emp.insert(0, emp_name_list[name_count - 1])
            date_list.insert(0, "Employee_name")
            df = pd.DataFrame([list_per_emp], columns=date_list)
            df.set_index = 'Employee_name'
            data = pd.concat([data, df], axis=0)
            list_per_emp = []
            emp_page_count = 1
            prev_fetch_dict = {}

if task_to_perform == 2:
    reg_str = eval('month_word') + "|Employee_name"
    data = data.filter(regex=reg_str)

    # Add status columns after each week
    for index, row in data.iterrows():
        period_dates = row[1:].values  # All the dates except the 'Employee_name'
        status_list = []

        # Loop through periods and determine status (dummy logic, replace with actual extraction logic)
        for period in period_dates:
            # Assuming we can get status from the period (this logic needs adjustment)
            # If we had a column "Status" somewhere in the line or data, use it to determine the status.
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


# Final Results
if task_to_perform == 1:
    print("\nTotal NOT APPROVED timesheets count:", not_approved_count)
if task_to_perform == 3:
    print("\nTotal Employee Count:", emp_count)

pdf.close()
