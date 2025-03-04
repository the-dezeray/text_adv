import yaml
import pytest

def _load_yaml_file(file_path):
    with open(file_path,"r") as f :
        data = yaml.safe_load(f)
        return data
def _get_next_nodes(story):
    story = _load_yaml_file("data/story.yaml")
    ary  = []
    for _chapter in story.items():
        for i in _chapter[1]["choices"]:
            print(i["next_node"])
            ary.append(i["next_node"])
    return ary
def _get_from_all_choices(key:str = ""):
    story = _load_yaml_file("data/story.yaml")
    ary  : list[str] = []
    for _chapter in story.items():
        for i in _chapter[1]["choices"]:
            _dict : dict =  i
            value = _dict.get(key,None)
            if value:
                ary.append(value)
    return ary

"""@pytest.mark.parametrize("func_call", _get_from_all_choices("function"))
def test_function_execution(func_call):
    try:
        eval(func_call)  # Execute function call
    except Exception as e:
        pytest.fail(f"Function execution failed: {func_call} - Error: {e}")"""
                    
def test_all_next_node_exist():

    story = _load_yaml_file("data/story.yaml")
   
    nodes = _get_next_nodes(story)
    for node in nodes:
        assert node in story

