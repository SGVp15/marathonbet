import openpyxl

from config import excel_file
from match import Match


def add_to_excel_file(matchs: [Match]):
    workbook = openpyxl.load_workbook(excel_file)
    worksheet = workbook.active

    row = worksheet.max_row
    # Create a list of values to write to the Excel file
    for m in matchs:
        row += 1
        # m.country
        # m.championship
        # m.command_first_name
        # m.command_second_name
        # m.value_1_col
        # m.value_2_col
        # m.match_total_first_team_1p5_value
        # m.match_total_second_team_1p5_value
        # m.goals_dict
        for val in (
                m.value_1_col,
                m.value_2_col,
                m.match_total_first_team_1p5_value,
                m.match_total_second_team_1p5_value
        ):
            # ID	League	Нome Team	Guest Team	Koef	Type	Date	SorareFilter
            values_to_write = [
                '',
                f'{m.country} {m.championship}',
                m.command_first_name,
                m.command_second_name,
                val,
                # _type,
                # _date
            ]
            # Write the numbers to the worksheet
            for i, v in enumerate(values_to_write):
                worksheet.cell(row=row + 1, column=i + 1, value=str(v))

    # Save the workbook to a file
    workbook.save(excel_file)
