# pyrefly: ignore[missing-import]
from Src.Ingestion.Cleaning.cleaner  import (
    remove_noise,
    remove_duplicate_lines,
    remove_empty_lines,
    remove_noise_keywords,
    remove_repeated_footer 

)





 
def test_remove_noise():
    text='Hello\npage 10\n world'

    res =remove_noise(text,r'page\d+')
    assert res=="Hello \n"