"""
!CENTRALIZED PLAYWRIGHT SELECTORS
"""


#^===========================================
#^              SEARCHING
#^===========================================

SEARCH_BOX = "input[name='q']"

def SEARCH_BUTTON(page):

    button = page.get_by_role("link" , name="SEARCH")
    return button


#^===========================================
#^              SEARCHING
#^===========================================
PRODUCT_CARD = 'div[data-qa-locator="product-item"]'
PRODUCT_TITLE = ".RfADt a"
PRODUCT_LINK = ".RfADt a"
PRODUCT_PRICE = ".ooOxS"
PRODUCT_PIC_SRC = ".picture-wrapper img"
PRODUCT_RATING = "i._9-ogB"
NEXT_PAGE = "button.ant-pagination-item-link:has(svg[data-icon='right'])"