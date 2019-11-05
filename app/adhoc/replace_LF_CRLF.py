
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'

file_path = r"\\property.local\shared\HOMETRACK_ROOT\Techdev\Raw Data\020_NHBCNewBuildDataset\data\201911\Polygon_WKT.csv"

# Open file and grab content
with open(file_path, 'rb') as open_file:
    content = open_file.read()

# Replace LF with the CRLF that we expect.
content = content.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)

# Re-save the amended file
with open(file_path, 'wb') as open_file:
    open_file.write(content)
