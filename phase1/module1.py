import sys
sys.path.append("..")
from phase0.FA_class import DFA, State
from visualization import visualizer
from utils import utils
from utils.utils import imageType


def solve(image: imageType) -> 'DFA':
    dfa = DFA()
    dfa.alphabet = ['0','1','2','3']
    q0 = dfa.add_state()
    dfa.assign_initial_state(q0)
    top_down = [0,len(image[0])-1]
    left_right = [0,len(image[0])-1]
    Divide(q0,image,top_down,left_right,dfa)
    return dfa

def Divide(q4 : State,image : imageType, top_down : list[int] , left_right : list[int],dfa : DFA):
    if top_down[0]==top_down[1]:
        if image[top_down[0]][left_right[0]]==1:
            dfa.add_final_state(q4)
        return
    mid_top_down = (int)((top_down[0]+top_down[1])/2)
    mid_left_right = (int)((left_right[0]+left_right[1])/2)
    q0 = dfa.add_state()
    dfa.add_transition(q4,q0,'0')
    Divide(q0,image,[top_down[0],mid_top_down],[left_right[0],mid_left_right],dfa)
    q1 = dfa.add_state()
    dfa.add_transition(q4,q1,'1')
    Divide(q1,image,[top_down[0],mid_top_down],[mid_left_right+1,left_right[1]],dfa)
    q2 = dfa.add_state()
    dfa.add_transition(q4,q2,'2')
    Divide(q2,image,[mid_top_down+1,top_down[1]],[left_right[0],mid_left_right],dfa)
    q3 = dfa.add_state()
    dfa.add_transition(q4,q3,'3')
    Divide(q3,image,[mid_top_down+1,top_down[1]],[mid_left_right+1,left_right[1]],dfa)




if __name__ == "__main__":
    image = [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]


    utils.save_image(image)
    fa = solve(image)
    print(fa.serialize_json())
