import sys
sys.path.append("..")
from phase0.FA_class import DFA, State
from utils import utils
from utils.utils import imageType


class ReturnBool:
    def __init__(self,b : bool) -> None:
        self.mybool=b

class Counter:
    def __init__(self) -> None:
        self.cnt=0
        

useThis = Counter()

def solve(json_str: str, image: imageType) -> bool:
    fa = DFA.deserialize_json(json_str)
    q0 = fa.init_state
    left_right = [0,len(image[0])-1]
    top_down   = [0,len(image[0])-1]
    notSolved  = ReturnBool(False)
    different   = Counter()
    same = Counter()
    Divide_Check(q0,image,left_right,top_down,fa,notSolved,different,same)
    useThis.cnt=100*(same.cnt/(different.cnt+same.cnt))
    print("{:.2f}".format(useThis.cnt))
    return not notSolved.mybool


def Divide_Check(q4 : State,image : list[list['int']],left_right : list['int'],top_down : list['int'],fa : DFA,notSolved : ReturnBool,different : Counter,same : Counter):
    if left_right[0]==left_right[1]:
        if (not fa.is_final(q4)) & image[top_down[0]][left_right[0]]==1:
            notSolved.mybool=True
        if fa.is_final(q4)!=image[top_down[0]][left_right[0]]:
            different.cnt+=1
        if image[top_down[0]][left_right[0]]==fa.is_final(q4):
            same.cnt+=1
        return
    mid_left_right = (int)((left_right[0]+left_right[1])/2)
    mid_top_down   = (int)((top_down[0]+top_down[1])/2)
    q0 = q4.transitions['0']
    Divide_Check(q0,image,[left_right[0],mid_left_right],[top_down[0],mid_top_down],fa,notSolved,different,same)
    q1 = q4.transitions['1']
    Divide_Check(q1,image,[mid_left_right+1,left_right[1]],[top_down[0],mid_top_down],fa,notSolved,different,same)
    q2 = q4.transitions['2']
    Divide_Check(q2,image,[left_right[0],mid_left_right],[mid_top_down+1,top_down[1]],fa,notSolved,different,same)
    q3 = q4.transitions['3']
    Divide_Check(q3,image,[mid_left_right+1,left_right[1]],[mid_top_down+1,top_down[1]],fa,notSolved,different,same)

        


if __name__ == "__main__":
    print(
        solve(
            '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
            '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
            '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
            '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
            '"3": "q_4"}}',
            [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]
        )
    )
