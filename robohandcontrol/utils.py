def map_range(
    x: int,
    in_min: int,
    in_max: int,
    out_min: int,
    out_max: int,
) -> int:
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
