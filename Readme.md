# Translation Workbench Tool

## Usage instructions

1. Open build_stf.py and edit line #9 in order to to configure the list of supported languages for which translations should be imported in the destination org.

    > supported_language_codes = ["fr", "es_MX", "ja", "ko", "pt_BR"]
 
2. Export bilingual .zip file containing translation files in .stf format from both source and destination org.
3. Place bilingual.zip file exported from source org inside _"input/source/"_ folder.
4. Place bilingual.zip file exported from destination org inside _"input/destination/"_ folder.
5. Execute python script and look for processed files inside _"output/"_ folder.

## Folders structure

Following is summarized the folder structure expected by the script.

> * _input_
>   * _destination_ (contains bilingual zip file exported from source org)
>   * _source_ (contains bilingual zip file exported from source org)
> * _output_ (where result files are written)