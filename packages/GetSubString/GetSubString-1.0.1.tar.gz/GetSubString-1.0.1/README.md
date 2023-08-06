# getsubstr

Utility that allows you get stdout line substring based on regexp.

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
  
  example:
```bash
echo "**** Error while updating article content id=498 ****" | getsub "id\=\d+" -l 3 -j "," --lwrap "\"" --rwrap "\""
"498"
```