import os

from util.status import *

def check_qe(filname):
    if not os.path.isfile(filname): return "ERROR"
    with open(filname) as fil:
        text    =   fil.read()
    if "JOB DONE" in text:  return "SUCCESS"
    else:                   return "ERROR"

def check_bgw(filname):
    if not os.path.isfile(filname): return "ERROR"
    with open(filname) as fil:
        text    =   fil.read()
    if "Job Done" in text or "TOTAL:" in text:  return "SUCCESS"
    else:                   return "ERROR"
direcs  =   []

for sw in ["QE", "BGW"]:
    for direc in list(os.walk(f"../{sw}"))[0][1]:
        direcs.append(direc)
direcs  =   sorted(direcs)

begin_status()
for direc in direcs:
    print(direc)
    if direc[:2] == "01":
        edit_status(direc, check_qe(f"../QE/{direc}/scf.out"))
    if direc[:2] in ["02", "03", "04"]:
        edit_status(direc, check_qe(f"../QE/{direc}/pw2bgw.out"))
    if direc[:2] == "07":
        edit_status(direc, check_bgw(f"../BGW/{direc}/epsilon.out"))
    if direc[:2] == "08":
        edit_status(direc, check_bgw(f"../BGW/{direc}/sigma.out"))
    if direc[:2] == "09":
        edit_status(direc, check_bgw(f"../BGW/{direc}/kernel.out"))
    if direc[:2] == "10":
        edit_status(direc, check_bgw(f"../BGW/{direc}/absorption.out"))



