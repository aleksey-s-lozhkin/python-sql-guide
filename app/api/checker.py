"""Сравнение результата ученика с эталоном — по данным, а не по тексту запроса."""
from collections import Counter
from datetime import date, datetime
from decimal import Decimal


def normalize_value(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (Decimal, float, int)):
        return round(float(value), 2)
    if isinstance(value, datetime):
        return value.isoformat(sep=" ")
    if isinstance(value, date):
        return value.isoformat()
    return value


def normalize_rows(rows):
    return tuple(tuple(normalize_value(v) for v in row) for row in rows)


def _fmt(row):
    return ", ".join("NULL" if v is None else str(v) for v in row)


def compare(got_rows, expected_rows, ordered: bool = False):
    got = normalize_rows(got_rows)
    expected = normalize_rows(expected_rows)

    if len(got) != len(expected):
        return {
            "ok": False,
            "error": "Ожидалось строк: {}, получено: {}.".format(len(expected), len(got)),
            "expected_count": len(expected),
            "got_count": len(got),
        }

    if ordered:
        for index, (g, e) in enumerate(zip(got, expected)):
            if g != e:
                return {
                    "ok": False,
                    "error": "Строка {} не совпадает: получено [{}], ожидалось [{}].".format(
                        index + 1, _fmt(g), _fmt(e)
                    ),
                    "expected_count": len(expected),
                    "got_count": len(got),
                }
        return {"ok": True, "expected_count": len(expected), "got_count": len(got)}

    got_counter = Counter(got)
    expected_counter = Counter(expected)
    if got_counter == expected_counter:
        return {"ok": True, "expected_count": len(expected), "got_count": len(got)}

    missing = list((expected_counter - got_counter).elements())
    extra = list((got_counter - expected_counter).elements())
    parts = []
    if missing:
        parts.append("не хватает строк: {} (например, [{}])".format(len(missing), _fmt(missing[0])))
    if extra:
        parts.append("лишние строки: {} (например, [{}])".format(len(extra), _fmt(extra[0])))
    return {
        "ok": False,
        "error": "Набор строк не совпал — " + "; ".join(parts) + ".",
        "expected_count": len(expected),
        "got_count": len(got),
        "missing": [_fmt(row) for row in missing[:5]],
        "extra": [_fmt(row) for row in extra[:5]],
    }
