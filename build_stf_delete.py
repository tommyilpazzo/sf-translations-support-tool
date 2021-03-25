# Import required libraries
import re
import glob
import datetime
import zipfile
import os

# List of supported language codes to be added to the final zip file
supported_language_codes = ["en_US", "ro"]
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

keys_to_ignore = []
# keys_to_ignore = ["CrtColumn.MRO_CasesWithOrWithoutSupplies.Supply__c.Status", "CrtColumn.MRO_CasesWithOrWithoutSupplies.Account.Name"]

# Unzip destination files. Unzip the last modified zip file.
filename = max(glob.iglob("input/destination/*.zip"), key=os.path.getctime)
zip = zipfile.ZipFile(filename)
zip.extractall("input/destination/")
# Iterate over destination files
for filename in glob.iglob("input/destination/*.stf"):
    language_code = filename[filename.index("_") + 1: filename.rfind("_")]
    if language_code in supported_language_codes:
        destination_files[language_code] = filename

# Iterate over supported language codes inside source zip file
for language_code in destination_files:

    result_file_keys = []
    result_file = open("output/result_" + language_code + "_delete_" + datetime_string + ".stf", "w", encoding='UTF8', newline='')

    # Build result stf file header
    result_file.write("Language code: " + language_code + "\n")
    result_file.write("Type: Bilingual\n")
    result_file.write("Translation type: Metadata\n")

    destination_file = open(destination_files[language_code], "r", encoding='UTF8')

    result_file.write("\n")
    result_file.write("------------------TRANSLATED-------------------\n")
    result_file.write("\n")
    result_file.write("# KEY	LABEL	TRANSLATION	OUT OF DATE\n")
    result_file.write("\n")

    # Iterate over dest file lines
    for line in destination_file:
        # Check if translated or untranslated line
        if translated_pattern.match(line) or untranslated_pattern.match(line):
            key = line.split("\t")[0]
            if key not in keys_to_ignore:
                if key not in result_file_keys:
                    result_file.write(key + "\t" + line.rstrip().split("\t")[1] + "\t<>\t-\n")
                    result_file_keys.append(key)
                else:
                    print("Duplicated key " + key)
            else:
                print("Ignored key " + key)

    result_file.write("\n")

    # Close destination file
    destination_file.close()

    # Close result file
    result_file.close()

# Move inside output folder
os.chdir("output/")
# Create zip file
zf = zipfile.ZipFile("result_delete_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".zip", "w")
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