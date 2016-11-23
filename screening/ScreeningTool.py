import sys
import codecs
import os
import os.path

from tkinter import *


data = ["Not about software engineering", 
    "No about API usability", 
    "Not a full paper contribution",
	"Screening tool problem", 
    "Other" ]   


def read(file):
    "Read the file"
    #o = codecs.open(file, 'r', "latin-1")
    o = codecs.open(file, 'r', "utf-8")
    return o.read()

def write(file, text, mode):
    #f = codecs.open(file, mode, "latin-1")
    f = codecs.open(file, mode, "utf-8")
    f.write(text)
    f.close()

# Initialisation
def parseDocTxtScopus(text):
	#Ajout Ed ---------------------------------
    #print("parseDocTxtScopus()")
    #Csv :
    #0Authors,    #1Title,    #2Year,    #3Source title,    #4Volume,
    #5Issue,    #6Art. No.,    #7Page start,    #8Page end,    #9Page count,
    #10Cited by,    #11Link,    #12Affiliations,    #13Authors with affiliations,
    #14Abstract,    #Author Keywords,    #Document Type,    #Source,    #EID
    #-----------
    
    #0 Authors
    #1 Title
    #2 (year) Conf
    #3 Lien scopus
    #4 Affiliations
    #5 Abstract
    #6 Keywords
    #7 doc type
    #8 Source
    "Separate the texts entries in txt from Scopus"
    t = text.split("\n")
    
    if len(t) <= 10:
        print("Only",len(t)," entrie(s) found.\n -> Check file '"+sys.argv[2]+"' for typos.\n\n !! Execution aborded !!")
        exit()
    print("  Entries found :",len(t))
    return t[0:-1]
    
#Fin ----------------------------Ajout Ed -


def parseDocScirus(text):
    "Separate the texts entries in ris"
    #print("In parse doc scirus")
    r = [i for k in str.split("JOUR") for j in k.split("CONF") for i in j.split("UNPB")]
    return r[1:]

def parseDocIEEE(text):
    "Separate the texts entries in csv"
    t = text.split(";")
    return t[2:-1]

def parseDoc(text, source):
    #print("parseDoc(",source,")")
    format = { "IEEE" : parseDocIEEE,
               "Scirus" : parseDocScirus,
               "TxtScopus" : parseDocTxtScopus}#Ajout Ed
    return format[source](text)


def parseIEEE(text):
    "Extract info from IEEE sources"
    t = text.split('"')
    titre = t[1]
    auteurs = t[3]
    abst = t[21]
    return auteurs+" $ "+titre+" $ "+abst+"\n"

#Ajout Ed ---------------------------------
def parseTxtScopus(text):
    "Extract info from Scopus Txt sources"
    t = text.split(';')
    titre = t[1]
    auteurs = t[0]
    abst = t[2]
    #print("parseTxtScopus(",auteurs," $ ",titre," $ ",abst,")")
    return auteurs+" $ "+titre+" $ "+abst+"\n"
#Fin ----------------------------Ajout Ed -

def parseScirus(text):
    "Extract info from Scirus sources"
    t = text.split("\n")
    titre = t[2]
    auteurs = t[1]
    try:
        abst = t[9]
    except:
        return ""
    return auteurs+" $ "+titre+" $ "+abst+"\n"

def parseEntry(text, source):
    "Return a single entry from the file"
    format = { "IEEE" : parseIEEE,
               "Scirus" : parseScirus,
               "TxtScopus" : parseTxtScopus}#Ajout Ed
    return format[source](text)

def writeEntry(text, user):
    "Add the results to Screening.data in latin-1" 
    write(user+".todo", text, "a")

def getUsers():
    users = []
    for k in dico.keys():
        if k != "init" and k != "final":
            users.append(k)
    return users

def outputNormalized(tab):
    "Create a todo file for each users"

    print("  Writing 'todo' file.")
    users = getUsers()
    for x in range(len(tab)):
        s = x % len(users)
        writeEntry(tab[x], users[s])
        writeEntry(tab[x], users[s-1])
    print("    Files ", users, ".todo written.")
    
def getEntries(file, source):
    f = read(file)
    doc = parseDoc(f,source)
    t = []
    for x in doc:
        t.append(parseEntry(x,source))
    return t

def merge(x,y):
    "Merge two arrays and remove duplicate"
    return list(set(x+y))

def screen(x,y):
    "Remove all items from y that are in x"
    return list(set(x+y) ^ set(x))

def initialize(u):
    "Setup the document file etc"
    file = sys.argv[2]        # the name of the file containing the data

#Modif Ed --------------------------------------
    
    print("Initialization (\""+file+"\")...")
    
    t = getEntries(file, "TxtScopus")
    outputNormalized(t)
    print("Done.")
    #t = getEntries(file, "IEEE")
    #try:
    #    file = sys.argv[3]
    #except:
    #    outputNormalized(t)
    #else:
    #    t2 = getEntries(file, "Scirus")
    #    t2 = screen(t,t2)
    #    print(len(t2))
    #    outputNormalized(t2)
#Fin -------------------------------- Modif Ed -

# Run
# Methods to parse normalized data

def readDoc(text):
    "Separate the texts entries in csv"
    t = text.split("\n")
    return t[:-1]

def readEntry(text):
    t = text.split('$')
    return t[2], t[1], t[0]

def output(r, user):
    "Add the results to Screening.data in latin-1"
    write(user+".out", r+"\n", "a")

# Methods to run
class Namespace(): pass

def display(abst, name, title):
    "Display the abstract and checklist"
    root = Tk()

    ns = Namespace()
    ns.saveStateFlag = False
    def saveState():
        ns.saveStateFlag = True
        root.quit()

    frame = Frame(root)
    frame.pack(fill = BOTH, expand = 1)

    cadre = Frame(frame)
    cadre.pack(side = TOP, fill = X)

    auteurs = Label(cadre, text=name)
    auteurs.pack(side = BOTTOM)
    title = Label(cadre, text=title)
    title.pack(side = TOP)
    
    text = Text(frame)
    text.insert(END, abst)
    scrollbar = Scrollbar(frame, command = text.yview)
    text.config(yscrollcommand = scrollbar.set)
    text.pack(side = LEFT, fill = BOTH, expand = 1)
    scrollbar.pack(side= LEFT, fill = Y)
    
    checks = Listbox(frame)
    for x in data:
        checks.insert(END, x)
    checks.pack(side = RIGHT)

    save = Button(frame, text = "Save and quit", command = saveState)
    save.pack(side = BOTTOM)
    button = Button(frame, text = "Save and continue", command = root.quit)
    button.pack(side = BOTTOM)
    
    root.bind_all("<Return>",  lambda x:root.quit())
    root.bind_all("<space>",  lambda x:root.quit())
    
    root.mainloop()
    try:
        critere = checks.curselection()
    except:
	    return "()", saveState
		
    root.destroy()
    return critere, ns.saveStateFlag

def run(user):
    "Run the code on every instances"  
    if not os.path.exists(user+".todo")	:
        print(" !! Requested file not found : '"+user+".todo' !!")
        exit()
    print("Screening...")
    f = read(user+".todo")

    doc = readDoc(f)
    txt = ""
    save = False
    for x in doc:
        if not save:
            a,n,t = readEntry(x)
            ex, save = display(a,n,t)

            r = n+" $ "+t+" $ "+user+" $ "+str(ex)
            ss = str(ex)
            if ss == "()":
                ss = "Accepted."
            else:
                ss = "Rejected ! "
            print(" - "+n+" : "+ss)
            output(r, user)
        else:
            txt= txt+x+"\n"
    os.remove(user+".todo")
    write(user+".todo", txt,"w")

# Finalization methods

def parseOut(text):
    "Return data from .out file"
    s = text.split("$")
    return s[-1].strip()

def parseID(text):
    "Return document's descriptor"
    s = text.split("$")
    return s[0].strip()+" "+s[1].strip()

def rater(ID):
    "Return the rater of an ID"
    s = ID.split("$")
    return s[-2].strip()
    
def calculateKappa(a, t, x, y):
    "Calulate Cohen Kappa on data"
    print(a,t,x,y)
    pa = (t-a)/t
    px = x/t
    py = y/t
    pe = px*py + (1.-px)*(1.-py)
    k = (pa - pe)/(1. - pe)
    
    return k

def readHandFed():
    f = read("handFed.pairs")
    f = f.replace("\n\n", "\n")
    t = f.split("\n")
    return [(i,j) for i,j in zip(t[0::2], t[1::2])]

def generatePairs(docs):
    "Return a set of pairs"
    i = 0
    groups = []
    # Instrumentation
    #a = 0
    #r = 0
    #n = 0

    while i < len(docs)-1 :
        first = docs[i]
        second = docs[i+1]
        
        if (parseID(first) == parseID(second)) and (rater(first) != rater(second)):
            groups += [(first, second)]
            i = i+1
             #a += 1
     #       print("accepted")
       # else:
        #    try:
        #        write("dif.pairs", first, "a")
        #        write("dif.pairs", second+"\n\n", "a")
        #    except:
        #        print("error")
        #        pass
        #    if rater(first) == rater(second):
        #        r += 1
        #    elif parseID(first) != parseID(second):
        #        n += 1
        i = i+1
     #   print("\n")
    #print("accepted: "+str(a)+" rejected: rater -> "+str(r)+" id -> "+str(n))
    try:
        other = readHandFed()
    except:
        other = []
    #for i,j in groups+other:
    #    try:
    #        print(i+"\n"+j+"\n\n")
    #    except:
    #        print("error")
    
    return groups+other
    

def accept(text):
    "Record data as accepted"
    write("accepted.dsv", text+"\n", "a")
    
def reject(text):
    "Record data as rejected"
    write("rejected.dsv", text+"\n", "a")

def ambiguous(t1, t2):
    "Record as disputed, stock both criteria"
    write("ambiguous.dsv", t1+"\n"+t2+"\n\n", "a")

	
def finalize(u):
    "Setup the result file etc"
    #load the result file for all users
    users = getUsers()
    docs = []
    
    if os.path.exists("results.txt")	:
        os.remove("results.txt")
    write("results.txt", "Results\n-------\n", "w")

    for x in users:
        try:
            f = read(x+".out")
            docs += readDoc(f)
        except:
            print(x+".out missing")
            pass
        print(x, len(docs))

    docs.sort()

    ambCount = 0.
    accCountA = 0.
    accCountB = 0.

    # Generate set of pairs
    pairs = generatePairs(docs)
    print(len(pairs))
    ss = "Pairs : "+str(len(pairs))+"\n"
    write("results.txt", ss, "a")
    
    # Iterate over all identical pairs and generate output structure
    for i,j in pairs:
        w = parseOut(i)
        z = parseOut(j)
        if w == "()": accCountA+=1
        if z == "()": accCountB+=1
        if w == z:
            if w == "()":
                accept(i)
            else:
                reject(i)
        else:
            ambiguous(i,j)
            ambCount += 1
                
    print(calculateKappa(ambCount, len(pairs), accCountA, accCountB))
    write("results.txt", "\nKappa:"+str(calculateKappa(ambCount, len(pairs), accCountA, accCountB))+"\n", "a")
    print("Results written in result.txt")
	

def checkUser(u):
    dico[u](u)


# Users dictionnary
dico = { "reviewer1": run,
      "reviewer2": run,
      "reviewer3": run,
      "reviewer4": run,
      "init": initialize,
      "final": finalize }

	  

print("ScreeningTool starts.")
if len(sys.argv) < 2:
    print(" Wrong arguments, expected:")
    print("  > init <file_name.csv>")
    print("  > <reviewer>    (in ",getUsers(),")")
    print("  > final")  
    exit()

if len(sys.argv) == 2 :
    if sys.argv[1] == "final":
        for x in getUsers():
            try:
                f = read(x+".out")
                docs = readDoc(f)
            except:
                print(x+".out missing")
                exit()
    elif sys.argv[1] not in getUsers():
        print(" Wrong arguments, expected:")
        print("  > init <file_name.csv>")
        print("  > <reviewer>    (in ",getUsers(),")")
        print("  > final")  
        exit()
	
	
	#and if not os.path.exists("")	:
     #   print(" !! Requested file not found : '"+user+".todo' !!")
        


u = sys.argv[1]               # the user's name

checkUser(u)
