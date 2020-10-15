matcher_1:
	python matcher.py --file1=model_fixed.json --file2=source/file_1.json
matcher_2:
	python matcher.py --file1=model_fixed.json --file2=source/file_2.json
matcher_3:
	python matcher.py --file1=model_fixed.json --file2=source/file_3.json
matcher_4:
	python matcher.py --file1=model_fixed.json --file2=source/file_4.json
matcher_5:
	python matcher.py --file1=model_fixed.json --file2=source/file_5.json
matcher_test:
	python matcher.py --file1=tests/test_model.json --file2=tests/test_file.json
reconcile:
	python reconcile.py
reconcile_fixed:
	python reconcile.py --model=model_fixed.json