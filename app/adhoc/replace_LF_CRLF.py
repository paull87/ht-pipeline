
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'

file_path = r"\\property.local\shared\HOMETRACK_ROOT\Techdev\Raw Data\020_NHBCNewBuildDataset\data\201911\Projects.csv"
new_file_path = r"\\property.local\shared\HOMETRACK_ROOT\Techdev\Raw Data\020_NHBCNewBuildDataset\data\201911\Projects_copy.csv"


def replace_lf_with_crlf():
    # Open file and grab content
    with open(file_path, 'rb') as open_file:
        content = open_file.read()

    # Replace LF with the CRLF that we expect.
    content = content.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)

    # Re-save the amended file
    with open(file_path, 'wb') as open_file:
        open_file.write(content)


def strip_trailing_commas():
    with open(file_path, 'r') as existing_file:
        with open(new_file_path, 'w') as new_file:
            for line in existing_file.readlines():
                print(line)
                updated_line = line.rstrip('\n').rstrip(',').rstrip('"')
                print(updated_line)
                new_file.write(f"{updated_line}\n")


if __name__ == '__main__':
    #strip_trailing_commas()

    # with open(file_path, 'r') as existing_file:
    #     for line in existing_file.readlines():
    #         if len(line.split('|')[-1]) > 2:
    #             print(repr(line))

    with open(r"S:\HOMETRACK_ROOT\Techdev\Raw Data\251_SantanderViaLGSurvey\data\2019-12_LGSantander.csv",
              'r') as file:
        lines = file.readlines()
        print(lines[0])
        print(lines[0].replace('ï»¿', ''))

    # with open(r"S:\HOMETRACK_ROOT\Techdev\Raw Data\202_RoyalBankOfScotlandViaLGSurvey\data\2019-12_LGRBOS.csv", 'r') as file:
    #     with open(r"S:\HOMETRACK_ROOT\Techdev\Raw Data\202_RoyalBankOfScotlandViaLGSurvey\data\2019-12_LGRBOS_copy.csv", 'w') as new_file:
    #         lines = file.readlines()
    #         lines[0] = lines[0].replace('ï»¿', '')
    #         new_file.writelines(lines)
