import sys, json

if __name__ == '__main__':
    j = None

    def recurse_c(branch):
        if type(branch) is dict:
            if len(branch)==1 and branch.get('file') is True:
                return None        

            keys = branch.keys()
            for k in keys:            
                branch[k] = recurse_c(branch[k])
            if 'file' in branch:
                del branch['file']

            # all nulls? convert to list
            keys = branch.keys()
            all_none = True
            for k in keys:
                if branch[k] != None:
                    all_none = False
            if all_none:
                return keys

        return branch


    with open(sys.argv[1], 'r') as f:
        j = json.load(f)
        j = recurse_c(j)

    json.dump(j, open(sys.argv[1] + '-pruned', 'w'), indent=4)