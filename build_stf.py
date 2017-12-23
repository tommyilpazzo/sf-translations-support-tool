# Import required libraries
import re
import glob
import datetime
import zipfile
import os

# List of supported language codes to be added to the final zip file
supported_language_codes = ["fr", "es_MX", "ja", "ko", "pt_BR"]
# Translated line reg ex pattern
translated_pattern = re.compile("^(?!#).*\t.*\t.*\t.*(?<!\t)$")
# Untranslated line reg ex pattern
untranslated_pattern = re.compile("^(?!#).*\t.*(?!<\t)$")
# Current date time string
datetime_string = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# Source files dict. Map of language code to filename
source_files = {}
# Destination files dict. Map of language code to filename
destination_files = {}

# Unzip destination files. Unzip the last modified zip file.
filename = max(glob.iglob("input/destination/*.zip"), key=os.path.getctime)
zip = zipfile.ZipFile(filename)
zip.extractall("input/destination/")
# Iterate over destination files
for filename in glob.iglob("input/destination/*.stf"):
     language_code = filename[filename.index("_")+1 : filename.rfind("_")]
     if language_code in supported_language_codes:
        destination_files[language_code] = filename

# Unzip source files. Unzip the last modified zip file.
filename = max(glob.iglob("input/source/*.zip"), key=os.path.getctime)
zip = zipfile.ZipFile(filename)
zip.extractall("input/source/")
# Iterate over source files
for filename in glob.iglob("input/source/*.stf"):
    language_code = filename[filename.index("_") + 1: filename.rfind("_")]
    if language_code in supported_language_codes:
        source_files[language_code] = filename

# Iterate over supported language codes inside source zip file
for language_code in source_files:

    # Check if current language code exists inside destination zip file
    if language_code in destination_files:

        source_file_dict = {}
        result_file_keys = []
        source_file = open(source_files[language_code], "r", encoding='UTF8')
        destination_file = open(destination_files[language_code], "r", encoding='UTF8')
        result_file = open("output/result_" + language_code + "_" + datetime_string + ".stf", "w", encoding='UTF8', newline='')

        # Iterate over source file lines
        for line in source_file:
            # Check if translated line
            if translated_pattern.match(line):
                source_file_dict[line.split("\t")[0]] = line.split("\t")[2]
            # Check if untraslated line
            elif untranslated_pattern.match(line):
                source_file_dict[line.split("\t")[0]] = line.rstrip().split("\t")[1]
        # Close source file
        source_file.close()

        # Build result stf file header
        result_file.write("Language code: " + language_code + "\n")
        result_file.write("Type: Bilingual\n")
        result_file.write("\n")
        result_file.write("------------------UNTRANSLATED-----------------\n")
        result_file.write("\n")
        result_file.write("# KEY	LABEL\n")
        result_file.write("\n")

        # Iterate over dest file lines
        for line in destination_file:
            # Check if translated line
            if translated_pattern.match(line):
                key = line.split("\t")[0]
                if key not in result_file_keys :
                    if key in source_file_dict :
                        result_file.write(key + "\t" + source_file_dict[key] + "\n")
                    else:
                        result_file.write(key + "\t" + line.split("\t")[2] + "\n")
                        #print("Missing key in source file " + key)
                    result_file_keys.append(key)
                else :
                    print("Duplicated key " + key)
            # Check if untraslated line
            elif untranslated_pattern.match(line):
                key = line.split("\t")[0]
                if key not in result_file_keys:
                    if key in source_file_dict :
                        result_file.write(key + "\t" + source_file_dict[key] + "\n")
                    else :
                        result_file.write(key + "\t" + line.rstrip().split("\t")[1] + "\n")
                        #print("Missing key in source file " + key)
                    result_file_keys.append(key)
                else:
                    print("Duplicated key " + key)
        # Close destination file
        destination_file.close()
        # Close result file
        result_file.close()

# Move inside output folder
os.chdir("output/")
# Create zip file
zf = zipfile.ZipFile("result_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".zip", "w")
for filename in glob.iglob("*.stf"):
    zf.write(filename)
zf.close()
# Exit output folder
os.chdir("../")

# Remove result files
for filename in glob.iglob("output/*.stf"):
    os.remove(filename)

# Remove unzipped files
for filename in glob.iglob("input/source/*.stf"):
    os.remove(filename)
for filename in glob.iglob("input/destination/*.stf"):
    os.remove(filename)