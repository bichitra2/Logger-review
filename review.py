import os
import fnmatch
import ruamel.yaml


def check_traceability(folder_path):
  with open("Code Review Result.txt", "w") as output_file:
    for java_file in find_java_files(folder_path):
                with open(java_file, "r") as f:
                    #print(java_file)
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
                        # search for controller class
                        if "RestController" in line:
                            has_rest_controller = True
                        # search for keyword for CICS mainframe requests
                        if "CICS request execute staments" in line:
                            cicsrec_count += 1
                        # search for keyword for third part service call requests
                        if "HTTP response key word for service call" in line:
                            closeable_count += 1
                        # search for keyword for DB execute statements
                        if "DB execute stament key word" in line:
                            dbcall_count += 1
                        if ("Unique identifier id in the message" in line) :
                            if ("Start" in line or "start" in line)  :
                             start_count += 1
                            if ("End" in line or "end" in line) :
                              end_count += 1
                            if ("response" in line or "Response Time" in line or "response time" in line)  :
                               response_count += 1
                    if (start_count != end_count or start_count == 0 or end_count == 0):
                        output_file.write(" \n")
                        output_file.write("{} -is missing Unique identifier id with 'Start' or 'End' \n".format(java_file))
                    if (has_rest_controller and response_count == 0):
                        output_file.write(" \n")
                        output_file.write("{} -is missing Unique identifier id with Response Time' \n".format(java_file))
                    if ((cicsrec_count > 0) and  (cicsrec_count!= response_count)):
                        output_file.write(" \n")
                        output_file.write("{} -is missing Unique identifier id with 'responseTime' for CICS call \n".format(java_file))
                    if ((closeable_count > 0) and  (closeable_count!= response_count)):
                        output_file.write(" \n")
                        output_file.write("{} -is missing 'responseTime' for service call \n".format(java_file))
                    if ((dbcall_count > 0) and  (dbcall_count!= response_count)):
                        output_file.write(" \n")
                        output_file.write("{} -is missing traceabilty id with 'responseTime' for DB call \n".format(java_file))


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


def ci_ver(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file1 in files:
            # search for continious integration deployment yaml file
            if file1 == ("deployment yaml file"):
                with open(os.path.join(root, file1), "r") as f:
                    contents = f.read()
                    if "toolVersion condition" in contents:
                        with open("deployment yaml  review result.txt", "w") as output_file:
                            output_file.write(" \n")
                            output_file.write((os.path.join(root,file1)))
                            output_file.write("\n borkvresion found in deployment yaml , pls remove. \n")
                    else:
                        with open ("deployment yaml  review result.txt" , "w") as output_file:
                            output_file.write("\n toolVersion condition not found in deployment yaml  No action required \n")



folder_path = input("Enter the source code folder path: ")
check_traceability(folder_path)
ci_ver(folder_path)
