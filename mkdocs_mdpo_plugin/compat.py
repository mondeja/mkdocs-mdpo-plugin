def removesuffix(s, suf):
    if suf and s.endswith(suf):
        return s[:-len(suf)]
    return s
