Kalkulator podatkowy w formie CLI, oblicza wartość podatku dochodowego dla różnych wariantów rozliczeń.
Uwzględniono stawki ZUS za 2021 rok. (Obecnie brak obsługi "ulgi na start" oraz "mały ZUS" przy rozliczaniu z ZUS).


## Instalacja

```shell
pip install polish-tax-calculator
```

## Użycie

```shell
ptc --help
```

#### przykład 1. opcje domyślne: pełen zus, podatek liniowy, bez składki chorobowej
```shell
ptc 5000 
```

#### przykład 2: obniżony zus, ryczałt 5%, składka chorobowa, więcej szczegółów (-v)
```shell
ptc -t income -z reduced -si -itr 5 -v 5500 
```
