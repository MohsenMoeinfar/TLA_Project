import sys
sys.path.append("..")
from phase0.FA_class import DFA
from utils.utils import imageType
from phase2 import module2


def solve(json_fa_list: list[str], images: list[imageType]) -> list[int]:
    ans = []
    adder = 0
    ismost = 0
    for json_fa in json_fa_list:
        adder+=1
        go = 0
        for image in images:
            go+=1
            module2.solve(json_fa,image)
            if module2.useThis.cnt>=ismost :
                ismost=module2.useThis.cnt
                if len(ans)==adder:
                    ans[adder-1]=go-1
                else:
                    ans.append(go-1)
    return ans



if __name__ == "__main__":
    ...
