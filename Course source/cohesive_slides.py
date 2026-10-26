"""Lesson 1 navigation and transitions, using the selected quiet title layout."""
import re


def section(ident):
    n=int(ident.split('-')[1])
    return 'RECURSION' if n<=4 else 'STAIRCASE' if n<=13 else 'FROG' if n<=19 else 'FROG EXTENSION' if n==21 else 'REVIEW'


def transition(topic,stxt,tex,start,end,number):
    stairs=topic=='STAIRCASE'
    title='From one call to many routes' if stairs else 'From counting routes to choosing one'
    intro=('We can now follow a recursive call and see where it stops. Next, use calls to count the routes up a staircase.' if stairs else
           'Keep the same three approaches. This time, compare the costs of complete routes and find the cheapest way across the stones.')
    descriptions=(['Explore the possible last moves with recursive calls.', 'Save answers so repeated calls do not repeat the work.', 'Fill earlier answers first, then use them for later steps.'] if stairs else
                  ['Explore the possible last jumps with recursive calls.', 'Save the cheapest cost of reaching each stone.', 'Fill earlier costs first, then use them for later stones.'])
    s=start+'\n'+stxt(1.5,16.5,29,40,r'\heavy '+tex(title))+stxt(1.5,13,29,24,tex(intro))
    for i,(title,body,color) in enumerate(zip(['Explore','Remember','Build in order'],descriptions,['callink','waitink','returnink'])):
        x=1.5+10*i
        s+=stxt(x,9.4,8.5,25,r'\textbf{'+str(i+1)+'. '+title+'}',color)
        s+=stxt(x,7.8,8.5,21,tex(body))
        if i<2:s+=rf'\draw[-{{Stealth[length=3mm]}},quiet,line width=1pt] ({x+8.5},8.9)--({x+9.3},8.9);'+'\n'
    asset='staircase' if stairs else 'frog-stones'
    s+=rf'\node[anchor=south,inner sep=0] at (16,1.6) {{\includegraphics[width=18cm,height=3.6cm,keepaspectratio]{{assets/slides/{asset}.png}}}};'+'\n'
    s+=stxt(1.5,0.8,28,12,'Lesson 1 / '+topic+' / OUR NEXT QUESTION','quiet')+number()+end+'\n'
    return s


def apply(source,stxt,tex,start,end,number):
    def frame(match):
        value=match.group(0)
        # Only footer IDs define the current exercise; prose may refer to others.
        footer=re.search(r'Lesson 1 / (L1-\d{2}) / (QUESTION[^}]*|ANSWER[^}]*)',value)
        if footer:
            ident=footer.group(1)
            value=value.replace('Lesson 1 / '+ident+' /','Lesson 1 / '+section(ident)+' / '+ident+' /',1)
        if 'The function continues on the next slide.' in value:
            value=value.replace('at (1.5,0.7)', 'at (1.5,1.3)')
        value=value.replace('at (1.5,12.4)','at (1.5,13.0)')
        value=value.replace('at (16,13.6)', 'at (16,13.0)')
        # Advice remains secondary; reserve diagram colours for calls and results.
        lines=[]
        for line in value.splitlines(keepends=True):
            if 'Watch for:' in line or 'Think on your own first.' in line:
                line=line.replace('text=teal','text=quiet')
            if r'\node(idea)' in line and r'\fontsize{36}' in line:
                line=line.replace(r'\fontsize{36}{\dimexpr36pt*6/5\relax}',r'\fontsize{40}{\dimexpr40pt*6/5\relax}')
            lines.append(line)
        value=''.join(lines)
        if footer and footer.group(2).startswith('QUESTION') and footer.group(1) in ('L1-05','L1-14'):
            value=transition(section(footer.group(1)),stxt,tex,start,end,number)+value
        return value
    return re.sub(r'\\begin\{frame\}.*?\\end\{frame\}',frame,source,flags=re.S)
