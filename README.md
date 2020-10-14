# Tool to reconcile category ids between different vifeco db

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

