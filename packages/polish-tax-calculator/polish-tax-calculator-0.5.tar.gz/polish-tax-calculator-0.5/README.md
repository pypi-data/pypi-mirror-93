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
