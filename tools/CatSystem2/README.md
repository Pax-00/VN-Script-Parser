## Parsing CatSystem2 Scripts

1. CatSystem2 script files are '.cst'. These can usually be found in scene.int or possibly an update.int.
2. Extract the VN's cst files with [GARbro](https://github.com/morkt/GARbro) to the /source directory here (create if not present).
3. May need to look through the extracted .cst files and remove any that aren't game dialogue. (ie. tests, tl notes, consider files < 1kb)
4. Run python convert.py, all files should appear as .txt in the /raw folder. Put them in a folder named after the VN title. (ex: Grisaia_no_Kajitsu)
5. Run python script_parser.py to parse all folders in /raw, parsed files will appear in /formatted_JSON and /formatted_TXT. Full scripts will have "[Script]" in filename.
6. Check if files need any extra cleanup, and add regex patterns to library/regex.py for the specific VN as needed.