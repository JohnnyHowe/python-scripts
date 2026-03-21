import re


BLANK_COLUMN = ""
SPACING = 1

_ansi_re = re.compile(r'\x1b\[[0-9;]*m')


def print_table(headers: list[str], rows: list[list[str]]):
	print(_get_table(headers, rows))


def _get_table(headers: list[str], rows: list[list[str]]):
	# ensure valid
	n_columns = len(headers)
	cleaned_rows = []

	# ensure rows have same number of values
	for row_n, row in enumerate(rows):

		if len(row) > n_columns:
			print(f"Skipping row {row_n}. It has too many items!")
			continue

		cleaned_row = list(row)
		while len(cleaned_row) < n_columns:
			cleaned_row.append(BLANK_COLUMN)
		cleaned_rows.append(cleaned_row)

	column_widths = _get_column_widths([headers] + rows) 

	header_separator_row = ["-" * width for width in column_widths]
	all_rows = [headers, header_separator_row] + cleaned_rows

	lines = []
	for row in all_rows:
		lines.append(_draw_row(row, column_widths))

	return "\n".join(lines)


def _get_column_widths(all_rows: list[list[str]]) -> list[int]:
	column_widths = [0] * len(all_rows[0])
	for row in all_rows:
		for column_n in range(len(row)):
			column_widths[column_n] = max(column_widths[column_n], _visible_len(row[column_n]))
	return column_widths


def _visible_len(s: str) -> int:
	return len(_ansi_re.sub('', s))


def _draw_row(row: list[str], column_widths: list[int]) -> str:
	if len(row) != len(column_widths):
		raise Exception("row length and colum_widths length differ!")

	items = []
	for i in range(len(row)):
		item: str = row[i]
		target_width = column_widths[i]
		padded = pad_ansi(item, target_width)
		items.append(padded)

	spacer = " " * SPACING

	inner = f"{spacer}|{spacer}".join(items)
	return f"|{spacer}{inner}{spacer}|"


def pad_ansi(s: str, width: int) -> str:
    return s + ' ' * max(0, width - _visible_len(s))
