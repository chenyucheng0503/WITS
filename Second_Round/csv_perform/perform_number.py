from Second_Round import sec_main_wits


def perform(num):
    sec_main_wits.CSV_start("csv/csv_"+str(num)+".csv", "2_error_log/error_"+str(num)+".txt",  "2_success_log/success_"+str(num)+".txt",  "line_log/linelog_"+str(num)+".txt")