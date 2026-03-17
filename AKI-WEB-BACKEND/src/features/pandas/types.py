from typing import Optional, Sequence, TypeVar, Union

IntOrStr = TypeVar("IntOrStr", bound=Union[int, str])


IntOrListOfIntsType = Optional[Sequence[int] | int]
ValueOrListType = Optional[int | str | Sequence[int] | Sequence[str]]
