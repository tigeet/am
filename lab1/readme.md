- `Input1.json` проверка работы со смешанными ограничениями  
  x=20, y=0, fmax = -60
- `Input2.json` проверка работы `gte`  
  x = 5, fmax = -5
- `Input3.json` проверка работы со смешанными ограничениями  
  x = 0, y = 6.5, z = 1, fmax = 17
- `Input4.json` проверка работы `eq`  
  x = 5, fmax = 5
- `Input5.json` Проверка работы с неограниченным условием
  Решение неограничено
- `Input6.json` Проверка работы с системой без решения
  Нет решения
- `Input7.json` Пример из методички  
  x = 0, y= 2, z = 1, fmax = 7

## `Input1.json`

```json
{
  "f": [-3, -4],
  "goal": "max",
  "constraints": [
    {
      "coefs": [1, 1],
      "type": "gte",
      "b": 20
    },

    {
      "coefs": [1, 2],
      "type": "gte",
      "b": 25
    },
    {
      "coefs": [-5, 1],
      "type": "lte",
      "b": 4
    }
  ]
}
```

## `Input2.json`

```json
{
  "f": [1],
  "goal": "min",
  "constraints": [
    {
      "coefs": [1],
      "type": "gte",
      "b": 5
    }
  ]
}
```

## `Input3.json`

```json
{
  "f": [3, 2, 4],
  "goal": "max",
  "constraints": [
    {
      "coefs": [3, 2, 5],
      "type": "lte",
      "b": 18
    },

    {
      "coefs": [4, 2, 3],
      "type": "lte",
      "b": 16
    },
    {
      "coefs": [2, 1, 1],
      "type": "gte",
      "b": 4
    }
  ]
}
```

## `Input4.json`

```json
{
  "f": [1],
  "goal": "max",
  "constraints": [
    {
      "coefs": [1],
      "type": "eq",
      "b": 5
    }
  ]
}
```

## `Input5.json`

```json
{
  "f": [1],
  "goal": "max",
  "constraints": [
    {
      "coefs": [1],
      "type": "gt",
      "b": 5
    }
  ]
}
```

## `Input6.json`

```json
{
  "f": [1],
  "goal": "max",
  "constraints": [
    {
      "coefs": [1],
      "type": "gt",
      "b": 5
    },
    {
      "coefs": [1],
      "type": "lt",
      "b": 3
    }
  ]
}
```

## `Input7.json`

```json
{
  "f": [1, 2, 3],
  "goal": "max",
  "constraints": [
    { "coefs": [1, 0, 0], "type": "lte", "b": 1 },
    { "coefs": [1, 1, 0], "type": "gte", "b": 2 },
    { "coefs": [1, 1, 1], "type": "eq", "b": 3 }
  ]
}
```
