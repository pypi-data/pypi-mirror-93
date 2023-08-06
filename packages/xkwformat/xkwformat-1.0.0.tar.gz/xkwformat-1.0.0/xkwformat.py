def print_list(movies,indent = False , level = 0 , fh = sys.stdout): 
        for each in movies:
                if isinstance(each,list):
                        print_list(each,indent,level+1,fh)
                else:
                        if indent:
                                for i in range(lever):
                                        print("\t",end = "",file = fh)
                        print(each,file = fh)
