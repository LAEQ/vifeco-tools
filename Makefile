matcher_1:
	python matcher.py --file1=model_fixed.json --file2=source/file_1.json
matcher_2:
	python matcher.py --file1=model_fixed.json --file2=source/file_2.json
reconcile:
	python reconcile.py
reconcile_fixed:
	python reconcile.py --model=model_fixed.json