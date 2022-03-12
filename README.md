# Aqua Exercise

### YamlEditor

```python
from src.yml_editor import YamlEditor
editor = YamlEditor(r"/path/to/file")
extra_config = {
    'metadata': {
        'spec': {
            'version': 'v3'
        }
    }
}
editor.add_config(extra_config)
editor.save(r"/path/to/saved/file")
# or to save to the exact file you edit
editor.save()
```
### Before
```yaml
apiVersion: machinelearning
kind: SeldonDeployment
metadata:
  labels:
    app: seldon
    version: v1.1
  name: seldon-deployment-{{workflow.name}}
  namespace: kubeflow
spec:
  annotations:
    deployment_version: v1
    project_name: NLP Pipeline
  name: seldon-deployment-{{workflow.name}}
```

### After
```yaml
apiVersion: machinelearning
kind: SeldonDeployment
metadata:
  labels:
    app: seldon
    version: v1.1
  name: seldon-deployment-{{workflow.name}}
  namespace: kubeflow
  spec:
    version: v3
spec:
  annotations:
    deployment_version: v1
    project_name: NLP Pipeline
  name: seldon-deployment-{{workflow.name}}

```

### Requirements Extractor

```python
from src.requirements_extractor import extract_requirements
main_file = r'/path/to/requirement/file'
dependencies_str = extract_requirements(main_file)
# returns
# PyYAML==6.0,detectron2,elasticsearch==7.9.1,docopt==0.6.1
```