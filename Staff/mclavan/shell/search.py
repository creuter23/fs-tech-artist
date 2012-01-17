
# Locates all the .py files created in the last 24hrs.
mclavan:RBA mclavan$ find ./students/Technical_Arts_Group/ -name *.py -mtime 0

# grep search 
mclavan:RBA mclavan$ grep -i rba -R ./students/Technical_Arts_Group/

# Opens all files it finds.
mclavan:RBA mclavan$ find ./students/Technical_Arts_Group/ -name *.py -mtime 0 -exec open {} \;

