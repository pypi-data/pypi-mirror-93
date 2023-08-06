# GetSubStr

Utility that allows you get substring of each stdout line based on regexp.

```
usage: getsub [-h] [-l CUT_LEFT] [-r CUT_RIGHT] [--lwrap L_WRAP]
              [--rwrap R_WRAP] [-s] [-j JOIN_RESULTS]
              [--join-matches JOIN_MATCHES] [-i]
              regexp_pattern

Get stdout line substring based on regexp.

positional arguments:
  regexp_pattern        Regexp pattern

optional arguments:
  -h, --help            show this help message and exit
  -l CUT_LEFT, --left-cut CUT_LEFT
                        Cut N chars from left side of result
  -r CUT_RIGHT, --right-cut CUT_RIGHT
                        Cut N chars from right side of result
  --lwrap L_WRAP        Wrap results from left side by specified char(s)
  --rwrap R_WRAP        Wrap results from left side by specified char(s)
  -s, --strip           Strip spaces from left and right side of result
  -j JOIN_RESULTS, --join-results JOIN_RESULTS
                        Join all results with specified char(s)
  --join-matches JOIN_MATCHES
                        Join more regexp matches with specified char(s).
                        Default is TAB \t
  -i, --ignore-errors   Ignore errors caused regexp.
  ```
  
example #1:
```bash
printf "**** Error while updating article content id=498 ****\n**** Error while updating article content id=512 ****\n" \
| getsub "id\=\d+" -l 3 -j "," --lwrap "\"" --rwrap "\""
```
output:
```
"498","512"
```

example #2:
```bash
printf "123 456\n789 012" | getsub "(\d+) (\d+)" --o "i='{0}'...j='{1}'"
```
output:
```
i='123'...j='456'
i='789'...j='012'
```
