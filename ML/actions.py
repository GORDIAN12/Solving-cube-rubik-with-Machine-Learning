ACTIONS = ['U',"U'",'D',"D'",'L',"L'",'R',"R'",'F',"F'",'B',"B'"]
ACTION_TO_IDX = {a:i for i,a in enumerate(ACTIONS)}
IDX_TO_ACTION = {i:a for a,i in ACTION_TO_IDX.items()}

INV = {'U':"U'", "U'":'U',
       'D':"D'", "D'":'D',
       'L':"L'", "L'":'L',
       'R':"R'", "R'":'R',
       'F':"F'", "F'":'F',
       'B':"B'", "B'":'B'}
