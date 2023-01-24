## VNDB API

Prelimary support for querying character data from vndb.
Requires the vndb id, which can be seen in the VN's page url on vndb.
Ex: https://vndb.org/v5154 -> vn_id = v5154

To use:
import vndb_api

get_character_data(vn_id) - Creates a json file with formatted character data.
get_character_names(vn_id) - Returns a list of main and side characters names (will be as senn on the VNDB page)