# Cryptopals

Solutions Python aux challenges de cryptographie Cryptopals.
Les challenges gardent leur num?ro global d'un set ? l'autre.

## Organisation

```text
set1/ ? set5/           Un dossier par set
  challengeN/          Solution, contexte et donn?es du challenge N
  __init__.py          Package Python pour les imports entre challenges
tests/                 Tests des fonctions partag?es
tools/check_structure.py  Contr?le statique de l'organisation
pyproject.toml         Configuration et d?pendances communes
uv.lock                Versions verrouill?es des d?pendances
```

| Set | Num?ros | Dossiers pr?sents |
| --- | --- | --- |
| 1 | 1?8 | 1?8 |
| 2 | 9?16 | 9?16 |
| 3 | 17?24 | 17?24 |
| 4 | 25?32 | 25?30 |
| 5 | 33?40 | 33?37, 39 |

Seuls les challenges commenc?s sont pr?sents. Leur pr?sence ne signifie pas
que chaque solution est termin?e ; le challenge 37 est notamment une ?bauche.
Les noms de fichiers existants sont conserv?s : selon le challenge, le point
d'entr?e s'appelle `solution.py`, `solve.py`, `attack.py` ou porte un nom sp?cifique.

## Installation et ex?cution

Pr?requis : Python 3.13 ou ult?rieur et uv. Depuis la racine du d?p?t :

```powershell
uv sync --locked
uv run python -m set2.challenge12.solution
uv run python -m set5.challenge34.MITM_attack_dh
```

Lancer les fichiers comme des modules depuis la racine permet ? Python de
r?soudre les imports entre challenges. Un seul environnement et une seule
configuration sont n?cessaires pour tout le d?p?t. Il n'y a pas de package
? construire ni de commande `cryptopals` ? installer.

## Fonctions partag?es

Les helpers restent dans leur challenge d'origine :

| Fonction | Module |
| --- | --- |
| XOR ? un octet, score anglais | `set1.challenge3.solution3` |
| Distance de Hamming | `set1.challenge6.hamming_distance` |
| Padding PKCS#7 | `set2.challenge9.padding` |
| AES-ECB et CBC | `set2.challenge10.solution` |
| Validation du padding | `set2.challenge15.solution` |
| CTR | `set3.challenge18.CTR_mode` |
| Mersenne Twister | `set3.challenge21.generateur` |
| SHA-1 avec reprise d'?tat | `set4.challenge28.sha1` |
| Diffie-Hellman et exponentiation modulaire | `set5.challenge33.diffle_hellman` |

Exemple d'import :

```python
from set2.challenge10.solution import CBC_decode, CBC_encode
```

Les variantes n?cessaires aux attaques restent explicites : options
`pad=False`, `unpad=False`, `validate_padding=True` pour CBC ; MAC avec cl?
suffix?e au challenge 28 et cl? pr?fix?e au challenge 29.

## V?rifications

Contr?ler la num?rotation, les packages, la syntaxe et les imports internes,
sans importer ni ex?cuter les solutions :

```powershell
uv run python tools/check_structure.py
```

Les tests sont dans `tests/` et dans les dossiers des challenges :

```powershell
uv run python -m pytest
```

Les environnements virtuels, caches et r?glages locaux de l'?diteur sont
exclus de Git.
