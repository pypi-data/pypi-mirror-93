# pystock
- running stock in Python3
- HTS API to Python

## HTS service

- 환경: Windows10
- 언어: Python3 

```
pip3 install pystock-hts
```
or
```
pip install pystock-hts
```

- 증권사 별 환경
    - 대신증권 : Cybos Plus 가 활성화 되어 있어야함. [다운로드](https://money2.daishin.com/E5/WTS/Customer/GuideTrading/DW_CybosPlus_Page.aspx?p=8812&v=8632&m=9508)
    ```python
    from StockApiService import Daishin

    ```

### StockApiService

- [Daishin API](Documents/daishin.md)

- [Kiwoom API](Documents/Kiwoom.md)