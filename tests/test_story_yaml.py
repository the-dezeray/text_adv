from util.file_handler import load_yaml_file
def _get_next_nodes(story):
    story = load_yaml_file("data/story.yaml")
    ary  = []
    for _chapter in story.items():
        for i in _chapter[1]["choices"]:
            print(i["next_node"])
            ary.append(i["next_node"])
    return ary
def test_all_next_node_exist():


    story = load_yaml_file("data/story.yaml")
   
    nodes = _get_next_nodes(story)
    for node in nodes:
        assert node in story
    