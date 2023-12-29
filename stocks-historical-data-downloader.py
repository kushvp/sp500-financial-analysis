import yfinance as yf
import investpy as invstng
import requests


# df = invstng.get_stock_information(stock="AAPL", country="united states")

# tickers = yf.Tickers(`AAPL MSFT AMZN NVDA GOOGL BRK.B GOOG TSLA XOM UNH META JPM JNJ V PG MA HD CVX MRK ABBV AVGO LLY PEP KO BAC PFE TMO COST CSCO WMT MCD CRM DIS LIN ABT WFC ACN DHR ADBE TXN VZ CMCSA PM NKE NEE RTX BMY NFLX AMD ORCL QCOM UPS COP T HON CAT MS UNP LOW AMGN GS SBUX INTU DE BA SCHW IBM PLD SPGI LMT ELV INTC CVS AXP MDT AMAT BLK GILD BKNG C ADI GE ADP AMT TJX NOW SYK MDLZ PYPL TMUS CI CB PGR MO ISRG MMC REGN ZTS SLB TGT FISV VRTX DUK SO ETN EOG NOC LRCX BSX BDX ITW CME APD EQIX CSX AON HUM MU USB MPC CL MMM PNC TFC FCX EL ICE GM ATVI CCI WM SNPS KLAC CDNS HCA ORLY SHW VLO F GD EMR FDX NSC DG PXD MCK EW NXPI PSX PSA APH GIS MRNA AZO SRE MAR MCHP MCO PH AEP D NUE OXY MET ROP JCI CTVA MSI TT ADSK DXCM ADM MSCI AIG CMG TRV A KMB TEL EXC O FTNT DOW HLT COF IDXX CARR PCAR SPG LHX AJG MNST IQV TDG ECL CNC CHTR SYY BIIB ROST AFL CTAS HES FIS WMB BK ANET AMP PAYX CMI DD YUM ON OTIS STZ DVN WELL XEL PRU HSY ROK KMI HAL WBD MTD URI NEM ALL ILMN ED VICI AME ODFL STT CTSH BKR APTV GWW RMD KR PPG CPRT KHC DLR GPN DFS FAST OKE DLTR ALB DHI EA PEG ENPH KDP VRSK CSGP KEYS WEC GEHC ULTA SBAC CDW CBRE IT PCG RSG WTW EIX ANSS ACGL GLW ES HPQ ZBH CEG TROW TSCO FANG LEN AWK DAL WBA ABC MTB EFX AVB EBAY ALGN GPC LYB VMC IR FTV HIG WST FITB PWR WY IFF MLM MPWR STLD DOV EXR AEE FE ARE FSLR ETR FRC EQR LH HBAN RJF DTE RF CHD LUV CTRA PPL TDY BAX HOLX HPE LVS PFG WAB NTRS CAH VTR MOS CFG NDAQ CINF WAT VRSN OMC CLX SWKS INVH MKC TTWO XYL EXPD STE SEDG DRI UAL MAA EPAM CNP BALL TRGP CMS TSN CAG BR IEX CF K AMCR NVR BBY COO AES TER MRO SJM HWM FMC EXPE KEY DGX ZBRA RCL FLT MOH J SYF ATO PKI SIVB IRM TXT JBHT FDS GRMN RE LKQ ESS MGM AVY NTAP LW ETSY POOL PAYC INCY TYL IPG MKTX IP EVRG WRB SNA BRO CBOE PKG UDR PTC LDOS LNT CHRW TRMB PHM VTRS APA PEAK CTLT STX SWK KIM CPT JKHY BWA HST WYNN NDSN AKAM WDC CE EQT HRL MAS TECH BF.B L KMX CZR NI DPZ CDAY PARA CRL TPR HSIC CPB GL MTCH AAL FOXA GEN TFX QRVO EMN BIO CCL TAP ALLE JNPR LYV REG PNR BXP BBWI RHI CMA PNW FFIV AOS HII UHS XRAY ROL AAP WRK NRG IVZ BEN FRT VFC GNRC WHR SEE ZION HAS NWSA AIZ SBNY NCLH DXC ALK OGN MHK NWL RL FOX LNC DVA DISH LUMN NWS')


tag = "AAPL"
url = "https://www.investing.com/equities/apple-computer-inc"

"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
    'X-Requested-With': 'XMLHttpRequest',
    #'Referer': 'http://www.investing.com/equities/aapl'
}
"""


headers = {
    #':authority': 'www.investing.com',
    #':method': 'GET',
    #':path': '/equities/apple-computer-inc',
    #':scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    #'cookie': '__qca=I0-396882050-1678507678975; PHPSESSID=brlp22tfdn8p0nsanbuoio47rk; geoC=US; browser-session-counted=true; user-browser-sessions=1; ab_test_header_bidding=headerBidding_enabled; adBlockerNewUserDomains=1678504794; gtmFired=OK; __cflb=0H28vY1WcQgbwwJpSw5YiDRSJhpofbx4UbDoKY9M1xG; protectedMedia=2; pms={"f":2,"s":2}; _gid=GA1.2.659453508.1678504796; udid=fbaef97acb399c30fbbea5ee020b37b6; _pbjs_userid_consent_data=3524755945110770; __gads=ID=4c775f48492a4713:T=1678504796:S=ALNI_MbdkTCyV70Wo370p2iYRLAwTH4xhw; __gpi=UID=0000095a42b46d49:T=1678504796:RT=1678504796:S=ALNI_MaRyvmtbwuP69qHgnax8dLOs-uq0g; _fbp=fb.1.1678504802387.368684464; adsFreeSalePopUp=3; invpc=3; nyxDorf=MDc%2Ba2UzYzw%2FY2hsN2Q4Mj5uZTQ1MDQ3ZmdlZWdqYjwwMzYxYmBibTZpOTZiYjU6Z20wOT9oMWdiMjM1Mz80YTA2PmRlOWNuP25oNw%3D%3D; g_state={"i_p":1678512057083,"i_l":1}; pm_score=clear; _hjSession_174945=eyJpZCI6IjM0ODI3ZDM1LTc3ZDItNDZhYi04MmE1LTc1MzNkZjk0MjIzZCIsImNyZWF0ZWQiOjE2Nzg1MDQ4NzY1MDksImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _lr_retry_request=true; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%2291168041-ece1-42ef-b622-b58b9b02fc97%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222023-02-11T03%3A21%3A20%22%7D; pbjs-unifiedid_last=Sat%2C%2011%20Mar%202023%2003%3A21%3A21%20GMT; panoramaId_expiry=1679109680251; _cc_id=c881f35433d9b6911ed7fa68f1cfc00; panoramaId=370c3a58f9d1ec3f23208de1f00f16d53938c63f6bc13c5222fb287162cbd05f; _hjSessionUser_174945=eyJpZCI6ImMxNzM5ZjQyLWI0MGUtNWVjZC04ZWVlLTNmODhmODRiNzM2MSIsImNyZWF0ZWQiOjE2Nzg1MDQ4NzY1MDAsImV4aXN0aW5nIjp0cnVlfQ==; SideBlockUser=a%3A1%3A%7Bs%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A1%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A6408%3Bs%3A10%3A%22pair_title%22%3Bs%3A5%3A%22Apple%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A28%3A%22%2Fequities%2Fapple-computer-inc%22%3B%7D%7D%7D%7D; smd=fbaef97acb399c30fbbea5ee020b37b6-1678507673; _gat_UA-2555300-55=1; gcc=US; gsc=TX; __cf_bm=6cwkw_ih1Kjx9vXqUqrgLkkygrUqFJOtnTvOuxSbPAQ-1678507673-0-AfXWPwaXLgQWwxHIEKik7Tk6GUnPKrXWuUYKgWdFBE8ke8xMu+oaLxBB4eYidsnRjQV4u8O5HvMOag89xNrshSQ=; _dd_s=logs=1&id=a8cc0424-f09e-40d7-8306-2e032bc24a1a&created=1678507674478&expire=1678508574478; page_view_count=8; OptanonConsent=isIABGlobal=false&datestamp=Fri+Mar+10+2023+22%3A07%3A55+GMT-0600+(Central+Standard+Time)&version=202209.2.0&hosts=&consentId=8b670b4f-205a-4bcd-97cb-94db72b7f9d3&interactionCount=1&landingPath=https%3A%2F%2Fwww.investing.com%2Fequities%2Fapple-computer-inc&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; _ga_C4NDLGKVMK=GS1.1.1678507673.2.1.1678507675.58.0.0; _ga=GA1.2.529226234.1678504796; _hjIncludedInSessionSample_174945=0',
    'pragma': 'no-cache',
    # 'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63'
}
session = requests.session()
data = session.get(url,
                   headers=headers,
                   verify=False
                  )
session.close()

# req = requests.get(url,
#                    headers=headers,
#                    verify=False
#                   )

print(data.status_code)
