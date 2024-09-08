import re


def clean_str(s: str) -> str:
    patterns = [
        r'<head>(.*)</head>',
        r'<script>(.*)</script>',
        r'<!---.*--->',
    ]
    s = re.sub('[\n\r]+', '', s)
    for p in patterns:
        # d = re.findall(p, s, flags=re.MULTILINE)
        s = re.sub(p, '', s, flags=re.MULTILINE)

    return s
