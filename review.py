import os
import fnmatch


def check_traceability(folder_path):
    for java_file in find_java_files(folder_path):
                with open(java_file, "r") as f:
                    print(java_file)
                    lines = f.readlines()

                    has_rest_controller = False
                    cicsrec_count = 0
                    closeable_count = 0
                    dbcall_count = 0
                    start_count = 0
                    end_count = 0
                    response_count = 0
                    output_text = ""
                    for line in lines:
                        # for controller class
                        if "RestController" in line:
                            has_rest_controller = True
                        # to find backend mainframe CICS call
                        if "CICSREC" in line:
                            cicsrec_count += 1
                        # to scound number of third party service or external service call
                        if "CloseableHttpResponse" in line:
                            closeable_count += 1
                        #to find number of DB call
                        if "PreparedStatement" in line:
                            dbcall_count += 1
                        # unique identfier with start in each method
                        if ("tracebilityId" in line and "Start".casefold() in line)  :
                            start_count += 1
                         # unique identfier with end in each method
                        if ("tracebilityId" in line and "End".casefold() in line) :
                            end_count += 1
                        # unique identfier with response time for each call
                        if ("tracebilityId" in line and "response".casefold() in line)  :
                            response_count += 1
                    if (start_count != end_count):
                        print("{}-is missing tracebilityId with 'Start' or 'End'".format(java_file))
                    if has_rest_controller and response_count == 0:
                        print("{} is missing tracebilityId with 'responseTime' ".format(java_file))
                    if ((cicsrec_count > 0) and  (cicsrec_count!= response_count)):
                        print("{} missing response time for FIS call ".format(java_file))
                    if ((closeable_count > 0) and  (closeable_count!= response_count)):
                        print("{} missing response time for service call ".format(java_file))
                    if ((dbcall_count > 0) and  (dbcall_count!= response_count)):
                        print("{} missing response time for DB call ".format(java_file))


def find_java_files(folder_path):
    # Define the file patterns to search for
    java_patterns = ['*.java']

    # Define the folder names to ignore
    ignore_folders = ['bo', 'model', 'config']

    # Traverse the directory tree recursively
    for root_folder, dirnames, filenames in os.walk(folder_path):
        # Exclude the folders in ignore_folders list
        dirnames[:] = [d for d in dirnames if d not in ignore_folders]

        # Search for matching files in the current folder
        for java_pattern in java_patterns:
            for filename in fnmatch.filter(filenames, java_pattern):
                yield os.path.join(root_folder, filename)


folder_path = input("Enter the source code folder path: ")
check_traceability(folder_path)
