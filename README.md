## Compare two json files from vifeco

Compare two feature counts from vifeco
```bash
python matcher.py --help

python matcher.py --file1=file1.json --file2=file_2.json
```

## Reconcile category ids between different vifeco db

### Arguments:
| name | desc | default value |
| --- | --- | --- |
| model | json file | ./model.json | 
| source |  path to folder containning files to reconcile | ./source |
| target | path to folder for saving the converted files | ./target | 

### Usage

help menu
```bash
python reconcile.py --help
```

Example: update the arguments accordingly with your environment
```bash
python reconcile.py --model=my_model_file.json source="C:\Users\David\Documents\folder target="C:\Users\David\vifeco\import"
```

### Database migration

```bash
python migrate_db.py --help

# db file target/vifecodb.mv.db
```
