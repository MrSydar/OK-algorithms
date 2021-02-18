# Alternatywne sformułowanie programowania dynamicznego dla problemu plecakowego

def plecak_tabelka_alt():
  P = 30 # max wartość plecaka (jak nieznana to wpisz np. 9999)
  b = 14 # max pojemność plecaka (tu tak samo jw. jak nieznane to 9999)
 
  # wartości
  w = [3, 4, 2, 6, 1]
 
  # wagi/rozmiary
  s = [5, 3, 2, 4, 3]
 
  n = len(w) # liczba przedmiotów 
 
  # niżej nic nie trzeba zmieniać
 
  # wypelnianie zerami i nieskonczonosciami
  tab = [[0]*(P+1) for _ in range(n+1)]
 
  for j in range(1, P+1):
    tab[0][j] = float('inf')
 
  # wypelnianie tabelki
  for i in range(1, n+1):
    for j in range(1, P+1):
      if w[i-1] > j:
        tab[i][j] = tab[i-1][j]
      else:
        tab[i][j] = min(tab[i-1][j-w[i-1]]+s[i-1], tab[i-1][j])
 
  # znajdowanie wyniku
  max_i = None
  max_j = None
  for j in range(P, -1, -1):
    for i in range(n, -1, -1):
      if tab[i][j] <= b:
        max_i = i
        max_j = j
        break
    if max_i != None: break
  max_s = tab[max_i][max_j]
 
  # print
  print(" j", " ".join([str(i).rjust(3) for i in range(0, P+1)]))
  print("i")
  for i in range(0, n+1):
    print(f"{i} ", " ".join([str(tab[i][j]).rjust(3) for j in range(0, P+1)]))
 
  print("Wartosc wzięta:", max_j)
 
  print("Wziete przedmioty:")
  print("waga(s) wartosc(w)")
 
  for i in range(n, 0, -1):
    if max_s <= 0:
      break
    if max_s == tab[i-1][max_j]:
      continue
    else:
      print(s[i-1], w[i-1])
      max_s -= s[i-1]
      max_j -= w[i-1]

plecak_tabelka_alt()