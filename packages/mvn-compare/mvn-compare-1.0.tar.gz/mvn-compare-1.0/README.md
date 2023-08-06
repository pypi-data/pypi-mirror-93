# Maven Version Comparator

Compare maven release versions

```shell
pip install mvn-compare
```

### Examples

```shell

~$ mvn-compare "1.0-alpha1" "1.0-beta1"
-1  

~$ mvn-compare "1.0" "1.0-beta1"
1

~$ mvn-compare "1.0-final" "1.0"
0

```
