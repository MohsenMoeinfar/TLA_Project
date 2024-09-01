import sys
sys.path.append("..")
from math import log2
from phase0.FA_class import DFA, State
from utils.utils import imageType


class Obj:
    def __init__(self) -> None:
        self.image = []

def solve(json_str: str, resolution: int) -> imageType:
    fa = DFA.deserialize_json(json_str)
    myobj = Obj()
    for i in range(resolution):
        myobj.image.append([])
        for j in range(resolution):
            myobj.image[-1].append(0)
    start = fa.init_state
    left_right = [0,resolution-1]
    top_down   = [0,resolution-1]
    Divide(start,fa,left_right,top_down,myobj)
    return myobj.image


def Divide(start: State,fa: DFA, left_right: list['int'], top_down: list['int'],obj : Obj):
    if (left_right[0]==left_right[1]):
        if fa.is_final(start):
            obj.image[top_down[0]][left_right[0]]=1
        return
    mid_top_down = (int)((top_down[0]+top_down[1])/2)
    mid_left_right = (int)((left_right[0]+left_right[1])/2)
    q0 = start.transitions['0']
    Divide(q0,fa,[left_right[0],mid_left_right],[top_down[0],mid_top_down],obj)
    q1 = start.transitions['1']
    Divide(q1,fa,[mid_left_right+1,left_right[1]],[top_down[0],mid_top_down],obj)
    q2 = start.transitions['2']
    Divide(q2,fa,[left_right[0],mid_left_right],[mid_top_down+1,top_down[1]],obj)
    q3 = start.transitions['3']
    Divide(q3,fa,[mid_left_right+1,left_right[1]],[mid_top_down+1,top_down[1]],obj)



if __name__ == "__main__":
    pic_arr = solve(
        '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
        '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
        '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
        '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
        '"3": "q_4"}}',
        4
    )
    print(pic_arr)
