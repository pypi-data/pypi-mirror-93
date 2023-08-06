# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thaifin', 'thaifin.models', 'thaifin.sources']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.16.0,<0.17.0',
 'beautifulsoup4>=4.9.1,<5.0.0',
 'cachetools>=4.2.1,<5.0.0',
 'furl>=2.1.0,<3.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'lxml>=4.5.1,<5.0.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=1.0.5,<2.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'tenacity>=6.3.1,<7.0.0']

extras_require = \
{'full': ['python-Levenshtein>=0.12.0,<0.13.0']}

setup_kwargs = {
    'name': 'thaifin',
    'version': '0.2.2',
    'description': 'A Python library for access thai stock fundamental data up to 10+ years.',
    'long_description': '# thaifin: ข้อมูลพื้นฐานหุ้น ง่ายแค่สามบรรทัด\n\n> The same author as [PythaiNAV](https://github.com/CircleOnCircles/pythainav)\n\n [**Documentation**](https://circleoncircles.github.io/thaifin/thaifin.html)\n\nA Python library for access thai stock fundamental data up to 10+ years. \n\n- faster and lesser load to server with [cachetools](https://pypi.org/project/cachetools/)\n- more robust with auto retry with expo wait via [tenacity](https://github.com/jd/tenacity)\n- better than nothing docs with [pdoc](https://pdoc.dev/)\n\n<a href="https://imgflip.com/i/4dxnzi"><img src="https://i.imgflip.com/4dxnzi.jpg" title="made at imgflip.com"/></a><div></div>\n\nไพทอนไลบารี่สำหรับเข้าถึงข้อมูลปัจจัยพื้นฐานของหุ้นในตลาดไทยมากถึง 10+ ปี\n\n## Get Started\n\n```bash\n# Pick one ✨\n$ pip install thaifin\n$ conda install thaifin\n```\n\n```python\n# get all stock symbols\nfrom thaifin import Stock\n\nStock.list_symbol() \n# [\'T\', \'A\', \'U\', \'J\', \'W\', \'B\', \'D\', \'S\', \'M\', \'K\', \'EE\', ...\n\ntop5match = Stock.search(\'จัสมิน\')\n# [<Stock JTS - updated just now>, <Stock JAS - updated just now>, <Stock JASIF - updated just now>, ...\n\nstock = Stock(\'PTT\')\n# <Stock PTT - updated just now>\n\nstock.quarter_dataframe\n\n#                 Cash            DA  ...  FinancingActivities         Asset\n# Time                                ...                                   \n# 2009Q1  9.383006e+07  1.070218e+07  ...         3.101551e+07  9.453044e+08\n# 2009Q2  9.643438e+07  8.893013e+06  ...         3.195314e+07  1.042480e+09\n# 2009Q3  1.050549e+08  1.127702e+07  ...         1.100019e+07  1.099084e+09\n# 2009Q4  1.040559e+08  1.227756e+07  ...        -1.356621e+07  1.103590e+09\n# ...\n# 2019Q4  2.925425e+08  3.581462e+07  ...        -2.179443e+07  2.484439e+09\n# 2020Q1  2.543450e+08  3.586543e+07  ...        -2.705637e+07  2.499666e+09\n# 2020Q2  2.578579e+08  3.460213e+07  ...         2.117104e+07  2.449277e+09\n# [46 rows x 35 columns]\n\nstock.yearly_dataframe\n\n                # Cash            DA  ...  FinancingActivities         Asset\n# Fiscal                              ...                                   \n# 2009    1.040559e+08  4.314976e+07  ...         6.040263e+07  1.103590e+09\n# 2010    1.356320e+08  5.122258e+07  ...         3.761321e+06  1.249148e+09\n# 2011    1.161321e+08  5.531816e+07  ...        -4.542309e+07  1.402412e+09\n# 2012    1.369176e+08  6.523743e+07  ...         2.771070e+07  1.631320e+09\n# 2013    1.576835e+08  7.631456e+07  ...        -5.579036e+07  1.801722e+09\n# 2014    2.037854e+08  1.170070e+08  ...        -4.731543e+07  1.779179e+09\n# 2015    2.399779e+08  1.488855e+08  ...        -1.638133e+08  2.173996e+09\n# 2016    2.155664e+08  1.297570e+08  ...        -1.162034e+08  2.232331e+09\n# 2017    1.661890e+08  1.171472e+08  ...        -1.624979e+08  2.232314e+09\n# 2018    2.921843e+08  1.235563e+08  ...        -1.114676e+08  2.355484e+09\n# 2019    2.925425e+08  1.332042e+08  ...        -7.022567e+07  2.484439e+09\n# [11 rows x 35 columns]\n\n```\n\n### Columns Data\n\n```python\nclass FinancialSheet(BaseModel):\n    SecurityID: Optional[int]\n    Fiscal: Optional[int]\n    Quarter: Optional[int]\n    Cash: Optional[float]\n    DA: Optional[float]\n    DebtToEquity: Optional[float]\n    Equity: Optional[float]\n    EarningPerShare: Optional[float]\n    EarningPerShareYoY: Optional[float]\n    EarningPerShareQoQ: Optional[float]\n    GPM: Optional[float]\n    GrossProfit: Optional[float]\n    NetProfit: Optional[float]\n    NetProfitYoY: Optional[float]\n    NetProfitQoQ: Optional[float]\n    NPM: Optional[float]\n    Revenue: Optional[float]\n    RevenueYoY: Optional[float]\n    RevenueQoQ: Optional[float]\n    ROA: Optional[float]\n    ROE: Optional[float]\n    SGA: Optional[float]\n    SGAPerRevenue: Optional[float]\n    TotalDebt: Optional[float]\n    DividendYield: Optional[float]\n    BookValuePerShare: Optional[float]\n    Close: Optional[float]\n    MKTCap: Optional[float]\n    PriceEarningRatio: Optional[float]\n    PriceBookValue: Optional[float]\n    EVPerEbitDA: Optional[float]\n    EbitDATTM: Optional[float]\n    PaidUpCapital: Optional[float]\n    CashCycle: Optional[float]\n    OperatingActivities: Optional[float]\n    InvestingActivities: Optional[float]\n    FinancingActivities: Optional[float]\n    Asset: Optional[float]\n```\n\n## Disclaimer\n\nเราไม่รับประกันความเสียหายใดๆทั้งสิ้นที่เกิดจาก แหล่งข้อมูล, library, source code,sample code, documentation, library dependencies และอื่นๆ\n\n## FAQ\nQ: อยากขอบคุณอ่ะ อยากตอบแทนอ่ะ 😋 ทำไงดี?\n\nA: ถ้าเป็น developer สามารถช่วยส่ง PR หรือ pull request ได้ครับ ไม่ว่าจะเป็นงานเล็กน้อยเช่นแก้การพิมพ์ผิด หรือช่วยทำคู่มือ ยินดีมากๆครับ สามารถสนับสนุนผม\nโดยการบริจาคครั้งเดียวผ่าน [Ko-fi](https://ko-fi.com/circleoncircles) หรือ [patreon](https://www.patreon.com/CircleOnCircles) ก็ได้เช่นกันครับ นอกจากนี้ยังสามารถเขียนให้กำลังใจผมได้ทาง [![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/nutchanon@codustry.com)\n\nQ: แจ้งปัญหาไงอ่ะ ?\n\nA: ถ้าเป็น error วิธีการใช้งานเขียน stackoverflow ได้ครับ ถ้าเป็น bug หรืออยากแนะนำขอ feature เขียน issue มาได้ครับ\n\nQ: ข้อมูลมาจากไหน เชื่อถือได้แค่ไหน ?\n\nA: ข้อมูลมาจากสาธารณะหลายแหล่งครับ ตอนที่เขียนมีเว็ป Finnomena, Set, Settrade เชื่อถือได้ไม่ได้คงต้องตัดสินเองนะครับ\n\nQ: สร้างมาทำไม ?\n\nA: สมัยเป็นนักศึกษา ผมก็อยากได้สิ่งนี้มาก่อนครับ เป็นเครื่องมือช่วยประกอบการลงทุน และใช้ความรู้ทาง data science กับข้อมูลได้ ตอนนั้นไม่มีใครทำครับ \nข้อมูลผูกขาดเฉพาะกับบริษัทลงทุนเท่านั้น ตอนนี้ก็ยังเหมือนเดิม เพิ่มเติมคือผมมีความสามารถที่จะสร้างมัน ก็อยากให้คนรุ่นต่อไปได้มี library ดีๆ เป็นสมบัติ\nของทุกคน(License ISC) ผมจึงใช้เวลาส่วนตัวมาพัฒนาครับ ทุกคนให้ความรักมันด้วยนะครับ code ก็ต้องการความรักนะ อิอิ\n\n \n \n',
    'author': 'Nutchanon Ninyawee',
    'author_email': 'me@nutchanon.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
