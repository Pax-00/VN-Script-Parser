## Parsing CatSystem2 Scripts

1. CatSystem2 script files are '.cst'. These can usually be found in scene.int or possibly an update.int.
2. Extract the VN's cst files with [GARbro](https://github.com/morkt/GARbro) to the /source directory here.
3. Run convert.py, all files should appear as .txt in the decrypted folder. Put them in a folder named after the VN title. (ex: Grisaia_no_Kajitsu)
4. Run script_parser.py to parse all folders in decrypted, parsed files will appear in /formatted_JSON and /formatted_TXT.
5. Check if files need any extra cleanup, and add regex patterns to library/regex.py as needed.