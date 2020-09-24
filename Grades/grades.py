import colours as c

SGE = ["Algebra liniowa", 4, 5, "Analiza matematyczna", 5, 7, "Eksploracja danych", 4.5, 2, "Fizyka 1", 5, 6,
       "Projektowanie konstrukcji z rysunkiem technicznym", 5, 3, "Wprowadzenie do automatyki i robotyki", 5, 3,
       "Wstęp do informatyki", 5, 3, "Elektronika cyfrowa", 4.5, 4, "Fizyka 2", 5, 6,
       "Inżynieria procesów produkcyjnych", 4, 1,
       "Narzędzia pracy grupowej", 5, 2, "Programowanie strukturalne i obiektowe", 5, 4,
       "Prototypowanie konstrukcji w technice druku 3D i CNC", 4, 3, "Rachunek prawdopodobieństwa i statystyka", 4.5, 5,
       "Równania różniczkowe", 5, 3, "Teoria obwodów", 4.5, 3]

subjects = SGE[::3]
grades = SGE[1::3]
ECTS = SGE[2::3]
SGE_touple = zip(subjects, grades, ECTS)
nom = 0
denom = 0
SGE_touple = list(SGE_touple)
for _, grade, ECTS_point in SGE_touple:
    nom += grade * ECTS_point
    denom += ECTS_point
print(f"Srednia wazona = {nom / denom:.2f}")
SGE_touple = list(SGE_touple)
MV_ECTS = list(zip(subjects, ECTS))
MV_ECTS.sort(key=lambda tup: tup[1])
MV_ECTS.reverse()
SGE_touple.sort(key=lambda tup: tup[1] * tup[2])
SGE_touple.reverse()
for index, tup in enumerate(zip(SGE_touple, MV_ECTS)):
    elem1, elem2 = tup
    sub1, grade, _ = elem1
    sub2, ect2 = elem2
    mess = f"{index + 1}. " \
          f"{c.green(sub1) if sub1 == sub2 else c.red(sub1)} - " \
          f"{c.green(sub2) if sub1 == sub2 else c.red(sub2)} "
    print(mess)
FG = [elem for elem in SGE_touple if elem[1] == 5]
FHG = [elem for elem in SGE_touple if elem[1] == 4.5]
FFG = [elem for elem in SGE_touple if elem[1] == 4]
print(f"5kowe : {len(FG)}")
print(f"4.5kowe : {len(FHG)}")
print(f"4kowe : {len(FFG)}")
