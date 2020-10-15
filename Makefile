matcher:
	python matcher.py --file1=model_fixed.json --file2=source/ID1_PA_2019-09-03_TRAJET01.mp4-1602098291846.json
reconcile:
	python reconcile.py
reconcile_fixed:
	python reconcile.py --model=model_fixed.json