import pandas

if __name__ == '__main__':
	df = pandas.read_csv('AC_CombinedFile.csv', header=0, sep=',', encoding='utf-8')
	hist= df.groupby('Booth_No')['EPIC'].nunique()
	print(df.groupby('Gender')['EPIC'].nunique())
	print(df.groupby('Age')['EPIC'].nunique())
	hist.to_csv('booth_hist333.csv', index=True)

